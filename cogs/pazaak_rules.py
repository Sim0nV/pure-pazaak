import discord
from discord.ext import commands
from discord import app_commands, Embed

from constants import env, colors


class PazaakRules(commands.Cog):
    """Cog for rules command"""

    # String for rules embed description
    RULES: str = (
        "TL;DR: Pazaak is Blackjack to 20 points, with playable plus or minus"
        " cards to manipulate your total. You can only play one card per turn."
        " The first to win three rounds wins the match.\n\nAt the beginning of"
        " the match, the game randomly decides who goes first and deals 4"
        " random cards to each player ranging from -6 to +6. The current"
        " player is then dealt a card from 1 to 10 at the start of each turn"
        " and has the choice to either: play a card, end their turn, stand, or"
        " forfeit. Only one card can be played per turn. If a player stands,"
        " their total remains the same until the end of the round. When the"
        " current player ends their turn, it becomes the other player's turn."
        " If the current player's total reaches 20, they automatically stand."
        " If the current player's total goes over 20 they bust, automatically"
        " losing the round.\n\nIf the current player decides to forfeit or"
        " doesn't respond in time, it will count as a loss in their record."
        " After 60 seconds pass, the other player can win by calling timeout."
        " After 5 minutes, a timeout occurs automatically.\n\nTo win, a player"
        " must either have a higher score (<=20) than the opponent at the end"
        " of the round, or have nine cards played (including dealer cards). If"
        " both players end with the same total, the round ends as a draw and"
        " no point is given to either player. The first player to win three"
        " rounds wins the match!"
    )

    # Dictionary for rules embed
    RULES_EMBED_DICT: dict = {
        "title": "Pazaak Ruleset",
        "description": RULES,
        "color": colors.RULES_HELP_COLOUR_VALUE,
        "thumbnail": {"url": env.RULES_HELP_THUMBNAIL},
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("pazaak_rules cog loaded")

    @app_commands.command(
        name="rules",
        description="Ruleset for Pure Pazaak",
    )
    async def rules_slash_command(self, interaction: discord.Interaction):
        """Slash command for rules

        Args:
            interaction (discord.Interaction): Interaction for command
        """
        await interaction.response.defer()
        if interaction.guild:
            # If command sent in server rather than DMs, reply in server
            await interaction.followup.send(
                content="<@"
                + str(interaction.user.id)
                + ">, please check your DMs for the Pazaak ruleset."
            )
        try:
            await interaction.user.send(
                embed=Embed.from_dict(self.RULES_EMBED_DICT)
            )
        except Exception as e:
            print("Failed to send rules embed: " + str(e))

    @commands.command(name="pazaak_rules")
    async def pazaak_rules_command(self, ctx: commands.Context):
        """Discord command for rules

        Args:
            ctx (commands.Context): Context of command
        """
        await ctx.defer()
        if ctx.guild:
            # If command sent in server rather than DMs, reply in server
            await ctx.reply(
                content="<@"
                + str(ctx.message.author.id)
                + ">, please check your DMs for the Pazaak ruleset."
            )
        try:
            await ctx.message.author.send(
                embed=Embed.from_dict(self.RULES_EMBED_DICT)
            )
        except Exception as e:
            print("Failed to send rules embed: " + str(e))


async def setup(bot):
    """Adds pazaak rules cog to passed bot

    Args:
        bot (discord.Bot): Bot for cog to be added
    """
    await bot.add_cog(PazaakRules(bot))
