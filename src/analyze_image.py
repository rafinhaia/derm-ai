from image_analysis import analisar_imagem
import sys

if len(sys.argv) < 2:
    print("Uso: python src/analyze_image.py caminho_da_imagem")
    exit()

imagem = sys.argv[1]

print("\nAnalisando imagem dermatológica...\n")

resultado = analisar_imagem(imagem)

print(resultado)