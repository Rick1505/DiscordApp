import os
import requests
import urllib
from not_main.database import Database
import datetime

from typing import List

API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_PLAYER = "https://api.clashofclans.com/v1/players/"

class Player():

    #Initialise the player + account_tag
    def __init__(self, account_tag : str) -> None:
        self.account_tag = account_tag
        self.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'content-type': 'application/json',
            "charset": "utf-8"
        }
    
    #Function to get all the information from the player
    def get_all_player_info(self):
        
        url = f'{BASE_URL_PLAYER}{self.account_tag}'
        encoded_url = urllib.parse.quote(url, safe=":/")
        
        try: 
            response = requests.get(url=encoded_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            return ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            return ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            return ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            return ("OOps: Something Else",err)
        else:
            player_info = response.json()
            return player_info
        
    #Check if the player is currently in legend league        
    def is_in_legend(self):
        data = self.get_all_player_info()
        if data["league"]["id"] == 29000022:
            return True
        else:
            return False
                
    def get_legend_history(self):
        db = Database("sqlite", "instances/legend_league.db")
        return db.get_user_information(user_tag=self.account_tag)
    
    def change_season_to_dates(self, legend_history: List):
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
    def get_trophies(self):
        player_info = self.get_all_player_info()
        return player_info["trophies"]
    
    #Get the latest recorded trophies in the database of a player
    def get_db_trophies(self):
        db = Database("sqlite", "instances/legend_league.db")
        db.get_player_trophies(account_tag= self.account_tag)   
        return db.get_player_trophies(account_tag= self.account_tag)        
        
    def get_name(self):
        data = self.get_all_player_info()
        return data["name"]
        
        
        
        
        
    
        
    