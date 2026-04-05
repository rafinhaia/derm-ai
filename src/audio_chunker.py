import os

MAX_SIZE_MB = 20


def dividir_audio(caminho_audio):
    tamanho_bytes = os.path.getsize(caminho_audio)
    tamanho_mb = tamanho_bytes / (1024 * 1024)

    # 👇 se for pequeno → normal
    if tamanho_mb <= MAX_SIZE_MB:
        return [caminho_audio]

    # 👇 se for grande → NÃO divide ainda (evita FFmpeg)
    return [caminho_audio]


def transcrever_audio_grande(caminho_audio, transcrever_func, progress_bar=None):

    partes = dividir_audio(caminho_audio)

    texto_final = ""

    total = len(partes)

    for i, parte in enumerate(partes):
        texto = transcrever_func(parte)
        texto_final += "\n" + texto

        if progress_bar:
            progress_bar.progress((i + 1) / total)

    return texto_final.strip()