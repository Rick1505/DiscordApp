from not_main.location import Location
from not_main.database import Database
from not_main.player   import Player
import time

loc = Location()

dutchies = loc.get_belgian_players()

# print(dutchies)

db = Database(database_type="sqlite", url_database="instances/legend_league.db")
# player = Player("#LJCLPU0PC")
# trophies = player.get_trophies()
# db.add_player_to_group(group=1, player= player, trophies=trophies)

# Get every tag you want to check
player_group = db.get_all_groups(768847345889575020)
print(player_group)

# #store every tag in a list
# all_groups = db.get_all_groups(interaction.guild.id)
group_names = [record.group for record in player_group]
group_names_unique = list(set(group_names))
print(group_names_unique)
#Check every individual tag for changes
# while True:

#     for tag in tags_to_check:
#         player = Player(tag)
#         new_trophies = player.get_trophies()
#         current_trophies = player.get_db_trophies()
        
#         if new_trophies != current_trophies:
#             db.add_mutation(account_tag=tag, current_trophies=current_trophies, new_trophies=new_trophies)
#         else:
#             print("Current is the same as new")
#     time.sleep(60)
        
    

    