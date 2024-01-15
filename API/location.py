import requests
import os
from urllib import parse
from database.database import BotDatabase
import aiohttp


API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_LEAGUE = "https://api.clashofclans.com/v1/locations/"

class Location():

    def __init__(self) -> None:
        self.api_session = aiohttp.ClientSession()

        self.netherlands_id = 32000166
        self.belgium_id = 32000029

    def get_dutch_players(self):
        url = f"{BASE_URL_LEAGUE}{self.netherlands_id}/rankings/players"
        
        response = requests.get(url=url, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        return data["items"]
    
    
    def get_belgian_players(self):
        url = f"{BASE_URL_LEAGUE}{self.belgium_id}/rankings/players"
        
        response = requests.get(url=url, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        return data["items"]
    
