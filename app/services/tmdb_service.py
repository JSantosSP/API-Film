import httpx
from app.config import TMDB_API_KEY

async def get_tmdb_movie_details(movie_id: str):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
