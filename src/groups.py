import cv2
import numpy as np
import os

def contar_fichas_por_grupo():
    img_path = os.path.join("static", "images","demo2.jpg")
    img = cv2.imread(img_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
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

    total_fichas_arriba = 0
    total_fichas_abajo = 0

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]

            # Determinar fila (arriba o abajo)
            fila = ""
            if center[1] < img.shape[0] / 2:
                fila = "Arriba"
                total_fichas_arriba += 1
                color_contorno = (255, 0, 0)
            else:
                fila = "Abajo"
                total_fichas_abajo += 1
                color_contorno = (0, 0, 255)

            cv2.circle(img, center, radius, color_contorno, 2)
            # Mostrar la fila en la que se encuentra la ficha
            cv2.putText(
                img,
                fila,
                (center[0], center[1] - radius - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

    print("Total de fichas arriba:", total_fichas_arriba)
    print("Total de fichas abajo:", total_fichas_abajo)

    save_path = "static/images/temp/group_res.jpg"
    d = cv2.imwrite(save_path, img)
    name ='Grupos'

    result = {'ruta_img':save_path, 'nombre':name, 'total_fichas_arriba':total_fichas_arriba, 'total_fichas_abajo':total_fichas_abajo}
    return result

