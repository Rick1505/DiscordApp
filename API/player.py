import aiohttp
import datetime
import asyncio

from urllib import parse
from database.database import BotDatabase
from typing import List


BASE_URL_PLAYER = "https://api.clashofclans.com/v1/players/"

class Player():

    #Initialise the player + account_tag
    def __init__(self, fetch) -> None:
        self.fetch = fetch
    
    #Function to get all the information from the player
    async def get_all_player_info(self) -> dict:
        api_session = aiohttp.ClientSession()

        url = f'{BASE_URL_PLAYER}{"#YPLG2JGV"}'
        encoded_url = parse.quote(url, safe=":/")
        
        async with api_session as session:
            return await self.fetch(session, encoded_url, timeout=30)
         
    async def is_in_legend(self) -> bool:
        data = await self.get_all_player_info()
        return data["league"]["id"] == 29000022
    
    async def get_trophies(self) -> int:
        player_info = await self.get_all_player_info()
        return player_info["trophies"]
            
    async def get_name(self) -> str:
        data = await self.get_all_player_info()
        return data["name"]
   
    
    #MAYBE SWITCH TO DB
    #Get the latest recorded trophies in the database of a player
    async def get_db_trophies(self, db):
        return db.get_player_trophies(account_tag= self.account_tag)     
    
    #CAN ACTUALLY BE REMOVED IF NOT CONTINUING WITH LEGEND HISTORY
    async def change_season_to_dates(self, legend_history: List):
        '''Function that was used to change all seasons in the all legend data to a date'''
        seasons_pre = []
        for record in legend_history:
            seasons_pre.append(record.season)

        seasons_post = []
        for s in seasons_pre:
            s = s.split("-")
            date = datetime.date(year=int(s[0]), month= int(s[1]), day=1)
            seasons_post.append(date)
            
        for i in range(len(legend_history)):
            legend_history[i].season = seasons_post[i]
        return legend_history     
    
    async def get_legend_history(self, db):
        return db.get_user_information(user_tag=self.account_tag)
        
        
        
        
    
        
    