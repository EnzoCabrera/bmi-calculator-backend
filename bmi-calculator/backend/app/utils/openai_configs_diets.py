from openai import OpenAI
from app.api.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_diets_with_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um nutricionista."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
