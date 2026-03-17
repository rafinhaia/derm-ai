from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extrair_dados(texto):

    prompt = f"""
Extraia os dados clínicos da consulta abaixo.

Retorne SOMENTE JSON válido.

Campos obrigatórios:

nome
queixa_principal
procedimento
localizacao
diagnostico_provavel

Consulta:
{texto}

Exemplo de saída:

{{
 "nome": "...",
 "queixa_principal": "...",
 "procedimento": "...",
 "localizacao": "...",
 "diagnostico_provavel": "..."
}}
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text