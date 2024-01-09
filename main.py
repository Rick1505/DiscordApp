import  discord
import  os
from    discord             import app_commands
from    discord.ext         import tasks
from    not_main.player     import Player
from    not_main.league     import League
from    not_main.emojis     import Emoji
from    not_main.clan       import Clan
from    not_main.utils      import make_embed
from    not_main.database   import Database
from    typing              import Any, Optional, List
from    enum                import Enum
from    asyncio             import TimeoutError

MY_GUILD = discord.Object(int(os.getenv("GUILD_ID")))  # replace with your guild id
MY_TOKEN = os.getenv("DISCORD_TOKEN")

emoji = Emoji()

class MyClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        
       
client = MyClient()

@client.event
async def on_ready():
    
    channel_id = discord.utils.get(client.get_all_channels(), name="testbot")
    print(f'Logged in as {client.user} (ID: {client.user.id})')

#TODO BEFORE LIVE REMOVE GUILD COMMAND
#Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.


#TODO SHOW INFORMATION ABOUT THE PLAYER
# @client.tree.command(name = "besttrophies", description = "This will show you your highest legend score", guild=MY_GUILD)
# @app_commands.rename(account_tag = "account")
# @app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
# async def best_trophies(interaction: discord.Interaction, account_tag: str ):
#     pass
 
 
#SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
@client.tree.command(name = "hero_equipment", description = "This will show you the hero equipment of a player", guild=MY_GUILD)
@app_commands.rename(account_tag = "account")
@app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def best_trophies(interaction: discord.Interaction, account_tag: str ):
    
    player = Player(account_tag=account_tag)
    info = player.get_all_player_info()
    hero_equip = info["heroEquipment"]
    embed = discord.Embed(title= info["name"], color=discord.Colour.from_rgb(0, 150, 255))

    
    for equip in hero_equip:
        embed.add_field(name=equip["name"], value=equip["level"], inline=True)
        
    await interaction.response.send_message(embed=embed)
  
 
#SHOW INFORMATION ABOUT THE CLAN 
# @client.tree.command(name = "claninfo", description = "This will show you the information about the clan", guild=MY_GUILD)
# @app_commands.rename(clan_tag = "clantag")
# @app_commands.describe(clan_tag = "The clan tag you want to check formatedd in '#ACCOUNT' ")
# async def best_trophies(interaction: discord.Interaction, clan_tag: str ):
    
#     clan = Clan(clan_tag=clan_tag)
#     info = clan.get_clan_info()
#     print(info)
#     await interaction.response.send_message("test")

#DISPLAYS ALL LEGEND SEASONS FROM 2021 TO 2023     
@client.tree.command(name="legend_seasons", description="This will show you all the ranks you have achieved in the different legend seasons", guild=MY_GUILD)
@app_commands.rename(account_tag = "account")
@app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def display_legend_seasons(interaction: discord.Interaction, account_tag: str): 
    await interaction.response.defer()

    player = Player(account_tag=account_tag)
    league = League()
    
    info = player.get_all_player_info()
    legend_info = player.get_legend_history()
        
    legend_info_dates = player.change_season_to_dates(legend_info)   
    description = []
    
    for year in range(2023, 2020, -1):
        description.append(f"**{year}**\n")
        
        for record in legend_info_dates:
            if record.season.year == year:    
                month = f'`{record.season.strftime("%B")}\t|`'
                description.append(month.expandtabs(11))
                
                rank = f'{client.get_emoji(emoji.get_emoji("legend_trophy"))} {record.trophies} | {client.get_emoji(emoji.get_emoji("earth"))} {record.rank} \n'
                description.append(rank)

    description = "".join(description)
        
    embed_legend_seasons = make_embed(
       title = "Legend seasons",
       author_icon = info["clan"]["badgeUrls"]["medium"],
       author_text = info["name"],
       thumbnail_url = league.get_specific_league_image(info["league"]["id"]),
       description=description,
       footer_text = info["tag"],
    )
    await interaction.followup.send(embed=embed_legend_seasons)


def create_standard_embed(player_name:str, player_tag: str, group_name: str, database: Database) -> discord.Embed:
    db = database
    
    data = db.get_all_mutations_per_day(account_tag=player_tag)
    
    offense = data["offense"]
    defense = data["defense"]
    
    field1 = "\n".join(str(attack) for attack in offense)
    field2 = "\n".join(str(defend) for defend in defense)
    
    description = f"""
    __*Overview*__ \n
    
    Total Offense: {sum(offense)}\n
    Total Defense: {sum(defense)}
    """
    custom_embed = discord.Embed(
        title=player_name,
        description= description,
        colour=discord.Colour.from_rgb(0, 150, 255)
    )
    custom_embed.add_field(name="**Offense**", value=field1, inline=True)
    custom_embed.add_field(name="**Defense**", value=field2, inline=True)
    
    custom_embed.set_footer(text=group_name)
    return custom_embed


