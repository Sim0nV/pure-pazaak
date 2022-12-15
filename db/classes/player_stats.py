class PlayerStats:
    """Player stats with wins, total games"""

    def __init__(
        self,
        wins: int,
        total_games: int,
    ) -> None:
        self.wins = wins
        self.total_games = total_games
