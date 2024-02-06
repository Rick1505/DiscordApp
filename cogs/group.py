import discord
import pandas
import datetime

from    discord         import app_commands
from    discord.ext     import commands

from    custom_bot      import MyBot
from    typing          import List
from    API.player      import Player



class LegendGroup(commands.Cog):
    """Description of what this file does"""
    group = app_commands.Group(name = "group", description="All group commands")
    group_player = app_commands.Group(name="player", description="All player comamnds", parent=group)
        
    def __init__(self, bot: MyBot):
        self.bot = bot  
        self.db = bot.dbconn
        
        self.db_group = self.bot.dbconn.group_queries 
        self.db_player = self.bot.dbconn.player_queries
        self.db_legendday = self.bot.dbconn.legend_day_queries 
        self.db_mutation = self.bot.dbconn.mutation_queries
        self.db_discord_user = self.bot.dbconn.discord_user_queries
    
    ##############################################################################################################################
    #AUTCOMPLETES
    ##############################################################################################################################  
    
    # TODO FIX AUTOCOMPLETE
    async def group_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    )   -> List[app_commands.Choice[str]]:
        
        all_groups = self.db_group.get_all_groups(interaction.guild.id)
        group_names = [record.group_name for record in all_groups]
        group_names_unique = list(set(group_names))
        
        return [
            app_commands.Choice(name=name, value=name)
            for name in group_names_unique if current.lower() in name.lower()
        ]   
        
    async def player_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    )   -> List[app_commands.Choice[str]]:
        namespace = interaction.namespace.old_group
        
        all_players = self.db_group.get_players(interaction.guild.id, namespace)
        player_accounts = [[record.ingame_name, record.tag] for record in all_players]
        player_accounts_unique = [list(player) for player in set(tuple(player) for player in player_accounts)]
            
        return [
            app_commands.Choice(name=f"{player[0]} - {player[1]}", value=player[1])
            for player in player_accounts_unique if current.lower() in player[0].lower()
        ]
    
    
    ##############################################################################################################################
    #PLAYER COMMANDS
    ##############################################################################################################################
    
    @group_player.command(name="add", description="This will add a player to a specific group")
    @app_commands.autocomplete(group = group_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag="The account you want to add to a group", group= "The group you want to add the account to")
    async def add_player_to_group(self, interaction: discord.Interaction, account_tag: str, group: str):
        await interaction.response.defer()
        dc_user = interaction.user
        
        #check if player exists
        player_exists = self.db.player_queries.get_player(account_tag)
        
        if player_exists:
            add_succeeds = self.db.group_queries.try_add_player(str(interaction.guild.id), group, player_exists, dc_user)
        else:
            #create and get player
            account_info = await self.bot.coc_api.player_queries.get_all_player_info(account_tag)
            create_player_succeeds = self.db.player_queries.try_add_player(account_info)
            player_exists = self.db.player_queries.get_player(account_tag)
                        
            if create_player_succeeds:
                #add player to group
                add_succeeds = self.db.group_queries.try_add_player(str(interaction.guild.id),group, player_exists, dc_user) 
            else:
                await interaction.followup.send("Player could not have been created")
        
        if add_succeeds:
            await interaction.followup.send("Player has succesuflly been added to the group.")
        else:
            await interaction.followup.send("Player could not have been added to the group. Try to create the group first")

    @group_player.command(name="remove", description="This will remove the player from the feed")
    @app_commands.autocomplete(group = group_autocomplete, account_tag = player_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag="The account you want to remove from the group")
    async def remove_player(self, interaction: discord.Interaction, group: str, account_tag: str):
        await interaction.response.defer()
        
        dc_user = interaction.user
        guild_id = str(interaction.guild_id)
        
        response = self.db_group.try_remove_player(guild_id, group, account_tag, dc_user)
        if response:
            await interaction.followup.send(f"The user has been succesfully removed from the group {group}")
        else:
            await interaction.followup.send("An error has occured please try again or contact the owner")
                
    @group_player.command(name="change", description="Change the player from one group to another")
    @app_commands.autocomplete(old_group = group_autocomplete, account_tag= player_autocomplete, new_group = group_autocomplete)
    @app_commands.rename(account_tag="account")
    @app_commands.describe(account_tag="The account you want to change groups", new_group = "The group you want the account to change to")
    async def change_player_group(self, interaction: discord.Interaction, old_group:str, account_tag: str, new_group:str):
        await interaction.response.defer()
        
        dc_user = interaction.user
        guild_id = str(interaction.guild_id)
        
        player = self.db_player.get_player(account_tag)
        remove_player = self.db_group.try_remove_player(guild_id, new_group, account_tag, dc_user)
        
        if remove_player:
            add_player  = self.db_group.try_add_player(guild_id, new_group, player, dc_user)
            
            if add_player:
                await interaction.followup.send(f"The player has been removed from {old_group} and has been added to {new_group}.")
            else:
                await interaction.followup.send(f"The player could not have been added to {new_group}, but has been removed from {old_group}.")
        else:
            await interaction.followup.send(f"The player could not been removed from the group")

    ##############################################################################################################################
    #ALL GROUP COMMANDS
    ##############################################################################################################################

    @group.command(name="info", description="Gives the information about a group")
    @app_commands.autocomplete(group_name = group_autocomplete)
    @app_commands.describe(group_name = "The group you want to show")
    async def group_information(self, interaction: discord.Interaction, group_name : str):
        await interaction.response.defer()
        
        guild_id = str(interaction.guild_id)
        
        all_players = self.db.group_queries.get_players(guild_id, group_name)
        
        
        information = []
        for player in all_players:
            tag = player.tag
            player_dict = {
                "name": player.ingame_name,
            }
            mutations = self.db.mutation_queries.get_today_hits_from_player(tag)
            
            
            player_dict["offense"] = len(mutations["offense"])
            player_dict["defense"] = len(mutations["defense"])
            delta = sum(mutations["offense"]) + sum(mutations["defense"])
            player_dict["delta"] = delta
            
            
            #TODO
            begin_trophies = self.db.legend_day_queries.get_start_trophies(tag, datetime.date.today())

                
            print(begin_trophies)
            if not begin_trophies:
                begin_trophies = 0
           
            player_dict["start"] = begin_trophies
            player_dict["now"] = begin_trophies + delta

            information.append(player_dict)
            
    
        df = pandas.DataFrame.from_dict(information)
        df.sort_values(by="now", ascending=False)
        df.set_index("now")
        df.index +=1
        
        
        custom_embed = discord.Embed(title=f"Legend overview of: **{group_name}**",description=f"```{df}```")
        
        await interaction.followup.send(embed=custom_embed)
    
    @group.command(name="create", description="This will create a group")
    @app_commands.describe(group_name = "The name of the group")
    async def create_group(self, interaction: discord.Interaction, group_name: str):
        await interaction.response.defer()
        
        guild_id = str(interaction.guild_id)
        dc_user = interaction.user
        add_group = self.db.group_queries.try_add_group(guild_id=guild_id, group_name=group_name, discord_user=dc_user)

        if add_group:
            await interaction.followup.send(f"{group_name} has been created")
        else:
            await interaction.followup.send("An error has occured")
            
    @group.command(name="remove", description="This will remove a group")
    @app_commands.autocomplete(group_name = group_autocomplete)
    @app_commands.describe(group_name = "The name of the group")
    async def remove_group(self, interaction: discord.Interaction, group_name: str):
        await interaction.response.defer()
        
        guild_id = str(interaction.guild_id)
        dc_user = interaction.user
        
        add_group = self.db.group_queries.try_remove_group(guild_id=guild_id, group_name=group_name, discord_user=dc_user)

        if add_group:
            await interaction.followup.send(f"{group_name} has been removed")
        else:
            await interaction.followup.send("An error has occured")
            
    
async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(LegendGroup(bot))