from fastapi import FastAPI
from routers import movie
from db.database import init_db

app = FastAPI()

app.include_router(movie.router)

 
@app.get("/")
def read_root():
    init_db()
    return {"message": "Welcome to the Movie API"}

