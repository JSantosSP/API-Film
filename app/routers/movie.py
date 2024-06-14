from fastapi import APIRouter, HTTPException
from app.services.tmdb_service import get_tmdb_movie_details
from app.services.omdb_service import get_omdb_movie_details
from app.services.chatgpt_service import ask_chatgpt
from app.schemas import Movie

router = APIRouter()

@router.get("/movie/{movie_id}", response_model=Movie)
async def get_movie_details(movie_id: str):
    tmdb_data = await get_tmdb_movie_details(movie_id)
    if "status_code" in tmdb_data and tmdb_data["status_code"] == 34:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    omdb_data = await get_omdb_movie_details(tmdb_data["title"])
    
    combined_data = {
        "title": tmdb_data["title"],
        "overview": tmdb_data["overview"]
    }
    
    return combined_data

@router.post("/ask")
async def ask_question(question: str):
    answer = await ask_chatgpt(question)
    return {"answer": answer}
