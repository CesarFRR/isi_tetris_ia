import cv2
import numpy as np
import csv

class Classifier:
    def __init__(self, csv_file):
        self.colors = {}
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                # Convert the RGB values from strings to integers
                r, g, b = map(float, row[1:])
                self.colors[row[0]] = np.array([r, g, b])

    def classify(self, image, threshold=20):
        height, width = image.shape[:2]
        closest_color_name = 'desconocida'
        min_distance = threshold
        color_pixel_min = None
        for y in range(height):
            pixel_color = image[y, width // 2]
            print(pixel_color)
            for color_name, color_value in self.colors.items():
                distance = np.sqrt(np.sum((pixel_color - color_value) ** 2))
                if distance < min_distance:
                    min_distance = distance
                    closest_color_name = color_name
                    color_pixel_min = pixel_color
        # print (min_distance, closest_color_name, color_pixel_min, self.colors[closest_color_name])
        return closest_color_name
    


# Instancia la clase Classifier con el archivo CSV de colores promedio
clasificador = Classifier('colores_promedio.csv')

# Lee la imagen
imagen = cv2.imread('./legos/purpura.jpg')

# Clasifica la imagen
color = clasificador.classify(imagen)

print(color)