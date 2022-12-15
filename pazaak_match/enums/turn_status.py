from enum import Enum, auto


class TurnResult(Enum):
    """Enum for turn outcome"""
    END_TURN = auto()
    STAND = auto()
    FORFEIT = auto()
    CARD_PLAYED = auto()
    TIMEOUT = auto()
