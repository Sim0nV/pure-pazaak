from discord import Message, Member, Embed, Guild
from discord.ext.commands import Bot

import random

from asyncio import sleep

from .classes.match_data import MatchData
from constants import env, strings, colors, numbers
from .update_embed import update_embed_with_match_data
from .enums.match_status import MatchStatus
from .enums.round_status import RoundStatus
from .enums.turn_status import TurnResult
from .classes.match_menu import MatchMenu
from .classes.match_messages import MatchMessages
from .handle_match_timeout import handle_match_timeout

from db.db import save_to_db
from .match_sfx import MatchSfx


class MatchPlayer:
    """Class for playing pazaak match"""

    MATCH_WAIT_TIME: int = 5  # Time to transition between embeds

    def __init__(
        self,
        match: MatchData,
        messages: MatchMessages,
        match_sfx: MatchSfx,
        thumbnail_index: int,
    ) -> None:
        self.match = match
        self.messages = messages
        self.match_sfx = match_sfx
        self.did_current_player_go_first = match.is_current_player_one
        self.thumbnail_index = thumbnail_index

    async def play_match(self):
        """Play pazaak rounds until match is over, then ends match"""
        while self.match.status == MatchStatus.IN_PROGRESS:
            self.match.reset_round_data()
            await self.play_round()
        await self.end_match()

    async def end_match(self):
        """Output match end embed based on match data"""

        CURRENT_TURN_USER_WIN_DESC = (
            "**Set "
            + str(self.match.round_number)
            + "** - "
            + "<@"
            + str(self.match.current_player_data.member.id)
            + "> has defeated <@"
            + str(self.match.other_player_data.member.id)
            + ">!"
        )

        OTHER_USER_WIN_DESC = (
            "**Set "
            + str(self.match.round_number)
            + "** - "
            + "<@"
            + str(self.match.other_player_data.member.id)
            + "> has defeated <@"
            + str(self.match.current_player_data.member.id)
            + ">!"
        )

        FORFEIT_DESC = (
            "**Set "
            + str(self.match.round_number)
            + "** - "
            + "<@"
            + str(self.match.current_player_data.member.id)
            + "> has forfeited.\n<@"
            + str(self.match.other_player_data.member.id)
            + "> wins the match!"
        )

        TIMEOUT_DESC = (
            "**Set "
            + str(self.match.round_number)
            + "** - "
            + "<@"
            + str(self.match.current_player_data.member.id)
            + "> didn't respond in time,\n<@"
            + str(self.match.other_player_data.member.id)
            + "> wins the match!"
        )

        match_end_embed_dict = {
            "title": strings.MATCH_TITLE,
            "color": colors.MATCH_COLOUR_VALUE,
            "thumbnail": {
                "url": env.MATCH_END_THUMBNAILS[
                    random.randint(0, len(env.MATCH_END_THUMBNAILS) - 1)
                ]
            },
            "footer": {"text": strings.MATCH_FOOTER},
        }

        if random.randint(0, 100) == 69:
            # If 1/100 chance hit, show easter egg thumbnail
            match_end_embed_dict["thumbnail"] = {"url": env.EGG_1_THUMBNAIL}

        winner: Member = None
        sound_to_play = env.FORFEIT_TIMEOUT_SOUND

        # Set match_end_embed_dict based on match outcome
        if self.match.status == MatchStatus.COMPLETED:
            if (
                self.match.current_player_data.wins
                == numbers.WINS_REQUIRED_TO_END
            ):
                match_end_embed_dict[
                    "description"
                ] = CURRENT_TURN_USER_WIN_DESC
                winner = self.match.current_player_data.member
            else:
                match_end_embed_dict["description"] = OTHER_USER_WIN_DESC
                winner = self.match.other_player_data.member
            sound_to_play = env.MATCH_END_SOUND
        elif self.match.status == MatchStatus.FORFEIT:
            match_end_embed_dict["description"] = FORFEIT_DESC
            match_end_embed_dict["thumbnail"] = {
                "url": env.FORFEIT_THUMBNAILS[
                    random.randint(0, len(env.FORFEIT_THUMBNAILS) - 1)
                ]
            }
            winner = self.match.other_player_data.member
        elif self.match.status == MatchStatus.TIMEOUT:
            match_end_embed_dict["description"] = TIMEOUT_DESC
            match_end_embed_dict["thumbnail"] = {
                "url": env.TIMEOUT_THUMBNAILS[
                    random.randint(0, len(env.TIMEOUT_THUMBNAILS) - 1)
                ]
            }
            winner = self.match.other_player_data.member

        self.match.set_winner(winner)  # Set match winner

        embed = Embed.from_dict(match_end_embed_dict)
        embed = update_embed_with_match_data(self.match, embed)
        await self.messages.update(
            self.match, content="", embed=embed, view=None
        )
        await self.match_sfx.play(sound_to_play)
        save_to_db(self.match)

    async def play_round(self):
        """Play turns until round is over, then end round"""
        round_status: RoundStatus = RoundStatus.IN_PROGRESS

        while round_status == RoundStatus.IN_PROGRESS:
            # Play turn for current player which affects match object
            await self.play_turn()

            # Check for round end states
            if (
                self.match.are_both_players_standing()
                or self.match.did_current_player_play_nine_cards()
                or self.match.did_current_player_bust()
                or self.match.status != MatchStatus.IN_PROGRESS
            ):
                round_status = RoundStatus.COMPLETE
            elif (
                not self.match.other_player_data.is_standing
                and round_status == RoundStatus.IN_PROGRESS
            ):
                # If round not over and other user not standing,
                # swap player turn
                self.match.swap_current_player_data()

        if round_status == RoundStatus.COMPLETE:
            # If round marked as complete, call end_round
            await self.end_round()

    async def end_round(self):
        """Output round end embed based on match data"""
        if self.match.status == MatchStatus.IN_PROGRESS:
            # Only output embed if match still in progress, else skip
            WIN_DESC = (
                " wins **Set "
                + str(self.match.round_number)
                + "**!\n"
                + "Starting the next set in 5 seconds..."
            )
            DRAW_DESC = (
                "<@"
                + str(self.match.get_player_one_data().member.id)
                + "> and "
                + "<@"
                + str(self.match.get_player_two_data().member.id)
                + "> draw **Set "
                + str(self.match.round_number)
                + "**!\n"
                + "Starting the next set in 5 seconds..."
            )

            round_end_embed_dict = {
                "title": strings.MATCH_TITLE,
                "color": colors.MATCH_COLOUR_VALUE,
                "thumbnail": {
                    "url": env.INGAME_THUMBNAILS[self.thumbnail_index]
                },
                "footer": {"text": strings.MATCH_FOOTER},
            }

            sound_to_play = env.ROUND_END_SOUND

            if (
                (
                    self.match.current_player_data.total
                    > self.match.other_player_data.total
                    and self.match.current_player_data.total < 21
                )
                or self.match.did_current_player_play_nine_cards()
                or self.match.other_player_data.total > 20
            ):
                if self.match.did_current_player_play_nine_cards():
                    sound_to_play = env.NINE_CARDS_SOUND

                # If current player won, increment wins and update embed
                mention_current_player = (
                    "<@" + str(self.match.current_player_data.member.id) + ">"
                )
                round_end_embed_dict["description"] = (
                    mention_current_player + WIN_DESC
                )
                self.match.current_player_data.increment_wins()
            elif (
                self.match.current_player_data.total
                == self.match.other_player_data.total
            ):
                # If players drew, update with draw embed
                round_end_embed_dict["description"] = DRAW_DESC
                sound_to_play = env.DRAW_SOUND
            else:
                # If other player won, update with other user win embed
                mention_other_user = (
                    "<@" + str(self.match.other_player_data.member.id) + ">"
                )
                round_end_embed_dict["description"] = (
                    mention_other_user + WIN_DESC
                )
                self.match.other_player_data.increment_wins()

            if (
                self.match.current_player_data.wins
                < numbers.WINS_REQUIRED_TO_END
                and self.match.other_player_data.wins
                < numbers.WINS_REQUIRED_TO_END
            ):
                # If player has not won match yet:
                self.match.increment_round_number()  # Advance round number

                # Output embed and transition
                embed = Embed.from_dict(round_end_embed_dict)
                embed = update_embed_with_match_data(self.match, embed)
                await self.messages.update(
                    self.match, content="", embed=embed, view=None
                )
                await self.match_sfx.play(sound_to_play)
                await self.sleep_to_transition()

                if (
                    self.match.is_current_player_one
                    and self.did_current_player_go_first
                ):
                    # Ensure starting player alternates between rounds
                    self.match.swap_current_player_data()

                self.did_current_player_go_first = (
                    not self.did_current_player_go_first
                )
            else:
                # Else if player won, set match to completed
                self.match.set_match_status(MatchStatus.COMPLETED)

    async def play_turn(self, did_user_play_card=False):
        """Plays pazaak turn, deals card if necessary
        and waits for user interaction

        Args:
            did_user_play_card (bool, optional): True if user already
            played card this turn. Defaults to False.
        """
        STAND_TEXT = (
            self.match.current_player_data.member.name
            + " has hit 20 and automatically stands!\n"
            + "Match continues in 5 seconds...\n"
        )

        sound_to_play = env.PLAY_CARD_SOUND

        if not did_user_play_card:
            # If card not played, deal card
            self.match.current_player_data.deal_card_to_played_cards()
            sound_to_play = env.DEAL_CARD_SOUND

        # True if player automatically standed this turn
        did_player_auto_stand = False

        menu = MatchMenu(self.match, did_user_play_card)

        match_embed_dict = {
            "title": strings.MATCH_TITLE,
            "description": "**Set "
            + str(self.match.round_number)
            + "** - <@"
            + str(self.match.current_player_data.member.id)
            + ">'s turn\n"
            + self.match.current_player_data.member.name
            + (" played a " if did_user_play_card else " rolled a ")
            + str(self.match.current_player_data.played_cards[-1])
            + "!\n",
            "color": colors.MATCH_COLOUR_VALUE,
            "thumbnail": {"url": env.INGAME_THUMBNAILS[self.thumbnail_index]},
            "footer": {"text": strings.MATCH_FOOTER},
        }

        if self.match.current_player_data.total == 20:
            # If user total is 20, update embed and stand
            match_embed_dict["description"] += STAND_TEXT
            self.match.current_player_data.set_is_standing(True)
            menu = None  # Remove menu buttons
            did_player_auto_stand = True  # Update automatic stand flag
        elif (
            self.match.current_player_data.total > 20
            and not did_user_play_card
        ):
            sound_to_play = env.BUST_SOUND

        embed = update_embed_with_match_data(
            self.match, Embed.from_dict(match_embed_dict)
        )

        # If nine cards played, do not edit embed since round is over
        if not self.match.did_current_player_play_nine_cards():
            await self.messages.update(
                self.match,
                content="",
                embed=embed,
                view=menu,
            )
            await self.match_sfx.play(sound_to_play)
            if not did_player_auto_stand:
                # If player not automatically standing, wait for button press

                timeout = await menu.wait()
                if timeout:
                    # If timeout occurs, call handle_match_timeout
                    menu.value = await handle_match_timeout(
                        self.match, self.messages, did_user_play_card, embed
                    )

                if menu.value == TurnResult.STAND:
                    # If user selected stand, set is_standing
                    self.match.current_player_data.set_is_standing(True)
                    if not self.match.are_both_players_standing():
                        # Play stand sound if first player to stand
                        await self.match_sfx.play(env.STAND_SOUND)
                elif menu.value == TurnResult.FORFEIT:
                    # If user forfeited, update match status
                    self.match.set_match_status(MatchStatus.FORFEIT)
                elif menu.value == TurnResult.CARD_PLAYED:
                    # If card played, play turn again without
                    # allowing cards to be played
                    await self.play_turn(True)
                elif menu.value == TurnResult.TIMEOUT:
                    # If current user timed out, set match status to timeout
                    self.match.set_match_status(MatchStatus.TIMEOUT)

            elif did_player_auto_stand:
                # If player automatically standed, sleep to transition
                await self.sleep_to_transition()

    async def sleep_to_transition(self):
        """Sleep for MATCH_WAIT_TIME to transition embed"""
        await sleep(self.MATCH_WAIT_TIME)


