from discord import Message
from .match_data import MatchData


class MatchMessages:
    """Has server message and player messages"""

    def __init__(
        self,
        server_message: Message,
        player_one_message: Message,
        player_two_message: Message,
    ) -> None:
        self.server_message = server_message
        self.player_one_message = player_one_message
        self.player_two_message = player_two_message

    async def update_current_player_message(
        self,
        match: MatchData,
        content="",
        embed=None,
        view=None,
    ):
        """Update current player's message based on passed parameters

        Args:
            match (MatchData): Match data to get players
            content (str, optional): Message content. Defaults to "".
            embed (Embed, optional): Message embed. Defaults to None.
            view (View, optional): Message view. Defaults to None.
        """
        # Get current player's match message
        current_player_message = self.player_one_message
        if not match.is_current_player_one:
            current_player_message = self.player_two_message

        await current_player_message.edit(
            content=content, embed=embed, view=view
        )

    async def update_other_player_message(
        self,
        match: MatchData,
        content="",
        embed=None,
        view=None,
    ):
        """Update other player's message based on passed parameters

        Args:
            match (MatchData): Match data to get players
            content (str, optional): Message content. Defaults to "".
            embed (Embed, optional): Message embed. Defaults to None.
            view (View, optional): Message view. Defaults to None.
        """
        # Get other player's match message
        other_player_message = self.player_one_message
        if match.is_current_player_one:
            other_player_message = self.player_two_message

        await other_player_message.edit(
            content=content, embed=embed, view=view
        )

    async def update(
        self,
        match: MatchData,
        content="",
        embed=None,
        view=None,
    ):
        """Update channel and player messages based on passed parameters

        Args:
            match (MatchData): Match data to get players
            content (str, optional): Message content. Defaults to "".
            embed (Embed, optional): Message embed. Defaults to None.
            view (View, optional): Message view. Defaults to None.
        """

        # Get current and other player's match messages
        current_player_message = self.player_one_message
        other_player_message = self.player_two_message
        if not match.is_current_player_one:
            # If current player is not player one,
            # update local message variables
            current_player_message = self.player_two_message
            other_player_message = self.player_one_message

        try:
            await self.server_message.edit(
                content=content, embed=embed, view=None
            )
        except Exception as e:
            # Catch server message edit failure so match continues
            # even if server message deleted
            print("Failed to edit server message: " + str(e))

        await current_player_message.edit(
            content=content, embed=embed, view=view
        )
        await other_player_message.edit(
            content=content, embed=embed, view=None
        )

        # Notifications removed due to Discord API Rate Limiting on delete

        # current_player = match.current_player_data.member
        # other_player = match.other_player_data.member
        # MENTION_CURRENT_PLAYER = "<@" + str(current_player.id) + ">"
        # if notify_current_player:
        #     # Notify current player that it is their turn
        #     try:
        #         reminder_message = await current_player.send(
        #             content=MENTION_CURRENT_PLAYER
        #             + ", it's your turn vs. "
        #             + other_player.name
        #             + "!"
        #         )
        #         await reminder_message.delete()
        #     except Exception:
        #         pass
