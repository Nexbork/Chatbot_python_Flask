import cv2
import numpy as np
import os

def contar_fichas_por_fila():
    img_path = os.path.join("static", "images","demo2.jpg")
    imagen = cv2.imread(img_path)

    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar un suavizado para reducir el ruido
    imagen_suavizada = cv2.medianBlur(imagen_gris, 5)

    # Aplicar la transformada de Hough para detectar círculos
    circulos = cv2.HoughCircles(
        imagen_suavizada,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=13,
        maxRadius=40,
    )

    circulos = np.uint16(np.around(circulos))

    # Ordenar los círculos por coordenada y
    circulos = sorted(circulos[0, :], key=lambda x: x[1])

    # Inicializar variables para rastrear la fila actual y la cantidad de fichas por fila
    fila_actual = circulos[0][1]
    fichas_por_fila = 0
    filas_detectadas = 0

    # Crear una copia de la imagen original para dibujar círculos
    imagen_resultante = imagen.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for circulo in circulos:
        x, y = circulo[0], circulo[1]

        # Verificar si el círculo pertenece a la misma fila
        if abs(y - fila_actual) < 10:
            fichas_por_fila += 1
            cv2.circle(imagen_resultante, (x, y), circulo[2], (0, 255, 0), 0)
        else:
            # Imprimir la cantidad de fichas para la fila actual y reiniciar para la nueva fila
            cv2.putText(
                imagen_resultante,
                f"{fichas_por_fila} fichas",
                (x + 30, fila_actual),
                font,
                0.5,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )
            fila_actual = y
            fichas_por_fila = 1
            filas_detectadas += 1

    # Imprimir la cantidad de fichas para la última fila
    cv2.putText(
        imagen_resultante,
        f"{fichas_por_fila} fichas",
        (x + 30, fila_actual),
        font,
        0.5,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    filas_detectadas += 1

    # Verificacion de filas
    print(f"Se detectaron {filas_detectadas} filas.")

    save_path = "static/images/temp/column_res.jpg"
    d = cv2.imwrite(save_path, imagen_resultante)

    name ='Filas'

    result = {'ruta_img':save_path, 'nombre':name, 'filas_detectadas':filas_detectadas}
    return result
