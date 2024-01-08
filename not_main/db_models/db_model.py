from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'legend_seasons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(String)
    tag = Column(String)
    name = Column(String)
    rank = Column(Integer)
    trophies = Column(Integer) 
    

class NationalityUser(Base):
    __tablename__ = "players_nationality"
    
    tag = Column(String, primary_key=True, unique=True)
    name = Column(String)
    country = Column(String)
    
    
class TrackedUser(Base):
    __tablename__ = "legend_mutations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String)
    current_trophies = Column(Integer)
    delta_trophies = Column(Integer)
    date = Column(DateTime)
    
class GroupUser(Base):
    __tablename__ = "user_groups"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild = Column(Integer)
    tag = Column(String)
    name = Column(String)
    group = Column(String)

