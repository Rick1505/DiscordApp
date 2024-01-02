import os
import requests
from urllib import parse

API_TOKEN = os.getenv("API_TOKEN_COC")
BASE_URL_CLAN = "https://api.clashofclans.com/v1/clans/"

class Clan():
    
    def __init__(self, clan_tag : str) -> None:
        self.clan_tag = clan_tag
        self.headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'content-type': 'application/json',
            "charset": "utf-8"
        }
        
    
    def get_clan_info(self):
        url = f'{BASE_URL_CLAN}{self.clan_tag}'
        encoded_url = parse.quote(url, safe=":/")
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
            clan_info = response.json()
            return clan_info
    
    def get_all_players(self):
        url = f"{BASE_URL_CLAN}{self.clan_tag}/members"
        encoded_url = parse.quote(url, safe=":/")
        
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
            all_members = response.json()
            return all_members
    
    def get_current_war(self):
        url = f"{BASE_URL_CLAN}{self.clan_tag}/currentwar"
        encoded_url = parse.quote(url, safe=":/")
        try:
            response = requests.get(url=encoded_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            return ("Oops: Something Else", err)
        else:
            return response.json()
    