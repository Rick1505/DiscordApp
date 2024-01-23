import os
from urllib import parse
import aiohttp


API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_LEAGUE = "https://api.clashofclans.com/v1/locations/"

class Location():

    def __init__(self, fetch) -> None:
        self.fetch = fetch
        self.api_session = aiohttp.ClientSession()

        self.netherlands_id = 32000166
        self.belgium_id = 32000029


    async def get_leaderboard(self, location_id):       
        api_session = aiohttp.ClientSession()

        url = f"{BASE_URL_LEAGUE}{location_id}/rankings/players"
        
        async with api_session as session:
            data = await self.fetch(session, url, timeout=30)
            return data["items"]

    
