from fastapi import FastAPI
from app.routers import movie
from app.db.database import init_db

app = FastAPI()

app.include_router(movie.router)

 
@app.get("/")
def read_root():
    init_db()
    return {"message": "Welcome to the Movie API"}

