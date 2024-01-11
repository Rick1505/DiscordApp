import discord
import os
import traceback

from discord.ext import commands
from discord import app_commands
from database.database import BotDatabase

description = "Discord Bot for a clash of clans server"

prefix = "!"

MY_GUILD = discord.Object(int(os.getenv("TEST_GUILD_ID")))  # replace with your guild id
MY_TOKEN = os.getenv("DISCORD_TOKEN_TUTORIAL")

initial_extensions = (
    "cogs.group",
    "cogs.legend_feed",
    "cogs.player_info"
)

SQLITE_FILE = "database/legend_league.db"


class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=prefix, description=description, intents=discord.Intents.all())
                
        self.dbconn = BotDatabase(SQLITE_FILE) 

    async def setup_hook(self):
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as extension:
                await traceback.print_exc()
        
            
        bot.tree.copy_global_to(guild=MY_GUILD)
        await bot.tree.sync(guild=MY_GUILD)
                 
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        


if __name__ == "__main__":
    try: 
        bot = MyBot()
        bot.run(MY_TOKEN)
       
    except:
        traceback.print_exc()


                
        