import discord
from discord.ext import commands
from discord import app_commands, Embed

from constants import env, colors


class PazaakAck(commands.Cog):
    """Cog for acknowledgements command"""

    ACK_EMBED_DICT: dict = {
        "title": "Acknowledgements",
        "description": "See who helped make this bot possible [here]("
        + env.ACK_URL
        + ").",
        "color": colors.RULES_HELP_COLOUR_VALUE,
        "thumbnail": {"url": env.RULES_HELP_THUMBNAIL},
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("pazaak_ack cog loaded")

    @app_commands.command(
        name="acknowledgements",
        description="Acknowledgements for Pure Pazaak",
    )
    async def ack_slash_command(self, interaction: discord.Interaction):
        """Slash command for acknowledgements

        Args:
            interaction (discord.Interaction): Interaction for command
        """
        await interaction.response.defer()
        await interaction.followup.send(
            embed=Embed.from_dict(self.ACK_EMBED_DICT)
        )


async def setup(bot):
    """Adds pazaak acknowledgements cog to passed bot

    Args:
        bot (discord.Bot): Bot for cog to be added
    """
    await bot.add_cog(PazaakAck(bot))
