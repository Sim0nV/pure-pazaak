import discord
from discord.ext import commands
from discord import app_commands, Embed

from constants import env, colors


class PazaakHelp(commands.Cog):
    """Cog for help command"""

    HELP_EMBED_DICT: dict = {
        "title": "Pazaak Commands",
        "color": colors.RULES_HELP_COLOUR_VALUE,
        "thumbnail": {"url": env.RULES_HELP_THUMBNAIL},
        "fields": [
            {
                "name": "``/pazaak [<@user>]\n$p [<@user>]``",
                "value": "Challenge someone to a Pazaak match",
            },
            {
                "name": "``/rules\n$pazaak_rules``",
                "value": "Learn the rules of Pazaak",
            },
            {
                "name": "``/sfx\n$pazaak_sfx``",
                "value": "Toggle Pazaak sound effects during the match",
            },
            {
                "name": "``/stats [<@user>] \n$ps [<@user>]``",
                "value": "View stats of a user or yourself",
            },
            {
                "name": "``/help\n$pazaak_help``",
                "value": "Show complete list of commands for Pure Pazaak",
            },
            {
                "name": "``/acknowledgements``",
                "value": "See who helped make this bot possible",
            },
        ],
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("pazaak_help cog loaded")

    @app_commands.command(
        name="help",
        description="Complete list of commands for Pure Pazaak",
    )
    async def help_slash_command(self, interaction: discord.Interaction):
        """Slash command for help

        Args:
            interaction (discord.Interaction): Interaction for command
        """
        await interaction.response.defer()
        await interaction.followup.send(
            embed=Embed.from_dict(self.HELP_EMBED_DICT)
        )

    @commands.command(name="pazaak_help")
    async def pazaak_help_command(self, ctx: commands.Context):
        """Discord command for help

        Args:
            ctx (commands.Context): Context of command
        """
        await ctx.defer()
        await ctx.reply(embed=Embed.from_dict(self.HELP_EMBED_DICT))


async def setup(bot):
    """Adds pazaak help cog to passed bot

    Args:
        bot (discord.Bot): Bot for cog to be added
    """
    await bot.add_cog(PazaakHelp(bot))
