from not_main.location import Location
from not_main.database import Database

loc = Location()

dutchies = loc.get_belgian_players()

# print(dutchies)

db = Database(database_type="sqlite", url_database="instances/legend_league.db")
db.add_dutch_players(data=dutchies, country="Belgium")


