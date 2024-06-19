from fastapi import APIRouter, HTTPException
from app.db.database import get_movie_details
from app.services.chatgpt_service import ask_chatgpt
from app.schemas import MovieRequest

router = APIRouter()



@router.get("/movies/{movie_id}")
async def get_movie_info(movie_id: str):
    movie = get_movie_details(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/ask")
async def ask_question(moviesReq: MovieRequest):
    movies_i_like = moviesReq.movies_i_like
    movies_i_dont_like = moviesReq.movies_i_dont_like
    recommendations = await ask_chatgpt(movies_i_like, movies_i_dont_like)
    print(recommendations)
    return {"answer": recommendations}
