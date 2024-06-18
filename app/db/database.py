import json
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from app.utils import process_movies_with_high_popularity  # Asegúrate de importar la función correctamente

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Inicializar la sesión de SQLAlchemy
    session = SessionLocal()
    
    try:
        # Llamar a la función para procesar películas con popularidad alta
        process_movies_with_high_popularity(session)
    finally:
        # Cerrar la sesión de SQLAlchemy al finalizar
        session.close()
        print("finalizado")