import discord
import pandas
import datetime

from    discord         import app_commands
from    discord.ext     import commands
from    bot             import MyBot
from    typing          import List
from    API.player      import Player


class LegendGroup(commands.GroupCog, name="group"):
    """Description of what this file does"""
    def __init__(self, bot: MyBot):
        self.bot = bot  
        self.db = bot.dbconn
    
    
        
    #AUTO POPULATE FOR A GROUP     
    async def group_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    )   -> List[app_commands.Choice[str]]:
        
        all_groups = self.db.get_all_groups(interaction.guild.id)
        group_names = [record.group for record in all_groups]
        group_names_unique = list(set(group_names))
        
        return [
            app_commands.Choice(name=group, value=group)
            for group in group_names_unique if current.lower() in group.lower()
        ]   
        
          
    # THIS ADDS A PLAYER TO A GROUP
    @app_commands.command(name="add_player", description="This will add a player to a specific group")
    @app_commands.autocomplete(group_tag = group_autocomplete)
    @app_commands.rename(account_tag="account", group_tag="group")
    @app_commands.describe(account_tag="The account you want to add to a group", group_tag= "The group you want to add the account to")
    async def add_player_to_group(self, interaction: discord.Interaction, account_tag: str, group_tag: str):
        await interaction.response.defer()
       
        player = Player(account_tag=account_tag)
        group_to_add = group_tag.lower()
        response = await self.db.add_player_to_group(group=group_to_add, player=player, guild_id=interaction.guild.id )
        
        await interaction.followup.send(response)    
    
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
            
    #THIS REMOVES A PLAYER
    @app_commands.command(name="remove_player", description="This will remove the player from the feed")
    @app_commands.autocomplete(account_tag = player_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag="The account you want to remove from the group")
    async def remove_player(self, interaction: discord.Interaction, account_tag: str):
        await interaction.response.defer()
        response = self.db.rm_player(player=account_tag, guild_id=interaction.guild.id)
        
        await interaction.followup.send(response)    
        
    #CHANGES THE PLAYER TO ANOTHER GROUP
    @app_commands.command(name="change_group", description="Change the player from one group to another")
    @app_commands.autocomplete(account_tag= player_autocomplete, new_group = group_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag="The account you want to change groups", new_group = "The group you want the account to change to")
    async def change_player_group(self, interaction: discord.Interaction, account_tag: str, new_group:str):
        await interaction.response.defer()
        
        response = self.db.change_player_group(guild_id = interaction.guild.id, account= account_tag, new_group = new_group)
            
        await interaction.followup.send(response)


    @app_commands.command(name="info", description="Gives the information about a group")
    @app_commands.autocomplete(group_id = group_autocomplete)
    @app_commands.describe(group_id = "The group you want to show")
    async def group_information(self, interaction: discord.Interaction, group_id : str):
        await interaction.response.defer()
        
        group_info = self.db.get_all_from_group(group_id=group_id, guild_id=interaction.guild_id)
    
        information = []
        for player in group_info:
            tag = player.tag
            player_dict = {
                "name": player.name,
            }
            mutations = self.db.get_all_mutations_per_day(tag)
            
            player_dict["offense"] = len(mutations["offense"])
            player_dict["defense"] = len(mutations["defense"])
            delta = sum(mutations["offense"]) + sum(mutations["defense"])
            player_dict["delta"] = delta
            
            begin_trophies = self.db.get_legend_start(account_tag=tag, date=datetime.date.today())

            if not begin_trophies:
                begin_trophies = 0
           
            player_dict["start"] = begin_trophies
            player_dict["now"] = begin_trophies + delta

            information.append(player_dict)
            
    
        df = pandas.DataFrame.from_dict(information)
        df.sort_values(by="now", ascending=False)
        df.set_index("now")
        df.index +=1
        
        
        custom_embed = discord.Embed(title=f"Legend overview of: **{group_id}**",description=f"```{df}```")
        
        await interaction.followup.send(embed=custom_embed)
        
async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(LegendGroup(bot))