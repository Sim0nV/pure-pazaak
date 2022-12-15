from discord import Embed

from .classes.player_data import PlayerData
from .classes.match_data import MatchData

from constants import env, numbers


def get_embed_field_value(player_data: PlayerData):
    """Returns field value string for passed PlayerData

    Args:
        player_data (PlayerData): Player data to fill field
        value with

    Returns:
        str: Field value with relevant player data
    """
    field_value: str = ""

    # Add filled circles for wins
    for i in range(player_data.wins):
        field_value += "◉"

    # Add empty circles for rest of rounds
    for i in range(numbers.WINS_REQUIRED_TO_END - player_data.wins):
        field_value += "◎"

    # Add played card total
    if player_data.is_standing:
        field_value += "\n[ " + str(player_data.total) + " ]\n\n"
    else:
        field_value += "\n" + str(player_data.total) + "\n\n"

    # Add played cards
    cards_in_row = 0
    for i in range(len(player_data.played_cards)):
        cards_in_row += 1
        if len(player_data.played_cards[i]) == 1:
            field_value += "|  " + player_data.played_cards[i] + "  |"
        else:
            field_value += "| " + player_data.played_cards[i] + " |"
        # Show 3 cards per row
        if cards_in_row == 3:
            field_value += "\n"
            cards_in_row = 0

    field_value = field_value.replace("|", "|​\u200b")
    field_value = field_value.replace(" ", " ​\u200b")
    return field_value


def update_embed_with_match_data(match: MatchData, embed: Embed):
    """Returns passed embed based on passed match data

    Args:
        match (MatchData): Match data to update embed with
        embed (Embed): Embed to be updated

    Returns:
        Embed: Embed updated with current match data
    """
    player_one_data = match.get_player_one_data()
    player_two_data = match.get_player_two_data()

    # Add field with challenger's data
    embed.add_field(
        name=player_one_data.member,
        value=get_embed_field_value(player_one_data),
        inline=True,
    )

    # Add field with challenged player's data
    embed.add_field(
        name=player_two_data.member,
        value=get_embed_field_value(player_two_data),
        inline=True,
    )

    if len(match.current_player_data.played_cards) != 0:
        # Set embed image to last played card
        lastPlayedCard = str(match.current_player_data.played_cards[-1])
        embed.set_image(url=env.CARD_IMAGES_DICT[lastPlayedCard])

    return embed
