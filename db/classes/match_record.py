class MatchRecord:
    """Match record info between two players"""

    def __init__(
        self,
        player_one_wins: int,
        player_two_wins: int,
        total_matches: int,
    ) -> None:
        self.player_one_wins = player_one_wins
        self.player_two_wins = player_two_wins
        self.total_matches = total_matches
