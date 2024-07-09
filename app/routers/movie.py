from fastapi import APIRouter, HTTPException
from app.db.database import get_movie_details, addFilm, get_movies_by_word_and_genres
from app.schemas import MovieRequest, AddFilm

router = APIRouter()



@router.get("/movies")
async def get_movie_info():
    movie = get_movie_details()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/moviesList")
async def randomList(moviesReq: MovieRequest):
    movie = moviesReq.movie
    moviesList = get_movies_by_word_and_genres(movie)
    return moviesList

@router.post("/addFilm")
async def ask_question(addFilmReq: AddFilm):
    if addFilmReq.passw == "1945":
        nfilms = addFilm()
    else:
        raise HTTPException(status_code=401, detail="Forbbiden")
    return {"addfilms": nfilms}