# async def create_standard_paging(embeds: List, channel:discord.TextChannel):
#     current_page = 0
            
#     message = await channel.send(embed=embeds[current_page])
    
#     await message.add_reaction("◀️")  # Left arrow reaction
#     await message.add_reaction("▶️")  # Right arrow reaction

#     while True:
#         try:
#             reaction, user = await client.wait_for('reaction_add', timeout=60.0)

#             if str(reaction.emoji) == "▶️":
#                 current_page = (current_page + 1) % len(embeds)
#             elif str(reaction.emoji) == "◀️":
#                 current_page = (current_page - 1) % len(embeds)

#             await message.edit(embed=embeds[current_page])
#             await message.remove_reaction(reaction, user)

#         except TimeoutError:
#             break   


    
#THIS WILL POST LEGEND HITS EVERY 60 SECONDS
@tasks.loop(seconds=60) 
async def legend_feed(channel: discord.TextChannel, guild_id: int):
    db = Database(database_type="sqlite", url_database="instances/legend_league.db")
    
    # Get tags from all groups
    player_group = db.get_all_groups(guild_id=guild_id)
    
    #store every tag in a list
    tags_to_check = [record.tag for record in player_group]
    
    #Create list of mutations
    mutations = []
    
    standard_embeds = []
    
    #Check every individual tag for changes
    for tag in tags_to_check:
        info = {}
        player = Player(tag)
        player_info = player.get_all_player_info()
        
        #Calculating trophies
        new_trophies = player_info["trophies"]
        current_trophies = player.get_db_trophies()
        #CHANGE TO DELTA
        delta_trophies = new_trophies - current_trophies
                        
        #TODO add all changes to a list in a list as a string with: emoji, cups, name
        #TODO make an embed with multiple pages, every page shows Title: name; Description: overview, total begin total now +/- and details with every attack. footer is group_name
        if delta_trophies != 0:
            #adds mutation to database
            db.add_mutation(account_tag=tag, current_trophies=current_trophies, new_trophies=new_trophies)

            #adds information to info
            info["name"] = player_info["name"]
            info["group_name"] = db.get_player_from_group(768847345889575020, account_tag=tag).group
            info["delta_trophies"] = delta_trophies
            
            standard_embeds.append(create_standard_embed(info["name"], tag, info["group_name"], db))
            
            #add information of mutation to list mutations
            mutations.append(info)
            
    #Check amount of mutations
    if len(mutations) > 1:    
        
        #create list of embeds
        embeds = []
        counter = 1
          
        description = ""    
        for mutation in mutations:

            if mutation["delta_trophies"] > 0:
                #Add positive mutation to description
                description =  description + (f"{counter} {client.get_emoji(emoji.get_emoji("plus_trophy"))} {mutation["delta_trophies"]} {mutation["name"]}\n")
                counter += 1
                
            else:
                #Add negative mutation to description
                description = description +  (f"{counter} {client.get_emoji(emoji.get_emoji("min_trophy"))} {mutation["delta_trophies"]} {mutation["name"]} \n")
                counter += 1
                
        #Create embed with lists of mutations
        custom_embed = discord.Embed(
                description = description,
                colour=discord.Colour.from_rgb(0, 150, 255)
        )
        
        #add custom_embed to list of embeds
        embeds.append(custom_embed)
        embeds = embeds + standard_embeds
        
        
        #check if there are any embeds
        if len(embeds) > 0:
            
            current_page = 0
            
            message = await channel.send(embed=embeds[current_page])
            
            await message.add_reaction("◀️")  # Left arrow reaction
            await message.add_reaction("▶️")  # Right arrow reaction

            while True:
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0)

                    if str(reaction.emoji) == "▶️":
                        current_page = (current_page + 1) % len(embeds)
                    elif str(reaction.emoji) == "◀️":
                        current_page = (current_page - 1) % len(embeds)

                    await message.edit(embed=embeds[current_page])
                    await message.remove_reaction(reaction, user)

                except TimeoutError:
                    break   
            
        
    elif len(mutations) == 1:
        embeds = []       
        mutation = mutations[0]
          
        if mutation["delta_trophies"] > 0:
            
            custom_embed = discord.Embed(
                title=mutation["name"],
                color= discord.Color.from_rgb(0, 200, 0),
                description= f"{client.get_emoji(emoji.get_emoji("plus_trophy"))} {mutation["delta_trophies"]}"
            ) 
            custom_embed.set_footer(text=tag)
            embeds.append(custom_embed)
            
        else:
            custom_embed = discord.Embed(
                title=mutation["name"],
                colour= discord.Colour.from_rgb(254, 0,0),
                description= f"{client.get_emoji(emoji.get_emoji("min_trophy"))} {mutation["delta_trophies"]}"
            ) 
            custom_embed.set_footer(text=tag)
            embeds.append(custom_embed)
        
        embeds = embeds + standard_embeds

                    
        if len(embeds) > 0:
            current_page = 0
            
            message = await channel.send(embed=embeds[current_page])
            
            await message.add_reaction("◀️")  # Left arrow reaction
            await message.add_reaction("▶️")  # Right arrow reaction

            while True:
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=180.0)

                    if str(reaction.emoji) == "▶️":
                        current_page = (current_page + 1) % len(embeds)
                    elif str(reaction.emoji) == "◀️":
                        current_page = (current_page - 1) % len(embeds)

                    await message.edit(embed=embeds[current_page])
                    await message.remove_reaction(reaction, user)

                except TimeoutError:
                    
                    break   
    else:
        pass

