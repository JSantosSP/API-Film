import httpx
from app.config import OMDB_API_KEY

async def get_omdb_movie_details(movie_title: str):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
