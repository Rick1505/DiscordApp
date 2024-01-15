import aiohttp
import asyncio
import API
from API.league import League
from API.player import Player
from database.database import BotDatabase
from bot import MyBot
import datetime
import pandas

SQLITE_FILE = "database/legend_league.db"


async def main():
    db = BotDatabase(SQLITE_FILE)
    
    group_info = db.get_all_from_group(group_id="test3", guild_id=1168911698288193667)
    
    information = []
    for player in group_info:
        tag = player.tag
        player_dict = {
            "name": player.name,
        }
        mutations = db.get_all_mutations_per_day(tag)
        
        player_dict["offense"] = len(mutations["offense"])
        player_dict["defense"] = len(mutations["defense"])
        delta = sum(mutations["offense"]) - sum(mutations["defense"])
        player_dict["delta"] = delta
        
        begin_trophies = db.get_legend_start(account_tag=tag, date=datetime.date.today())
        player_dict["legend_start"] = begin_trophies
        player_dict["current_trophies"] = begin_trophies + delta

        information.append(player_dict)
        
 
    df = pandas.DataFrame.from_dict(information)
    df.sort_values(by="current_trophies", ascending=False)
    df.set_index("current_trophies")
    df.index +=1
    print(df)
    
async def main2():
    
    db = BotDatabase(SQLITE_FILE)
    
    print(db.get_legend_start("#YPLG2JGV", date=datetime.date.today()))
    # tuples = []
    # all_tags = db.get_all_unique_tags()
    # for tag in all_tags:
    #     player = Player(tag)
    #     trophies = await player.get_trophies()
    #     tuples.append((tag, trophies))
    
    # db.add_legend_start(tuples)

asyncio.run(main())