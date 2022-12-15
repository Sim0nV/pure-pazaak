import discord
from discord import Interaction, ButtonStyle
from discord.ui import View, Button

from .match_data import MatchData
from pazaak_match.enums.turn_status import TurnResult
from constants import numbers


class MatchMenu(View):
    """Pazaak match menu with card and gameplay buttons"""

    def __init__(
        self,
        match: MatchData,
        should_hide_cards=False,
        timeout=numbers.TIME_UNTIL_TIMEOUT_BUTTON,
    ):
        super().__init__()
        self.value = None
        self.timeout = timeout
        self.match = match

        if not should_hide_cards:
            self.add_card_buttons_to_menu()

    @discord.ui.button(label="End Turn", style=discord.ButtonStyle.grey, row=1)
    async def end_turn(self, interaction: Interaction, button: Button):
        """End turn button callback

        Args:
            interaction (Interaction): Button interaction
            button (Button): End turn button
        """
        # Disable buttons, update menu value, stop listening to interactions
        self.disable_buttons()
        await interaction.response.edit_message(view=self)
        self.value = TurnResult.END_TURN
        self.stop()

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.grey, row=1)
    async def stand(self, interaction: Interaction, button: Button):
        """Stand button callback

        Args:
            interaction (Interaction): Button interaction
            button (Button): Accept button
        """
        # Disable buttons, update menu value, stop listening to interactions
        self.disable_buttons()
        await interaction.response.edit_message(view=self)
        self.value = TurnResult.STAND
        self.stop()

    @discord.ui.button(label="Forfeit", style=discord.ButtonStyle.grey, row=1)
    async def forfeit(self, interaction: Interaction, button: Button):
        """Forfeit button callback

        Args:
            interaction (Interaction): Button interaction
            button (Button): Accept button
        """
        # Disable buttons, update menu value, stop listening to interactions
        self.disable_buttons()
        await interaction.response.edit_message(view=self)
        self.value = TurnResult.FORFEIT
        self.stop()

    async def interaction_check(self, interaction: Interaction) -> bool:
        """interaction_check override checks if interaction
        is valid before processing

        Args:
            interaction (Interaction): Interaction to check

        Returns:
            bool: True if valid interaction and should be processed,
            false if invalid and to skip processing
        """
        # If interaction is by current player, process interaction
        return interaction.user.id == self.match.current_player_data.member.id

    async def on_timeout(self):
        """Timeout callback, show timeout embed"""
        self.stop()

    def add_card_buttons_to_menu(self):
        """Adds card buttons to menu"""

        # Card callback functions to be assigned to buttons
        async def card0_callback(interaction: Interaction):
            await play_card(interaction, 0)

        async def card1_callback(interaction: Interaction):
            await play_card(interaction, 1)

        async def card2_callback(interaction: Interaction):
            await play_card(interaction, 2)

        async def card3_callback(interaction: Interaction):
            await play_card(interaction, 3)

        async def play_card(interaction: Interaction, index: int):
            """Plays selected card

            Args:
                interaction (Interaction): interaction to be deferred
                index (int): Index of card to play
            """
            self.match.current_player_data.play_card_from_deck(index)
            self.value = TurnResult.CARD_PLAYED
            self.disable_buttons()
            await interaction.response.edit_message(view=self)
            self.stop()

        for index, card in enumerate(self.match.current_player_data.cards):
            # If card is positive, button is blue. Otherwise red
            style = ButtonStyle.blurple if card[0] == "+" else ButtonStyle.red
            button = Button(label=card, style=style, row=0)

            # Assign button callback based on index
            if index == 0:
                button.callback = card0_callback
            elif index == 1:
                button.callback = card1_callback
            elif index == 2:
                button.callback = card2_callback
            elif index == 3:
                button.callback = card3_callback

            self.add_item(button)

    def disable_buttons(self):
        """Sets all buttons to disabled
        Note: Must edit menu to apply changes
        """
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = True
