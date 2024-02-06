import discord
from discord        import app_commands
from discord.ext    import commands

from typing         import List
from design         import emojis 
from custom_bot     import MyBot

class PlayerInfo(commands.Cog):
    
    group = app_commands.Group(name = "player", description="All player commands")
    legend = app_commands.Group(name = "legend", description="All legend commands", parent=group)
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.db = bot.dbconn
        self.emoji = emojis.Emoji() 
        
        self.league_q = self.bot.coc_api.league_queries
        self.player_q = self.bot.coc_api.player_queries
        
        self.db_group = self.bot.dbconn.group_queries 
        self.db_player = self.bot.dbconn.player_queries
        self.db_legendday = self.bot.dbconn.legend_day_queries 
        self.db_mutation = self.bot.dbconn.mutation_queries
        self.db_discord_user = self.bot.dbconn.discord_user_queries
    
    ##############################################################################################################################
    #AUTCOMPLETES
    ##############################################################################################################################  
    
    async def player_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    )   -> List[app_commands.Choice[str]]:
        
        all_players = self.db.group_queries.get_all_players_in_guild(interaction.guild.id)
        player_accounts = [[record.ingame_name, record.tag] for record in all_players]
        player_accounts_unique = [list(player) for player in set(tuple(player) for player in player_accounts)]
            
        return [
            app_commands.Choice(name=f"{player[0]} - {player[1]}", value=player[1])
            for player in player_accounts_unique if current.lower() in player[0].lower()
        ]
 
    ##############################################################################################################################
    #PLAYER INFORMATION
    ##############################################################################################################################  
                
    #SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
    @group.command(name = "equipment", description = "This will show you the hero equipment of a player")
    @app_commands.autocomplete(account_tag=player_autocomplete)
    @app_commands.rename(account_tag = "account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def get_equipment(self, interaction: discord.Interaction, account_tag: str ):      
       
        player_info = await self.player_q.get_all_player_info(account_tag=account_tag)
        hero_equip = player_info["heroEquipment"]
        embed = discord.Embed(title= player_info["name"], color=discord.Colour.from_rgb(0, 150, 255))
        
        for equip in hero_equip:
            embed.add_field(name=equip["name"], value=equip["level"], inline=True)
            
        await interaction.response.send_message(embed=embed)
        
    ##############################################################################################################################
    #LEGEND INFORMATION
    ##############################################################################################################################  


    @legend.command(name="day", description="Shows information about the legend day of a player")
    @app_commands.autocomplete(account_tag=player_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def legend_day(self, interaction: discord.Interaction, account_tag: str):
        await interaction.response.defer()

        player_info = await self.player_q.get_all_player_info(account_tag=account_tag)
        
        embed_cog = self.bot.get_cog("CustomEmbeds")
        embed = await embed_cog.embed_player_overview(player_name = player_info["name"], player_tag= account_tag)

        await interaction.followup.send(embed=embed)
    
    @legend.command(name="month", description="Shows information about the legend day of a player")
    @app_commands.autocomplete(account_tag=player_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    async def legend_month(self, interaction: discord.Interaction, account_tag: str):
        await interaction.response.defer()
        
        #get all data from legend_days for player
        
        await interaction.followup.send("All information about the player legend month")

    # #DISPLAYS ALL LEGEND SEASONS FROM 2021 TO 2023     
    # OUT OF ORDER
    # @legend.command(name="seasons", description="This will show you all the ranks you have achieved in the different legend seasons")
    # @app_commands.autocomplete(account_tag=player_autocomplete)
    # @app_commands.rename(account_tag = "account")
    # @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
    # async def display_legend_seasons(self, interaction: discord.Interaction, account_tag: str): 
    #     await interaction.response.defer()
               
    #     info = await self.player_q.get_all_player_info(account_tag=account_tag)
    #     legend_info = await self.player_q.get_legend_history(db= self.db, account_tag=account_tag)
            
    #     legend_info_dates = await self.player_q.change_season_to_dates(legend_info)   
    #     description = []
        
    #     for year in range(2023, 2020, -1):
    #         description.append(f"**{year}**\n")
            
    #         for record in legend_info_dates:
    #             if record.season.year == year:    
    #                 month = f'`{record.season.strftime("%B")}\t|`'
    #                 description.append(month.expandtabs(11))
                    
    #                 rank = f'{self.bot.get_emoji(self.emoji.get_emoji("legend_trophy"))} {record.trophies} | {self.bot.get_emoji(self.emoji.get_emoji("earth"))} {record.rank} \n'
    #                 description.append(rank)

    #     description = "".join(description)
            
    #     embed_legend_seasons = discord.Embed(
    #        title = "Legend seasons",
    #        description=description
    #     )
    #     embed_legend_seasons.set_author(name=info["name"], icon_url=info["clan"]["badgeUrls"]["medium"])
    #     embed_legend_seasons.set_thumbnail(url= await self.league_q.get_specific_league_image(info["league"]["id"]))
    #     embed_legend_seasons.set_footer(text=info["tag"])
        
    #     await interaction.followup.send(embed=embed_legend_seasons)
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PlayerInfo(bot))