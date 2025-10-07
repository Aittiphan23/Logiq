"""
Verification Cog for Logiq
Handles user verification with multiple methods
"""

import discord
from discord import app_commands
from discord.ext import commands
import random
import string
from typing import Optional
import logging

from utils.embeds import EmbedFactory, EmbedColor
from utils.permissions import is_admin
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class VerificationButton(discord.ui.View):
    """Button-based verification view"""

    def __init__(self, cog: 'Verification'):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_button", emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle verification button click"""
        await self.cog.verify_user(interaction)


class CaptchaModal(discord.ui.Modal, title="Verification Captcha"):
    """Captcha verification modal"""

    def __init__(self, correct_code: str, cog: 'Verification'):
        super().__init__()
        self.correct_code = correct_code
        self.cog = cog

    captcha_code = discord.ui.TextInput(
        label="Enter the code shown",
        placeholder="Enter captcha code",
        required=True,
        max_length=6
    )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle captcha submission"""
        if self.captcha_code.value.upper() == self.correct_code:
            await self.cog.verify_user(interaction)
        else:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Verification Failed", "Incorrect captcha code. Please try again."),
                ephemeral=True
            )


class Verification(commands.Cog):
    """Verification system cog"""

    def __init__(self, bot: commands.Bot, db: DatabaseManager, config: dict):
        self.bot = bot
        self.db = db
        self.config = config
        self.module_config = config.get('modules', {}).get('verification', {})

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Handle new member join - Send DM verification (PRIVATE)"""
        if not self.module_config.get('enabled', True):
            return

        guild_config = await self.db.get_guild(member.guild.id)
        if not guild_config:
            return

        verified_role_id = guild_config.get('verified_role')
        if not verified_role_id:
            return

        verification_type = guild_config.get('verification_type', 'button')
        welcome_message = guild_config.get('welcome_message',
            f"Welcome to **{member.guild.name}**! 👋\n\n"
            "Please verify yourself by clicking the button below to gain access to the server."
        )

        try:
            # Send DM to user with verification
            if verification_type == 'button':
                embed = EmbedFactory.create(
                    title=f"🔐 Welcome to {member.guild.name}",
                    description=welcome_message,
                    color=EmbedColor.PRIMARY
                )
                embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else None)
                view = VerificationButton(self)
                await member.send(embed=embed, view=view)

            elif verification_type == 'captcha':
                # Generate captcha code
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                embed = EmbedFactory.create(
                    title=f"🔐 Welcome to {member.guild.name}",
                    description=f"{welcome_message}\n\n**Your verification code:** `{code}`\n\nClick the button below and enter this code.",
                    color=EmbedColor.PRIMARY
                )
                embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else None)

                button = discord.ui.Button(label="Enter Code", style=discord.ButtonStyle.green, custom_id=f"captcha_{member.id}")

                async def captcha_callback(interaction: discord.Interaction):
                    if interaction.user.id != member.id:
                        await interaction.response.send_message("This verification is not for you!", ephemeral=True)
                        return
                    modal = CaptchaModal(code, self)
                    await interaction.response.send_modal(modal)

                button.callback = captcha_callback
                view = discord.ui.View(timeout=None)
                view.add_item(button)

                await member.send(embed=embed, view=view)

            logger.info(f"Sent DM verification to {member} in {member.guild}")

        except discord.Forbidden:
            # User has DMs disabled - log but don't announce publicly
            logger.warning(f"Could not DM {member} in {member.guild} - DMs disabled")

            # Optionally send to log channel if configured
            log_channel_id = guild_config.get('log_channel')
            if log_channel_id:
                log_channel = member.guild.get_channel(log_channel_id)
                if log_channel:
                    await log_channel.send(
                        embed=EmbedFactory.error(
                            "Verification DM Failed",
                            f"Could not send verification DM to {member.mention} (DMs disabled)"
                        )
                    )

    async def verify_user(self, interaction: discord.Interaction):
        """Verify a user and assign role (SILENT - no public announcements)"""
        guild_config = await self.db.get_guild(interaction.guild.id)
        if not guild_config:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "Server not configured"),
                ephemeral=True
            )
            return

        verified_role_id = guild_config.get('verified_role')
        if not verified_role_id:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "Verified role not configured"),
                ephemeral=True
            )
            return

        verified_role = interaction.guild.get_role(verified_role_id)
        if not verified_role:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "Verified role not found"),
                ephemeral=True
            )
            return

        if verified_role in interaction.user.roles:
            await interaction.response.send_message(
                embed=EmbedFactory.info("Already Verified", "You are already verified!"),
                ephemeral=True
            )
            return

        try:
            # Silently add verified role
            await interaction.user.add_roles(verified_role)

            # Send private success message
            await interaction.response.send_message(
                embed=EmbedFactory.success(
                    "✅ Verified Successfully!",
                    f"Welcome to **{interaction.guild.name}**!\n\nYou now have access to all channels."
                ),
                ephemeral=True
            )

            # Log silently (no public announcement)
            logger.info(f"Verified user {interaction.user} in {interaction.guild} (silent)")

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to assign roles"),
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error verifying user: {e}", exc_info=True)
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "An error occurred during verification"),
                ephemeral=True
            )

    @app_commands.command(name="setup-verification", description="Setup verification system (Admin)")
    @app_commands.describe(
        role="Role to assign upon verification",
        verification_type="Type of verification (button/captcha)"
    )
    @is_admin()
    async def setup_verification(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        verification_type: str = "button"
    ):
        """Setup verification system - DM based (ADMIN ONLY)"""
        if verification_type not in ['button', 'captcha']:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Type", "Verification type must be 'button' or 'captcha'"),
                ephemeral=True
            )
            return

        guild_config = await self.db.get_guild(interaction.guild.id)
        if not guild_config:
            guild_config = await self.db.create_guild(interaction.guild.id)

        await self.db.update_guild(interaction.guild.id, {
            'verified_role': role.id,
            'verification_type': verification_type
        })

        embed = EmbedFactory.success(
            "✅ Verification Setup Complete",
            f"**Verified Role:** {role.mention}\n"
            f"**Type:** {verification_type}\n"
            f"**Method:** DM (Private)\n\n"
            "New members will receive a DM with a verification button."
        )
        await interaction.response.send_message(embed=embed)
        logger.info(f"Verification setup completed in {interaction.guild}")

    @app_commands.command(name="set-welcome-message", description="Set custom welcome DM message (Admin)")
    @app_commands.describe(message="Custom welcome message for new members")
    @is_admin()
    async def set_welcome_message(self, interaction: discord.Interaction, message: str):
        """Set custom welcome message for verification DMs (ADMIN ONLY)"""
        guild_config = await self.db.get_guild(interaction.guild.id)
        if not guild_config:
            guild_config = await self.db.create_guild(interaction.guild.id)

        await self.db.update_guild(interaction.guild.id, {
            'welcome_message': message
        })

        embed = EmbedFactory.success(
            "✅ Welcome Message Updated",
            f"**New Welcome Message:**\n{message}\n\n"
            "This will be sent in DMs to new members along with the verification button."
        )
        await interaction.response.send_message(embed=embed)
        logger.info(f"Welcome message updated in {interaction.guild}")

    @app_commands.command(name="send-verification", description="Send verification button in current channel (Admin)")
    @is_admin()
    async def send_verification(self, interaction: discord.Interaction):
        """Manually send verification button to current channel (ADMIN ONLY)"""
        guild_config = await self.db.get_guild(interaction.guild.id)
        if not guild_config or not guild_config.get('verified_role'):
            await interaction.response.send_message(
                embed=EmbedFactory.error("Not Configured", "Please setup verification first with /setup-verification"),
                ephemeral=True
            )
            return

        embed = EmbedFactory.verification_prompt()
        view = VerificationButton(self)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(
            embed=EmbedFactory.success("Sent", "Verification button sent to this channel!"),
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(Verification(bot, bot.db, bot.config))
