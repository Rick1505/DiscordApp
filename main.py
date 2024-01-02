import  discord
import  os
from    discord             import app_commands
from    not_main.player     import Player
from    not_main.league     import League
from    not_main.emojis     import Emoji
from    not_main.clan       import Clan
from    not_main.utils      import make_embed
from    typing              import Any, Optional
import  asyncio

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
    print(f'Logged in as {client.user} (ID: {client.user.id})')

#Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.


#SHOW INFORMATION ABOUT THE PLAYER
@client.tree.command(name = "besttrophies", description = "This will show you your highest legend score", guild=MY_GUILD)
@app_commands.rename(account_tag = "account")
@app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def best_trophies(interaction: discord.Interaction, account_tag: str ):
    
    player = Player(account_tag=account_tag)
    league = League()
    info = player.get_all_player_info()
    
    embed_legend_seasons = make_embed(
       title = "Legend seasons",
       author_icon = info["clan"]["badgeUrls"]["medium"],
       author_text = info["name"],
       thumbnail_url = league.get_specific_league_image(info["league"]["id"]),
       fields = [("September", f'{client.get_emoji(emoji.get_emoji("legend_trophy"))} {info["bestTrophies"]}', False)],
       footer_text = info["tag"]
    )
   
    await interaction.response.send_message(embed=embed_legend_seasons)
 
 
#SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
@client.tree.command(name = "hero_equipment", description = "This will show you the hero equipment of a player", guild=MY_GUILD)
@app_commands.rename(account_tag = "account")
@app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def best_trophies(interaction: discord.Interaction, account_tag: str ):
    
    player = Player(account_tag=account_tag)
    info = player.get_all_player_info()
    hero_equip = info["heroEquipment"]
    embed = discord.Embed(title= info["name"])
    
    for equip in hero_equip:
        embed.add_field(name=equip["name"], value=equip["level"], inline=True)
        
    await interaction.response.send_message(embed=embed)
  
 
#SHOW INFORMATION ABOUT THE CLAN 
@client.tree.command(name = "claninfo", description = "This will show you the information about the clan", guild=MY_GUILD)
@app_commands.rename(clan_tag = "clantag")
@app_commands.describe(clan_tag = "The clan tag you want to check formatedd in '#ACCOUNT' ")
async def best_trophies(interaction: discord.Interaction, clan_tag: str ):
    
    clan = Clan(clan_tag=clan_tag)
    info = clan.get_clan_info()
    print(info)
    await interaction.response.send_message("test")
    
@app_commands.guild_only      
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
      
client.run(MY_TOKEN)
