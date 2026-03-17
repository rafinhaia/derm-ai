from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_pedido_biopsia(texto):

    prompt = f"""
Você é dermatologista.

Com base na consulta abaixo gere um pedido de exame anatomopatológico.

Inclua:

- localização da lesão
- hipótese diagnóstica
- tipo de biópsia
- pergunta clínica ao patologista

Consulta:
{texto}
"""

    r = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return r.output_text