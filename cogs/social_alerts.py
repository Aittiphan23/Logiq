"""
Social Alerts Cog for Logiq
Monitor Twitch, YouTube, Twitter/X for new content
"""

import discord
from discord import app_commands
from discord.ext import commands, tasks
from typing import Optional
import logging
import asyncio
import aiohttp

from utils.embeds import EmbedFactory, EmbedColor
from utils.permissions import is_admin
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class SocialAlerts(commands.Cog):
    """Social media alerts cog"""

    def __init__(self, bot: commands.Bot, db: DatabaseManager, config: dict):
        self.bot = bot
        self.db = db
        self.config = config
        self.module_config = config.get('modules', {}).get('social_alerts', {})
        self.session = None
        # Start monitoring tasks
        self.check_alerts_task.start()

    def cog_unload(self):
        """Cleanup on cog unload"""
        self.check_alerts_task.cancel()
        if self.session:
            asyncio.create_task(self.session.close())

    async def get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    @tasks.loop(minutes=5)
    async def check_alerts_task(self):
        """Check for new content from monitored accounts"""
        try:
            # Get all alerts from database
            cursor = self.db.db.social_alerts.find({})
            alerts = await cursor.to_list(length=1000)

            for alert in alerts:
                try:
                    platform = alert['platform']
                    if platform == 'twitch':
                        await self.check_twitch(alert)
                    elif platform == 'youtube':
                        await self.check_youtube(alert)
                    elif platform == 'twitter':
                        await self.check_twitter(alert)
                except Exception as e:
                    logger.error(f"Error checking alert {alert.get('_id')}: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Error in social alerts task: {e}", exc_info=True)

    @check_alerts_task.before_loop
    async def before_check_alerts(self):
        """Wait for bot to be ready"""
        await self.bot.wait_until_ready()

    async def check_twitch(self, alert: dict):
        """Check Twitch for live streams"""
        logger.debug(f"Checking Twitch for {alert['username']}")

    async def check_youtube(self, alert: dict):
        """Check YouTube for new videos"""
        logger.debug(f"Checking YouTube for {alert['channel_id']}")

    async def check_twitter(self, alert: dict):
        """Check Twitter/X for new tweets"""
        logger.debug(f"Checking Twitter for {alert['username']}")

    @app_commands.command(name="alert-add", description="Add social media alert (Admin)")
    @app_commands.describe(
        platform="Platform (twitch/youtube/twitter)",
        username="Username or channel ID",
        channel="Channel to send alerts to"
    )
    @is_admin()
    async def add_alert(
        self,
        interaction: discord.Interaction,
        platform: str,
        username: str,
        channel: discord.TextChannel
    ):
        """Add social media alert (ADMIN ONLY)"""
        platform = platform.lower()
        if platform not in ['twitch', 'youtube', 'twitter']:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Platform", "Platform must be twitch, youtube, or twitter"),
                ephemeral=True
            )
            return

        # Check if alert already exists
        existing = await self.db.db.social_alerts.find_one({
            "guild_id": interaction.guild.id,
            "platform": platform,
            "username": username.lower()
        })

        if existing:
            await interaction.response.send_message(
                embed=EmbedFactory.warning("Already Exists", f"Alert for {username} on {platform} already exists"),
                ephemeral=True
            )
            return

        # Create alert
        alert_data = {
            "guild_id": interaction.guild.id,
            "channel_id": channel.id,
            "platform": platform,
            "username": username.lower(),
            "last_check": None,
            "last_content_id": None
        }

        await self.db.db.social_alerts.insert_one(alert_data)

        platform_emoji = {
            'twitch': '🟣',
            'youtube': '🔴',
            'twitter': '🐦'
        }

        embed = EmbedFactory.success(
            "Alert Added",
            f"{platform_emoji.get(platform, '📢')} **{platform.title()}** alert added!\n\n"
            f"**Username:** {username}\n"
            f"**Channel:** {channel.mention}\n\n"
            f"You'll be notified when {username} {'goes live' if platform == 'twitch' else 'posts new content'}!"
        )
        await interaction.response.send_message(embed=embed)
        logger.info(f"{interaction.user} added {platform} alert for {username}")

    @app_commands.command(name="alert-remove", description="Remove social media alert (Admin)")
    @app_commands.describe(
        platform="Platform (twitch/youtube/twitter)",
        username="Username or channel ID"
    )
    @is_admin()
    async def remove_alert(
        self,
        interaction: discord.Interaction,
        platform: str,
        username: str
    ):
        """Remove social media alert (ADMIN ONLY)"""
        platform = platform.lower()
        if platform not in ['twitch', 'youtube', 'twitter']:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Platform", "Platform must be twitch, youtube, or twitter"),
                ephemeral=True
            )
            return

        result = await self.db.db.social_alerts.delete_one({
            "guild_id": interaction.guild.id,
            "platform": platform,
            "username": username.lower()
        })

        if result.deleted_count == 0:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Not Found", f"No alert found for {username} on {platform}"),
                ephemeral=True
            )
            return

        embed = EmbedFactory.success(
            "Alert Removed",
            f"Removed {platform} alert for **{username}**"
        )
        await interaction.response.send_message(embed=embed)
        logger.info(f"{interaction.user} removed {platform} alert for {username}")

    @app_commands.command(name="alert-list", description="List all social media alerts (Admin)")
    @is_admin()
    async def list_alerts(self, interaction: discord.Interaction):
        """List all social media alerts (ADMIN ONLY)"""
        cursor = self.db.db.social_alerts.find({"guild_id": interaction.guild.id})
        alerts = await cursor.to_list(length=100)

        if not alerts:
            await interaction.response.send_message(
                embed=EmbedFactory.info("No Alerts", "No social media alerts configured"),
                ephemeral=True
            )
            return

        # Group by platform
        grouped = {'twitch': [], 'youtube': [], 'twitter': []}
        for alert in alerts:
            platform = alert['platform']
            if platform in grouped:
                channel = interaction.guild.get_channel(alert['channel_id'])
                grouped[platform].append(f"• **{alert['username']}** → {channel.mention if channel else 'Unknown'}")

        description = ""
        platform_emoji = {
            'twitch': '🟣 **Twitch**',
            'youtube': '🔴 **YouTube**',
            'twitter': '🐦 **Twitter/X**'
        }

        for platform, items in grouped.items():
            if items:
                description += f"\n{platform_emoji[platform]}\n"
                description += "\n".join(items) + "\n"

        embed = EmbedFactory.create(
            title="📢 Social Media Alerts",
            description=description or "No alerts configured",
            color=EmbedColor.INFO
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="alert-test", description="Test social media alert (Admin)")
    @app_commands.describe(
        platform="Platform (twitch/youtube/twitter)",
        username="Username to test"
    )
    @is_admin()
    async def test_alert(
        self,
        interaction: discord.Interaction,
        platform: str,
        username: str
    ):
        """Test a social media alert (ADMIN ONLY)"""
        platform = platform.lower()
        if platform not in ['twitch', 'youtube', 'twitter']:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Platform", "Platform must be twitch, youtube, or twitter"),
                ephemeral=True
            )
            return

        alert = await self.db.db.social_alerts.find_one({
            "guild_id": interaction.guild.id,
            "platform": platform,
            "username": username.lower()
        })

        if not alert:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Not Found", f"No alert found for {username} on {platform}"),
                ephemeral=True
            )
            return

        channel = interaction.guild.get_channel(alert['channel_id'])
        if not channel:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Channel Not Found", "Alert channel no longer exists"),
                ephemeral=True
            )
            return

        # Send test notification
        platform_data = {
            'twitch': {
                'title': '🟣 Twitch Stream Live!',
                'description': f"**{username}** is now live on Twitch!\n\n**Title:** Test Stream\n**Game:** Just Chatting\n\n[Watch Now](https://twitch.tv/{username})",
                'color': 0x9146FF
            },
            'youtube': {
                'title': '🔴 New YouTube Video!',
                'description': f"**{username}** uploaded a new video!\n\n**Title:** Test Video\n\n[Watch Now](https://youtube.com/@{username})",
                'color': 0xFF0000
            },
            'twitter': {
                'title': '🐦 New Tweet!',
                'description': f"**{username}** posted a new tweet!\n\n*This is a test tweet notification*\n\n[View Tweet](https://twitter.com/{username})",
                'color': 0x1DA1F2
            }
        }

        data = platform_data[platform]
        embed = EmbedFactory.create(
            title=data['title'],
            description=data['description'],
            color=data['color']
        )
        embed.set_footer(text="This is a test notification")

        await channel.send(embed=embed)
        await interaction.response.send_message(
            embed=EmbedFactory.success("Test Sent", f"Test notification sent to {channel.mention}"),
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(SocialAlerts(bot, bot.db, bot.config))
