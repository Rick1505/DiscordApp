import discord

from discord.ext    import commands
from discord        import app_commands
from API.player     import Player
from API.league     import League
from design         import emojis
from custom_bot     import MyBot
from typing         import List

class PlayerInfo(commands.GroupCog, name="player"):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.db = bot.dbconn
        self.emoji = emojis.Emoji() 
        
        self.league_q = self.bot.coc_api.league_queries
        self.player_q = self.bot.coc_api.player_queries
    
    # #AUTO POPULATE FOR A PLAYER
    async def player_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    )   -> List[app_commands.Choice[str]]:
        
        all_players = self.db.get_all_groups(interaction.guild.id)
        player_accounts = [[record.name, record.tag] for record in all_players]
        player_accounts_unique = [list(player) for player in set(tuple(player) for player in player_accounts)]
            
        return [
            app_commands.Choice(name=f"{player[0]} - {player[1]}", value=player[1])
            for player in player_accounts_unique
        ]
                
    #SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
    @app_commands.command(name = "equipment", description = "This will show you the hero equipment of a player")
    @app_commands.autocomplete(account_tag=player_autocomplete )
    @app_commands.rename(account_tag = "account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def best_trophies(self, interaction: discord.Interaction, account_tag: str ):      
       
        player_info = await self.player_q.get_all_player_info(account_tag=account_tag)
        hero_equip = player_info["heroEquipment"]
        embed = discord.Embed(title= player_info["name"], color=discord.Colour.from_rgb(0, 150, 255))
        
        for equip in hero_equip:
            embed.add_field(name=equip["name"], value=equip["level"], inline=True)
            
        await interaction.response.send_message(embed=embed)
        
    # #DISPLAYS ALL LEGEND SEASONS FROM 2021 TO 2023     
    @app_commands.command(name="legend_history", description="This will show you all the ranks you have achieved in the different legend seasons")
    @app_commands.autocomplete(account_tag=player_autocomplete)
    @app_commands.rename(account_tag = "account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def display_legend_seasons(self, interaction: discord.Interaction, account_tag: str): 
        await interaction.response.defer()
               
        info = await self.player_q.get_all_player_info(account_tag=account_tag)
        legend_info = await self.player_q.get_legend_history(db= self.db, account_tag=account_tag)
            
        legend_info_dates = await self.player_q.change_season_to_dates(legend_info)   
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
            
        embed_legend_seasons = discord.Embed(
           title = "Legend seasons",
           description=description
        )
        embed_legend_seasons.set_author(name=info["name"], icon_url=info["clan"]["badgeUrls"]["medium"])
        embed_legend_seasons.set_thumbnail(url= await self.league_q.get_specific_league_image(info["league"]["id"]))
        embed_legend_seasons.set_footer(text=info["tag"])
        
        await interaction.followup.send(embed=embed_legend_seasons)

    @app_commands.command(name="legend_day", description="Shows information about the legend day of a player")
    @app_commands.autocomplete(account_tag=player_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def legend_day(self, interaction: discord.Interaction, account_tag: str):
        await interaction.response.defer()

        player_info = await self.player_q.get_all_player_info(account_tag=account_tag)
        group = self.db.get_player_from_group(guild_id=interaction.guild_id, account_tag=account_tag).group

        embed_cog = self.bot.get_cog("CustomEmbeds")
        embed = await embed_cog.embed_player_overview(db = self.db, player_name= player_info["name"], player_tag= account_tag, group_name= group)

        await interaction.followup.send(embed=embed)
    
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlayerInfo(bot))