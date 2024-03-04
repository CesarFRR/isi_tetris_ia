import cv2

class Framer:
    def __init__(self, img_path = None):
        self.last_bordes_centrales = None
        self.last_next = None
        self.last_hold = None
        self.imagen = img_path
        if img_path is not None:
            self.imagen = cv2.imread(img_path)

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
    
    def obtener_grid(self, bordes, imagen = None):
        if imagen is None:
            imagen = self.imagen
        h = bordes[1] - bordes[0]
        w = bordes[3] - bordes[2]
        borde_superior_grid = bordes[0] 
        borde_inferior_grid = bordes[1] - int(0.01 * h)
        borde_izquierdo_grid =  bordes[2] + int(0.26 * h)
        borde_derecho_grid = bordes[2] + int(0.717 * w)

        self.last_grid = [
            borde_superior_grid,
            borde_inferior_grid,
            borde_izquierdo_grid,
            borde_derecho_grid,
        ]

        return self.last_grid
    
    def obtener_bordes_centrales_img(self, imagen=None):
        if imagen is None:
            imagen = self.imagen.copy()
        bordes = self.encontrar_bordes_centrales(imagen)
        return imagen[bordes[0]:bordes[1], bordes[2]:bordes[3]]

    def obtener_next_img(self, imagen=None):
        if imagen is None:
            imagen = self.imagen.copy()
        bordes = self.obtener_next(self.last_bordes_centrales, imagen)
        return imagen[bordes[0]:bordes[1], bordes[2]:bordes[3]]

    def obtener_hold_img(self, imagen=None):
        if imagen is None:
            imagen = self.imagen.copy()
        bordes = self.obtener_hold(self.last_bordes_centrales, imagen)
        return imagen[bordes[0]:bordes[1], bordes[2]:bordes[3]]
