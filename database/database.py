import datetime 
import os

from urllib.parse import quote_plus
from sqlalchemy import create_engine, Column, Integer, String, text, delete, and_, update 
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session
from database.db_models.db_model import User, NationalityUser, GroupUser, TrackedUser, LegendDay, Base
from datetime import date
from settings import Config


class TrackedUserQueries:
    def __init__(self, session: Session) -> None:
        self.session = Session
    
    def add_mutation(self, account_tag, current_trophies, new_trophies):
        """Adds a mutation to the table mutations"""
        #Calculate the difference in trophies
        delta_trophies = new_trophies - current_trophies
        
        #Add a new mutation to the database
        new_mutation = TrackedUser(tag=account_tag, current_trophies= new_trophies, delta_trophies = delta_trophies, date=datetime.datetime.now(datetime.UTC))
        self.session.add(new_mutation)
        self.session.commit()  
        
    def get_player_trophies(self, account_tag: str):
        """Gets the latest player trophies in the database"""
        data = self.session.query(TrackedUser.current_trophies).filter_by(tag=account_tag).order_by(TrackedUser.id.desc()).first()
        return data.current_trophies
    
    def check_if_player_is_tracked(self, account_tag: str) -> bool:
        """
        Checks if a plyer is tracked in the mutations\n
        Returns False if a player is not tracked
        """
        #Returns False if not tracked, returns True if tracked
        return self.session.query(TrackedUser.id).filter_by(tag=account_tag).first() is not None

    def get_all_mutations_per_day(self, account_tag: str) -> dict:
        """
        This function returns a dictionary with two attributes.
        Offense: all positive mutations of the legend day
        Defense: all negative mutations of the legend sday
        """
        
        #Get current time in UTC
        now = datetime.datetime.now(datetime.UTC)
        tomorrow = now + datetime.timedelta(days=1)  
        yesterday = now + datetime.timedelta(days=1)  
              
        
        #Check if current time is before or after legend reset of today
        if now.hour >= 6:
            
            #If it is after set begin_time as today, end_time as tomorrow
            begin_time = datetime.datetime(now.year,now.month, now.day,5,0,0,0, datetime.UTC)
            end_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day,5,0,0,0,datetime.UTC)   
        else:

            #If it is before set begin_time as yesterday, end_time as today
            begin_time = datetime.datetime(yesterday.year,yesterday.month, yesterday.day,5,0,0,0, datetime.UTC) 
            end_time = datetime.datetime(now.year,now.month, now.day,5,0,0,0, datetime.UTC)
            
        data = self.session.query(TrackedUser.delta_trophies).filter(TrackedUser.date > begin_time, TrackedUser.date < end_time, TrackedUser.tag == account_tag).all()
        data = [record.delta_trophies for record in data]        
        
        mutations = {
            "offense": [],
            "defense": [],
            "error": []
        }
        
        for mutation in data:
            if mutation > 0:
                mutations["offense"].append(mutation)
            elif mutation < 0:
                mutations["defense"].append(mutation)
            else:
                mutations["error"].append(mutation)
       
        return mutations       
                
