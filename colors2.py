import cv2
import numpy as np
from collections import Counter
import csv
def obtener_color_mas_frecuente(imagen):
  """
  Obtiene el color más frecuente en una imagen.

  Parámetros:
    imagen: La imagen a analizar.

  Retorno:
    El color más frecuente en formato BGR.
  """

  # Redimensionar la imagen a una dimensión y convertir a tuplas
  pixels = map(tuple, imagen.reshape(-1, 3))

  # Contar la frecuencia de los colores
  colores_frecuentes = Counter(pixels)

  # Encontrar el color más frecuente
  color_mas_frecuente = colores_frecuentes.most_common(1)[0][0]

  return color_mas_frecuente

# Lista de legos
legos = ['amarillo', 'morado', 'naranja', 'purpura', 'rojo', 'verde-azulado', 'verde-lima']

# Iterar sobre cada lego
colores_frecuentes = {'amarillo': [0, 0, 0], 'morado': [0, 0, 0], 'naranja': [0, 0, 0], 'purpura': [0, 0, 0], 'rojo': [0, 0, 0], 'verde-azulado': [0, 0, 0], 'verde-lima': [0, 0, 0]}
for lego in legos:
  # Construir la ruta de la imagen
  ruta_imagen = './legos/' + lego + '.jpg'
  
  # Leer la imagen
  imagen = cv2.imread(ruta_imagen)
  
  # Calcular el color más frecuente
  color_mas_frecuente = obtener_color_mas_frecuente(imagen)
  colores_frecuentes[lego] = color_mas_frecuente[::-1]
  # Imprimir el color más frecuente
  print(f"{lego}.jpg - Color más frecuente: {color_mas_frecuente}")
  # Crear una imagen de 200x200 con el color más frecuente
  imagen_color = np.full((200, 200, 3), color_mas_frecuente, dtype=np.uint8)
  
  # Mostrar la imagen
  cv2.imshow(f"{lego}.jpg - Color más frecuente: {color_mas_frecuente}", imagen_color)
  cv2.waitKey(0)



with open('colores_frecuentes.csv', 'w', newline='') as archivo:
    # Crea un escritor de CSV
    escritor = csv.writer(archivo)

    # Escribe la fila de encabezado
    escritor.writerow(['nombre', 'r', 'g', 'b'])

    # Escribe las filas de datos
    for nombre, color in colores_frecuentes.items():
        escritor.writerow([nombre, *color])