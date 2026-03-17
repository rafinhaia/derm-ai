from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

transcricao = """
O paciente Bruno Alves realizou hoje uma consulta e ele também fez uma biópsia incisional na região de raiz nasal.
"""

prompt = f"""
Você é um dermatologista especialista.

Transforme a consulta abaixo em um prontuário médico estruturado contendo:

- Identificação
- Procedimento realizado
- Localização da lesão
- Descrição do procedimento
- Plano / orientações

Consulta:
{transcricao}
"""

response = client.responses.create(
    model="gpt-4.1",
    input=prompt
)

print("\nPRONTUÁRIO GERADO:\n")
print(response.output_text)