import cv2
import numpy as np


def analisar_multiplas_lesoes(img_path):

    img = cv2.imread(img_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    resultados = []

    contador = 1

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 500:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        lesao = img[y:y + h, x:x + w]

        # Assimetria
        esquerda = lesao[:, :w // 2]
        direita = cv2.flip(lesao[:, w // 2:], 1)

        if esquerda.shape == direita.shape:
            assimetria = np.mean(
                cv2.absdiff(esquerda, direita)
            )
        else:
            assimetria = 0

        # Bordas
        perimetro = cv2.arcLength(cnt, True)

        circularidade = (4 * np.pi * area) / (perimetro ** 2) if perimetro != 0 else 0

        irregularidade_borda = 1 - circularidade

        # Cores
        cor = np.std(lesao)

        # Score simples
        score = (assimetria * 0.4) + (irregularidade_borda * 100 * 0.3) + (cor * 0.3)

        if score > 60:
            risco = "alto"
        elif score > 30:
            risco = "moderado"
        else:
            risco = "baixo"

        resultados.append({
            "lesao": contador,
            "assimetria": float(assimetria),
            "borda": float(irregularidade_borda),
            "cor": float(cor),
            "score": float(score),
            "risco": risco
        })

        # desenhar caixa
        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

        # escrever número da lesão
        cv2.putText(
            img,
            f"L{contador}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        contador += 1

    return img, resultados