import random
import copy
from discord import Member


class PlayerData:
    """Match data for individual player ex. current cards"""

    def __init__(self, member: Member):
        SIDE_DECK = [
            "-6",
            "-5",
            "-4",
            "-3",
            "-2",
            "-1",
            "+1",
            "+2",
            "+3",
            "+4",
            "+5",
            "+6",
        ]

        self.member = member
        # Draw 4 cards from side deck
        self.cards = random.sample(SIDE_DECK, 4)  # Playable cards
        self.played_cards = []  # Cards played on table

    total = 0  # Number total for cards on table
    wins = 0  # Round wins
    is_standing = False

    def copy(self):
        """Return deep copy of PlayerData object

        Returns:
            PlayerData: Deep copy of PlayerData object
        """
        deep_copy = PlayerData(self.member)
        deep_copy.total = self.total
        deep_copy.wins = self.wins
        deep_copy.is_standing = self.is_standing
        deep_copy.played_cards = copy.deepcopy(self.played_cards)
        deep_copy.cards = self.cards
        return deep_copy

    def reset_data(self):
        """Reset data between rounds"""
        self.total = 0
        self.set_is_standing(False)
        self.played_cards.clear()

    def add_card_to_played_cards(self, card: str):
        """Add passed card to played_cards

        Args:
            card (str): Card to be added
        """
        self.played_cards.append(card)

    def play_card_from_deck(self, index):
        """Add card from deck to played_cards,
        then remove from deck

        Args:
            index (int): Index of card to be played
        """
        self.add_card_to_played_cards(self.cards[index])
        self.total += int(self.cards[index])
        self.cards.pop(index)

    def deal_card_to_played_cards(self):
        """Deal random card from 1-10 to played_cards"""
        roll = random.randint(1, 10)
        self.add_card_to_played_cards(str(roll))
        self.total += roll

    def increment_wins(self):
        """Increment player wins"""
        self.wins += 1

    def set_is_standing(self, is_standing):
        """Sets is_standing bool

        Args:
            is_standing (bool): Bool to set to
        """
        self.is_standing = is_standing
