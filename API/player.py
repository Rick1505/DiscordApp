import os
import requests
import urllib
import aiohttp
import datetime

from database.database import BotDatabase
from typing import List
from API.aiosession import fetch


API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_PLAYER = "https://api.clashofclans.com/v1/players/"

class Player():

    #Initialise the player + account_tag
    def __init__(self, account_tag : str) -> None:
        self.account_tag = account_tag
        self.api_session = aiohttp.ClientSession()
    
    #Function to get all the information from the player
    async def get_all_player_info(self):
        url = f'{BASE_URL_PLAYER}{self.account_tag}'
        encoded_url = urllib.parse.quote(url, safe=":/")
        
        async with self.api_session as session:
            data = await fetch(session, encoded_url, timeout=30)
            return data
        
    #Check if the player is currently in legend league        
    async def is_in_legend(self):
        data = await self.get_all_player_info()
        if data["league"]["id"] == 29000022:
            return True
        else:
            return False
                
    async def get_legend_history(self):
        db = BotDatabase("database/legend_league.db")
        return db.get_user_information(user_tag=self.account_tag)
    
    async def change_season_to_dates(self, legend_history: List):
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

    #Get the current trophies of a player
    async def get_trophies(self):
        player_info = await self.get_all_player_info()
        return player_info["trophies"]
    
    #Get the latest recorded trophies in the database of a player
    async def get_db_trophies(self):
        db = BotDatabase("database/legend_league.db")
        db.get_player_trophies(account_tag= self.account_tag)   
        return db.get_player_trophies(account_tag= self.account_tag)        
        
    async def get_name(self):
        data = await self.get_all_player_info()
        return data["name"]
        
        
        
        
        
    
        
    