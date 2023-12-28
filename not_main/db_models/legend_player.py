from sqlalchemy import Column, Integer, String
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