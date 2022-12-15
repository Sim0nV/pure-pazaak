import discord
from discord import Interaction
from discord.ui import View, Button

from constants import numbers


class TimeoutMenu(View):
    """Timeout button menu"""

    def __init__(self):
        super().__init__()
        self.timeout = (
            numbers.MATCH_INTERACTION_TIMEOUT
            - numbers.TIME_UNTIL_TIMEOUT_BUTTON
        )

    @discord.ui.button(label="Win By Timeout", style=discord.ButtonStyle.grey)
    async def win_by_timeout(self, interaction: Interaction, button: Button):
        """Win by timeout button callback

        Args:
            interaction (Interaction): Button interaction
            button (Button): End turn button
        """
        # Disable buttons, stop listening to interactions
        self.disable_buttons()
        await interaction.response.edit_message(view=self)
        self.stop()

    async def on_timeout(self):
        """Timeout callback, show timeout embed"""
        self.stop()

    def disable_buttons(self):
        """Sets all buttons to disabled
        Note: Must edit menu to apply changes
        """
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = True
