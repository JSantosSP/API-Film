import openai
from app.config import CHATGPT_API_KEY

openai.api_key = CHATGPT_API_KEY

async def ask_chatgpt(question: str):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()

