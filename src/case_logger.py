import json
import os
from datetime import datetime

def salvar_caso(texto_consulta, analise_clinica, analise_imagem):

    pasta = "data/cases"
    os.makedirs(pasta, exist_ok=True)

    caso = {
        "data": datetime.now().isoformat(),
        "transcricao": texto_consulta,
        "analise_clinica": analise_clinica,
        "analise_imagem": analise_imagem
    }

    arquivo = os.path.join(pasta, "casos.json")

    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = []

    dados.append(caso)

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)