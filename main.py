import  discord
import  os
from    discord             import app_commands
from    not_main.player     import Player
from    not_main.league     import League
from    not_main.emojis     import Emoji
from    not_main.clan       import Clan
from    not_main.utils      import make_embed
from    typing              import Optional


MY_GUILD = discord.Object(int(os.getenv("GUILD_ID")))  # replace with your guild id
MY_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
emoji = Emoji()

@client.event
async def on_ready():
    await tree.sync(guild=MY_GUILD)
    print(f'Logged in as {client.user} (ID: {client.user.id})')

#Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.


#SHOW INFORMATION ABOUT THE PLAYER
@tree.command(name = "besttrophies", description = "This will show you your highest legend score", guild=MY_GUILD)
@app_commands.rename(account_tag = "account")
@app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def best_trophies(interaction: discord.Interaction, account_tag: str ):
    
    player = Player(account_tag=account_tag)
    league = League()
    info = player.get_all_player_info()
    
    custom_embed = make_embed(
       title = "Legend seasons",
       author_icon = info["clan"]["badgeUrls"]["medium"],
       author_text = info["name"],
       thumbnail_url = league.get_specific_league_image(info["league"]["id"]),
       fields = [("September", f'{client.get_emoji(emoji.get_emoji("legend_trophy"))} {info["bestTrophies"]}', False)],
       footer_text = info["tag"]
    )
   
    await interaction.response.send_message(embed=custom_embed)
 
 
#SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
@tree.command(name = "hero_equipment", description = "This will show you the hero equipment of a player", guild=MY_GUILD)
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
@tree.command(name = "claninfo", description = "This will show you the information about the clan", guild=MY_GUILD)
@app_commands.rename(clan_tag = "clantag")
@app_commands.describe(clan_tag = "The clan tag you want to check formatedd in '#ACCOUNT' ")
async def best_trophies(interaction: discord.Interaction, clan_tag: str ):
    
    clan = Clan(clan_tag=clan_tag)
    info = clan.get_clan_info()
    print(info)
    await interaction.response.send_message("test")
    
    
#This command was used to test the embed function  
@tree.command(name="embed_test", description="embed_tested", guild=MY_GUILD)
@app_commands.describe(message = "the thing you want to say", message2= "the second thing you want to say", inline = "Either True or False, defaults to False") 
async def display_textbox(interaction: discord.Interaction, message: str, message2: str, inline: Optional[bool] = False):
    
    embed = make_embed(
        title= "test",
        description= "test1",
        url= "https://api-assets.clashofclans.com/leagues/36/R2zmhyqQ0_lKcDR5EyghXCxgyC9mm_mVMIjAbmGoZtw.png",
        thumbnail_url= "https://api-assets.clashofclans.com/badges/70/h4etl6xNbZuLCXRFD3JD90vz3a1K4hjCyEZ9ihu_RI0.png",
        image_url= "https://api-assets.clashofclans.com/leagues/72/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png",
        author_text= "test123",
        author_url= "https://api-assets.clashofclans.com/leagues/72/uUJDLEdAh7Lwf6YOHmXfNM586ZlEvMju54bTlt2u6EE.png",
        author_icon= "https://cdn.discordapp.com/attachments/1187745572464107621/1187895063397798059/Play.png?ex=65988c7d&is=6586177d&hm=9e051a1169ef49e14ced3e913ccddf8347034e136873f1462bab01a2b3ba3906&",
        footer_text= "test123",
        footer_icon= "https://api-assets.clashofclans.com/leagues/36/R2zmhyqQ0_lKcDR5EyghXCxgyC9mm_mVMIjAbmGoZtw.png",
    )
    await interaction.response.send_message(embed=embed)
    

@tree.command(name="legend_seasons2", description="This will show you all the ranks you have achieved in the different legend seasons", guild=MY_GUILD)
@app_commands.rename(account_tag = "account")
@app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def display_legend_seasons(interaction: discord.Interaction, account_tag: str):
    
    player = Player(account_tag=account_tag)
    league = League()
    
    info = player.get_all_player_info()
    # legend_info = player.get_legend_history()
    
    custom_embed = make_embed(
       title = "Legend seasons",
       author_icon = info["clan"]["badgeUrls"]["medium"],
       author_text = info["name"],
       thumbnail_url = league.get_specific_league_image(info["league"]["id"]),
       footer_text = info["tag"],
       fields = [("September", f'{client.get_emoji(emoji.get_emoji("legend_trophy"))} {info["bestTrophies"]}', False)]
    )
    
    await interaction.response.send_message(embed=custom_embed)

    
    
@tree.command(name="legend_seasons", description="This will show you all the ranks you have achieved in the different legend seasons", guild=MY_GUILD)
@app_commands.rename(account_tag = "account")
@app_commands.describe(account_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def display_legend_seasons(interaction: discord.Interaction, account_tag: str):
    
    await interaction.response.defer()

    player = Player(account_tag=account_tag)
    league = League()
    
    info = player.get_all_player_info()
    legend_info = player.get_legend_history()
    
    list = [f"{record.season} - {record.rank}" for record in legend_info]
    description = "\n".join(list)
    
    custom_embed = make_embed(
       title = "Legend seasons",
       author_icon = info["clan"]["badgeUrls"]["medium"],
       author_text = info["name"],
       thumbnail_url = league.get_specific_league_image(info["league"]["id"]),
       description=description,
       footer_text = info["tag"],
       fields = [("September", f'{client.get_emoji(emoji.get_emoji("legend_trophy"))} {info["bestTrophies"]}', False)]
    )
    await interaction.followup.send(embed=custom_embed)
            
client.run(MY_TOKEN)