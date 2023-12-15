import cv2
import numpy as np
import os


# Función para contar fichas por color, fila y grupo
def contar_fichas_por_color():

    img_path = os.path.join("static", "images","demo2.jpg")
    img = cv2.imread(img_path)

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un suavizado para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detección de círculos utilizando la transformada de Hough
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=17,
        maxRadius=40,
    )

    # Contadores de fichas negras y blancas
    total_fichas_negras = 0
    total_fichas_blancas = 0

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            center = (i[0], i[1])

            # Extraer la región de interés (ROI) alrededor del círculo
            radius = i[2]
            roi = img[
                center[1] - radius : center[1] + radius,
                center[0] - radius : center[0] + radius,
            ]

            # Calcular el promedio de color en la ROI
            promedio_color = np.mean(roi, axis=(0, 1))

            # Determinar si el promedio de color indica una ficha negra o blanca
            if (
                np.mean(promedio_color) < 100
            ):  # Puedes ajustar este umbral según tus necesidades
                total_fichas_negras += 1
                color_contorno = (0, 0, 255)  # Rojo para fichas negras
            else:
                total_fichas_blancas += 1
                color_contorno = (255, 0, 0)  # Azul para fichas blancas

            # Dibujar el círculo y el color correspondiente en la imagen original
            cv2.circle(img, center, radius, color_contorno, 2)

    save_path = "static/images/temp/color_res.jpg"
    d = cv2.imwrite(save_path, img)
    print(d)

    name ='Colores'

    # Imprimir el total de fichas detectadas
    print("Total de fichas negras:", total_fichas_negras)
    print("Total de fichas blancas:", total_fichas_blancas)

    result = {'ruta_img':save_path, 'nombre':name, 'total_fichas_blancas':total_fichas_blancas, 'total_fichas_negras':total_fichas_negras}

    return result