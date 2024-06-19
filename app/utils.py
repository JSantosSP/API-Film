import requests
import os
import json
import time
from sqlalchemy.orm import Session
from app.models import Movie, Limite
from datetime import date
from app.config import TMDB_API_KEY, OMDB_API_KEY

def get_tmdb_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        print("tmdb ok")
        return response.json()
    return None

def get_omdb_movie_details(imdb_id, type):
    url = f"http://www.omdbapi.com/?{type}={imdb_id}&apikey={OMDB_API_KEY}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        print("omdb ok")
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
        poster=movie_data["Poster"],
        imdb_id=movie_data["imdb_id"],
        vote_average=movie_data["vote_average"],
        genero=movie_data["genero"]
    )
    session.add(movie)
    session.commit()

def insert_movie_into_datos_json(movie_data):
    movie_new = {
        "tmdb_id":movie_data["tmdb_id"],
        "original_title":movie_data["original_title"],
        "overview":movie_data["overview"],
        "poster":movie_data["Poster"],
        "imdb_id":movie_data["imdb_id"],
        "vote_average":movie_data["vote_average"],
        "genero":movie_data["genero"]
    }

    json_file_path = os.path.join(os.path.dirname(__file__), 'db/datos.json')
    print(json_file_path)
    
    movies_data = []
    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                movie = json.loads(line.strip())
                movies_data.append(movie)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")

    # Añadir el nuevo objeto
    movies_data.append(movie_new)

    # Escribir de vuelta al archivo, cada objeto en una línea separada
    with open(json_file_path, 'w', encoding='utf-8') as file:
        for movie in movies_data:
            file.write(json.dumps(movie) + '\n')

def get_and_insert_movie_details(tmdb_id: str, session: Session):
    tmdb_data = get_tmdb_movie_details(tmdb_id)
    print(f"API TMDB película: {tmdb_data['imdb_id']}")
    if tmdb_data['imdb_id'] == "":
        get_omdb_movie_details(tmdb_data["original_title"],"t")
    else:
        omdb_data = get_omdb_movie_details(tmdb_data["imdb_id"],"i")
    print(f"API OMDb película: {omdb_data['Poster']}")
    
    if tmdb_data and omdb_data:
        genres_concatenated = "; ".join([genres["name"] for genres in tmdb_data["genres"]])
        movie_data = {
            "tmdb_id": tmdb_data["id"],
            "original_title": tmdb_data["original_title"],
            "overview": tmdb_data["overview"],
            "Poster": omdb_data["Poster"],
            "imdb_id": tmdb_data["imdb_id"],
            "vote_average": tmdb_data["vote_average"],
            "genero":genres_concatenated
        }
        
        insert_movie_into_db(session, movie_data)
        
        return movie_data
    
    return None


def process_movies_with_high_popularity(session: Session):

    json_file_path = os.path.join(os.path.dirname(__file__), 'movie_ids_05_15_2024.json')
    
    # Cargar el archivo JSON
    movies_data = []

    # Leer el archivo línea por línea
    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Decodificar cada línea como un objeto JSON
                movie = json.loads(line)
                movies_data.append(movie)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line}. Error: {e}")
    # Filtrar películas con popularidad > 6
    movies_to_process = [movie for movie in movies_data if movie.get("popularity", 0) > 6]
    # Procesar cada película filtrada
    iter = 1;
    max = 1;
    for movie in movies_to_process:
        if iter == 40:
            iter = 0
            time.sleep(1)
        else:
            iter += 1
        tmdb_id = str(movie.get("id"))
        original_title = str(movie.get("original_title"))
        max += 1
        if max >= (1000-428):
            print(max)
            break
        else:
            print("antes de get_and_insert")
            # Llamar a get_movie_details para obtener y almacenar los detalles en la base de datos
            movie_data_last = get_and_insert_movie_details(tmdb_id, session)
            for movie in movies_data:
                if movie['id'] == movie_data_last['tmdb_id']:
                    movie['popularity'] = 0
                    break
            if movie_data_last:
                print(f"Procesada película: {movie_data_last['original_title']}")
            else:
                print(f"No se pudo procesar película con TMDB ID: {tmdb_id} y nombre: {original_title}")
    with open(json_file_path, 'w', encoding='utf-8') as file:
        for movie in movies_data:
            file.write(json.dumps(movie) + '\n')

