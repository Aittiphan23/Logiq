"""
Roles Cog for Logiq
Self-assignable roles and reaction roles
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, List
import logging

from utils.embeds import EmbedFactory, EmbedColor
from utils.permissions import is_admin
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class RoleSelectMenu(discord.ui.Select):
    """Dropdown menu for role selection"""

    def __init__(self, roles: List[discord.Role]):
        options = [
            discord.SelectOption(
                label=role.name,
                description=f"Get the {role.name} role",
                value=str(role.id),
                emoji="🎭"
            )
            for role in roles[:25]  # Max 25 options
        ]

        super().__init__(
            placeholder="Select roles to add/remove",
            min_values=0,
            max_values=len(options),
            options=options,
            custom_id="role_select"
        )

    async def callback(self, interaction: discord.Interaction):
        """Handle role selection"""
        selected_role_ids = {int(value) for value in self.values}
        current_role_ids = {role.id for role in interaction.user.roles}

        roles_to_add = []
        roles_to_remove = []

        # Get all available roles from options
        available_role_ids = {int(option.value) for option in self.options}

        for role_id in available_role_ids:
            role = interaction.guild.get_role(role_id)
            if not role:
                continue

            if role_id in selected_role_ids and role_id not in current_role_ids:
                roles_to_add.append(role)
            elif role_id not in selected_role_ids and role_id in current_role_ids:
                roles_to_remove.append(role)

        try:
            if roles_to_add:
                await interaction.user.add_roles(*roles_to_add)
            if roles_to_remove:
                await interaction.user.remove_roles(*roles_to_remove)

            added_text = ", ".join([r.mention for r in roles_to_add]) if roles_to_add else "None"
            removed_text = ", ".join([r.mention for r in roles_to_remove]) if roles_to_remove else "None"

            embed = EmbedFactory.success(
                "Roles Updated",
                f"**Added:** {added_text}\n**Removed:** {removed_text}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to manage roles"),
                ephemeral=True
            )


class RoleSelectView(discord.ui.View):
    """View containing role select menu"""

    def __init__(self, roles: List[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(RoleSelectMenu(roles))


class Roles(commands.Cog):
    """Role management cog"""

    def __init__(self, bot: commands.Bot, db: DatabaseManager, config: dict):
        self.bot = bot
        self.db = db
        self.config = config
        self.module_config = config.get('modules', {}).get('roles', {})
        self.self_assign_roles = {}  # guild_id: [role_ids]

    @app_commands.command(name="role-menu", description="Create a self-assignable role menu")
    @app_commands.describe(roles="Roles to make self-assignable (mention them)")
    @is_admin()
    async def role_menu(self, interaction: discord.Interaction, roles: str):
        """Create role selection menu"""
        # Parse mentioned roles
        role_list = []
        for role_mention in roles.split():
            role_id = role_mention.strip('<@&>')
            try:
                role = interaction.guild.get_role(int(role_id))
                if role and not role.is_bot_managed() and not role.is_premium_subscriber():
                    role_list.append(role)
            except ValueError:
                continue

        if not role_list:
            await interaction.response.send_message(
                embed=EmbedFactory.error("No Valid Roles", "Please mention valid roles"),
                ephemeral=True
            )
            return

        if len(role_list) > 25:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Too Many Roles", "Maximum 25 roles per menu"),
                ephemeral=True
            )
            return

        # Create embed and view
        embed = EmbedFactory.create(
            title="🎭 Self-Assignable Roles",
            description="Select roles from the dropdown menu below to add or remove them.\n\n"
                       "**Available Roles:**\n" + "\n".join([f"• {role.mention}" for role in role_list]),
            color=EmbedColor.PRIMARY
        )

        view = RoleSelectView(role_list)

        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(
            embed=EmbedFactory.success("Menu Created", "Role menu has been created!"),
            ephemeral=True
        )

        # Store roles for persistence
        self.self_assign_roles[interaction.guild.id] = [role.id for role in role_list]
        logger.info(f"Role menu created in {interaction.guild} with {len(role_list)} roles")

    @app_commands.command(name="addrole", description="Add a role to a user")
    @app_commands.describe(
        user="User to add role to",
        role="Role to add"
    )
    @is_admin()
    async def add_role(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role
    ):
        """Add role to user"""
        if role in user.roles:
            await interaction.response.send_message(
                embed=EmbedFactory.info("Already Has Role", f"{user.mention} already has {role.mention}"),
                ephemeral=True
            )
            return

        try:
            await user.add_roles(role)
            embed = EmbedFactory.success(
                "Role Added",
                f"Added {role.mention} to {user.mention}"
            )
            await interaction.response.send_message(embed=embed)
            logger.info(f"{interaction.user} added role {role} to {user}")

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to manage roles"),
                ephemeral=True
            )

    @app_commands.command(name="removerole", description="Remove a role from a user")
    @app_commands.describe(
        user="User to remove role from",
        role="Role to remove"
    )
    @is_admin()
    async def remove_role(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role
    ):
        """Remove role from user"""
        if role not in user.roles:
            await interaction.response.send_message(
                embed=EmbedFactory.info("Doesn't Have Role", f"{user.mention} doesn't have {role.mention}"),
                ephemeral=True
            )
            return

        try:
            await user.remove_roles(role)
            embed = EmbedFactory.success(
                "Role Removed",
                f"Removed {role.mention} from {user.mention}"
            )
            await interaction.response.send_message(embed=embed)
            logger.info(f"{interaction.user} removed role {role} from {user}")

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to manage roles"),
                ephemeral=True
            )

    @app_commands.command(name="roleinfo", description="Get information about a role")
    @app_commands.describe(role="Role to get info about")
    async def role_info(self, interaction: discord.Interaction, role: discord.Role):
        """Get role information"""
        embed = EmbedFactory.create(
            title=f"Role Information: {role.name}",
            color=role.color if role.color.value != 0 else EmbedColor.PRIMARY,
            fields=[
                {"name": "ID", "value": str(role.id), "inline": True},
                {"name": "Color", "value": str(role.color), "inline": True},
                {"name": "Position", "value": str(role.position), "inline": True},
                {"name": "Members", "value": str(len(role.members)), "inline": True},
                {"name": "Mentionable", "value": "Yes" if role.mentionable else "No", "inline": True},
                {"name": "Hoisted", "value": "Yes" if role.hoist else "No", "inline": True},
                {"name": "Created", "value": role.created_at.strftime("%Y-%m-%d"), "inline": False}
            ]
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="members-with-role", description="List members with a specific role")
    @app_commands.describe(role="Role to check")
    async def members_with_role(self, interaction: discord.Interaction, role: discord.Role):
        """List members with role"""
        members = role.members

        if not members:
            await interaction.response.send_message(
                embed=EmbedFactory.info("No Members", f"No one has the {role.mention} role"),
                ephemeral=True
            )
            return

        # Create pages if too many members
        members_list = [m.mention for m in members[:50]]  # Limit to 50
        description = "\n".join(members_list)

        if len(members) > 50:
            description += f"\n\n*...and {len(members) - 50} more*"

        embed = EmbedFactory.create(
            title=f"Members with {role.name}",
            description=description,
            color=role.color if role.color.value != 0 else EmbedColor.PRIMARY
        )
        embed.set_footer(text=f"Total: {len(members)} members")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(Roles(bot, bot.db, bot.config))
