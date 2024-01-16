import discord
import os
import traceback



from discord.ext        import commands,tasks
from discord            import app_commands
from database.database  import BotDatabase
from typing             import Optional
from dotenv             import load_dotenv



description = "Discord Bot for a clash of clans server"

prefix = "!"

MY_GUILD = discord.Object(int(os.getenv("TEST_GUILD_ID")))  # replace with your guild id
MY_TOKEN = os.getenv("DISCORD_TOKEN_TUTORIAL")

SQLITE_FILE = "database/legend_league.db"

class MyBot(commands.Bot):
    def __init__(
        self,
        # session: aiohttp.ClientSession,
    ):
        super().__init__(command_prefix=prefix, description=description, intents=discord.Intents.all())
        
        self.dbconn: BotDatabase = BotDatabase(SQLITE_FILE)
        self.initial_extensions = (
            "cogs.group",
            "cogs.legend_feed",
            "cogs.player_info",
            "cogs.background_tasks",
            "design.custom_embeds"
        )
   
    async def setup_hook(self):
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as extension:
                traceback.print_exc()       
        
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
                 
    async def on_ready(self):
        # await self.wait_until_ready()
        print(f'Logged in as {self.user} (ID: {self.user.id})')

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with MyBot(session=session) as bot:
#             nest_asyncio.apply()
#             bot.run(MY_TOKEN)

if __name__ == "__main__":
    try: 
        bot = MyBot()
        bot.run(MY_TOKEN)
    except:
        traceback.print_exc()


                
        