"""
Leveling Cog for Logiq
XP and leveling system with rank cards
"""

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from typing import Optional
import logging
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from utils.embeds import EmbedFactory, EmbedColor
from utils.constants import calculate_level_xp
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class Leveling(commands.Cog):
    """Leveling system cog"""

    def __init__(self, bot: commands.Bot, db: DatabaseManager, config: dict):
        self.bot = bot
        self.db = db
        self.config = config
        self.module_config = config.get('modules', {}).get('leveling', {})
        self.xp_cooldown = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Award XP for messages"""
        if not self.module_config.get('enabled', True):
            return

        if message.author.bot or not message.guild:
            return

        # Check cooldown
        user_key = f"{message.guild.id}_{message.author.id}"
        current_time = datetime.utcnow().timestamp()

        if user_key in self.xp_cooldown:
            if current_time - self.xp_cooldown[user_key] < self.module_config.get('xp_cooldown', 60):
                return

        self.xp_cooldown[user_key] = current_time

        # Get or create user
        user_data = await self.db.get_user(message.author.id, message.guild.id)
        if not user_data:
            user_data = await self.db.create_user(message.author.id, message.guild.id)

        # Calculate XP
        xp_gain = self.module_config.get('xp_per_message', 10)
        new_xp = user_data.get('xp', 0) + xp_gain
        current_level = user_data.get('level', 0)

        # Check for level up
        next_level_xp = calculate_level_xp(current_level + 1)

        if new_xp >= next_level_xp:
            new_level = current_level + 1
            await self.db.update_user(message.author.id, message.guild.id, {
                'xp': new_xp,
                'level': new_level
            })

            # Send level up message
            embed = EmbedFactory.level_up(message.author, new_level, new_xp)
            await message.channel.send(embed=embed)
            logger.info(f"{message.author} leveled up to {new_level} in {message.guild}")
        else:
            await self.db.update_user(message.author.id, message.guild.id, {'xp': new_xp})

    @app_commands.command(name="rank", description="View your rank card")
    @app_commands.describe(user="User to check (optional)")
    async def rank(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        """View rank card"""
        target = user or interaction.user

        user_data = await self.db.get_user(target.id, interaction.guild.id)
        if not user_data:
            user_data = await self.db.create_user(target.id, interaction.guild.id)

        # Get rank
        leaderboard = await self.db.get_leaderboard(interaction.guild.id, limit=1000)
        rank = next((i + 1 for i, u in enumerate(leaderboard) if u['user_id'] == target.id), 0)

        level = user_data.get('level', 0)
        xp = user_data.get('xp', 0)
        next_level_xp = calculate_level_xp(level + 1)

        embed = EmbedFactory.rank_card(target, level, xp, rank, next_level_xp)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="View XP leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        """View leaderboard"""
        leaderboard = await self.db.get_leaderboard(interaction.guild.id, limit=10)

        if not leaderboard:
            await interaction.response.send_message(
                embed=EmbedFactory.info("No Data", "No leaderboard data available"),
                ephemeral=True
            )
            return

        embed = EmbedFactory.leaderboard(
            "XP Leaderboard",
            leaderboard,
            field_name="xp",
            color=EmbedColor.LEVELING
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setlevel", description="Set user's level (Admin only)")
    @app_commands.describe(
        user="User to modify",
        level="New level"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_level(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        level: int
    ):
        """Set user level"""
        if level < 0:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Level", "Level must be 0 or greater"),
                ephemeral=True
            )
            return

        xp = sum(calculate_level_xp(i) for i in range(1, level + 1))

        await self.db.update_user(user.id, interaction.guild.id, {
            'level': level,
            'xp': xp
        })

        embed = EmbedFactory.success(
            "Level Set",
            f"Set {user.mention}'s level to **{level}**"
        )
        await interaction.response.send_message(embed=embed)
        logger.info(f"{interaction.user} set {user}'s level to {level}")

    @app_commands.command(name="resetlevels", description="Reset all levels (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_levels(self, interaction: discord.Interaction):
        """Reset all levels in guild"""
        # This would require a bulk update - implementing basic version
        await interaction.response.send_message(
            embed=EmbedFactory.warning(
                "Reset Levels",
                "This feature will reset all user levels. This is a destructive action.\n\n"
                "To implement: Use database bulk operations to reset all users in this guild."
            ),
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(Leveling(bot, bot.db, bot.config))
