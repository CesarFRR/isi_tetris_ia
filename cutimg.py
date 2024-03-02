import numpy as np
import cv2

def recortar_elementos_centrales(imagen):
  """
  Recorta la imagen para obtener solo los elementos centrales del juego.

  Parámetros:
    imagen: La imagen a recortar.

  Retorno:
    La imagen recortada con los elementos centrales del juego.
  """

  # Convertir la imagen a formato NumPy
  img_np = np.array(imagen)

  # Encontrar los bordes del área que contiene los elementos centrales
  bordes = encontrar_bordes_centrales(img_np)
  for p in bordes:
      print(p, type(p))

  # Recortar la imagen usando los bordes encontrados
  imagen_recortada = img_np[bordes[0]:bordes[1], bordes[2]:bordes[3]]

  return imagen_recortada

def encontrar_bordes_centrales(imagen):
  """
  Encuentra los bordes del área que contiene los elementos centrales del juego.

  Parámetros:
    imagen: La imagen a analizar.

  Retorno:
    Una lista con los cuatro bordes: [borde superior, borde inferior, borde izquierdo, borde derecho].
  """

  # Convertir la imagen a escala de grises
  gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

  # Aplicar un filtro de desenfoque para eliminar ruido
  desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)

  # Binarizar la imagen para facilitar la búsqueda de bordes
  umbral = cv2.threshold(desenfoque, 127, 255, cv2.THRESH_BINARY)[1]

  # Encontrar los contornos de las figuras en la imagen
  contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Obtener el área del contorno más grande, que corresponde al área central del juego
  area_max = 0
  for contorno in contornos:
    area = cv2.contourArea(contorno)
    if area > area_max:
      area_max = area
      contorno_max = contorno

  # Obtener los bordes del contorno máximo
  x, y, w, h = cv2.boundingRect(contorno_max)

  # Ajustar los bordes para obtener un margen alrededor del área central
  borde_superior = y - int(0.1 * h)
  borde_inferior = y + h + int(0.1 * h)
  borde_izquierdo = x - int(0.1 * w)
  borde_derecho = x + w + int(0.1 * w)

  #return [borde_superior, borde_inferior, borde_izquierdo, borde_derecho]
  # Devolver las coordenadas del rectángulo delimitador asi nada más
  return [y, y + h, x, x + w]


def obtener_next(imagen_recortada):
    """
    Obtiene la imagen del Next a partir de una imagen recortada del juego.

    Parámetros:
        imagen_recortada: La imagen recortada que contiene el Next.

    Retorno:
        La imagen del Next.
    """

    # Definir la región de interés del Next
    borde_superior_next = 0
    borde_inferior_next = imagen_recortada.shape[0] - int(0.2 * imagen_recortada.shape[0])
    borde_izquierdo_next = int(0.75 * imagen_recortada.shape[1])
    borde_derecho_next = imagen_recortada.shape[1]

    # Recortar la imagen del Next
    imagen_next = imagen_recortada[borde_superior_next:borde_inferior_next, 
                                                                borde_izquierdo_next:borde_derecho_next]

    return imagen_next




def obtener_hold(imagen_recortada):
  """
  Obtiene la imagen del Hold a partir de una imagen recortada del juego.

  Parámetros:
    imagen_recortada: La imagen recortada que contiene el Hold.

  Retorno:
    La imagen del Hold.
  """

  # Definir la región de interés del Hold
  borde_superior_hold = 0
  borde_inferior_hold = int(0.2 * imagen_recortada.shape[0])
  borde_izquierdo_hold = 0
  borde_derecho_hold = int(0.25 * imagen_recortada.shape[1])

  # Recortar la imagen del Hold
  imagen_hold = imagen_recortada[borde_superior_hold:borde_inferior_hold, 
                                borde_izquierdo_hold:borde_derecho_hold]

  return imagen_hold




# Ejemplo de uso
imagen = cv2.imread("imagen_tetris.jpg")
imagen_recortada = recortar_elementos_centrales(imagen)

# Guardar la imagen recortada
cv2.imwrite("imagen_tetris_recortada.jpg", imagen_recortada)
cv2.imshow("Imagen recortada", imagen_recortada)
cv2.waitKey(0)

# Ejemplo de uso
imagen_recortada = cv2.imread("imagen_tetris_recortada.jpg")
imagen_next = obtener_next(imagen_recortada)
cv2.imshow("Imagen Next", imagen_next)
cv2.waitKey(0)

# Ejemplo de uso
imagen_recortada = cv2.imread("imagen_tetris_recortada.jpg")
imagen_hold = obtener_hold(imagen_recortada)
cv2.imshow("Imagen Hold", imagen_hold)
cv2.waitKey(0)