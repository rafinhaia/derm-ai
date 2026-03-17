import cv2
import numpy as np

def detectar_lesao(caminho):

    img = cv2.imread(caminho)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    _,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        c = max(contours,key=cv2.contourArea)

        (x,y),radius = cv2.minEnclosingCircle(c)

        center = (int(x),int(y))

        radius = int(radius)

        cv2.circle(img,center,radius,(0,0,255),2)

        diametro_pixels = radius*2

        return img,diametro_pixels

    return img,None