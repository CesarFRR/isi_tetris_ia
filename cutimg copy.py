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

  # # Recortar la imagen usando los bordes encontrados
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
  # borde_superior = y - int(0.1 * h)
  # borde_inferior = y + h + int(0.1 * h)
  # borde_izquierdo = x - int(0.1 * w)
  # borde_derecho = x + w + int(0.1 * w)

  #return [borde_superior, borde_inferior, borde_izquierdo, borde_derecho]
  # Devolver las coordenadas del rectángulo delimitador asi nada más
  return [y, y + h, x, x + w]
def obtener_next(bordes):
    """
    Obtiene la imagen del Next a partir de una imagen recortada del juego.

    Parámetros:
        imagen_recortada: La imagen recortada que contiene el Next.

    Retorno:
        La imagen del Next.
    """

    # Definir la región de interés del Next
    h= bordes[1] - bordes[0]
    w= bordes[3] - bordes[2]
    borde_superior_next = bordes[0]
    borde_inferior_next = bordes[0] + int(0.8 * h)
    borde_izquierdo_next = bordes[2] + int(0.75 * w)
    borde_derecho_next = bordes[3]

    # # Recortar la imagen del Next
    # imagen_next = imagen_recortada[borde_superior_next:borde_inferior_next, 
    #                                                             borde_izquierdo_next:borde_derecho_next]
   

    return [borde_superior_next, borde_inferior_next, borde_izquierdo_next, borde_derecho_next]



def obtener_hold(bordes):
  """
  Obtiene la imagen del Hold a partir de una imagen recortada del juego.

  Parámetros:
    imagen_recortada: La imagen recortada que contiene el Hold.

  Retorno:
    La imagen del Hold.
  """

  # Definir la región de interés del Hold
  h= bordes[1] - bordes[0]
  w= bordes[3] - bordes[2]
  borde_superior_hold = bordes[0]
  borde_inferior_hold = bordes[0] + int(0.2 * h)
  borde_izquierdo_hold = bordes[2]
  borde_derecho_hold = bordes[2] + int(0.25 * w)

  # # Recortar la imagen del Hold
  # imagen_hold = imagen_recortada[borde_superior_hold:borde_inferior_hold, 
  #                               borde_izquierdo_hold:borde_derecho_hold]

  return [borde_superior_hold,borde_inferior_hold, borde_izquierdo_hold,borde_derecho_hold]


# Ejemplo de uso
imagen = cv2.imread("tetris_full2.jpg")
bordes_central = encontrar_bordes_centrales(imagen)

# Guardar la imagen recortada
# cv2.imwrite("imagen_tetris_recortada.jpg", imagen_recortada)
print(f"Bordes central: {bordes_central}")
cv2.imshow("Imagen recortada", imagen[bordes_central[0]:bordes_central[1], bordes_central[2]:bordes_central[3]])
cv2.waitKey(0)

# Ejemplo de uso
coordenadas_next = obtener_next(bordes_central)
next_h = coordenadas_next[1] - coordenadas_next[0]
next_w = coordenadas_next[3] - coordenadas_next[2]
next_img = imagen[int(coordenadas_next[0] + (next_h)*(0.055)):coordenadas_next[1] - int(next_h*0.04), int(coordenadas_next[2] + (next_w*0.045)):int(coordenadas_next[3] - (next_w*0.03))]
cv2.imshow("Imagen Next_0", next_img)
cv2.waitKey(0)

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(next_img, cv2.COLOR_BGR2GRAY)

# Aplicar umbralización para crear una máscara del objeto en primer plano
_, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

# Encontrar contornos en la imagen
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = list(contours)
# Para cada contorno, aproximar a una forma con menos vértices
for i in range(len(contours)):
    epsilon = 0.02*cv2.arcLength(contours[i],True)
    contours[i] = cv2.approxPolyDP(contours[i], epsilon, True)

# Dibujar los contornos en la imagen
cv2.drawContours(next_img, contours, -1, (0,255,0), 3)

cv2.imshow("Imagen con contornos", next_img)
cv2.waitKey(0)

for i in range(1, 6):
  
  print(f"Coordenadas del Next: {coordenadas_next}")
  imagen_next = imagen[coordenadas_next[0] +int((coordenadas_next[1]-coordenadas_next[0])*((i-1)/5 + 0.1)):coordenadas_next[0] +int((coordenadas_next[1]-coordenadas_next[0])*(i/5 )), coordenadas_next[2]:coordenadas_next[2] +int((coordenadas_next[3]-coordenadas_next[2]))]
  
  # Calcula las coordenadas del centro de la imagen
  centro_y, centro_x = imagen_next.shape[0] // 2, imagen_next.shape[1] // 2

  # Pone un pixel blanco en el centro de la imagen
  print(f"color centro: {imagen_next[centro_y, centro_x]}")
  imagen_next[centro_y, centro_x] = [255, 255, 255]

  cv2.imshow("Imagen Next", imagen_next)
  cv2.waitKey(0)

# Ejemplo de uso
# Ejemplo de uso
coordenadas_hold = obtener_hold(bordes_central)
print(f"Coordenadas del Hold: {coordenadas_hold}")
imagen_hold = imagen[coordenadas_hold[0]:coordenadas_hold[1], 
                             coordenadas_hold[2]:coordenadas_hold[3]]
cv2.imshow("Imagen Hold", imagen_hold)
cv2.waitKey(0)




def identificar_color(rgb):
    # Definir los colores y sus rangos
    colores = {
        "verde_turquesa": [[30, 140, 100], [70, 180, 140]],
        "verde_lima": [[110, 160, 30], [150, 200, 70]]
    }

    # Iterar sobre cada color y verificar si el píxel cae en su rango
    for color, (minimo, maximo) in colores.items():
        if all(minimo[i] <= rgb[i] <= maximo[i] for i in range(3)):
            return color

    # Si no se encontró ningún color, devolver None
    return None

def escanear_colores(img, y1, y2, x1, x2):
    # Leer la imagen
    

    # Recortar la imagen
    img_cortada = img[y1:y2, x1:x2]
    cv2.imshow("Imagen recortada", img_cortada)
    cv2.waitKey(0)


    # Lista para almacenar los colores
    colores = []

    # Calcular la columna central de la imagen recortada
    columna_central = x1 + ((x2 - x1) // 2)
    cv2.imshow("Imagen recortada2",  img_cortada[:, x1:columna_central])
    cv2.waitKey(0)
    print(f"Columna central: {columna_central} x1: {x1} x2: {x2} y1: {y1} y2: {y2}")

    # Iterar sobre cada píxel en la columna central de la imagen recortada
    for pixel_bgr in img_cortada[:, x1:columna_central]:
        # Convertir el color del píxel de BGR a RGB
        pixel_rgb = pixel_bgr[::-1]
        print(f"{pixel_rgb}")
        # # Identificar el color del píxel
        # color = identificar_color(pixel_rgb)

        # # Si se identificó un color, agregarlo a la lista
        # if color is not None:
        #     colores.append(color)

    return colores

# # Ejemplo de uso
# colores = escanear_colores(imagen, coordenadas_next[0], coordenadas_next[1], coordenadas_next[2], coordenadas_next[3])
# print(colores)