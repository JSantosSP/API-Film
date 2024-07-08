from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import movie


app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movie.router)

 
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API"}




