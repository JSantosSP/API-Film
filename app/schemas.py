from pydantic import BaseModel

class MovieBase(BaseModel):
    tmdb_id: str
    original_title: str
    overview: str
    poster: str
    imdb_id: str
    vote_average: float
    genero: str

class MovieRequest(BaseModel):
    movies_i_like: list[str]
    movies_i_dont_like: list[str]

class AddFilm(BaseModel):
    passw: str