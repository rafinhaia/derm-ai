from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def sugerir_perguntas(texto):

    prompt = f"""
Você é um dermatologista especialista.

Com base na consulta abaixo, sugira perguntas clínicas importantes
que o médico deveria fazer para completar a avaliação.

Consulta:
{texto}
"""

    r = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return r.output_text