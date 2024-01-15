import discord
import aiohttp

from discord.ext import commands
from discord import app_commands
from API.player import Player
from API.league import League
from utils  import make_embed
from design.emojis import Emoji
from bot import MyBot

class PlayerInfo(commands.GroupCog, name="player"):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.db = bot.dbconn
        self.emoji = Emoji() 
        
    #SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
    @app_commands.command(name = "equipment", description = "This will show you the hero equipment of a player")
    @app_commands.rename(account_tag = "account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def best_trophies(self, interaction: discord.Interaction, account_tag: str ):      
        player = Player(account_tag=account_tag)
        info = await player.get_all_player_info()
        hero_equip = info["heroEquipment"]
        embed = discord.Embed(title= info["name"], color=discord.Colour.from_rgb(0, 150, 255))
        
        for equip in hero_equip:
            embed.add_field(name=equip["name"], value=equip["level"], inline=True)
            
        await interaction.response.send_message(embed=embed)
        
    # #DISPLAYS ALL LEGEND SEASONS FROM 2021 TO 2023     
    @app_commands.command(name="legend_history", description="This will show you all the ranks you have achieved in the different legend seasons")
    @app_commands.rename(account_tag = "account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def display_legend_seasons(self, interaction: discord.Interaction, account_tag: str): 
        await interaction.response.defer()
        player = Player(account_tag=account_tag)
        league = League()
        
        info = await player.get_all_player_info()
        legend_info = await player.get_legend_history()
            
        legend_info_dates = await player.change_season_to_dates(legend_info)   
        description = []
        
        for year in range(2023, 2020, -1):
            description.append(f"**{year}**\n")
            
            for record in legend_info_dates:
                if record.season.year == year:    
                    month = f'`{record.season.strftime("%B")}\t|`'
                    description.append(month.expandtabs(11))
                    
                    rank = f'{self.bot.get_emoji(self.emoji.get_emoji("legend_trophy"))} {record.trophies} | {self.bot.get_emoji(self.emoji.get_emoji("earth"))} {record.rank} \n'
                    description.append(rank)

        description = "".join(description)
            
        embed_legend_seasons = make_embed(
           title = "Legend seasons",
           author_icon = info["clan"]["badgeUrls"]["medium"],
           author_text = info["name"],
           thumbnail_url = await league.get_specific_league_image(info["league"]["id"]),
           description=description,
           footer_text = info["tag"],
        )
        await interaction.followup.send(embed=embed_legend_seasons)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlayerInfo(bot))