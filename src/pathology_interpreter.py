from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def interpretar_laudo(laudo):

    prompt = f"""
Você é dermatologista.

Interprete o laudo anatomopatológico abaixo.

Explique:

- diagnóstico
- significado clínico
- conduta recomendada
- necessidade de cirurgia

Laudo:
{laudo}
"""

    r = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return r.output_text