import openai
from app.config import CHATGPT_API_KEY
from app.db.database import get_movie_info

openai.api_key = CHATGPT_API_KEY

async def ask_chatgpt(movies_i_like: list, movies_i_dont_like: list):
    prompt = (
        f"He visto las siguientes películas. Estas me han gustado:\n\n"
    )
       
    for movie in movies_i_like:
        info = get_movie_info(movie)  
        prompt += f"{info}\n\n"


    prompt += (
        f"Estas NO me han gustado:\n\n"
    )
        
    for movie in movies_i_dont_like:
        info = get_movie_info(movie)  
        prompt += f"{info}\n\n"
    
    prompt += (
        "¿Me puedes recomendar 6 películas que podrían gustarme basándote en mis gustos?"
    )

    prompt = "¿Recomiendas 6 películas?"
    
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150
    )

    # Extraer y devolver las películas recomendadas
    recommended_movies = response.choices[0].text.strip().split('\n')
    return [movie.strip() for movie in recommended_movies if movie.strip()]
