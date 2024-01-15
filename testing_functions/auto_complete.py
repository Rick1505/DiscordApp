import discord

from discord import app_commands
from typing import List
from    dataclasses             import dataclass


class AutoComplete():
    """This is a class which has all the different functions for commands to auto_complete"""
    def __init__(self, bot) -> None:
        self.bot = bot
        self.db = bot.dbconn
    
    async def player_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    )   -> List[app_commands.Choice[str]]:
        
        all_players = self.bot.dbconn.get_all_groups(interaction.guild.id)
        player_accounts = [[record.name, record.tag] for record in all_players]
        player_accounts_unique = [list(player) for player in set(tuple(player) for player in player_accounts)]
            
        return [
            app_commands.Choice(name=f"{player[0]} - {player[1]}", value=player[1])
            for player in player_accounts_unique if current in player
        ]
    
    async def group_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    )   -> List[app_commands.Choice[str]]:
        
        all_groups = self.bot.dbconn.get_all_groups(interaction.guild.id)
        group_names = [record.group for record in all_groups]
        group_names_unique = list(set(group_names))
        
        return [
            app_commands.Choice(name=group, value=group)
            for group in group_names_unique if current.lower() in group.lower()
        ] 
        
def setup(bot):
    bot.add_cog(AutoComplete(bot))