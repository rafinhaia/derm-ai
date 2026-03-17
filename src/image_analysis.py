from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisar_imagem(caminho_imagem):

    prompt = """
Você é um dermatologista especialista.

Analise a imagem dermatológica e forneça:

1. Descrição clínica da lesão
2. Diagnóstico provável
3. Diagnósticos diferenciais
4. Conduta sugerida
"""

    with open(caminho_imagem, "rb") as f:
        img = f.read()

    base64_image = base64.b64encode(img).decode("utf-8")

    image_url = f"data:image/jpeg;base64,{base64_image}"

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": image_url
                    }
                ]
            }
        ]
    )

    return response.output_text