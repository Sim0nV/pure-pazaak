import asyncio

from discord.ext.commands import Bot
from discord import utils, FFmpegOpusAudio, VoiceClient, Guild

from .classes.url_queue import URLQueue


class MatchSfx:
    """Plays match sound effects if possible"""

    queue = URLQueue(3)  # Queue of sound URLs to play

    def __init__(
        self,
        bot: Bot,
        guild: Guild,
    ) -> None:
        self.bot = bot
        self.guild = guild  # Guild of match

    async def play_queue(self, voice_client: VoiceClient):
        """Pop sound from queue and play it

        Args:
            voice_client (VoiceClient): Voice client of match
        """
        if not self.queue.is_empty() and voice_client:
            # If sound in queue and voice client exists, pop sound
            url = self.queue.pop()
            if not voice_client.is_playing() and not voice_client.is_paused():
                # If sound not already playing, play sound
                source = await FFmpegOpusAudio.from_probe(
                    url,
                    method="fallback",
                )

                try:
                    # Recursively call play_queue after sound done playing
                    voice_client.play(
                        source,
                        after=lambda e: asyncio.run(
                            self.play_queue(voice_client)
                        ),
                    )
                except Exception as e:
                    print(e)
                # Pause, wait, and resume to prevent playback glitches
                voice_client.pause()
                await asyncio.sleep(0.6)
                voice_client.resume()
            else:
                # If sound still playing, skip sound and call
                # play_queue after waiting 2 seconds
                await asyncio.sleep(2)
                await self.play_queue(voice_client)

    async def play(self, url: str):
        """Plays passed sound effect if possible


        Args:
            url (str): url string of sound effect
        """
        if url and url != "":
            voice_client: VoiceClient = utils.get(
                self.bot.voice_clients, guild=self.guild
            )

            # If voice client not connected, don't try to play anything
            if voice_client and voice_client.is_connected():
                # Add sound to queue
                self.queue.enqueue(url)
                if (
                    not voice_client.is_playing()
                    and not voice_client.is_paused()
                ):
                    # If client not already playing, start playing
                    await self.play_queue(voice_client)
