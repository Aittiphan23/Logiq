"""
Moderation Cog for Logiq
Comprehensive moderation tools with AI-powered auto-moderation
"""

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from typing import Optional
import logging
import asyncio

from utils.embeds import EmbedFactory, EmbedColor
from utils.permissions import is_moderator, PermissionChecker
from utils.converters import TimeConverter
from database.db_manager import DatabaseManager
from database.models import Warning

logger = logging.getLogger(__name__)


class Moderation(commands.Cog):
    """Moderation system cog"""

    def __init__(self, bot: commands.Bot, db: DatabaseManager, config: dict):
        self.bot = bot
        self.db = db
        self.config = config
        self.module_config = config.get('modules', {}).get('moderation', {})
        self.spam_tracker = {}  # Track spam
        self.toxicity_filter_enabled = self.module_config.get('auto_mod', {}).get('toxicity_filter', True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Auto-moderation on messages"""
        if not self.module_config.get('enabled', True):
            return

        if message.author.bot or not message.guild:
            return

        # Check spam
        if self.module_config.get('auto_mod', {}).get('spam_detection', True):
            await self._check_spam(message)

        # Check excessive mentions
        max_mentions = self.module_config.get('auto_mod', {}).get('max_mentions', 5)
        if len(message.mentions) > max_mentions:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} Please don't spam mentions!",
                delete_after=5
            )
            return

    async def _check_spam(self, message: discord.Message):
        """Check for spam messages"""
        user_id = message.author.id
        current_time = datetime.utcnow().timestamp()

        if user_id not in self.spam_tracker:
            self.spam_tracker[user_id] = []

        # Add message timestamp
        self.spam_tracker[user_id].append(current_time)

        # Remove old timestamps (older than 5 seconds)
        self.spam_tracker[user_id] = [
            ts for ts in self.spam_tracker[user_id]
            if current_time - ts < 5
        ]

        # Check if spam threshold exceeded
        if len(self.spam_tracker[user_id]) > 5:
            try:
                await message.author.timeout(timedelta(minutes=5), reason="Spam detected")
                await message.channel.send(
                    f"{message.author.mention} has been timed out for 5 minutes due to spam.",
                    delete_after=10
                )
                self.spam_tracker[user_id] = []
                logger.info(f"Auto-muted {message.author} for spam")
            except discord.Forbidden:
                pass

    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.describe(
        user="User to warn",
        reason="Reason for warning"
    )
    @is_moderator()
    async def warn(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str
    ):
        """Warn a user"""
        can_moderate, error = PermissionChecker.can_moderate(interaction.user, user)
        if not can_moderate:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Cannot Warn", error),
                ephemeral=True
            )
            return

        # Create warning
        warning = Warning(
            moderator_id=interaction.user.id,
            reason=reason
        )

        # Get or create user
        user_data = await self.db.get_user(user.id, interaction.guild.id)
        if not user_data:
            user_data = await self.db.create_user(user.id, interaction.guild.id)

        # Add warning
        await self.db.add_warning(user.id, interaction.guild.id, warning.to_dict())

        # Get total warnings
        warnings = await self.db.get_warnings(user.id, interaction.guild.id)

        embed = EmbedFactory.moderation_action("Warning", user, interaction.user, reason)
        embed.add_field(name="Total Warnings", value=str(len(warnings)), inline=False)

        await interaction.response.send_message(embed=embed)

        # DM user
        try:
            dm_embed = EmbedFactory.warning(
                "You have been warned",
                f"**Server:** {interaction.guild.name}\n**Reason:** {reason}\n**Total Warnings:** {len(warnings)}"
            )
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            pass

        # Log
        await self._log_action(interaction.guild, embed)
        logger.info(f"{interaction.user} warned {user} in {interaction.guild}")

    @app_commands.command(name="warnings", description="View user warnings")
    @app_commands.describe(user="User to check")
    @is_moderator()
    async def warnings(self, interaction: discord.Interaction, user: discord.Member):
        """View user warnings"""
        warnings = await self.db.get_warnings(user.id, interaction.guild.id)

        if not warnings:
            await interaction.response.send_message(
                embed=EmbedFactory.info("No Warnings", f"{user.mention} has no warnings."),
                ephemeral=True
            )
            return

        description = ""
        for i, warning in enumerate(warnings, 1):
            moderator = interaction.guild.get_member(warning['moderator_id'])
            mod_name = moderator.mention if moderator else f"<@{warning['moderator_id']}>"
            timestamp = datetime.fromtimestamp(warning['timestamp']).strftime("%Y-%m-%d %H:%M")
            description += f"**{i}.** {warning['reason']}\n   *By {mod_name} on {timestamp}*\n\n"

        embed = EmbedFactory.create(
            title=f"⚠️ Warnings for {user.display_name}",
            description=description,
            color=EmbedColor.WARNING,
            thumbnail=user.display_avatar.url
        )
        embed.set_footer(text=f"Total warnings: {len(warnings)}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="timeout", description="Timeout a user")
    @app_commands.describe(
        user="User to timeout",
        duration="Duration (e.g., 1h, 30m, 1d)",
        reason="Reason for timeout"
    )
    @is_moderator()
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        duration: str,
        reason: str = "No reason provided"
    ):
        """Timeout a user"""
        can_moderate, error = PermissionChecker.can_moderate(interaction.user, user)
        if not can_moderate:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Cannot Timeout", error),
                ephemeral=True
            )
            return

        seconds = TimeConverter.parse(duration)
        if not seconds or seconds > 2419200:  # Max 28 days
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Duration", "Duration must be valid and less than 28 days"),
                ephemeral=True
            )
            return

        try:
            await user.timeout(timedelta(seconds=seconds), reason=reason)
            embed = EmbedFactory.moderation_action("Timeout", user, interaction.user, reason)
            embed.add_field(name="Duration", value=TimeConverter.format_seconds(seconds), inline=False)
            await interaction.response.send_message(embed=embed)

            # DM user
            try:
                dm_embed = EmbedFactory.warning(
                    "You have been timed out",
                    f"**Server:** {interaction.guild.name}\n**Duration:** {TimeConverter.format_seconds(seconds)}\n**Reason:** {reason}"
                )
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                pass

            # Log
            await self._log_action(interaction.guild, embed)
            logger.info(f"{interaction.user} timed out {user} for {duration} in {interaction.guild}")

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to timeout this user"),
                ephemeral=True
            )

    @app_commands.command(name="kick", description="Kick a user")
    @app_commands.describe(
        user="User to kick",
        reason="Reason for kick"
    )
    @is_moderator()
    async def kick(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "No reason provided"
    ):
        """Kick a user"""
        can_moderate, error = PermissionChecker.can_moderate(interaction.user, user)
        if not can_moderate:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Cannot Kick", error),
                ephemeral=True
            )
            return

        try:
            # DM user before kicking
            try:
                dm_embed = EmbedFactory.warning(
                    "You have been kicked",
                    f"**Server:** {interaction.guild.name}\n**Reason:** {reason}"
                )
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                pass

            await user.kick(reason=reason)
            embed = EmbedFactory.moderation_action("Kick", user, interaction.user, reason)
            await interaction.response.send_message(embed=embed)

            # Log
            await self._log_action(interaction.guild, embed)
            logger.info(f"{interaction.user} kicked {user} from {interaction.guild}")

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to kick this user"),
                ephemeral=True
            )

    @app_commands.command(name="ban", description="Ban a user")
    @app_commands.describe(
        user="User to ban",
        reason="Reason for ban",
        delete_messages="Delete messages from last N days (0-7)"
    )
    @is_moderator()
    async def ban(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str = "No reason provided",
        delete_messages: int = 0
    ):
        """Ban a user"""
        can_moderate, error = PermissionChecker.can_moderate(interaction.user, user)
        if not can_moderate:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Cannot Ban", error),
                ephemeral=True
            )
            return

        if delete_messages < 0 or delete_messages > 7:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Parameter", "delete_messages must be between 0-7"),
                ephemeral=True
            )
            return

        try:
            # DM user before banning
            try:
                dm_embed = EmbedFactory.error(
                    "You have been banned",
                    f"**Server:** {interaction.guild.name}\n**Reason:** {reason}"
                )
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                pass

            await user.ban(reason=reason, delete_message_days=delete_messages)
            embed = EmbedFactory.moderation_action("Ban", user, interaction.user, reason)
            await interaction.response.send_message(embed=embed)

            # Log
            await self._log_action(interaction.guild, embed)
            logger.info(f"{interaction.user} banned {user} from {interaction.guild}")

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to ban this user"),
                ephemeral=True
            )

    @app_commands.command(name="unban", description="Unban a user")
    @app_commands.describe(user_id="ID of user to unban")
    @is_moderator()
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str
    ):
        """Unban a user"""
        try:
            user_id_int = int(user_id)
            user = await self.bot.fetch_user(user_id_int)
            await interaction.guild.unban(user)

            embed = EmbedFactory.success(
                "User Unbanned",
                f"{user.mention} ({user.id}) has been unbanned by {interaction.user.mention}"
            )
            await interaction.response.send_message(embed=embed)

            # Log
            await self._log_action(interaction.guild, embed)
            logger.info(f"{interaction.user} unbanned {user} in {interaction.guild}")

        except ValueError:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid ID", "Please provide a valid user ID"),
                ephemeral=True
            )
        except discord.NotFound:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Not Found", "This user is not banned"),
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to unban users"),
                ephemeral=True
            )

    async def _log_action(self, guild: discord.Guild, embed: discord.Embed):
        """Log moderation action to log channel"""
        guild_config = await self.db.get_guild(guild.id)
        if not guild_config:
            return

        log_channel_id = guild_config.get('log_channel')
        if not log_channel_id:
            return

        log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                logger.warning(f"Cannot send to log channel in {guild}")


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(Moderation(bot, bot.db, bot.config))
