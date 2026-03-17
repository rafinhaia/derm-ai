from database import salvar_consulta
from transcriber import transcrever_audio
from clinical_ai import analisar_consulta
from structured_data import extrair_dados
import sys

# Verificar se o usuário passou um arquivo de áudio
if len(sys.argv) < 2:
    print("Uso: python src/main.py caminho_do_audio")
    print("Exemplo: python src/main.py data/audio/consulta.m4a")
    exit()

audio_path = sys.argv[1]

print("\nTranscrevendo consulta...\n")

# 1️⃣ Transcrição do áudio
texto = transcrever_audio(audio_path)

print("Transcrição:")
print(texto)

print("\nAnalisando consulta...\n")

# 2️⃣ Geração do prontuário clínico
resultado = analisar_consulta(texto)

print("\nRESULTADO:\n")
print(resultado)

# 3️⃣ Salvar prontuário em texto
with open("data/prontuarios/prontuario.txt", "w", encoding="utf-8") as f:
    f.write(resultado)

print("\nProntuário salvo em data/prontuarios/prontuario.txt")

print("\nExtraindo dados estruturados...\n")

# 4️⃣ Extrair dados estruturados
dados = extrair_dados(texto)
salvar_consulta(dados)
print("\nConsulta adicionada ao banco de dados")

print("Dados estruturados:")
print(dados)

# 5️⃣ Salvar dados estruturados
with open("data/prontuarios/dados_struct.json", "w", encoding="utf-8") as f:
    f.write(dados)

print("\nDados estruturados salvos em data/prontuarios/dados_struct.json")