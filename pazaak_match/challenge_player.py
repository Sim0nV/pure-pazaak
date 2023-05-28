import discord
from discord import Interaction, Embed
from discord.ext import commands
from discord.ui import View, Button

from constants import env, colors, strings
from .play_match import begin_match
from random import randint


class ChallengeMenu(View):
    """Challenge player menu"""

    def __init__(
        self,
        player_one: discord.Member,
        player_two: discord.Member,
        message: discord.Message,
        guild: discord.Guild,
    ):
        super().__init__()
        self.value = None
        self.timeout = 900.0
        self.player_one = player_one
        self.player_two = player_two
        self.message = message
        self.guild = guild

    CHALLENGE_TIMEOUT_ERROR_STR = "Pazaak challenge request timed out."
    CHALLENGE_DECLINED_STR = "Pazaak challenge request declined."
    CHALLENGE_WITHDRAWN_STR = "Pazaak challenge request withdrawn."
    ERROR_EMBED_DICT = {
        "title": strings.CHALLENGE_TITLE,
        "color": colors.ERROR_COLOUR_VALUE,
        "thumbnail": {
            "url": env.ERROR_THUMBNAILS[
                randint(0, len(env.ERROR_THUMBNAILS) - 1)
            ]
        },
    }

    @discord.ui.button(emoji="✅", style=discord.ButtonStyle.grey)
    async def accept(self, interaction: Interaction, button: Button):
        """Accept button callback, if pressed by challenged
        member then start challenge and stop listening to
        challenge menu interaction events

        Args:
            interaction (Interaction): Button interaction
            button (Button): Accept button
        """
        if interaction.user.id == self.player_two.id:
            await interaction.response.defer()
            self.stop_listening_challenge_menu()
            try:
                await begin_match(
                    interaction.client,
                    self.player_one,
                    self.player_two,
                    self.message,
                    self.guild,
                )
            except Exception as e:
                # If error occurs, send to channel and raise
                # so it shows in logs
                MENTION_USERS_CONTENT = (
                    "<@"
                    + str(self.player_one.id)
                    + ">"
                    + "<@"
                    + str(self.player_two.id)
                    + ">"
                )
                BEGIN_ERROR_EMBED_DICT = {
                    **self.ERROR_EMBED_DICT,
                    **{
                        "description": "Error: "
                        + str(e)
                        + "\n\n"
                        + strings.SUPPORT_SERVER_PLEASE_REPORT
                    },
                }
                await interaction.followup.send(
                    content=MENTION_USERS_CONTENT,
                    embed=Embed.from_dict(BEGIN_ERROR_EMBED_DICT),
                )
                await self.player_one.send(
                    content=MENTION_USERS_CONTENT,
                    embed=Embed.from_dict(BEGIN_ERROR_EMBED_DICT),
                )
                await self.player_two.send(
                    content=MENTION_USERS_CONTENT,
                    embed=Embed.from_dict(BEGIN_ERROR_EMBED_DICT),
                )
                raise e

    @discord.ui.button(emoji="❌", style=discord.ButtonStyle.grey)
    async def decline(self, interaction: Interaction, button: Button):
        """Decline button callback, show decline embed

        Args:
            interaction (Interaction): Button interaction
            button (Button): Decline button
        """
        if interaction.user.id == self.player_one.id:
            await self.show_error_embed(self.CHALLENGE_WITHDRAWN_STR)
        elif interaction.user.id == self.player_two.id:
            await self.show_error_embed(self.CHALLENGE_DECLINED_STR)

    async def show_error_embed(self, description):
        """Edit message to show error embed, then
        stop listening to interaction events

        Args:
            description (str): Description of error embed
        """
        DESC_ERROR_EMBED_DICT = {
            **self.ERROR_EMBED_DICT,
            **{"description": description},
        }
        await self.message.edit(
            embed=Embed.from_dict(DESC_ERROR_EMBED_DICT), view=None
        )
        self.stop_listening_challenge_menu()

    def stop_listening_challenge_menu(self):
        """Clear challenge menu items, stop listening
        to challenge menu interactions
        """
        self.clear_items()
        self.value = False
        self.stop()

    async def on_timeout(self):
        """Timeout callback, show timeout embed"""
        await self.show_error_embed(self.CHALLENGE_TIMEOUT_ERROR_STR)


async def send_challenge(
    ctx: commands.Context,
    player_one: discord.Member,
    player_two: discord.Member,
):
    """Send pazaak challenge message

    Args:
        ctx (commands.Context): Context for pazaak challenge
        player_one (discord.Member): Member who sent challenge
        player_two (discord.Member): Member who is receiving challenge
    """
    MENTION_PLAYER_ONE = "<@" + str(player_one.id) + ">"
    MENTION_PLAYER_TWO = "<@" + str(player_two.id) + ">"
    CHALLENGE_MESSAGE_CONTENT = (
        MENTION_PLAYER_TWO
        + ", would you like to play a game of pazaak with "
        + MENTION_PLAYER_ONE
        + "?"
    )

    CHALLENGE_EMBED_DICT = {
        "title": strings.CHALLENGE_TITLE,
        "description": MENTION_PLAYER_TWO
        + ", "
        + MENTION_PLAYER_ONE
        + " has challenged you to a game of Pazaak.\n\nDo you accept?",
        "color": colors.PAZAAK_CHALLENGE_COLOUR_VALUE,
        "thumbnail": {
            "url": env.CHALLENGE_THUMBNAILS[
                randint(0, len(env.CHALLENGE_THUMBNAILS) - 1)
            ]
        },
    }

    channel_message = await ctx.send(
        content="Loading...",
    )

    await channel_message.edit(
        content=CHALLENGE_MESSAGE_CONTENT,
        embed=Embed.from_dict(CHALLENGE_EMBED_DICT),
        view=ChallengeMenu(player_one, player_two, channel_message, ctx.guild),
    )
