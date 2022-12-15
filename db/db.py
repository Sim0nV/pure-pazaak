from pazaak_match.classes.match_data import MatchData
from pymongo import MongoClient
from discord import Member
from constants import env
from .classes.player_stats import PlayerStats
from .classes.match_record import MatchRecord
from datetime import datetime

# Database Variables
client = None
db = None
player_stats_db = None
matches_db = None

if env.DB_CONNECTION_URL != "":
    # If DB_CONNECTION_URL is not empty,
    # Initialize db variables

    client = MongoClient(env.DB_CONNECTION_URL)

    # Set database to dev collection or prod collection
    # Depending on if debug mode
    db = (
        client[env.DEV_DB_COLLECTION]
        if env.IS_DEBUG_MODE
        else client[env.PROD_DB_COLLECTION]
    )
    player_stats_db = db["playerStats"]
    matches_db = db["matches"]
else:
    print("DB_CONNECTION_URL empty, database initialization skipped")


def get_or_create_player(id: int) -> dict:
    """Retrieves player document from database, or
    creates it if it does not exist

    Args:
        id (int): ID of player to retrieve or create document for

    Returns:
        Dict: Player document from database
    """
    player_document = None

    if client:
        # If mongo client initialized:

        # Check if player's document exists in database
        player_document = player_stats_db.find_one({"_id": id})

        if not player_document:
            # If player's document does not exist, create one
            player_stats_db.insert_one({"_id": id, "wins": 0, "totalGames": 0})
            player_document = player_stats_db.find_one({"_id": id})

    return player_document


def get_player_stats(player: Member) -> PlayerStats:
    """Returns player stats object for passed player

    Args:
        player (Member): Player to get stats for

    Returns:
        PlayerStats: Stats object for player
    """
    stats_object = PlayerStats(0, 0)

    if client:
        # If mongo client initialized:

        stats_document = get_or_create_player(player.id)

        stats_object = PlayerStats(
            stats_document["wins"],
            stats_document["totalGames"],
        )

    return stats_object


def get_match_record(player_one: Member, player_two: Member) -> MatchRecord:
    """Returns head to head match record between two players

    Args:
        player_one (Member): Player one to get match record of
        player_two (Member): Player two to get match record of

    Returns:
        MatchRecord: Match record object
    """
    match_record = MatchRecord(0, 0, 0)

    if client:
        # If mongo client initialized:

        matches = matches_db.find(
            {"players": {"$all": [player_one.id, player_two.id]}}
        )
        player_one_wins = 0
        player_two_wins = 0

        for match in matches:
            if match["winner"] == player_one.id:
                player_one_wins += 1
            else:
                player_two_wins += 1

        total_matches = player_one_wins + player_two_wins

        match_record = MatchRecord(
            player_one_wins, player_two_wins, total_matches
        )

    return match_record


def save_match(match: MatchData):
    """Saves passed match data onto database

    Args:
        match (MatchData): Match data to save onto database
    """
    if client:
        # If mongo client initialized:

        now = datetime.now()
        date_string = now.strftime("%m/%d/%Y, %H:%M:%S")
        matches_db.insert_one(
            {
                "players": [
                    match.get_player_one_data().member.id,
                    match.get_player_two_data().member.id,
                ],
                "winner": match.winner.id,
                "date": date_string,
            }
        )


def update_stats(id: int, is_winner: bool):
    """Updates player stats in database

    Args:
        id (int): ID of player to update stats for
        is_winner (bool, optional): Whether player is a winner.
        Defaults to False.
    """
    if client:
        # If mongo client initialized:

        player_document = get_or_create_player(id)

        if is_winner:
            # Increment player's wins
            player_document["wins"] += 1

        # Increment player's total games
        player_document["totalGames"] += 1

        # Update player's document in database
        player_stats_db.update_one({"_id": id}, {"$set": player_document})


def save_to_db(match: MatchData):
    """Saves passed match and updates player stats

    Args:
        match (MatchData): Match data to save onto database
    """

    is_current_player_winner = (
        match.winner.id == match.current_player_data.member.id
    )

    save_match(match)
    update_stats(match.current_player_data.member.id, is_current_player_winner)
    update_stats(
        match.other_player_data.member.id, not is_current_player_winner
    )
