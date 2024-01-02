import requests
import os
from urllib import parse
from not_main.database import Database


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
    
    def add_players_to_legend_db(self):
        db = Database(database_type="sqlite", url_database="instances/legend_league.db")
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


            

    
        