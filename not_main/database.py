from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from not_main.db_models.db_model import User, NationalityUser, Base
import asyncio

class Database():
    def __init__(self, database_type: str, url_database: str) -> None:
        self.engine = create_engine(f'{database_type}:///{url_database}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = Base

    def create_specific_table(self, table):
        self.Base.metadata.create_all(self.engine, tables = [table.__table__])
        
    def create_all_tables(self):
        self.Base.metadata.create_all(self.engine)
           
    def add_season_to_legend_db(self, data: list, season: str):
        self.create_specific_table(User)
        
        #Add users to a list
        data_to_add = [User(season=season, tag=item["tag"], name=item["name"], rank=item["rank"], trophies=item["trophies"]) for item in data]
        
        #Add all useres to the database
        self.session.add_all(data_to_add)
        self.session.commit()
        
    def get_user_information(self, user_tag):
        return self.session.query(User).filter_by(tag=user_tag).all()

    def add_dutch_players(self, data : list, country: str):
        self.create_specific_table(NationalityUser)
    
        #Add all data to list
        data_to_add = [[item["tag"], item["name"], country] for item in data]    
        
        
        # print(data_to_add)        
        # Make an insert statement so I don't get duplicates using IGNORE 
        insert_statement = text("""
            INSERT OR IGNORE INTO players_nationality (tag, name, country)
            values (:tag, :name, :country)
        """)
        
        for row in data_to_add:
            self.session.execute(insert_statement, {"tag":row[0], "name": row[1], "country":row[2]})
        
        self.session.commit()
            
    # def add_mutation(self, data: list):
            
        
        
        
        
        