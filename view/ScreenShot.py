import mss
import numpy as np

class ScreenShot:
    def __init__(self):
        self.sct = mss.mss()
        self.w, self.h = self.sct.monitors[1]["width"], self.sct.monitors[1]["height"]
        self.margen = self.w // 5

    def capture(self):
        # Define la región de la pantalla que quieres capturar
        region = {'top': 0, 'left': self.margen, 'width': self.w - 2*self.margen, 'height': self.h}
        screenshot = self.sct.grab(region)  # Captura la región especificada
        return np.array(screenshot)  # Convierte la captura de pantalla a un array de NumPy
    
    def capture_in(self, top, left, width, height):
        region = {'top': top, 'left': left, 'width': width, 'height': height}
        screenshot = self.sct.grab(region)
        return np.array(screenshot)

        

# ss = ScreenShot()
# time.sleep(5)
# img = ss.capture()
# cv2.imwrite('screenshot2.jpg', img)
# cv2.imshow('Screenshot', img)
# cv2.waitKey(0)
