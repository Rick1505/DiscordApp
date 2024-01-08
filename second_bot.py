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

MY_GUILD = discord.Object(int(os.getenv("TEST_GUILD_ID")))  # replace with your guild id
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

#TODO BEFORE LIVE REMOVE GUILD COMMAND
#Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
 
#SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
@client.tree.command(name = "hero_equipment_clan", description = "This will show you the hero equipment of a player", guild=MY_GUILD)
@app_commands.rename(clan_tag = "account")
@app_commands.describe(clan_tag = "The account tag you want to check formatedd in '#ACCOUNT' ")
async def best_trophies(interaction: discord.Interaction, clan_tag: str ):
    await interaction.response.defer()

    clan = Clan(clan_tag)
    members = clan.get_all_players()
    all_tags = [member["tag"] for member in members["items"]]
    embeds = []
    for tag in all_tags:
        player = Player(tag)
        info = player.get_all_player_info()
        hero_equip = info["heroEquipment"]
        embed = discord.Embed(title= info["name"], color=discord.Colour.from_rgb(0, 150, 255))

        
        for equip in hero_equip:
            embed.add_field(name=equip["name"], value=equip["level"], inline=True)
        
        embeds.append(embed)    
        
    current_page = 0
    if len(embeds) != 0:            

        message = await interaction.followup.send(embed=embeds[current_page])
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
       
#SHOW INFORMATION ABOUT THE HERO EQUIPMENT OF A PLAYER
@client.tree.command(name = "hero_equipment_player", description = "This will show you the hero equipment of a player", guild=MY_GUILD)
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
    
           
client.run(MY_TOKEN)
