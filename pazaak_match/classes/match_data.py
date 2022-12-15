from discord import Member

from .player_data import PlayerData
from pazaak_match.enums.match_status import MatchStatus


class MatchData:
    """Holds data for pazaak match ex. round number, player wins"""

    status: MatchStatus = MatchStatus.IN_PROGRESS
    round_number: int = 1
    winner: Member = None

    def __init__(
        self,
        player_one: Member,
        player_two: Member,
        does_player_one_get_first_turn=True,
    ):
        """Initialize MatchData object

        Args:
            player_one (discord.Member): Challenger member object
            player_two (discord.Member): Challenged member's object
            does_player_one_get_first_turn (bool, optional): True if
            player one gets first turn. Defaults to true.
        """
        # If player one gets first turn:
        if does_player_one_get_first_turn:

            # Make PlayerData objects for players
            self.current_player_data = PlayerData(player_one)
            self.other_player_data = PlayerData(player_two)

            self.is_current_player_one = True

        else:
            # Make PlayerData objects for players
            self.current_player_data = PlayerData(player_two)
            self.other_player_data = PlayerData(player_one)

            self.is_current_player_one = False

    def swap_current_player_data(self):
        """Swaps the current player's and the other player's data.
        Used when switching turns
        """
        temp_player_data = self.current_player_data.copy()
        self.current_player_data = self.other_player_data.copy()
        self.other_player_data = temp_player_data.copy()

        # Swap is_current_player_one bool
        self.is_current_player_one = not self.is_current_player_one

    def get_player_one_data(self) -> PlayerData:
        """Returns PlayerData of player_one

        Returns:
            PlayerData: PlayerData of player_one
        """
        if self.is_current_player_one:
            return self.current_player_data
        else:
            return self.other_player_data

    def get_player_two_data(self) -> PlayerData:
        """Returns PlayerData of player_two

        Returns:
            PlayerData: PlayerData of player_two
        """
        if self.is_current_player_one:
            return self.other_player_data

        else:
            return self.current_player_data

    def increment_round_number(self):
        """Increments round number"""
        self.round_number += 1

    def reset_round_data(self):
        """Resets PlayerData objects with round info"""
        self.current_player_data.reset_data()
        self.other_player_data.reset_data()

    def are_both_players_standing(self):
        """Return true if both players standing

        Returns:
            bool: True if both players standing, false otherwise
        """
        return (
            self.current_player_data.is_standing
            and self.other_player_data.is_standing
        )

    def did_current_player_bust(self):
        """Return true if current player busted

        Returns:
            bool: True if current player busted, false otherwise
        """
        return self.current_player_data.total > 20

    def did_current_player_play_nine_cards(self):
        """Return true if current player has 9 cards played

        Returns:
            bool: True if current player has 9 cards played, false otherwise
        """
        return len(self.current_player_data.played_cards) == 9

    def set_match_status(self, status: MatchStatus):
        """Sets match status to passed status

        Args:
            status (MatchStatus): Status to set to
        """
        self.status = status

    def set_winner(self, member: Member):
        """Sets winner to passed user

        Args:
            member (Member): Nember to set winner to
        """
        self.winner = member
