from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from not_main.db_models.legend_player import User, Base

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
           
    def add_season_to_legend_db(self, data, season):
        self.create_specific_table(User)
        
        #Add users to a list
        data_to_add = [User(season=season, tag=item["tag"], name=item["name"], rank=item["rank"], trophies=item["trophies"]) for item in data]
        
        #Add all useres to the database
        self.session.add_all(data_to_add)
        self.session.commit()
        
    def get_user_information(self, user_tag):
        return self.session.query(User).filter_by(tag=user_tag).all()

