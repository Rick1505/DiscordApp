from database.database import PlayerQueries, MutationQueries, GroupQueries
from sqlalchemy import create_engine, delete, and_, update, select 
from sqlalchemy.orm import sessionmaker, Session
from settings import Config
from API.coc_api_tasks import APICalls
from discord import Webhook
import asyncio
import aiohttp
import datetime


config = Config()
engine = create_engine(config.db_connection_string)
session_maker = sessionmaker(bind=engine)
session: Session = session_maker()
coc_api = APICalls(config)
player_api_calls = coc_api.player_queries

player_queries_db = PlayerQueries(session=session)
group_queries_db = GroupQueries(session, player_queries_db)
mutation_queries_db = MutationQueries(session, player_queries_db)

async def update_legend_start():
    player_info = await player_api_calls.get_all_player_info("#YPLG2JGV")
    player_to_add = player_queries_db.try_add_player(account_information=player_info, alias="HammmyTest")
    print(player_to_add)
        
async def mutation_get():
    # test = mutation_queries_db.add("#YPLG2JGV", 505, 6000)
    test = mutation_queries_db.get_today_hits_from_player("#YPLG2JGV")
    print(test)
    
async def group_functions():
    
    # test = group_queries_db.try_add_group(str(747819040549896294), "tesfs")
    # test2 = group_queries_db.try_add_player(str(747819040549896294),"tesfs", "#YPLG2JGV")
    test = group_queries_db.get_all_unique_tags(str(1168911698288193667))
    for player in test:
        print(player.tag)
    print(set(test))


async def webhook_test():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url="https://discord.com/api/webhooks/1202247359652974602/4uzDp9FxJRrDFlXe0UwkTJVS1Ng8Ozba16TnPF0OsEQ0V5XUdxRxyZ09Qi2Cgl-sZSxw", session=session)
        # test = webhook.user()
        await webhook.send("Hello world")

async def main():
    # await update_legend_start()
    # await mutation_get()
    # await group_functions()
    await webhook_test()
    
if __name__ == "__main__":
    asyncio.run(main())
