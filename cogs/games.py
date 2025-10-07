"""
Games Cog for Logiq
Interactive mini-games
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import logging
import random

from utils.embeds import EmbedFactory, EmbedColor
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class Games(commands.Cog):
    """Games and entertainment cog"""

    def __init__(self, bot: commands.Bot, db: DatabaseManager, config: dict):
        self.bot = bot
        self.db = db
        self.config = config
        self.module_config = config.get('modules', {}).get('games', {})
        self.trivia_questions = self._load_trivia()

    def _load_trivia(self):
        """Load trivia questions"""
        return [
            {
                "question": "What year was Python first released?",
                "options": ["1989", "1991", "1995", "2000"],
                "answer": 1
            },
            {
                "question": "What does CPU stand for?",
                "options": ["Central Processing Unit", "Computer Personal Unit", "Central Process Union", "Computer Processing Unit"],
                "answer": 0
            },
            {
                "question": "Who created Linux?",
                "options": ["Bill Gates", "Linus Torvalds", "Steve Jobs", "Dennis Ritchie"],
                "answer": 1
            },
            {
                "question": "What is the maximum value of a 32-bit signed integer?",
                "options": ["2,147,483,647", "4,294,967,295", "65,535", "2,147,483,648"],
                "answer": 0
            },
            {
                "question": "Which programming language is known as the 'mother of all languages'?",
                "options": ["C", "Assembly", "Fortran", "COBOL"],
                "answer": 0
            }
        ]

    @app_commands.command(name="trivia", description="Play a trivia game")
    async def trivia(self, interaction: discord.Interaction):
        """Start trivia game"""
        if not self.module_config.get('enabled', True):
            await interaction.response.send_message(
                embed=EmbedFactory.error("Module Disabled", "Games module is currently disabled"),
                ephemeral=True
            )
            return

        # Select random question
        question_data = random.choice(self.trivia_questions)

        embed = EmbedFactory.create(
            title="🎯 Trivia Time!",
            description=f"**{question_data['question']}**\n\n" +
                       "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(question_data['options'])]),
            color=EmbedColor.INFO
        )
        embed.set_footer(text="You have 30 seconds to answer!")

        # Create buttons
        view = TriviaView(question_data['answer'], self)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="roulette", description="Play roulette with currency")
    @app_commands.describe(
        bet="Amount to bet",
        choice="Your bet (number 0-36, red, black, odd, even)"
    )
    async def roulette(self, interaction: discord.Interaction, bet: int, choice: str):
        """Play roulette"""
        if bet <= 0:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Bet", "Bet must be positive"),
                ephemeral=True
            )
            return

        # Check balance
        user_data = await self.db.get_user(interaction.user.id, interaction.guild.id)
        if not user_data:
            user_data = await self.db.create_user(interaction.user.id, interaction.guild.id)

        if user_data.get('balance', 0) < bet:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Insufficient Funds", "You don't have enough currency"),
                ephemeral=True
            )
            return

        # Spin roulette
        result = random.randint(0, 36)
        is_red = result in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        is_black = result != 0 and not is_red
        is_odd = result % 2 == 1
        is_even = result % 2 == 0 and result != 0

        won = False
        payout = 0
        choice = choice.lower()

        if choice.isdigit() and int(choice) == result:
            won = True
            payout = bet * 35
        elif choice == "red" and is_red:
            won = True
            payout = bet
        elif choice == "black" and is_black:
            won = True
            payout = bet
        elif choice == "odd" and is_odd:
            won = True
            payout = bet
        elif choice == "even" and is_even:
            won = True
            payout = bet

        if won:
            await self.db.add_balance(interaction.user.id, interaction.guild.id, payout)
            embed = EmbedFactory.success(
                "🎉 You Won!",
                f"The ball landed on **{result}** ({'Red' if is_red else 'Black' if is_black else 'Green'})!\n\n"
                f"You won **💎 {payout:,}**!"
            )
        else:
            await self.db.remove_balance(interaction.user.id, interaction.guild.id, bet)
            embed = EmbedFactory.error(
                "You Lost!",
                f"The ball landed on **{result}** ({'Red' if is_red else 'Black' if is_black else 'Green'})!\n\n"
                f"You lost **💎 {bet:,}**!"
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dice", description="Roll dice")
    @app_commands.describe(sides="Number of sides (default: 6)")
    async def dice(self, interaction: discord.Interaction, sides: int = 6):
        """Roll dice"""
        if sides < 2 or sides > 100:
            await interaction.response.send_message(
                embed=EmbedFactory.error("Invalid Dice", "Sides must be between 2 and 100"),
                ephemeral=True
            )
            return

        result = random.randint(1, sides)

        embed = EmbedFactory.create(
            title="🎲 Dice Roll",
            description=f"You rolled a **d{sides}** and got:\n\n# {result}",
            color=EmbedColor.INFO
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="8ball", description="Ask the magic 8-ball")
    @app_commands.describe(question="Your question")
    async def eightball(self, interaction: discord.Interaction, question: str):
        """Magic 8-ball"""
        responses = [
            "Yes, definitely!",
            "It is certain.",
            "Without a doubt.",
            "Most likely.",
            "Outlook good.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]

        response = random.choice(responses)

        embed = EmbedFactory.create(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n\n**Answer:** {response}",
            color=EmbedColor.INFO
        )

        await interaction.response.send_message(embed=embed)


class TriviaView(discord.ui.View):
    """View for trivia game"""

    def __init__(self, correct_answer: int, cog: Games):
        super().__init__(timeout=30)
        self.correct_answer = correct_answer
        self.cog = cog
        self.answered = False

    @discord.ui.button(label="1", style=discord.ButtonStyle.primary)
    async def option_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._check_answer(interaction, 0)

    @discord.ui.button(label="2", style=discord.ButtonStyle.primary)
    async def option_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._check_answer(interaction, 1)

    @discord.ui.button(label="3", style=discord.ButtonStyle.primary)
    async def option_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._check_answer(interaction, 2)

    @discord.ui.button(label="4", style=discord.ButtonStyle.primary)
    async def option_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._check_answer(interaction, 3)

    async def _check_answer(self, interaction: discord.Interaction, answer: int):
        """Check if answer is correct"""
        if self.answered:
            await interaction.response.send_message("This trivia has already been answered!", ephemeral=True)
            return

        self.answered = True
        correct = answer == self.correct_answer

        if correct:
            # Award currency
            await self.cog.db.add_balance(interaction.user.id, interaction.guild.id, 50)
            embed = EmbedFactory.success(
                "Correct! 🎉",
                f"{interaction.user.mention} got it right!\nYou earned **💎 50**!"
            )
        else:
            embed = EmbedFactory.error(
                "Incorrect! ❌",
                f"The correct answer was **{self.correct_answer + 1}**!"
            )

        # Disable all buttons
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    """Setup function for cog loading"""
    await bot.add_cog(Games(bot, bot.db, bot.config))
