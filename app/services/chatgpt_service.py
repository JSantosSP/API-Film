import openai
from app.config import CHATGPT_API_KEY

openai.api_key = CHATGPT_API_KEY

async def ask_chatgpt(question: str, movies_i_like: list, movies_i_havent_seen: list):
    prompt = f"Movies I like: {', '.join(movies_i_like)}\nMovies I haven't seen: {', '.join(movies_i_havent_seen)}\n\n{question}"

    response = openai.TextEmbeddings.create(
        model="text-embedding-3-large",
        inputs=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=64
    )

    return response['outputs'][0]['embeddings']
