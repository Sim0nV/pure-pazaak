import discord
from discord.ext import commands
from discord import app_commands, Embed

from constants import env, colors
from db.db import get_player_stats, get_match_record
from db.classes.player_stats import PlayerStats
from db.classes.match_record import MatchRecord
from utils.get_prefix_info_embed import get_prefix_info_embed


class PazaakStats(commands.Cog):
    """Cog for stats command"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("pazaak_stats cog loaded")

    def get_stats_embed(
        self, sender: discord.User, mentioned_user: discord.User = None
    ):
        """Returns stats embed for stats command

        Args:
            sender (discord.User): User who sent command
            mentioned_user (discord.User): Mentioned user. Defaults to None.

        Returns:
            Embed: Stats embed
        """

        # Show mentioned user stats if non-bot user
        # mentioned, else show sender stats
        player = (
            mentioned_user
            if mentioned_user and not mentioned_user.bot
            else sender
        )

        stats: PlayerStats = get_player_stats(player)

        stats_embed_dict: dict = {
            "title": "Pazaak Stats",
            "color": colors.RULES_HELP_COLOUR_VALUE,
            "thumbnail": {"url": env.STATS_THUMBNAIL},
            "fields": [
                {
                    "name": "Wins",
                    "value": "``"
                    + str(stats.wins)
                    + (
                        " ("
                        + str(round(stats.wins / (stats.total_games) * 100))
                        + "%)"
                        if stats.total_games > 0
                        else ""
                    )
                    + "``",
                    "inline": True,
                },
                {
                    "name": "Total Games",
                    "value": "``" + str(stats.total_games) + "``",
                    "inline": True,
                },
            ],
            "author": {
                "name": player.display_name + "'s Profile",
                "icon_url": player.display_avatar.url,
            },
        }

        if sender.id != player.id:
            # If non-bot user mentioned and user is not the same as sender,
            # Add match record to footer
            record: MatchRecord = get_match_record(sender, mentioned_user)
            stats_embed_dict["footer"] = {
                "text": str(sender.name)
                + " has a "
                + str(record.player_one_wins)
                + "-"
                + str(record.player_two_wins)
                + (
                    (
                        " ("
                        + str(
                            round(
                                (record.player_one_wins / record.total_matches)
                                * 100
                            )
                        )
                        + "%)"
                    )
                    if record.total_matches > 0
                    else ""
                )
                + " record against "
                + str(mentioned_user.name)
                + "!"
            }

        return Embed.from_dict(stats_embed_dict)

    @app_commands.command(
        name="stats",
        description="View your Pazaak stats",
    )
    @app_commands.describe(user="User to check stats of (Optional)")
    async def stats_slash_command(
        self, interaction: discord.Interaction, user: discord.User = None
    ):
        """Slash command for stats

        Args:
            interaction (discord.Interaction): Interaction for command
        """
        await interaction.response.defer()
        embed = self.get_stats_embed(interaction.user, user)
        await interaction.followup.send(embed=embed)

    @commands.command(name="ps")
    async def pazaak_stats_command(self, ctx: commands.Context):
        """Discord command for stats

        Args:
            ctx (commands.Context): Context of command
        """
        await ctx.reply(embed=get_prefix_info_embed("/stats"))


async def setup(bot):
    """Adds pazaak help cog to passed bot

    Args:
        bot (discord.Bot): Bot for cog to be added
    """
    await bot.add_cog(PazaakStats(bot))
