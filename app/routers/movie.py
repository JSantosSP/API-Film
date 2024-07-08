from fastapi import APIRouter, HTTPException
from app.db.database import get_movie_details, addFilm
from app.schemas import MovieRequest, AddFilm

router = APIRouter()



@router.get("/movies")
async def get_movie_info():
    movie = get_movie_details()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/ask")
async def ask_question(moviesReq: MovieRequest):
    
    return {"answer": None}

@router.post("/addFilm")
async def ask_question(addFilmReq: AddFilm):
    if addFilmReq.passw == "1945":
        nfilms = addFilm()
    else:
        raise HTTPException(status_code=401, detail="Forbbiden")
    return {"addfilms": nfilms}
