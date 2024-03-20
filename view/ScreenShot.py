import time
import mss
import numpy as np
import cv2
import os
class ScreenShot:
    def __init__(self):
        
        self.sct = mss.mss()
        self.w, self.h = self.sct.monitors[1]['width'], self.sct.monitors[1]['height']
        self.margen_w = self.w // 5
        self.margen_h = self.h // 5
        self.time_lapse = float(os.environ.get("MSS_T"))

    def capture(self):
        """ Captura una imagen de la pantalla y la devuelve en formato BGR. """
        # Define la región de la pantalla que quieres capturar
        region = {'top': self.margen_h, 'left': self.margen_w, 'width': self.w - 2*self.margen_w, 'height': self.h- self.margen_h}
        time.sleep(self.time_lapse)
        img_0 = self.sct.grab(region) # screenshot!
        img = np.array(img_0)
        # Descartar el canal Alpha para solo tener RGB
        img_rgb = img[..., :3]
        return img_rgb
    
    def capture_in(self, top, left, width, height):
        region = {'top': top, 'left': left, 'width': width, 'height': height}
        time.sleep(self.time_lapse)
        img_0 = self.sct.grab(region) # screenshot!
        img = np.array(img_0) 
        img_rgb = img[..., :3]
        cv2.imshow('Screenshot', img_rgb)
        cv2.waitKey(0)
        return img_rgb

           

# ss = ScreenShot()
# time.sleep(5)
# img = ss.capture()
# cv2.imwrite('screenshot2.jpg', img)
# cv2.imshow('Screenshot', img)
# cv2.waitKey(0)
