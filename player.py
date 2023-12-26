import os
import requests
import urllib

API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_PLAYER = "https://api.clashofclans.com/v1/players/"

class Player:
    
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
        
        
    
        
    