import discord
from discord.ext import commands
from discord import Embed

from constants import env, colors, strings
from pazaak_match import challenge_player
from utils.get_prefix_info_embed import get_prefix_info_embed

from random import randint


class Pazaak(commands.Cog):
    """Cog for pazaak command"""

    # Embed dictionary for pazaak usage
    USAGE_EMBED_DICT = {
        "title": "Welcome to the Game of Pazaak",
        "description": (
            "Use the command ``/pazaak @player`` to"
            " challenge someone to a set of Pazaak!"
        ),
        "color": colors.PAZAAK_CHALLENGE_COLOUR_VALUE,
        "thumbnail": {"url": env.USAGE_THUMBNAIL},
        "footer": {"text": "Type /help for a complete list of commands"},
    }

    CHALLENGE_SELF_ERROR_STR = "you cannot challenge yourself!"
    CHALLENGE_BOT_ERROR_STR = "you cannot challenge a bot!"
    CHALLENGE_ME_ERROR_STR = "you cannot challenge me!"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("pazaak cog loaded")

    def get_error_embed(self, error_message: str, member: discord.Member):
        """Get embed for Pazaak error

        Args:
            error_message (str): Error message to include in embed
            member (discord.Member): Member to mention in
                embed description

        Returns:
            discord.Embed: Embed for Pazaak error
        """

        MENTION_MEMBER = "<@" + str(member.id) + ">"

        ERROR_EMBED_DICT = {
            "title": strings.CHALLENGE_TITLE,
            "description": MENTION_MEMBER
            + ", "
            + error_message
            + "\nUsage: ``/pazaak @player``",
            "color": colors.ERROR_COLOUR_VALUE,
            "thumbnail": {
                "url": env.ERROR_THUMBNAILS[
                    randint(0, len(env.ERROR_THUMBNAILS) - 1)
                ]
            },
        }
        embed = Embed.from_dict(ERROR_EMBED_DICT)
        return embed

    async def pazaak_command(
        self,
        ctx: commands.Context,
        player_one: discord.Member,
        player_two: discord.Member,
    ):
        """Outputs usage embed or sends challenge if player mentioned

        Args:
            ctx (commands.Context): Context of pazaak command
            player_one (discord.Member): Member for player one (challenger)
            player_two (discord.Member): Member for player two (challenged)
        """
        await ctx.defer()

        # Check parameters
        if not player_two:
            # If no player two parameter passed, reply with usage embed
            await ctx.reply(embed=Embed.from_dict(self.USAGE_EMBED_DICT))
        elif not player_one:
            # If player one does not exist, reply with error
            await ctx.reply(content="Error: player_one does not exist")
        elif player_two.id == player_one.id and not env.IS_DEBUG_MODE:
            # If member challenges themselves, reply with error embed
            await ctx.reply(
                embed=self.get_error_embed(
                    self.CHALLENGE_SELF_ERROR_STR, player_one
                )
            )
        elif (
            player_two.id == env.DEV_BOT_ID or player_two.id == env.PROD_BOT_ID
        ):
            # If member challenges Pure Pazaak, reply with error embed
            await ctx.reply(
                embed=self.get_error_embed(
                    self.CHALLENGE_ME_ERROR_STR, player_one
                )
            )
        elif player_two.bot:
            # If member challenges bot, reply with error embed
            await ctx.reply(
                embed=self.get_error_embed(
                    self.CHALLENGE_BOT_ERROR_STR, player_one
                )
            )
        else:
            # Send challenge message
            await challenge_player.send_challenge(
                ctx,
                player_one,
                player_two,
            )

    @commands.hybrid_command(
        name="pazaak",
        with_app_command=True,
        description="Challenge someone to a Pazaak match",
    )
    async def pazaak_hybrid_command(
        self, ctx: commands.Context, user: discord.Member = None
    ):
        """Hybrid command for pazaak, calls pazaak_command function

        Args:
            ctx (commands.Context): Context of command
        """

        player_one = None

        if ctx.interaction:
            # If slash command,
            # set player one to interaction's user
            player_one = ctx.interaction.user
            await self.pazaak_command(ctx, player_one, user)
        elif ctx.message:
            # If prefix command, reply with prefix info embed
            await ctx.reply(embed=get_prefix_info_embed("/pazaak"))

    @commands.command(name="p")
    async def p_shortcut_command(self, ctx: commands.Context):
        """Shortcut command for pazaak, calls pazaak_command function

        Args:
            ctx (commands.Context): Context of command
        """
        await ctx.reply(embed=get_prefix_info_embed("/pazaak"))


async def setup(bot):
    """Adds pazaak help cog to passed bot

    Args:
        bot (discord.Bot): Bot for cog to be added
    """
    await bot.add_cog(Pazaak(bot))
