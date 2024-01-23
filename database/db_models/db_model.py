from typing                     import Optional, List
from sqlalchemy                 import Integer, String, DateTime, Date
from sqlalchemy                 import ForeignKey, Column, Table, UniqueConstraint
from sqlalchemy.orm             import Mapped, DeclarativeBase
from sqlalchemy.orm             import mapped_column, relationship

class Base(DeclarativeBase):
    pass

association_table = Table(
    "association_table",
    Base.metadata,
    Column("tag", ForeignKey("player.tag"), primary_key=True),
    Column("id", ForeignKey("group.id"), primary_key=True),
    
)

class Player(Base):
    __tablename__ = "player"
    
    tag: Mapped[String] = mapped_column(String(20), primary_key=True, unique=True)
    ingame_name: Mapped[String] = mapped_column(String(20), unique=True)
    alias: Mapped[Optional[String]] = mapped_column(String(20), unique=True)
    
    #Parent of Mutation
    mutations: Mapped[List["Mutation"]] = relationship(back_populates="player")
    
    #Parent of LegendDay
    legend_days: Mapped[List["LegendDay"]] = relationship(back_populates="player")
    
    #Child of DiscordUser
    discord_user_id: Mapped[Optional[String]] = mapped_column(ForeignKey("discord_user.id"))
    discord_user: Mapped[Optional["DiscordUser"]] = relationship(back_populates="accounts")
    
    #Child of Group
    groups: Mapped[List["Group"]] = relationship(
        secondary=association_table, back_populates="players"
    )
    

class DiscordUser(Base):
    __tablename__ = "discord_user"
    
    id: Mapped[String] = mapped_column(String(30), primary_key=True) #discordid
    nickname: Mapped[String] = mapped_column(String(30), unique=True) #discordname
    alias: Mapped[Optional[String]] = mapped_column(String(30), unique=True)
    
    #Parent of Player
    accounts: Mapped[List["Player"]] = relationship(back_populates="discord_user")
    

class Group(Base):
    __tablename__ = "group"
    
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[String] = mapped_column(String(30))
    group_name: Mapped[String] = mapped_column(String(30))

    #Parent of Player
    players: Mapped[List["Player"]] = relationship(
        secondary=association_table, back_populates="groups"
    )
    

class Mutation(Base):
    __tablename__ = "mutation"
    
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    current_trophies: Mapped[int] = mapped_column(Integer)
    delta_trophies: Mapped[int]
    datetime: Mapped[DateTime] = mapped_column(DateTime())
    
    #Child of Player
    player_id: Mapped[String] = mapped_column(ForeignKey("player.tag"))
    player: Mapped["Player"] = relationship(back_populates="mutations")

class LegendDay(Base):
    __tablename__ = "legend_day"
    
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_trophies: Mapped[int]
    total_offense: Mapped[int]
    total_defense: Mapped[int]
    date: Mapped[Date] = mapped_column(Date())
    
    #Child of Player
    player_id: Mapped[String] = mapped_column(ForeignKey("player.tag"))
    player: Mapped["Player"] = relationship(back_populates="legend_days")
    



# # OLDTABLES
# class User(Base):
#     __tablename__ = 'legend_seasons'

#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     season: Mapped[str] = mapped_column(String(20))
#     tag: Mapped[str] = mapped_column(String(15))
#     name: Mapped[str] = mapped_column(String(30))
#     rank: Mapped[int]
#     trohpies: Mapped[int]
    
# class NationalityUser(Base):
#     __tablename__ = "players_nationality"
    
#     tag: Mapped[str]= mapped_column(String(15), primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     country: Mapped[str] = mapped_column(String(30))
      
# class TrackedUser(Base):
#     __tablename__ = "legend_mutations"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     tag: Mapped[str]= mapped_column(String(15))
#     current_trophies: Mapped[int]
#     delta_trophies: Mapped[int]
#     date: Mapped[DateTime] = mapped_column(DateTime())
    
# class GroupUser(Base):
#     __tablename__ = "user_groups"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     guild: Mapped[str] = mapped_column(String(30))
#     tag: Mapped[str]= mapped_column(String(15))
#     name: Mapped[str] = mapped_column(String(30))
#     group: Mapped[str] = mapped_column(String(30))
       
# class LegendDay(Base):
#     __tablename__ = "legend_start"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     tag: Mapped[str]= mapped_column(String(15))
#     trophies: Mapped[int]
#     date: Mapped[Date] = mapped_column(Date())

    



# # OLDTABLES
# class User(Base):
#     __tablename__ = 'legend_seasons'

#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     season: Mapped[str] = mapped_column(String(20))
#     tag: Mapped[str] = mapped_column(String(15))
#     name: Mapped[str] = mapped_column(String(30))
#     rank: Mapped[int]
#     trohpies: Mapped[int]
    
# class NationalityUser(Base):
#     __tablename__ = "players_nationality"
    
#     tag: Mapped[str]= mapped_column(String(15), primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     country: Mapped[str] = mapped_column(String(30))
      
# class TrackedUser(Base):
#     __tablename__ = "legend_mutations"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     tag: Mapped[str]= mapped_column(String(15))
#     current_trophies: Mapped[int]
#     delta_trophies: Mapped[int]
#     date: Mapped[DateTime] = mapped_column(DateTime())
    
# class GroupUser(Base):
#     __tablename__ = "user_groups"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     guild: Mapped[str] = mapped_column(String(30))
#     tag: Mapped[str]= mapped_column(String(15))
#     name: Mapped[str] = mapped_column(String(30))
#     group: Mapped[str] = mapped_column(String(30))
       
# class LegendDay(Base):
#     __tablename__ = "legend_start"
    
#     id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     tag: Mapped[str]= mapped_column(String(15))
#     trophies: Mapped[int]
#     date: Mapped[Date] = mapped_column(Date())
