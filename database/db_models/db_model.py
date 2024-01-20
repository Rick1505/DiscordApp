from sqlalchemy import Column, Integer, String, DateTime, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm     import Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = 'legend_seasons'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    season: Mapped[str] = mapped_column(String(20))
    tag: Mapped[str] = mapped_column(String(15))
    name: Mapped[str] = mapped_column(String(30))
    rank: Mapped[int]
    trohpies: Mapped[int]
    

class NationalityUser(Base):
    __tablename__ = "players_nationality"
    
    tag: Mapped[str]= mapped_column(String(15), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    
    
class TrackedUser(Base):
    __tablename__ = "legend_mutations"
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str]= mapped_column(String(15))
    current_trophies: Mapped[int]
    delta_trophies: Mapped[int]
    date: Mapped[DateTime] = mapped_column(DateTime())
    
class GroupUser(Base):
    __tablename__ = "user_groups"
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild: Mapped[str] = mapped_column(String(30))
    tag: Mapped[str]= mapped_column(String(15))
    name: Mapped[str] = mapped_column(String(30))
    group: Mapped[str] = mapped_column(String(30))
    
    
class LegendDay(Base):
    __tablename__ = "legend_start"
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str]= mapped_column(String(15))
    trophies: Mapped[int]
    date: Mapped[Date] = mapped_column(Date())
