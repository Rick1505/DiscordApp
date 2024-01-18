import discord
import datetime
import traceback

from discord.ext import commands
from design.emojis  import Emoji
from database.database import BotDatabase
from settings import Config

class MyBot(commands.Bot):
    def __init__(self, config: Config):
        super().__init__(command_prefix="!",
                            case_insensitive=True,
                            intents=discord.Intents.all(),
                            help_command=None,
                            activity=discord.Game('/info'))
        self.config = config
        self.dev_guild: discord.Guild = config.guild_id
        self.emoji = Emoji()
        #TODO SETUP_LOGGER
        self.start_time = datetime.datetime.now()
        #TODO SETUP_DATABASE
        self.dbconn = BotDatabase(config.db_connection_string)
        
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        
    async def setup_hook(self):
        for extension in self.config.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                traceback.print_exc()
        await self.tree.sync()
