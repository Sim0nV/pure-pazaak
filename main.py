import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from logging import WARNING, INFO

import os

from constants import env, strings, colors

from random import randint


class PurePazaakBot(commands.Bot):
    """Pure Pazaak Discord Bot"""

    def __init__(self):
        """Initialize Discord bot with command prefix, intents"""
        # Set intents (bot permissions)
        intents = discord.Intents.default()
        intents.members = True
        # Initialize discord bot
        super().__init__(command_prefix="$", intents=intents)
        self.remove_command("help")  # Remove default discord help command

    async def setup_hook(self):
        """Bot setup coroutine: Sync commands and load cogs"""
        if env.IS_DEBUG_MODE:
            print("Running in Debug Mode")
        await self.load_cogs()
        await bot.sync_commands()

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """Command error handler"""
        if not isinstance(error, CommandNotFound):
            # If not CommandNotFound error, send error
            ERROR_EMBED_DICT = {
                "title": strings.MATCH_TITLE,
                "description": str(error)
                + "\n\n"
                + strings.SUPPORT_SERVER_PLEASE_REPORT,
                "color": colors.ERROR_COLOUR_VALUE,
                "thumbnail": {
                    "url": env.ERROR_THUMBNAILS[
                        randint(0, len(env.ERROR_THUMBNAILS) - 1)
                    ]
                },
            }
            await ctx.send(
                content="<@" + str(ctx.author.id) + ">",
                embed=discord.Embed.from_dict(ERROR_EMBED_DICT),
            )
            raise error

    async def sync_commands(self):
        """Sync slash commands"""
        if env.SHOULD_SYNC_COMMANDS:
            # Only sync slash commands if SHOULD_SYNC_COMMANDS
            # environment variable is true
            await self.tree.sync()  # Sync commands globally
            print(f"Synced slash commands for {self.user}.")
        else:
            print("Skipped syncing commands")

    async def load_cogs(self):
        """Load all cogs in the cogs folder"""
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")


bot = PurePazaakBot()  # Initialize pure pazaak bot


async def update_presence(bot: PurePazaakBot):
    """Updates bot presence with number of servers

    Args:
        bot (PurePazaakBot): Pazaak bot to update presence of
    """
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=("/pazaak | " + str(len(bot.guilds)) + " servers"),
        )
    )


@bot.event
async def on_ready():
    """On bot ready callback"""
    await update_presence(bot)


@bot.event
async def on_guild_join(guild: discord.Guild):
    """On server join callback"""
    await update_presence(bot)


@bot.event
async def on_guild_remove(guild: discord.Guild):
    """On server remove callback"""
    await update_presence(bot)


# Run dev bot token if debug mode, else run production bot token
# Have more verbose logs if debug mode
bot.run(
    env.DEV_BOT_TOKEN if env.IS_DEBUG_MODE else env.PROD_BOT_TOKEN,
    log_level=INFO if env.IS_DEBUG_MODE else WARNING,
)
