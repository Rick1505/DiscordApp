from sqlalchemy import create_engine, Column, Integer, String, text, delete, and_, update
from sqlalchemy.orm import sessionmaker
from not_main.db_models.db_model import User, NationalityUser, GroupUser, TrackedUser, Base
from datetime import datetime as dt


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
    
    #LEGEND_TROPHIES TABLE       
    def add_season_to_legend_db(self, data: list, season: str):
        self.create_specific_table(User)
        
        #Add users to a list
        data_to_add = [User(season=season, tag=item["tag"], name=item["name"], rank=item["rank"], trophies=item["trophies"]) for item in data]
        
        #Add all useres to the database
        self.session.add_all(data_to_add)
        self.session.commit()
        
    def get_user_information(self, user_tag: str):
        return self.session.query(User).filter_by(tag=user_tag).all()


    #LOCATIONS TABLE
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
    
    
    #TRACKED_USERS TABLE          
    def add_mutation(self, account_tag, current_trophies, new_trophies):
        #Create the table
        self.create_specific_table(TrackedUser)
        
        #Calculate the difference in trophies
        delta_trophies = new_trophies - current_trophies
        
        #Add a new mutation to the database
        new_mutation = TrackedUser(tag=account_tag, current_trophies= new_trophies, delta_trophies = delta_trophies, date=dt.now())
        self.session.add(new_mutation)
        self.session.commit()
        
        
    def get_player_trophies(self, account_tag: str):
        self.create_specific_table(TrackedUser)

        #Gets the latest player trophies in the database
        data = self.session.query(TrackedUser.current_trophies).filter_by(tag=account_tag).order_by(TrackedUser.id.desc()).first()
        return data.current_trophies
    
    def check_if_player_is_tracked(self, account_tag: str) -> bool:
        self.create_specific_table(TrackedUser)

        #Returns False if not tracked, returns True if tracked
        return self.session.query(TrackedUser.id).filter_by(tag=account_tag).first() is not None
        
        
    #GROUPS TABLE    TODO ADD GUILD_ID
    def get_all_from_group(self, group_id: int, guild_id: int):
        #Gets all the objects from a specific group
        self.create_specific_table(GroupUser)
        
        return self.session.query(GroupUser).filter_by(group=group_id, guild=guild_id).all()
    
    def get_all_groups(self, guild_id: int):
        #Gets all the objects in all groups
        return self.session.query(GroupUser).filter_by(guild = guild_id).all()
    
    def add_player_to_group(self, group: str, player, guild_id: int):
        self.create_specific_table(GroupUser)
        
        #Check if player is already added to the group in the current guild
        exists = self.session.query(GroupUser.id).filter_by(tag=player.account_tag, group=group, guild = guild_id).first() is not None
                
        if not exists:
            name = player.get_name()
            #If player isn't in the group add it to group
            self.session.add(GroupUser(group=group, tag=player.account_tag, guild = guild_id, name=name))
            
            #Also check if player is tracked already
            is_tracked = self.check_if_player_is_tracked(player.account_tag)
            self.session.commit()
            
            if not is_tracked:
                #If not tracked get player trophies
                current_trophies = player.get_trophies()
                #Add player to TRACKED_USERS Table
                self.add_mutation(account_tag=player.account_tag, current_trophies=0, new_trophies=current_trophies)
                self.session.commit()
                self.session.close()
                return "User is starting to get tracked and has been added to the group"
            else:
                self.session.close()
                #TODO return an a string with this answer so discord can send a message user is already being tracked
                return "User is added to the group"                
        else:
            #TODO return an a string with this answer so discord can send a message
            #Return error player is in the group
            return "User is already in the group"
    
    def rm_player(self,player: str, guild_id:int):
        #delete the user from a specific group
        delete_statement = delete(GroupUser).where(and_(GroupUser.guild==guild_id, GroupUser.tag==player))
        
        self.session.execute(delete_statement)
        self.session.commit()
        self.session.close()
        return "User has been deleted"

    def get_current_group(self, account: str, guild_id: int):
        response = self.session.query(GroupUser).filter_by(guild=guild_id, tag=account).scalar()
        return response.group
    
    def change_player_group(self, account: str, new_group: str, guild_id: int):
        
        update_statement = update(GroupUser).where(and_(GroupUser.guild == guild_id, GroupUser.tag==account)).values(group=new_group)
        
        self.session.execute(update_statement)
        self.session.commit()
        self.session.close()
        
        if self.get_current_group(account=account, guild_id=guild_id) == new_group:
            return "User has been updated"
        else:
            return "There has ben an error"
    
        
        
        
        
    
            
        
        
        
        
        