async def begin_match(
    bot: Bot,
    player_one: Member,
    player_two: Member,
    message: Message,
    guild: Guild,
):
    """Initialize match objects and start match

    Args:
        bot (Bot): Pazaak bot
        player_one (Member): Player one (challenger)
        player_two (Member): Player two (challenged)
        message (Message): Server message for pazaak match
        guild (Guild): Guild of match
    """
    # Create MatchData object for this match
    # Randomly select who gets first turn
    does_player_one_get_first_turn = random.choice([True, False])
    match = MatchData(player_one, player_two, does_player_one_get_first_turn)
    thumbnail_index = random.randint(0, len(env.INGAME_THUMBNAILS) - 1)

    MATCH_START_EMBED_DICT = {
        "title": strings.MATCH_TITLE,
        "description": "<@"
        + str(match.current_player_data.member.id)
        + "> was randomly chosen to play the first turn!\n"
        + "The game will begin in "
        + str(MatchPlayer.MATCH_WAIT_TIME)
        + " seconds...",
        "color": colors.MATCH_COLOUR_VALUE,
        "thumbnail": {"url": env.INGAME_THUMBNAILS[thumbnail_index]},
        "footer": {"text": strings.MATCH_FOOTER},
    }

    # Display match start embed, send to players
    embed = update_embed_with_match_data(
        match, Embed.from_dict(MATCH_START_EMBED_DICT)
    )

    # Edit server message
    await message.edit(content="", embed=embed, view=None)

    try:
        # Send message to player one
        player_one_message: Message = await player_one.send(
            content="", embed=embed, view=None
        )
    except Exception:
        # If message fails to send, edit message with error
        PLAYER_ONE_FAIL_EMBED_DICT = {
            "title": strings.MATCH_TITLE,
            "description": "Unable to send match message to <@"
            + str(player_one.id)
            + ">.\nPlease enable direct messages!"
            + "\n\n"
            + strings.SUPPORT_SERVER_PLUG,
            "color": colors.ERROR_COLOUR_VALUE,
            "thumbnail": {"url": env.MESSAGE_ERROR_THUMBNAIL},
        }
        await message.edit(
            content=(
                "<@" + str(player_one.id) + "> <@" + str(player_two.id) + ">"
            ),
            embed=Embed.from_dict(PLAYER_ONE_FAIL_EMBED_DICT),
            view=None,
        )
    else:
        try:
            # Send message to player two
            player_two_message: Message = await player_two.send(
                content="", embed=embed, view=None
            )
        except Exception:
            # If message fails to send, edit message with error
            PLAYER_TWO_FAIL_EMBED_DICT = {
                "title": strings.MATCH_TITLE,
                "description": "Unable to send match message to <@"
                + str(player_two.id)
                + ">.\nPlease enable direct messages!"
                + "\n\n"
                + strings.SUPPORT_SERVER_PLUG,
                "color": colors.ERROR_COLOUR_VALUE,
                "thumbnail": {"url": env.MESSAGE_ERROR_THUMBNAIL},
            }
            await message.edit(
                content=(
                    "<@"
                    + str(player_one.id)
                    + "> <@"
                    + str(player_two.id)
                    + ">"
                ),
                embed=Embed.from_dict(PLAYER_TWO_FAIL_EMBED_DICT),
                view=None,
            )
            # Edit sent player_one_message with fail embed
            await player_one_message.edit(
                embed=Embed.from_dict(PLAYER_TWO_FAIL_EMBED_DICT),
                view=None,
            )
        else:
            # Only start match if messages successfully sent
            # Sleep to show match start embed before transition
            messages = MatchMessages(
                message, player_one_message, player_two_message
            )

            match_sfx = MatchSfx(bot, guild)
            player = MatchPlayer(match, messages, match_sfx, thumbnail_index)

            await player.sleep_to_transition()
            await player.play_match()
