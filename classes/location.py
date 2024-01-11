import requests
import os
from urllib import parse
from database.database import BotDatabase


API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_LEAGUE = "https://api.clashofclans.com/v1/locations/"

class Location():

    def __init__(self) -> None:
        self.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'content-type': 'application/json',
            "charset": "utf-8"
        }
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
    
