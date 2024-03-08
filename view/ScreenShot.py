import mss
import numpy as np
import cv2
class ScreenShot:
    def __init__(self):
        self.sct = mss.mss()
        self.w, self.h = self.sct.monitors[1]['width'], self.sct.monitors[1]['height']
        self.margen_w = self.w // 5
        self.margen_h = self.h // 5

    def capture(self):
        """ Captura una imagen de la pantalla y la devuelve en formato BGR. """
        # Define la región de la pantalla que quieres capturar
        region = {'top': self.margen_h, 'left': self.margen_w, 'width': self.w - 2*self.margen_w, 'height': self.h- self.margen_h}
        img = np.array(self.sct.grab(region)) # screenshot!
        # Descartar el canal Alpha para solo tener RGB
        img_rgb = img[..., :3]
        return img_rgb
    
    def capture_in(self, top, left, width, height):
        region = {'top': top, 'left': left, 'width': width, 'height': height}
        screenshot = self.sct.grab(region)
        return self.mss_to_bgr(screenshot)

        

# ss = ScreenShot()
# time.sleep(5)
# img = ss.capture()
# cv2.imwrite('screenshot2.jpg', img)
# cv2.imshow('Screenshot', img)
# cv2.waitKey(0)
