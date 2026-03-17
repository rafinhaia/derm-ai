import json

caminho = "data/database/consultas.json"

with open(caminho, "r", encoding="utf-8") as f:
    consultas = json.load(f)

total = len(consultas)

biopsias = 0
lesoes_nasal = 0
cbc_suspeita = 0

for c in consultas:

    if isinstance(c, dict):

        procedimento = str(c.get("procedimento", "")).lower()
        localizacao = str(c.get("localizacao", "")).lower()
        diagnostico = str(c.get("diagnostico_provavel", "")).lower()

        if "biópsia" in procedimento:
            biopsias += 1

        if "nasal" in localizacao:
            lesoes_nasal += 1

        if "basocelular" in diagnostico:
            cbc_suspeita += 1


print("\n===== ESTATÍSTICAS DO BANCO DERMATOLÓGICO =====\n")

print("Total de consultas:", total)
print("Biópsias realizadas:", biopsias)
print("Lesões em região nasal:", lesoes_nasal)
print("Suspeitas de carcinoma basocelular:", cbc_suspeita)

print("\n===============================================\n")