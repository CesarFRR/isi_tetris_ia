import cv2
import numpy as np

def obtener_rango_colores(imagen):
  """
  Obtiene el rango de colores en una imagen, exceptuando el color blanco, negro y colores desaturados.

  Parámetros:
    imagen: La imagen a analizar.

  Retorno:
    Una lista con los valores mínimo y máximo de cada canal de color (BGR).
  """

  # Convertir la imagen a espacio de color HSV
  imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

  # Definir los rangos para blanco, negro y colores desaturados
  blanco_min = np.array([0, 0, 220], np.uint8)
  blanco_max = np.array([255, 255, 255], np.uint8)
  negro_min = np.array([0, 0, 0], np.uint8)
  negro_max = np.array([180, 255, 80], np.uint8)
  desaturado_min = np.array([0, 0, 0], np.uint8)
  desaturado_max = np.array([180, 25, 255], np.uint8)

  # Crear una máscara para los píxeles que no son blanco, negro ni desaturados
  mascara = cv2.inRange(imagen_hsv, blanco_min, blanco_max) + cv2.inRange(imagen_hsv, negro_min, negro_max) + cv2.inRange(imagen_hsv, desaturado_min, desaturado_max)

  # Obtener los valores mínimo y máximo de cada canal de color en la máscara
  min_valores = [cv2.minMaxLoc(canal, mask=mascara)[0] for canal in cv2.split(imagen_hsv)]
  max_valores = [cv2.minMaxLoc(canal, mask=mascara)[1] for canal in cv2.split(imagen_hsv)]

  # Retornar el rango de colores
  return [min_valores, max_valores]


# Ejemplo de uso
imagen = cv2.imread("morado.jpg")
rango_colores = obtener_rango_colores(imagen)
print(f"Rango de colores: {rango_colores}")


# Tus rangos de colores
min_valores = rango_colores[0]
max_valores = rango_colores[1]

# Crear una imagen vacía para la paleta
paleta = np.zeros((50, 300, 3), dtype=np.uint8)

# Rellenar la paleta con los colores del rango
for i in range(50):
    for j in range(300):
        # Calcular el valor de cada canal de color
        h = min_valores[0] + (max_valores[0] - min_valores[0]) * j / 300
        s = min_valores[1] + (max_valores[1] - min_valores[1]) * i / 50
        v = min_valores[2] + (max_valores[2] - min_valores[2]) * i / 50
        # Asignar el color a la paleta
        paleta[i, j] = [h, s, v]

# Convertir la paleta de HSV a BGR
paleta = cv2.cvtColor(paleta, cv2.COLOR_HSV2BGR)

# Mostrar la paleta
cv2.imshow('Paleta de colores', paleta)
cv2.waitKey(0)
cv2.destroyAllWindows()