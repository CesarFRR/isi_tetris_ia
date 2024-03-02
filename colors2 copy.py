import cv2
import numpy as np

def obtener_color_promedio(imagen):
  """
  Obtiene el color promedio de una imagen.

  Parámetros:
    imagen: La imagen a analizar.

  Retorno:
    El color promedio en formato RGB.
  """

  # Calcular el color promedio en formato BGR
  color_promedio_bgr = np.mean(imagen, axis=(0, 1))



  return color_promedio_bgr

# Lista de legos
legos = ['amarillo', 'morado', 'naranja', 'purpura', 'rojo', 'verde-azulado', 'verde-lima']

# Iterar sobre cada lego
colores_promedio ={'amarillo': [0, 0, 0], 'morado': [0, 0, 0], 'naranja': [0, 0, 0], 'purpura': [0, 0, 0], 'rojo': [0, 0, 0], 'verde-azulado': [0, 0, 0], 'verde-lima': [0, 0, 0]}
for lego in legos:
  # Construir la ruta de la imagen
  ruta_imagen = './legos/' + lego + '.jpg'
  
  # Leer la imagen
  imagen = cv2.imread(ruta_imagen)
  
  # Calcular el color promedio
  color_promedio = obtener_color_promedio(imagen)
  colores_promedio[lego] = color_promedio[::-1]
  # color_promedio = color_promedio.astype(int)


  
  # Crear una imagen de 200x200 con el color promedio
  imagen_color = np.full((200, 200, 3), color_promedio, dtype=np.uint8)
  #Mostrar la imagen
  print(f"{lego}.jpg - Color promedio: {color_promedio[::-1]}")
  # cv2.imshow(f"{lego}.jpg - Color promedio: {color_promedio[::-1]}", imagen_color)
  # cv2.waitKey(0)
print('Colores promedio:\n\n')
for i in colores_promedio:
  print(i, colores_promedio[i],  sep='\n')


import csv

# Abre el archivo CSV en modo escritura
with open('colores_promedio.csv', 'w', newline='') as archivo:
    # Crea un escritor de CSV
    escritor = csv.writer(archivo)

    # Escribe la fila de encabezado
    escritor.writerow(['nombre', 'r', 'g', 'b'])

    # Escribe las filas de datos
    for nombre, color in colores_promedio.items():
        escritor.writerow([nombre, *color])