from pydantic import BaseModel

class MovieBase(BaseModel):
    tmdb_id: str
    original_title: str
    overview: str
    poster: str
    imdb_id: str
    vote_average: float
    genero: str