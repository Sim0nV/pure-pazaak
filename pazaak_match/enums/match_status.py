from enum import Enum, auto


class MatchStatus(Enum):
    """Enum for match status"""
    IN_PROGRESS = auto()  # Match still in progress
    COMPLETED = auto()  # A player has won the match
    TIMEOUT = auto()  # A player has timed out
    FORFEIT = auto()  # A player has forfeited
