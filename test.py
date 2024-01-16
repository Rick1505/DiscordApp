from database.database import BotDatabase 
import datetime


SQLITE_FILE = "database/legend_league.db"

db = BotDatabase(SQLITE_FILE)
begin_trophies = db.get_legend_start(account_tag="#YPLG2JGV", date=datetime.date.today())
print(begin_trophies)
if not begin_trophies:
    print(db.get_player_trophies("#YPLG2JGV")    )
else:
    print(begin_trophies)
    
