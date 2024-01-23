import requests
import os
import aiohttp

from urllib import parse
# from database.database import BotDatabase
# from API.aiosession import fetch

API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_LEAGUE = "https://api.clashofclans.com/v1/leagues"
    
class League():

    def __init__(self, fetch) -> None:
        self.fetch = fetch
    
    async def get_all_leagues(self):
        api_session = aiohttp.ClientSession()

        url = BASE_URL_LEAGUE
        async with api_session as session:
            return await self.fetch(session, url, timeout=60)
    
    async def get_specific_league(self, league_id):
        api_session = aiohttp.ClientSession()

        url = f"{BASE_URL_LEAGUE}/{league_id}"
        encoded_url = parse.quote(url, safe=":/")
        
        async with api_session as session:
            return await self.fetch(session=session, url=encoded_url, timeout=60)
           
    async def get_specific_league_image(self, league_id):
        data = await self.get_specific_league(league_id)
        return data["iconUrls"]["tiny"]
    
    #CHANGE THIS TO DB OR REMOVE
    async def add_players_to_legend_db(self):
        db = BotDatabase(url_database="database/legend_league.db")
        seasons= ["2021-01"]        
                
        for s in seasons:           
            #Set the correct season to get the api from
            url = f"{BASE_URL_LEAGUE}/29000022/seasons/{s}"
            
            #encode the url so # won't matter
            encoded_url = parse.quote(url, safe=":/?=")
            response = requests.get(url=encoded_url, headers=self.headers)
            
            #Get the data and only get all the players in data_items
            data = response.json()
            data_items = data["items"]
            for s in seasons:
                db.add_season_to_legend_db(data_items, season=s)


            

    
        