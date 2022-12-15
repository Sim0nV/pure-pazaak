from enum import Enum, auto


class RoundStatus(Enum):
    """Enum for round status"""
    IN_PROGRESS = auto()
    COMPLETE = auto()
