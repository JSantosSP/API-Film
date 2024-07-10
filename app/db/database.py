import random
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, func
from app.config import DATABASE_URL
from app.models import Movie
from app.utils import process_movies_with_high_popularity, process_list 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

def getAll():
    session = SessionLocal()
    try:
        # Consultar todas las películas en la base de datos
        movies = session.query(Movie).all()

        # Crear una lista para almacenar todos los atributos de las películas
        movies_list = []
        for movie in movies:
            movie_dict = {
                "tmdb_id": movie.tmdb_id,
                "original_title": movie.original_title,
                "overview": movie.overview,
                "poster": movie.poster,
                "imdb_id": movie.imdb_id,
                "vote_average": movie.vote_average,
                "genero": movie.genero
            }
            movies_list.append(movie_dict)

        process_list(movies_list)

    finally:
        # Cerrar la sesión
        session.close()  


def addFilm():
    nfilms = process_movies_with_high_popularity()
    return nfilms

def get_movie_details():
    session = SessionLocal()
    
    try:
        # Filtrar películas cuyo género no sea nulo
        movies = session.query(Movie).filter(Movie.genero.isnot(None)).all()

        # Seleccionar una película aleatoria de la lista
        movie = random.choice(movies) if movies else None

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
    finally:
        # Cerrar la sesión
        session.close()

def get_movies_by_word_and_genres(word):
    session = SessionLocal()
    try:
        # Convertir la palabra a minúsculas y crear un conjunto de letras únicas
        word_set = set(word.lower())
        
        # Filtrar películas cuya longitud de título sea igual a la longitud de la palabra
        movies = session.query(Movie).filter(
            and_(
                func.length(Movie.original_title) == len(word),
                func.lower(Movie.original_title).op('regexp')('[' + ''.join(word_set) + ']+')
            )
        ).all()

        # Seleccionar al azar hasta 12 películas de los resultados
        selected_movies = random.sample(movies, min(12, len(movies)))
        
        
        return [
             movie.original_title
         for movie in selected_movies]
    finally:
        # Cerrar la sesión
        session.close()