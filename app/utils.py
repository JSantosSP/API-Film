import requests
import os
import json
import time
from app.models import Movie
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


def insert_movie_into_json(movie_data):
    filename = 'movies_data.json'
    
    # Verificar si el archivo existe
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)  # Inicializar el archivo con una lista vacía si no existe
    
    # Cargar los datos actuales del archivo
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Agregar el nuevo objeto movie_data a la lista de objetos
    data.append(movie_data)
    
    # Escribir los datos actualizados de vuelta al archivo
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)  # Escribir los datos con formato JSON indentado

def get_and_insert_movie_details(tmdb_id: str):
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
        
        insert_movie_into_json(movie_data)
        
        return movie_data
    
    return None


def process_movies_with_high_popularity():

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
        if max >= (1000):
            break
        else:
            print("antes de get_and_insert")
            # Llamar a get_movie_details para obtener y almacenar los detalles en la base de datos
            movie_data_last = get_and_insert_movie_details(tmdb_id)
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
    return max

def process_list(movies_list):
    filename = 'movies_data.json'
    
    # Verificar si el archivo existe
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)  # Inicializar el archivo con una lista vacía si no existe
    
    # Cargar los datos actuales del archivo
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Agregar los nuevos datos a la lista existente
    data.extend(movies_list)
    
    # Escribir los datos actualizados de vuelta al archivo
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)  # Escribir los datos con formato JSON indentado



