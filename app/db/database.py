import json
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from app.models import Movie
from app.utils import process_movies_with_high_popularity  # Asegúrate de importar la función correctamente

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def addFilm():
    session = SessionLocal()
    try:
        nfilms = process_movies_with_high_popularity(session)
    finally:
        # Cerrar la sesión de SQLAlchemy al finalizar
        session.close()
    return nfilms

def get_movie_info(movie_id):
    session = SessionLocal()

    # Realizar la consulta a la base de datos
    movie = session.query(Movie.original_title, Movie.overview).filter_by(tmdb_id=movie_id).first()

    # Cerrar la sesión
    session.close()

    # Devolver el resultado
    if movie:
        return {
            "original_title": movie.original_title,
            "overview": movie.overview
        }
    else:
        return None

def get_movie_details(movie_id):
    session = SessionLocal()

    # Realizar la consulta a la base de datos
    movie = session.query(Movie).filter_by(tmdb_id=movie_id).first()

    # Cerrar la sesión
    session.close()

    # Devolver el resultado
    if movie:
        return {
            "tmdb_id": movie.tmdb_id,
            "original_title": movie.original_title,
            "overview": movie.overview,
            "poster": movie.poster,
            "imdb_id": movie.imdb_id,
            "vote_average": movie.vote_average,
            "genero": movie.genero
        }
    else:
        return None