class GroupQueries:
    def __init__(self, session: Session) -> None:
        self.session = session
         
    def get_all_unique_tags(self):
        data = self.session.query(GroupUser.tag).all()
        all_tags =  [record.tag for record in data]
        return set(all_tags)
    
    def get_all_from_group(self, group_id: int, guild_id: int):
        """Gets all the objects from a specific group"""
        return self.session.query(GroupUser).filter_by(group=group_id, guild=guild_id).all()
    
    def get_all_groups(self, guild_id: int):
        """Returns all the objects in every group"""
        return self.session.query(GroupUser).filter_by(guild = guild_id).all()
    
    async def add_player_to_group(self, group: str, player, guild_id: int) -> str:
        """This function adds a player to a group in the table 'Groups'
        It returns a string whether an user is added or not
        """
        player_info = await player.get_all_player_info()
        account_tag = player_info["tag"]
        #Check if player is already added to the group in the current guild
        exists = self.session.query(GroupUser.id).filter_by(tag=account_tag, group=group, guild = str(guild_id)).first() is not None
                
        if not exists:
            name = player_info["name"]
            #If player isn't in the group add it to group
            self.session.add(GroupUser(group=group, tag=account_tag, guild = str(guild_id), name=name))
            
            #Also check if player is tracked already
            is_tracked = self.check_if_player_is_tracked(account_tag)
            self.session.commit()
            
            if not is_tracked:
                #If not tracked get player trophies
                
                current_trophies = player_info["trophies"]
                #Add player to TRACKED_USERS Table
                self.add_mutation(account_tag=account_tag, current_trophies=0, new_trophies=current_trophies)
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
    
    def rm_player(self,player: str, guild_id:int) -> str:
        """
        Deletes the user from all groups in this specific guild.\n
        Returns a string that tells you the user has been deleted
        """
        delete_statement = delete(GroupUser).where(and_(GroupUser.guild==str(guild_id), GroupUser.tag==player))
        
        self.session.execute(delete_statement)
        self.session.commit()
        self.session.close()
        return "User has been deleted"

    def get_current_group(self, account: str, guild_id: int):
        """Returns the group name of a specific group an account is in"""
        response = self.session.query(GroupUser).filter_by(guild=str(guild_id), tag=account).scalar()
        return response.group
    
    def change_player_group(self, account: str, new_group: str, guild_id: int) -> str:
        """
        Changes the group for a specific player in the guild the action has been performed\n
        Returns a string whether the user has been updated or not
        """
        update_statement = update(GroupUser).where(and_(GroupUser.guild == str(guild_id), GroupUser.tag==account)).values(group=new_group)
        
        self.session.execute(update_statement)
        self.session.commit()
        self.session.close()
        
        if self.get_current_group(account=account, guild_id=str(guild_id)) == new_group:
            return "User has been updated"
        else:
            return "There has ben an error"
    
    def get_player_from_group(self, guild_id, account_tag):
        """Returns a player object from a specific group in the current guild"""
        return self.session.query(GroupUser).filter_by(guild=str(guild_id), tag=account_tag).scalar()

class LegendDay:
       
    def __init__(self, session: Session) -> None:
        self.session = session
       
    def add_legend_start(self, players: list[tuple]):
        #players ia list of tuples with format: (account_tag, trophies)
        
        mutations = [LegendDay(tag= tuple[0], trophies = tuple[1], date = datetime.date.today()) for tuple in players]
        self.session.add_all(mutations)
        self.session.commit()
        
    def get_legend_start(self, account_tag: str, date: date):
        try:
            query = self.session.query(LegendDay.trophies).filter_by(tag=account_tag, date=date).scalar()
        except NoResultFound as e:
            return e
        else:
            return query
        
class LegendSeasons:
    
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_season_to_legend_db(self, data: list, season: str):       
        #Add users to a list
        data_to_add = [User(season=season, tag=item["tag"], name=item["name"], rank=item["rank"], trophies=item["trophies"]) for item in data]
        
        #Add all useres to the database
        self.session.add_all(data_to_add)
        self.session.commit()
        
    def get_user_information(self, user_tag: str):
        return self.session.query(User).filter_by(tag=user_tag).all()

class BotDatabase:
    def __init__(self, config: Config) -> None:
        self.is_connected = False
        self.config = config
        self.connection = self.connect()
        self.session: Session = self.session_maker()
        
        self.tracked_user_queries = TrackedUserQueries(self.session)
        self.group_queries = GroupQueries(self.session)
        self.legend_day_queries = LegendDay(self.session)
        self.legend_seasons_queries = LegendSeasons(self.session)
        
      
    def connect(self) -> None:
        self.engine = create_engine(self.config.db_connection_string)
        self.session_maker = sessionmaker(bind=self.engine)
        self.Base = Base
        self.initiate_db()
        self.is_connected = True
        
    def close_connection(self) -> None:
        self.connection.close()
        
    def initiate_db(self):
        self.Base.metadata.create_all(self.engine)

   
    # #LOCATIONS TABLE
    # def add_dutch_players(self, data : list, country: str):
    #     #Add all data to list
    #     data_to_add = [[item["tag"], item["name"], country] for item in data]    
        
        
    #     # print(data_to_add)        
    #     # Make an insert statement so I don't get duplicates using IGNORE 
    #     insert_statement = text("""
    #         INSERT OR IGNORE INTO players_nationality (tag, name, country)
    #         values (:tag, :name, :country)
    #     """)
        
    #     for row in data_to_add:
    #         self.session.execute(insert_statement, {"tag":row[0], "name": row[1], "country":row[2]})
        
    #     self.session.commit()
    
          
        
    
            
        
        
        
        
        