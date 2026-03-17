from openai import OpenAI

client = OpenAI()

def gerar_laudo_paciente(texto_consulta, prontuario):

    prompt = f"""
Você é um médico dermatologista elaborando um LAUDO MÉDICO FORMAL para ser entregue ao paciente.

O laudo deve ser escrito em LINGUAGEM MÉDICA FORMAL e em TEXTO CORRIDO (parágrafos contínuos).

O documento deve conter:

- identificação do paciente (se disponível)
- descrição clínica da condição dermatológica
- diagnóstico provável
- CID-10 correspondente
- possíveis limitações relacionadas à doença
- orientações médicas importantes
- recomendações de cuidados
- necessidade de acompanhamento ou tratamento
- possibilidade de apresentação em trabalho ou instituição se necessário

Evite listas ou tópicos.  
Escreva em parágrafos contínuos como em um documento médico oficial.

História clínica da consulta:

{texto_consulta}

Prontuário médico gerado:

{prontuario}
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text