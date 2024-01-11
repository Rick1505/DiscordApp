from not_main.location import Location
from database.database import Database
from not_main.player   import Player
from not_main.clan     import Clan
import datetime
import requests
import os
import urllib
import time

# db = Database(database_type="sqlite", url_database="instances/legend_league.db")
    
# mutations = db.get_all_mutations_per_day("#YPLG2JGV")

# print(mutations["offense"])

# offense = [10,2,3,5,6,9,7]
# print(sum(offense))

# # offense = mutations["offense"]
# defense = mutations["defense"]

# field1 = "\n".join(str(attack) for attack in offense)

# print(field1)
# # field2 = "\n".join(defense)
# # now = datetime.datetime.now(datetime.UTC)

# print(now.hour)

 
# now_later = now + datetime.timedelta(days=1)
# now_earlier = now + datetime.timedelta(days=-1)
# print(now_later)
# print(now_earlier)







# async def legend_feed(channel: discord.TextChannel, guild_id: int):
#     db = Database(database_type="sqlite", url_database="instances/legend_league.db")
    
#     # Get tags from all groups
#     player_group = db.get_all_groups(guild_id=guild_id)
    
#     #store every tag in a list
#     tags_to_check = [record.tag for record in player_group]
#     mutations = []
#     #Check every individual tag for changes
#     for tag in tags_to_check:
#         info = []
#         player = Player(tag)
#         player_info = player.get_all_player_info()
        
#         new_trophies = player_info["trophies"]
#         current_trophies = player.get_db_trophies()
#         delta_trophies = new_trophies - current_trophies
                       
#         #TODO add all changes to a list in a list as a string with: emoji, cups, name
#         #TODO make an embed with multiple pages, every page shows Title: name; Description: overview, total begin total now +/- and details with every attack. footer is group_name           
#         if new_trophies > current_trophies:
#             db.add_mutation(account_tag=tag, current_trophies=current_trophies, new_trophies=new_trophies)
#             custom_embed = discord.Embed(
#                 title=player_info["name"],
#                 color= discord.Color.from_rgb(0, 200, 0),
#                 description= f"{client.get_emoji(emoji.get_emoji("plus_trophy"))} {delta_trophies}"
#             ) 
#             custom_embed.set_footer(text=tag)
#             mutations.append(custom_embed)

#             # await channel.send(embed=custom_embed)  

#         elif new_trophies < current_trophies:
#             db.add_mutation(account_tag=tag, current_trophies=current_trophies, new_trophies=new_trophies)
#             custom_embed = discord.Embed(
#                 title=player_info["name"],
#                 colour= discord.Colour.from_rgb(254, 0,0),
#                 description= f"{client.get_emoji(emoji.get_emoji("min_trophy"))} {delta_trophies}"
#             ) 
#             custom_embed.set_footer(text=tag)
#             mutations.append(custom_embed)
            
#             # await channel.send(embed=custom_embed)  
        
               
#     if len(mutations) > 0:            
#         current_page = 0
        
#         message = await channel.send(embed=mutations[current_page])
#         await message.add_reaction("◀️")  # Left arrow reaction
#         await message.add_reaction("▶️")  # Right arrow reaction

#         while True:
#             try:
#                 reaction, user = await client.wait_for('reaction_add', timeout=60.0)

#                 if str(reaction.emoji) == "▶️":
#                     current_page = (current_page + 1) % len(mutations)
#                 elif str(reaction.emoji) == "◀️":
#                     current_page = (current_page - 1) % len(mutations)

#                 await message.edit(embed=mutations[current_page])
#                 await message.remove_reaction(reaction, user)

#             except TimeoutError:
#                 break