import discord

from    discord                 import app_commands
from    discord.ext             import commands
from    classes.player          import Player
from    typing                  import List




class Group(commands.GroupCog, name="group"):
    """Description of what this file does"""
    def __init__(self, bot):
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
    @app_commands.autocomplete(account_tag=AutoComplete().player_autocomplete)
    @app_commands.rename(account_tag="account", group_tag="group")
    @app_commands.describe(account_tag="The account you want to add to a group", group_tag= "The group you want to add the account to")
    async def add_player_to_group(self, interaction: discord.Interaction, account_tag: str, group_tag: str):
        choices = await self.autocomplete.
        
        await interaction.response.defer()

        player = Player(account_tag=account_tag)
        group_to_add = group_tag.lower()
        response = self.db.add_player_to_group(group=group_to_add, player=player,guild_id=interaction.guild.id )
        
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
            for player in player_accounts_unique if current in player
        ]
            
    #THIS REMOVES A PLAYER
    @app_commands.command(name="remove_player", description="This will remove the player from the feed")
    @app_commands.autocomplete(account_tag = player_auto_complete)
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
            
        await interaction.send(response)    


async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(Group(bot))