"""
Roles Cog for Logiq
Self-assignable roles with exclusive categories
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


class ExclusiveRoleSelect(discord.ui.Select):
    """Dropdown for exclusive role selection (pick only one)"""

    def __init__(self, roles: List[discord.Role], category_name: str):
        options = [
            discord.SelectOption(
                label=role.name,
                description=f"Select {role.name}",
                value=str(role.id),
                emoji="🎭"
            )
            for role in roles[:25]
        ]

        super().__init__(
            placeholder=f"Choose your {category_name}",
            min_values=1,
            max_values=1,
            options=options,
            custom_id=f"exclusive_role_{category_name}"
        )
        self.role_ids = [role.id for role in roles]
        self.category_name = category_name

    async def callback(self, interaction: discord.Interaction):
        """Handle exclusive role selection"""
        selected_role_id = int(self.values[0])
        selected_role = interaction.guild.get_role(selected_role_id)

        if not selected_role:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "Role not found"),
                ephemeral=True
            )
            return

        # Remove all other roles in this category
        roles_to_remove = []
        for role_id in self.role_ids:
            if role_id != selected_role_id:
                role = interaction.guild.get_role(role_id)
                if role and role in interaction.user.roles:
                    roles_to_remove.append(role)

        try:
            if roles_to_remove:
                await interaction.user.remove_roles(*roles_to_remove)

            if selected_role not in interaction.user.roles:
                await interaction.user.add_roles(selected_role)

            embed = EmbedFactory.success(
                "Role Updated",
                f"You now have the {selected_role.mention} role!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to manage roles"),
                ephemeral=True
            )


class ExclusiveRoleView(discord.ui.View):
    """View for exclusive role selection"""

    def __init__(self, roles: List[discord.Role], category_name: str):
        super().__init__(timeout=None)
        self.add_item(ExclusiveRoleSelect(roles, category_name))


class RoleSelectMenu(discord.ui.Select):
    """Dropdown menu for multiple role selection"""

    def __init__(self, roles: List[discord.Role]):
        options = [
            discord.SelectOption(
                label=role.name,
                description=f"Get the {role.name} role",
                value=str(role.id),
                emoji="🎭"
            )
            for role in roles[:25]
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
        self.self_assign_roles = {}

    @app_commands.command(name="exclusive-role-category", description="Create exclusive role category (pick one only)")
    @app_commands.describe(
        category_name="Name of the category (e.g., Region, Team)",
        roles="Roles to include (mention them)"
    )
    @is_admin()
    async def exclusive_role_category(self, interaction: discord.Interaction, category_name: str, roles: str):
        """Create exclusive role category"""
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
                embed=EmbedFactory.error("Too Many Roles", "Maximum 25 roles per category"),
                ephemeral=True
            )
            return

        embed = EmbedFactory.create(
            title=f"🎭 {category_name}",
            description=f"Select ONE {category_name} from the dropdown below.\n\n"
                       "**Available Options:**\n" + "\n".join([f"• {role.mention}" for role in role_list]),
            color=EmbedColor.PRIMARY
        )

        view = ExclusiveRoleView(role_list, category_name)

        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(
            embed=EmbedFactory.success("Category Created", f"Exclusive role category '{category_name}' created!"),
            ephemeral=True
        )

        logger.info(f"Exclusive role category '{category_name}' created in {interaction.guild}")

    @app_commands.command(name="role-menu", description="Create multi-select role menu")
    @app_commands.describe(roles="Roles to make self-assignable (mention them)")
    @is_admin()
    async def role_menu(self, interaction: discord.Interaction, roles: str):
        """Create role selection menu"""
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

        embed = EmbedFactory.create(
            title="🎭 Self-Assignable Roles",
            description="Select roles from the dropdown menu below.\n\n"
                       "**Available Roles:**\n" + "\n".join([f"• {role.mention}" for role in role_list]),
            color=EmbedColor.PRIMARY
        )

        view = RoleSelectView(role_list)

        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(
            embed=EmbedFactory.success("Menu Created", "Role menu has been created!"),
            ephemeral=True
        )

        self.self_assign_roles[interaction.guild.id] = [role.id for role in role_list]
        logger.info(f"Role menu created in {interaction.guild} with {len(role_list)} roles")

    @app_commands.command(name="addrole", description="Add a role to a user (Admin)")
    @app_commands.describe(user="User to add role to", role="Role to add")
    @is_admin()
    async def add_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        """Add role to user"""
        if role in user.roles:
            await interaction.response.send_message(
                embed=EmbedFactory.info("Already Has Role", f"{user.mention} already has {role.mention}"),
                ephemeral=True
            )
            return

        try:
            await user.add_roles(role)
            embed = EmbedFactory.success("Role Added", f"Added {role.mention} to {user.mention}")
            await interaction.response.send_message(embed=embed)
            logger.info(f"{interaction.user} added role {role} to {user}")
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to manage roles"),
                ephemeral=True
            )

    @app_commands.command(name="removerole", description="Remove a role from a user (Admin)")
    @app_commands.describe(user="User to remove role from", role="Role to remove")
    @is_admin()
    async def remove_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        """Remove role from user"""
        if role not in user.roles:
            await interaction.response.send_message(
                embed=EmbedFactory.info("Doesn't Have Role", f"{user.mention} doesn't have {role.mention}"),
                ephemeral=True
            )
            return

        try:
            await user.remove_roles(role)
            embed = EmbedFactory.success("Role Removed", f"Removed {role.mention} from {user.mention}")
            await interaction.response.send_message(embed=embed)
            logger.info(f"{interaction.user} removed role {role} from {user}")
        except discord.Forbidden:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Error", "I don't have permission to manage roles"),
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(Roles(bot, bot.db, bot.config))
