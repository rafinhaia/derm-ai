from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisar_consulta(texto):

    prompt = f"""
Você é um dermatologista especialista.

Analise a consulta abaixo e gere:

1. Prontuário dermatológico estruturado
2. Diagnóstico provável
3. Diagnósticos diferenciais
4. Sugestão de exames complementares
5. Conduta terapêutica inicial baseada em evidências

Consulta:
{texto}
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text