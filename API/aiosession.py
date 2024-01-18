import aiohttp
import asyncio
import os

API_TOKEN = os.getenv("API_TOKEN_TESTING")

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'content-type': 'application/json',
    "charset": "utf-8"
}   

async def fetch(session, url, timeout):
    
    try:
        async with session.get(url, params=headers, timeout=timeout) as response:
            if response.status == 200:
                data = await response.json()
                print(f"Succesfully fetched {url} ")
                return data
            else:
                print(response.status)
                print("failed")
    except aiohttp.ClientError as e:
        return e
        

