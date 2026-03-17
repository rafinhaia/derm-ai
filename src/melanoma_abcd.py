import cv2
import numpy as np


def analisar_abcd(image_path):

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    _, thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    c = max(contours,key=cv2.contourArea)

    area = cv2.contourArea(c)

    perimeter = cv2.arcLength(c,True)

    # -------------------------
    # A — ASSIMETRIA
    # -------------------------

    x,y,w,h = cv2.boundingRect(c)

    roi = gray[y:y+h,x:x+w]

    flipped = cv2.flip(roi,1)

    diff = cv2.absdiff(roi,flipped)

    assimetria = np.mean(diff)

    # -------------------------
    # B — BORDAS
    # -------------------------

    circularidade = (4*np.pi*area)/(perimeter*perimeter)

    irregularidade_borda = 1 - circularidade

    # -------------------------
    # C — CORES
    # -------------------------

    roi_color = img[y:y+h,x:x+w]

    cores = np.std(roi_color)

    # -------------------------
    # D — DIÂMETRO
    # -------------------------

    (_, _), radius = cv2.minEnclosingCircle(c)

    diametro = radius*2

    # -------------------------
    # SCORE SIMPLES
    # -------------------------

    score = 0

    if assimetria > 20:
        score += 1

    if irregularidade_borda > 0.3:
        score += 1

    if cores > 40:
        score += 1

    if diametro > 80:
        score += 1

    # -------------------------
    # CLASSIFICAÇÃO
    # -------------------------

    if score <= 1:
        risco = "baixo"

    elif score == 2:
        risco = "moderado"

    else:
        risco = "alto"

    return {
        "assimetria": round(float(assimetria),2),
        "irregularidade_borda": round(float(irregularidade_borda),2),
        "variacao_cor": round(float(cores),2),
        "diametro_pixels": round(float(diametro),2),
        "score": score,
        "risco": risco
    }