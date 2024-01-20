from API import clan, league, location, player
from settings   import Config
from aiohttp    import ClientSession, ClientError


class APICalls:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.clan_queries = clan.Clan(self.fetch)
        self.league_queries = league.League(self.fetch) 
        self.location_queries = location.Location(self.fetch)
        self.player_queries = player.Player(self.fetch)
        
        self.headers = { 
            'Authorization': f'Bearer {self.config.coc_api_token}',
            'content-type': 'application/json',
            "charset": "utf-8"
        }
        
    async def fetch(self, session: ClientSession, url:str, timeout: int):
        try:
            async with session.get(url=url, params=self.headers, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Succesfully fetched {url} ")
                    return data
                else:
                    response.raise_for_status
                    print(response.status)
                    print("failed")
        except ClientError as e:
            return e
        
    
    async def close(self, session: ClientSession) -> None:
        if not session.closed:
            await session.close()
