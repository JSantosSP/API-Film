from fastapi import FastAPI
from app.routers import movie


app = FastAPI()

app.include_router(movie.router)

 
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API"}

