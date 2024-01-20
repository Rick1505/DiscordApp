import os
import requests
from urllib import parse
from discord.ext import commands
import aiohttp

API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_CLAN = "https://api.clashofclans.com/v1/clans/"

class Clan():
    
    def __init__(self, fetch) -> None:
        self.fetch = fetch
    
    async def get_clan_info(self, clan_tag):
        api_session = aiohttp.ClientSession()
        url = f'{BASE_URL_CLAN}{clan_tag}'
        encoded_url = parse.quote(url, safe=":/")
        
        async with api_session as session:
            return await self.fetch(session, encoded_url, timeout=60)
           
           
    async def get_all_players(self, clan_tag):
        api_session = aiohttp.ClientSession()

        url = f"{BASE_URL_CLAN}{clan_tag}/members"
        encoded_url = parse.quote(url, safe=":/")
        
        async with api_session as session:
            return await self.fetch(session, encoded_url, timeout=60)
    
    
    async def get_current_war(self, clan_tag):
        api_session = aiohttp.ClientSession()

        url = f"{BASE_URL_CLAN}{clan_tag}/currentwar"
        encoded_url = parse.quote(url, safe=":/")
        
        async with api_session as session:
            return await self.fetch(session, encoded_url, timeout=60)
        

