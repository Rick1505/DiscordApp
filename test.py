from database.database import BotDatabase
from API.player        import Player
from datetime           import date
import asyncio

db = BotDatabase("test")

async def update_legend_start():
        tuples = []
        
        all_tags = db.get_all_unique_tags()
        print(all_tags)
        for tag in all_tags:
            player = Player(tag)
            trophies = await player.get_trophies()
            tuples.append((tag, trophies))
        print(tuples)
        
        db.add_legend_start(tuples)
        
        
async def get_legend_start2():
    all_tags = db.get_all_unique_tags()
    print(all_tags)
    for tag in all_tags:
        legend_start = db.get_legend_start(tag, date.today())
        print(legend_start)
        
async def main():
    db.clear_legend_start()
    await update_legend_start()
    await get_legend_start2()
    
if __name__ == "__main__":
    asyncio.run(main())
        