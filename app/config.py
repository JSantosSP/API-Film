import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
