from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    
    tmdb_id = Column(String, primary_key=True)
    original_title = Column(String)
    overview = Column(String)
    poster = Column(String)
    imdb_id = Column(String)
    vote_average = Column(Float)
    genero = Column(String)

class Limite(Base):
    __tablename__ = "limite"

    fecha_actual = Column(Date, primary_key=True)  
    ctOpenIA = Column(Integer, default=0)  
    ctOMDb = Column(Integer, default=0)  