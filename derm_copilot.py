from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("\nTranscrevendo áudio da consulta...\n")

audio_file = open("consulta.m4a", "rb")

transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

texto_consulta = transcript.text

print("Transcrição:")
print(texto_consulta)

print("\nGerando prontuário...\n")

prompt = f"""
Você é um dermatologista especialista.

Transforme a consulta abaixo em um prontuário médico estruturado.

Inclua:

- Identificação
- Queixa principal
- História clínica
- Procedimento realizado
- Localização da lesão
- Plano terapêutico

Consulta:
{texto_consulta}
"""

response = client.responses.create(
    model="gpt-4.1",
    input=prompt
)

print("\nPRONTUÁRIO GERADO:\n")
print(response.output_text)