import requests
import json
import time
from sqlalchemy.orm import Session
from app.models import Movie, Limite
from datetime import date
from app.config import TMDB_API_KEY, OMDB_API_KEY

def get_tmdb_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_omdb_movie_details(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def update_or_insert_limite(session: Session):
    session = session
    today = date.today()
    
    try:
        # Query the existing record for today's date
        limite_record = session.query(Limite).filter(Limite.fecha == today).first()
        
        if limite_record:
            if limite_record.ctOMDb == 1000:
                return "MaximRequest"
            else:
                # If a record exists for today, update ctOMDb and leave ctOpenIA unchanged
                limite_record.ctOMDb += 1
        else:
            # If no record exists for today, create a new one with ctOpenIA=0 and ctOMDb=1
            new_record = Limite(fecha=today, ctOpenIA=0, ctOMDb=1)
            session.add(new_record)
        
        # Commit the transaction
        session.commit()
    except Exception as e:
        print(f"Error película: {e}")
        # Rollback in case of any error
        session.rollback()
        raise e
    finally:
        # Close the session
        session.close()
    return None

def insert_movie_into_db(session: Session, movie_data):
    movie = Movie(
        tmdb_id=movie_data["tmdb_id"],
        original_title=movie_data["original_title"],
        overview=movie_data["overview"],
        poster=movie_data["poster"],
        imdb_id=movie_data["imdb_id"],
        vote_average=movie_data["vote_average"]
    )
    session.add(movie)
    session.commit()

def get_and_insert_movie_details(tmdb_id: str, session: Session):
    tmdb_data = get_tmdb_movie_details(tmdb_id)
    print(f"API TMDB película: {tmdb_data}")
    omdb_data = get_omdb_movie_details(tmdb_data["imdb_id"])
    print(f"API OMDb película: {omdb_data}")
    
    if tmdb_data and omdb_data:
        movie_data = {
            "tmdb_id": tmdb_data["id"],
            "original_title": tmdb_data["original_title"],
            "overview": tmdb_data["overview"],
            "poster": omdb_data["Poster"],
            "imdb_id": tmdb_data["imdb_id"],
            "vote_average": tmdb_data["vote_average"]
        }
        
        insert_movie_into_db(session, movie_data)
        
        return movie_data
    
    return None


def process_movies_with_high_popularity(session: Session):

    json_file_path = "./movie_ids_05_15_2024.json"
    # Cargar el archivo JSON
    with open(json_file_path, "r", encoding="utf-8") as file:
        movies_data = json.load(file)
    
    # Filtrar películas con popularidad > 20000
    movies_to_process = [movie for movie in movies_data if movie.get("popularity", 0) > 20000]
    
    # Procesar cada película filtrada
    iter = 1;
    for movie in movies_to_process:
        if iter == 40:
            iter = 0
            time.sleep(1)
        else:
            iter += 1
        tmdb_id = str(movie.get("id"))
        original_title = str(movie.get("original_title"))
        max = update_or_insert_limite(session)
        if max:
            break
        else:
            # Llamar a get_movie_details para obtener y almacenar los detalles en la base de datos
            movie_data_last = get_and_insert_movie_details(tmdb_id, session)
            for movie in movies_data:
                if movie['tmdb_id'] == movie_data_last['tmdb_id']:
                    movie['popularity'] = 0
                    break
            if movie_data_last:
                print(f"Procesada película: {movie_data_last['original_title']}")
            else:
                print(f"No se pudo procesar película con TMDB ID: {tmdb_id} y nombre: {original_title}")
    
    with open(json_file_path, 'w') as file:
        json.dump(movies_data, file, indent=4)