#ACTIVATES THE LEGEND_FEED   
@client.tree.command(name = "set_legend_feed", description = "This will set the correct channel for the legend feed.", guild=MY_GUILD)
@app_commands.rename(channel = "channel")
@app_commands.describe(channel = "The channel you want the bot to post all hits in")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    legend_feed.start(channel, interaction.guild.id)
       
    await interaction.response.send_message(f"The channel has successfully been set {channel}")
              
#AUTO POPULATE FOR A GROUP       
async def group_autocomplete(
    interaction: discord.Interaction,
    current: str,
)   -> List[app_commands.Choice[str]]:
    db = Database(database_type="sqlite", url_database="instances/legend_league.db")
    
    all_groups = db.get_all_groups(interaction.guild.id)
    group_names = [record.group for record in all_groups]
    group_names_unique = list(set(group_names))
    
    return [
        app_commands.Choice(name=group, value=group)
        for group in group_names_unique if current.lower() in group.lower()
    ] 
      
#THIS ADDS A PLAYER TO A GROUP       
@client.tree.command(name="add_player_to_group", description="This will add a player to a specific group", guild=MY_GUILD)
@app_commands.autocomplete(group_tag = group_autocomplete)
@app_commands.rename(account_tag="account", group_tag="group")
@app_commands.describe(account_tag="The account you want to add to a group", group_tag= "The group you want to add the account to")
async def add_player_to_group(interaction: discord.Interaction, account_tag: str, group_tag: str):
    await interaction.response.defer()

    db = Database(database_type="sqlite", url_database="instances/legend_league.db")   
    player = Player(account_tag=account_tag)
    group_to_add = group_tag.lower()
    response = db.add_player_to_group(group=group_to_add, player=player,guild_id=interaction.guild.id )
    
    await interaction.followup.send(response)    

#AUTO POPULATE FOR A PLAYER
async def player_autocomplete(
    interaction: discord.Interaction,
    current: str,
)   -> List[app_commands.Choice[str]]:
    db = Database(database_type="sqlite", url_database="instances/legend_league.db")
    
    all_players = db.get_all_groups(interaction.guild.id)
    player_accounts = [[record.name, record.tag] for record in all_players]
    player_accounts_unique = [list(player) for player in set(tuple(player) for player in player_accounts)]
           
    return [
        app_commands.Choice(name=f"{player[0]} - {player[1]}", value=player[1])
        for player in player_accounts_unique
    ]
           
#THIS REMOVES A PLAYER
@client.tree.command(name="remove_player", description="This will remove the player from the feed", guild=MY_GUILD)
@app_commands.autocomplete(account_tag = player_autocomplete)
@app_commands.rename(account_tag="account")
@app_commands.describe(account_tag="The account you want to remove from the group")
async def remove_player(interaction: discord.Interaction, account_tag: str):
    await interaction.response.defer()
    db = Database(database_type="sqlite", url_database="instances/legend_league.db")
    response = db.rm_player(player=account_tag, guild_id=interaction.guild.id)
    
    await interaction.followup.send(response)    
    
#CHANGES THE PLAYER TO ANOTHER GROUP
@client.tree.command(name="change_group", description="Change the player from one group to another", guild=MY_GUILD)
@app_commands.autocomplete(account_tag= player_autocomplete, new_group = group_autocomplete)
@app_commands.rename(account_tag="account")
@app_commands.describe(account_tag="The account you want to change groups", new_group = "The group you want the account to change to")
async def change_player_group(interaction: discord.Interaction, account_tag: str, new_group:str):
    await interaction.response.defer()
    
    db = Database(database_type="sqlite", url_database="instances/legend_league.db")
    response = db.change_player_group(guild_id = interaction.guild.id, account= account_tag, new_group = new_group)
        
    await interaction.send(response)    
                 
client.run(MY_TOKEN)
