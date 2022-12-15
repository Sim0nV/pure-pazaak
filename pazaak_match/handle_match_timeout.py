from .classes.match_menu import MatchMenu
from .classes.match_data import MatchData
from .classes.match_messages import MatchMessages
from .classes.timeout_menu import TimeoutMenu
from .enums.turn_status import TurnResult
from discord import Embed

from constants import numbers

import asyncio
from contextlib import suppress


async def handle_match_timeout(
    match: MatchData,
    messages: MatchMessages,
    did_user_play_card: bool,
    embed: Embed,
):
    """Handles match timeout by updating messages and
    showing win by timeout button

    Args:
        match (MatchData): Match data
        messages (MatchMessages): Match messages
        did_user_play_card (bool): True if user played card, else false
        embed (Embed): Current match embed

    Returns:
        TurnResult: Turn result of current turn
    """
    turn_result = None

    # Refresh current player's embed with buttons and updated timeout
    current_player_menu = MatchMenu(
        match,
        did_user_play_card,
        numbers.MATCH_INTERACTION_TIMEOUT - numbers.TIME_UNTIL_TIMEOUT_BUTTON,
    )
    await messages.update_current_player_message(
        match=match,
        embed=embed,
        view=current_player_menu,
    )

    # Show win by timeout button to other player
    timeout_menu = TimeoutMenu()
    await messages.update_other_player_message(
        match=match,
        embed=embed,
        view=timeout_menu,
    )

    # Wait for first menu interaction
    current_player_task = asyncio.ensure_future(current_player_menu.wait())
    other_player_task = asyncio.ensure_future(timeout_menu.wait())
    tasks = (current_player_task, other_player_task)
    done, pending = await asyncio.wait(
        tasks, return_when=asyncio.FIRST_COMPLETED
    )

    # Cancel pending tasks
    for task in pending:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task

    finished_task = done.pop()

    if (finished_task == other_player_task) or (
        finished_task == current_player_task and finished_task.result()
    ):
        # If other player pressed timeout button,
        # Or current player timed out,
        # Set turn result to timeout
        turn_result = TurnResult.TIMEOUT
    else:
        # If current player pressed button,
        # Set turn result to button press result
        turn_result = current_player_menu.value

    return turn_result
