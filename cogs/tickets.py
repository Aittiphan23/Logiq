"""
Tickets Cog for Logiq
Support ticket system
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import logging

from utils.embeds import EmbedFactory, EmbedColor
from utils.permissions import is_admin
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class TicketCreateView(discord.ui.View):
    """View for creating tickets"""

    def __init__(self, cog: 'Tickets'):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green, custom_id="create_ticket", emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle ticket creation"""
        await self.cog.create_ticket_for_user(interaction)


class Tickets(commands.Cog):
    """Support ticket system cog"""

    def __init__(self, bot: commands.Bot, db: DatabaseManager, config: dict):
        self.bot = bot
        self.db = db
        self.config = config
        self.module_config = config.get('modules', {}).get('tickets', {})

    async def create_ticket_for_user(self, interaction: discord.Interaction):
        """Create a ticket for a user"""
        guild_config = await self.db.get_guild(interaction.guild.id)
        if not guild_config:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Not Configured", "Ticket system not configured"),
                ephemeral=True
            )
            return

        ticket_category_id = guild_config.get('ticket_category')
        if not ticket_category_id:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Not Configured", "Ticket category not set up"),
                ephemeral=True
            )
            return

        category = interaction.guild.get_channel(ticket_category_id)
        if not category or not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "Ticket category not found"),
                ephemeral=True
            )
            return

        # Check if user already has an open ticket
        existing_tickets = [
            ch for ch in category.channels
            if ch.name.startswith(f"ticket-{interaction.user.name.lower()}")
        ]

        if existing_tickets:
            await interaction.response.send_message(
                embed=EmbedFactory.warning(
                    "Ticket Exists",
                    f"You already have an open ticket: {existing_tickets[0].mention}"
                ),
                ephemeral=True
            )
            return

        try:
            # Create ticket channel
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            # Add support role if configured
            support_role_id = guild_config.get('support_role')
            if support_role_id:
                support_role = interaction.guild.get_role(support_role_id)
                if support_role:
                    overwrites[support_role] = discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True
                    )

            channel = await category.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                overwrites=overwrites
            )

            # Create ticket in database
            ticket_data = {
                "guild_id": interaction.guild.id,
                "user_id": interaction.user.id,
                "channel_id": channel.id,
                "category": "General Support",
                "status": "open"
            }
            ticket_id = await self.db.create_ticket(ticket_data)

            # Send welcome message
            embed = EmbedFactory.create(
                title="🎫 Support Ticket",
                description=f"Hello {interaction.user.mention}!\n\n"
                           f"Thank you for creating a support ticket. Please describe your issue "
                           f"and a staff member will assist you shortly.\n\n"
                           f"**Ticket ID:** {ticket_id}",
                color=EmbedColor.SUCCESS
            )
            await channel.send(embed=embed)

            await interaction.response.send_message(
                embed=EmbedFactory.success(
                    "Ticket Created",
                    f"Your ticket has been created: {channel.mention}"
                ),
                ephemeral=True
            )

            logger.info(f"Ticket created for {interaction.user} in {interaction.guild}")

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to create channels"),
                ephemeral=True
            )

    @app_commands.command(name="ticket-setup", description="Setup ticket system")
    @app_commands.describe(
        category="Category for ticket channels",
        support_role="Role to ping for new tickets (optional)"
    )
    @is_admin()
    async def ticket_setup(
        self,
        interaction: discord.Interaction,
        category: discord.CategoryChannel,
        support_role: Optional[discord.Role] = None
    ):
        """Setup ticket system"""
        guild_config = await self.db.get_guild(interaction.guild.id)
        if not guild_config:
            guild_config = await self.db.create_guild(interaction.guild.id)

        update_data = {'ticket_category': category.id}
        if support_role:
            update_data['support_role'] = support_role.id

        await self.db.update_guild(interaction.guild.id, update_data)

        embed = EmbedFactory.success(
            "Ticket System Setup",
            f"✅ Category: {category.mention}\n" +
            (f"✅ Support Role: {support_role.mention}" if support_role else "")
        )
        await interaction.response.send_message(embed=embed)
        logger.info(f"Ticket system setup in {interaction.guild}")

    @app_commands.command(name="ticket-panel", description="Send ticket creation panel")
    @is_admin()
    async def ticket_panel(self, interaction: discord.Interaction):
        """Send ticket panel"""
        embed = EmbedFactory.create(
            title="🎫 Support Tickets",
            description="Need help? Click the button below to create a support ticket!\n\n"
                       "A private channel will be created where you can discuss your issue with staff.",
            color=EmbedColor.PRIMARY
        )

        view = TicketCreateView(self)
        await interaction.channel.send(embed=embed, view=view)

        await interaction.response.send_message(
            embed=EmbedFactory.success("Panel Sent", "Ticket panel created!"),
            ephemeral=True
        )

    @app_commands.command(name="close-ticket", description="Close a ticket")
    @app_commands.describe(reason="Reason for closing")
    async def close_ticket(self, interaction: discord.Interaction, reason: Optional[str] = "Resolved"):
        """Close a ticket"""
        # Check if in ticket channel
        if not interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message(
                embed=EmbedFactory.error("Not a Ticket", "This command can only be used in ticket channels"),
                ephemeral=True
            )
            return

        embed = EmbedFactory.warning(
            "Ticket Closing",
            f"This ticket is being closed.\n\n**Reason:** {reason}\n\n"
            f"Channel will be deleted in 10 seconds..."
        )
        await interaction.response.send_message(embed=embed)

        logger.info(f"Ticket {interaction.channel.name} closed by {interaction.user}")

        await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=10))

        try:
            await interaction.channel.delete()
        except discord.Forbidden:
            pass


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(Tickets(bot, bot.db, bot.config))
