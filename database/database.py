import discord 
import datetime

from typing import Optional
from urllib.parse import quote_plus
from sqlalchemy import create_engine, delete, and_, func, update, select, cast, Date
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session

from database.db_models.db_model import Player, DiscordUser, Group, Mutation, LegendDay, Base
from settings import Config

class PlayerQueries:
    
    def __init__(self, session: Session) -> None:
        self.session = session       
    
    def get_player(self, player_tag:str) -> Optional[Player]:
        player_tag = player_tag.upper()
        return self.session.scalars(select(Player).filter_by(tag=player_tag)).first()
    
    def try_add_player(self, account_information: dict, alias: str = None, discord_user: discord.User = None, group: str = None) -> bool:
        """
        returns true if succeeded, else false
        """
        count_query = select(func.count(Player.tag))
        pre_count = self.session.scalar(count_query)
        
        all_account_info = account_information
        user_to_add = None
        
        tag:str = account_information["tag"]

        if discord_user:
            user_to_add = self.session.scalars(select(DiscordUser).filter_by(id = str(discord_user.id))).first() 
            if not user_to_add:
                return False
               
        mutation_to_add = Mutation(
            current_trophies = int(all_account_info["trophies"]),
            delta_trophies = int(all_account_info["trophies"]),
            datetime = datetime.datetime.now(datetime.UTC)
        )
                  
        player = Player(
            tag = tag.upper(),
            ingame_name = all_account_info["name"], 
            alias = alias,
            discord_user = user_to_add,
            mutations = [mutation_to_add]
        )
        
        self.session.add(player)
        self.session.commit()
        post_count = self.session.scalar(count_query)
        return post_count > pre_count
                                   
    #PROBABLY BELONGS TO LEGEND DAYS
    #TODO
    #return fales if no player exists
    def get_all_legend_days(self, player_tag: str):
        player = self.get_player(player_tag)
        
        if player:
            return player.legend_days
        else:
            return False         
class DiscordUserQueries:
    
    def __init__(self, session: Session) -> None:
        self.session = session
               
    def get_user(self, discord_user: discord.User):
        return self.session.scalars(select(DiscordUser).filter_by(id = str(discord_user.id))).first()
                  
    def try_add_user(self, discord_user: discord.User, alias= None) -> bool:
        count_query = select(func.count(LegendDay.id))
        pre_count = self.session.scalar(count_query)
        
        discord_id = str(discord_user.id)
        discord_name = discord_user.name

        if not self.get_user(discord_user):
            user = DiscordUser(id = discord_id, nickname = discord_name, alias= alias)      
            self.session.add(user)
            self.session.commit()
            post_count = self.session.scalar(count_query)
        
            return post_count > pre_count
        else:
            False   
    
    def link_clash_account(self, discord_user: discord.User, player_tag:str) -> bool:
        player = self.session.scalars(select(Player).filter_by(tag=player_tag)).first()
        user = self.get_user(discord_user)
        
        if player:  
            # create user if not exists
            if not user:
                if self.try_add_user(discord_user):
                    user = self.get_user(discord_user)
                else:
                    return False
                
            user.accounts.append(player)
            return True
        else:
            return False               
                  
    def change_alias(self, discord_user: discord.User, alias: str):
        user_to_change = self.get_user(discord_user= discord_user)
        
        if user_to_change:
            user_to_change.alias = alias
            return True
        else:
            return False 
