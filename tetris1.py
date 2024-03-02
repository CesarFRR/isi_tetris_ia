import mss
import numpy as np
import cv2

# Capturar la pantalla
sct = mss.mss()
monitor = sct.monitors[0]
img = sct.grab(monitor)
# Convertir la imagen a formato NumPy
img_np = np.array(img)

# Procesar la imagen
gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extraer la información de las figuras
for i, contour in enumerate(contours):
    # Obtener la posición y la rotación de la figura
    x, y, w, h = cv2.boundingRect(contour)
    rect = cv2.minAreaRect(contour)
    angle = rect[-1]

    # Mostrar la primera figura con su contorno en color verde
    if i == 0:
        cv2.drawContours(img_np, [contour], 0, (0, 255, 0), 2)
        cv2.imshow("Figura con contorno verde", img_np)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break
