import discord
import datetime

from discord.ext import commands, tasks
from custom_bot import MyBot
from API.player import Player

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot: MyBot = bot
        self.db = bot.dbconn
        self.update_legend_start.start()
    
    @tasks.loop(time=datetime.time(4,59,0))        
    async def update_legend_start(self):
        tuples = []

        all_tags = self.db.group_queries.get_all_unique_tags()
        for tag in all_tags:
            player = Player(tag)
            trophies = await player.get_trophies()
            tuples.append((tag, trophies))
        
        self.db.legend_day_queries.add_legend_start(tuples)
        
    

async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(BackgroundTasks(bot))
         