import numpy as np
import cv2
from Classifier import Classifier
import cv2

class Framer:
    def __init__(self, imagenUrl = None):
        self.last_bordes_centrales = None
        self.last_next = None
        self.last_hold = None
        self.imagen = imagenUrl
        if imagenUrl is not None:
            self.imagen = cv2.imread(imagenUrl)

    def encontrar_bordes_centrales(self, imagen = None):
        if imagen is None:
            imagen = self.imagen
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)
        umbral = cv2.threshold(desenfoque, 127, 255, cv2.THRESH_BINARY)[1]
        contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        area_max = 0
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > area_max:
                area_max = area
                contorno_max = contorno

        x, y, w, h = cv2.boundingRect(contorno_max)
        self.last_bordes_centrales = [y, y + h, x, x + w]

        return self.last_bordes_centrales

    def obtener_next(self, bordes, imagen = None):
        if imagen is None:
            imagen = self.imagen
        h = bordes[1] - bordes[0]
        w = bordes[3] - bordes[2]
        borde_superior_next = bordes[0] + int(0.05 * h)
        borde_inferior_next = bordes[1] - int(0.2* h)
        borde_izquierdo_next = bordes[2] + int(0.77 * w)
        borde_derecho_next = bordes[3] - int(0.01 * w)

        self.last_next = [
            borde_superior_next,
            borde_inferior_next,
            borde_izquierdo_next,
            borde_derecho_next,
        ]

        return self.last_next

    def obtener_hold(self, bordes, imagen = None):
        if imagen is None:
            imagen = self.imagen
        h = bordes[1] - bordes[0]
        w = bordes[3] - bordes[2]
        borde_superior_hold = bordes[0] + int(0.05 * h)
        borde_inferior_hold = bordes[0] + int(0.18 * h)
        borde_izquierdo_hold = bordes[2] + int(0.02 * w)
        borde_derecho_hold = bordes[2] + int(0.22 * w)

        self.last_hold = [
            borde_superior_hold,
            borde_inferior_hold,
            borde_izquierdo_hold,
            borde_derecho_hold,
        ]

        return self.last_hold

# Ejemplo de uso
fr = Framer()
imagen = cv2.imread("./tests/tetris_full2.jpg")
bordes_central = fr.encontrar_bordes_centrales(imagen)

# Guardar la imagen recortada
# cv2.imwrite("imagen_tetris_recortada.jpg", imagen_recortada)
print(f"Bordes central: {bordes_central}")
cv2.imshow(
    "Imagen recortada",
    imagen[
        bordes_central[0] : bordes_central[1], bordes_central[2] : bordes_central[3]
    ],
)
cv2.waitKey(0)

# Ejemplo de uso
coordenadas_next = fr.obtener_next(bordes_central)

next_img = imagen[
    coordenadas_next[0] : coordenadas_next[1], coordenadas_next[2] : coordenadas_next[3]
]


cv2.imshow("Imagen Next_0", next_img)
cv2.waitKey(0)
cls = Classifier()

for i in range(1, 6):

    print(f"Coordenadas del Next: {coordenadas_next}")
    imagen_next = imagen[
        coordenadas_next[0]
        + int(
            (coordenadas_next[1] - coordenadas_next[0]) * ((i - 1) / 5)
        ) : coordenadas_next[0]
        + int((coordenadas_next[1] - coordenadas_next[0]) * (i / 5)),
        coordenadas_next[2] : coordenadas_next[3],
    ]

    # Calcula las coordenadas del centro de la imagen
    centro_y, centro_x = imagen_next.shape[0] // 2, imagen_next.shape[1] // 2

    # Pone un pixel blanco en el centro de la imagen
    print(f"color centro: {imagen_next[centro_y, centro_x]}")
    imagen_next[centro_y, centro_x] = [255, 255, 255]
    print(f"precedir color lego: ", cls.predict_piece(imagen_next))
    cv2.imshow("Imagen Next", imagen_next)
    cv2.waitKey(0)



# Ejemplo de uso

coordenadas_hold = fr.obtener_hold(bordes_central)
print(f"Coordenadas del Hold: {coordenadas_hold}")
imagen_hold = imagen[coordenadas_hold[0]:coordenadas_hold[1],
                             coordenadas_hold[2]:coordenadas_hold[3]]
cv2.imshow("Imagen Hold", imagen_hold)
cv2.waitKey(0)