class GroupQueries:
    
    def __init__(self, session: Session, player_queries: PlayerQueries) -> None:
        self.session = session
        self.player_queries = player_queries
   
    def get_group(self, guild_id: str, group_name: str) -> Optional[Group]:
        stmt = select(Group).filter(and_(Group.guild_id == guild_id, Group.group_name == group_name))
        return self.session.scalars(stmt).first()
    
    def get_players(self, guild_id, group_name) -> list[Player]:
        group_to_query = self.get_group(guild_id, group_name)
        
        if group_to_query:
            return group_to_query.players
        else:
            return "No group found with these id's"
        
    def try_add_group(self, guild_id: str, group_name) -> bool:
        group = self.get_group(guild_id, group_name)
        
        if not group:
            count_query = select(func.count(Group.id))
            pre_count = self.session.scalar(count_query)
            
            new_group = Group(
                guild_id = guild_id,
                group_name = group_name
            )
            self.session.add(new_group)
            self.session.commit()
            
            post_count = self.session.scalar(count_query)
            return post_count > pre_count
        else:
            return False
    
    def try_remove_group(self, guild_id, group_name) -> bool:
        group = self.get_group(guild_id, group_name)
        
        if group:
            count_query = select(func.count(Group.id))
            pre_count = self.session.scalar(count_query)
    
            self.session.delete(group)
            self.session.commit()
            
            post_count = self.session.scalar(count_query)
            
            return post_count < pre_count
        else:
            return False

    def try_add_player(self, guild_id, group_name, player_tag) -> bool:
        
        group_to_add = self.get_group(guild_id, group_name)
        player_to_add = self.player_queries.get_player(player_tag)
        
        if group_to_add and player_to_add:
            group_to_add.players.append(player_to_add)
            player_to_add.groups.append(group_to_add)
            self.session.commit()
            return True
        else:
            return False
        
    def change_player(self, guild_id, old_group, new_group, player_tag):
        group_to_remove = self.get_group(guild_id, old_group)
        group_to_add = self.get_group(guild_id, new_group)
        player_to_change = self.player_queries.get_player(player_tag)
        
        if group_to_remove and player_to_change:
            group_to_remove.players.remove(player_to_change)
            
            if group_to_add:
                group_to_add.players.append(player_to_change)
                player_to_change.groups = [group_to_add]
                
                self.session.commit()
                return True
            #if group doesn't exist make it
            else:
                group_add = self.try_add_group(guild_id, new_group)
                #if group is added:
                if group_add:
                    #retrieve new group
                    group_to_add = self.get_group(guild_id, new_group)
                    
                    #add group to new _players
                    group_to_add.players.append(player_to_change)
                    player_to_change.groups = [group_to_add]
                    self.session.commit()
                    return True
                else:
                    return False
        else:
            return False

    def remove_player(self, guild_id, group_name, player_tag):
        group = self.get_group(guild_id, group_name)
        player_to_remove = self.player_queries.get_player(player_tag)
        
        if group and player_to_remove:
            group.players.remove(player_to_remove)
            player_to_remove.groups.remove(group)
            
            self.session.commit()
            return True
        else:
            return False

    #TODO
    def get_all_unique_tags(self):
        all_players = self.session.execute(select(Group.players)) 
        
        # all_tags =  [record.tag for record in data]
        # return set(all_tags)
    
    # async def add_player_to_group(self, group: str, player, guild_id: int) -> str:
        # """This function adds a player to a group in the table 'Groups'
        # It returns a string whether an user is added or not
        # """
        # player_info = await player.get_all_player_info()
        # player_tag = player_info["tag"]
        # #Check if player is already added to the group in the current guild
        # exists = self.session.query(GroupUser.id).filter_by(tag=player_tag, group=group, guild = str(guild_id)).first() is not None
                
        # if not exists:
        #     name = player_info["name"]
        #     #If player isn't in the group add it to group
        #     self.session.add(GroupUser(group=group, tag=player_tag, guild = str(guild_id), name=name))
            
        #     #Also check if player is tracked already
        #     is_tracked = self.check_if_player_is_tracked(player_tag)
        #     self.session.commit()
            
        #     if not is_tracked:
        #         #If not tracked get player trophies
                
        #         current_trophies = player_info["trophies"]
        #         #Add player to TRACKED_USERS Table
        #         self.add_mutation(player_tag=player_tag, current_trophies=0, new_trophies=current_trophies)
        #         self.session.commit()
        #         self.session.close()
        #         return "User is starting to get tracked and has been added to the group"
        #     else:
        #         self.session.close()
        #         #TODO return an a string with this answer so discord can send a message user is already being tracked
        #         return "User is added to the group"                
        # else:
        #     #TODO return an a string with this answer so discord can send a message
        #     #Return error player is in the group
        #     return "User is already in the group"
class MutationQueries:
    
    def __init__(self, session: Session, player_queries: PlayerQueries) -> None:
        self.session = session
        self.player_queries = player_queries
        
    def add(self, player_tag, current_trophies, new_trophies):
        """Adds a mutation to the table mutations"""
        #Calculate the difference in trophies
        delta_trophies = new_trophies - current_trophies
        
        #Add a new mutation to the database
        player_to_add = self.player_queries.get_player(player_tag)
        new_mutation = Mutation(
            current_trophies= new_trophies, 
            delta_trophies = delta_trophies, 
            datetime = datetime.datetime.now(datetime.UTC)
        )

        if player_to_add:
            player_to_add.mutations.append(new_mutation) 
            self.session.add(new_mutation)
            self.session.commit() 
        else:
            return False
    #TODO 
    def remove_all_from_player(self):
        pass
    #TODO
    def remove_all(self):
        pass
    
    def get_player_trophies(self, player_tag):
        """Gets the latest player trophies in the database"""
        stmt = select(Mutation.current_trophies).filter_by(tag=player_tag).order_by(Mutation.id.desc())
        data = self.session.execute(stmt).first()
        return data.current_trophies
    #TODO TEST
    def get_today_hits_from_player(self, player_tag:str) -> dict:  
        
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
            
        data = self.session.execute(select(Mutation.delta_trophies).filter(and_(Mutation.datetime > begin_time, Mutation.datetime < end_time, Mutation.player_id == player_tag))).all()
        data = [row.delta_trophies for row in data]        
        
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
class LegendDaysQueries:
    
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def add(self, start_trophies, total_offense, total_defense, player_tag):
        count_query = select(func.count(LegendDay.id))
        pre_count = self.session.scalar(count_query)
        
        player_to_add = self.session.scalars(select(Player).filter_by(tag=player_tag)).first()
        
        if player_to_add:
            legend_day_to_add = LegendDay(
                start_trophies = start_trophies,
                total_offense = total_offense,
                total_defense = total_defense,
                player = player_to_add
            )
            
            self.session.add(legend_day_to_add)
            self.session.commit() 
            
            post_count = self.session.scalar(count_query)
            return post_count > pre_count                
        else:
            return False   
class BotDatabase:
    def __init__(self, config: Config) -> None:
        self.is_connected = False
        self.config = config
        self.connection = self.connect()
        self.session: Session = self.session_maker()
               
        self.player_queries = PlayerQueries(self.session)
        self.group_queries = GroupQueries(self.session, self.player_queries)
        self.legend_day_queries = LegendDaysQueries(self.session)
        self.mutation_queries = MutationQueries(self.session, self.player_queries)
        
      
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
    
          
        
    
            
        
        
        
        
        