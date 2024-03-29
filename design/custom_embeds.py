import discord
import datetime

from discord.ext import commands
from database.database import BotDatabase
from design.emojis import Emoji
from custom_bot import MyBot

class CustomEmbeds(commands.Cog):
    def __init__(self, bot: MyBot) -> None:
          self.bot = bot
          self.db = bot.dbconn
          
          self.db_group = self.bot.dbconn.group_queries 
          self.db_player = self.bot.dbconn.player_queries
          self.db_legendday = self.bot.dbconn.legend_day_queries 
          self.db_mutation = self.bot.dbconn.mutation_queries
          self.db_discord_user = self.bot.dbconn.discord_user_queries
          
    async def embed_player_overview(self, player_name:str, player_tag: str, group_name: str) -> discord.Embed:
            """Creates a discord embed for a legend_overview of a player"""
            emoji = Emoji()
            
            min_trophy = emoji.get_emoji("min_trophy")
            plus_trophy = emoji.get_emoji("plus_trophy")
                
            data = self.db_mutation.get_today_hits_from_player(account_tag=player_tag)
                        
            offense = data["offense"]
            defense = data["defense"]
            
            sum_offense = sum(offense)
            sum_defense = sum(defense)
            
            begin_trophies = self.db_legendday.get_start_trophies(player_tag, datetime.date.today())                        
            # begin_trophies = self.db.get_legend_start(account_tag=player_tag, date=datetime.date.today())

            if not begin_trophies:
                begin_trophies = 0
            
            #defense is negative that's why +
            current_trophies = begin_trophies  + (sum_offense + sum_defense)
            
            custom_embed = discord.Embed(
                title=player_name,
                colour=discord.Colour.from_rgb(0, 150, 255)
            )
            
            #Create fields
            overview_info = f'Daystart: {self.bot.get_emoji(plus_trophy)} {begin_trophies}\nCurrent: {self.bot.get_emoji(min_trophy)} {current_trophies}\n'
            total_info = f'Offense: {self.bot.get_emoji(plus_trophy)} {sum_offense}\nDefense: {self.bot.get_emoji(min_trophy)} {sum_defense}'   
            offensive_info = "\n".join(f"{self.bot.get_emoji(emoji.get_emoji('plus_trophy'))}{str(attack)}"  for attack in offense)
            defensive_info = "\n".join(f"{self.bot.get_emoji(emoji.get_emoji('min_trophy'))}{str(defend)}" for defend in defense)

            custom_embed.add_field(name="Overview", value=overview_info, inline=True)
            custom_embed.add_field(name="Total", value=total_info, inline=False)

            custom_embed.add_field(name="**Offense**", value=offensive_info, inline=True)  
            custom_embed.add_field(name="**Defense**", value=defensive_info, inline=True)
            
            custom_embed.set_footer(text=group_name)
            return custom_embed

async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(CustomEmbeds(bot))