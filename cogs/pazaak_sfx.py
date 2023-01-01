import discord
from discord.ext import commands
from discord import Member, VoiceState, VoiceClient, Embed

import asyncio
from random import randint

from constants import colors, env, strings
from utils.get_prefix_info_embed import get_prefix_info_embed


class PazaakSFX(commands.Cog):
    """Cog for sfx command"""

    JOIN_CHANNEL_ERROR_STR = (
        "please join a voice channel to use the sfx command!"
    )
    SERVER_CHANNEL_ERROR_STR = (
        "the sfx command can only be used in a server text channel!"
    )
    SAME_CHANNEL_ERROR_STR = (
        "you must be in the same voice channel as me to use the sfx command!"
    )
    FAIL_JOIN_ERROR_STR = (
        "I have failed to join your voice channel! Please make sure the"
        " channel is not private. "
    )

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("pazaak_sfx cog loaded")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        """On voice state update callback

        Args:
            member (Member): The member whose voice states changed.
            before (VoiceState): The voice state prior to the changes.
            after (VoiceState): The voice state after the changes.
        """
        voice_client: VoiceClient = discord.utils.get(
            self.bot.voice_clients, guild=member.guild
        )
        if voice_client:
            INACTIVITY_TIME_SEC = 300
            if len(voice_client.channel.members) <= 1:
                # If bot is connected and is alone, disconnect
                await voice_client.disconnect()
            elif not before.channel:
                # If bot just joined channel, start inactivity timer
                time = 0
                while True:
                    await asyncio.sleep(1)
                    time = time + 1
                    if (
                        voice_client.is_playing()
                        and not voice_client.is_paused()
                    ):
                        # If sound plays, reset timer
                        time = 0
                    if time == INACTIVITY_TIME_SEC:
                        # If inactivity time reached, disconnect
                        await voice_client.disconnect()
                    if not voice_client.is_connected():
                        break

    def get_error_embed(self, error_message: str, user: discord.User):
        """Get embed for Pazaak error

        Args:
            error_message (str): Error message to include in embed
            user (discord.User): User to mention in
                embed description

        Returns:
            discord.Embed: Embed for Pazaak error
        """

        MENTION_USER = "<@" + str(user.id) + ">"

        ERROR_EMBED_DICT = {
            "title": strings.SFX_TITLE,
            "description": MENTION_USER + ", " + error_message,
            "color": colors.ERROR_COLOUR_VALUE,
            "thumbnail": {
                "url": env.ERROR_THUMBNAILS[
                    randint(0, len(env.ERROR_THUMBNAILS) - 1)
                ]
            },
        }
        embed = Embed.from_dict(ERROR_EMBED_DICT)
        return embed

    async def is_valid_context(
        self, ctx: commands.Context, user: discord.User
    ) -> bool:
        """Error checks sfx command context.
        Returns true if context is valid for sfx command,
        False otherwise.

        Args:
            ctx (commands.Context): Context of command

        Returns:
            bool: True if context is valid for sfx command,
            False otherwise
        """
        is_valid_context: bool = False

        if ctx.guild:
            if ctx.message.author.voice:
                is_valid_context = True
            else:
                await ctx.reply(
                    embed=self.get_error_embed(
                        self.JOIN_CHANNEL_ERROR_STR, user
                    )
                )
        else:
            await ctx.reply(
                embed=self.get_error_embed(self.SERVER_CHANNEL_ERROR_STR, user)
            )
        return is_valid_context

    async def toggle_sfx(self, ctx: commands.Context, user: discord.User):
        """Toggles sound effects

        Args:
            ctx (commands.Context): Context of command
        """
        await ctx.defer()

        MENTION_USER = "<@" + str(user.id) + ">"

        OFF_EMBED_DICT: dict = {
            "title": strings.SFX_TITLE,
            "description": MENTION_USER + ", " + "sound effects are now off.",
            "color": colors.RULES_HELP_COLOUR_VALUE,
            "thumbnail": {
                "url": env.SFX_OFF_THUMBNAILS[
                    randint(0, len(env.SFX_OFF_THUMBNAILS) - 1)
                ]
            },
        }

        ON_EMBED_DICT: dict = {
            "title": strings.SFX_TITLE,
            "description": MENTION_USER + ", " + "sound effects are now on!",
            "color": colors.RULES_HELP_COLOUR_VALUE,
            "thumbnail": {
                "url": env.SFX_ON_THUMBNAILS[
                    randint(0, len(env.SFX_ON_THUMBNAILS) - 1)
                ]
            },
        }

        # Check context
        is_valid_context = await self.is_valid_context(ctx, user)

        if is_valid_context:
            user_voice_channel = ctx.message.author.voice.channel
            voice_client: VoiceClient = discord.utils.get(
                self.bot.voice_clients, guild=ctx.guild
            )
            if not voice_client or (
                voice_client and not voice_client.is_connected()
            ):
                try:
                    # If voice client disconnected, connect and notify user
                    voice_client = await user_voice_channel.connect(
                        timeout=10.0, self_deaf=True
                    )
                    await ctx.reply(embed=Embed.from_dict(ON_EMBED_DICT))
                except Exception as e:
                    await ctx.reply(
                        embed=self.get_error_embed(
                            self.FAIL_JOIN_ERROR_STR + str(e),
                            user,
                        )
                    )
            elif user_voice_channel.id != voice_client.channel.id:
                # If user not in same voice channel as bot, send error
                await ctx.reply(
                    embed=self.get_error_embed(
                        self.SAME_CHANNEL_ERROR_STR, user
                    )
                )
            elif voice_client and voice_client.is_connected():
                # If voice client connected and user in same voice channel,
                # disconnect voice client and notify user
                await voice_client.disconnect()
                await ctx.reply(embed=Embed.from_dict(OFF_EMBED_DICT))

    @commands.hybrid_command(
        name="sfx",
        description=(
            "Toggle sound effects for Pazaak (must be in a voice channel)"
        ),
    )
    async def sfx_slash_command(self, ctx: commands.Context):
        """Hybrid command for sfx

        Args:
            ctx (commands.Context): Context of command
        """
        user = None

        if ctx.interaction:
            # If slash command,
            # set user to interaction's user
            user = ctx.interaction.user
            await self.toggle_sfx(ctx, user)
        elif ctx.message:
            # If prefix command, reply with prefix info embed
            await ctx.reply(embed=get_prefix_info_embed("/sfx"))

    @commands.command(name="pazaak_sfx")
    async def pazaak_sfx_command(self, ctx: commands.Context):
        """Discord command for sfx

        Args:
            ctx (commands.Context): Context of command
        """
        await ctx.reply(embed=get_prefix_info_embed("/sfx"))


async def setup(bot):
    """Adds pazaak sfx cog to passed bot

    Args:
        bot (discord.Bot): Bot for cog to be added
    """
    await bot.add_cog(PazaakSFX(bot))
