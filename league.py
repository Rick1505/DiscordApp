import requests
import os
from urllib import parse


API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_LEAGUE = "https://api.clashofclans.com/v1/leagues"
    
class League():

    def __init__(self) -> None:
        self.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'content-type': 'application/json',
            "charset": "utf-8"
        }
    
    def get_all_leagues(self):
        url = BASE_URL_LEAGUE
        encoded_url =  parse.quote(url, safe= ":/")
        response = requests.get(encoded_url, headers=self.headers)
        return response.json()
    
    def get_specific_league(self, league_id):
        url = f"{BASE_URL_LEAGUE}/{league_id}"
        encoded_url = parse.quote(url, safe=":/")
        response = requests.get(encoded_url, headers=self.headers)
        return response.json()
           
    
    def get_specific_league_image(self, league_id):
        data = self.get_specific_league(league_id)
        return data["iconUrls"]["tiny"]
    
        