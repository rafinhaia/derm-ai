import json

def salvar_consulta(dados):

    caminho = "data/database/consultas.json"

    # carregar banco atual
    with open(caminho, "r", encoding="utf-8") as f:
        banco = json.load(f)

    # converter string JSON para objeto
    try:
        consulta = json.loads(dados)
    except:
        consulta = {"raw": dados}

    banco.append(consulta)

    # salvar novamente
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(banco, f, indent=2, ensure_ascii=False)