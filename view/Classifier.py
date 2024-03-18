import cv2
import numpy as np
import os


class Classifier:
    def __init__(self):
        self.legos = [
            os.path.splitext(file)[0]
            for file in os.listdir("data/legos")
            if os.path.isfile(os.path.join("data/legos", file))
        ]
        self.histograms = []

        for name in self.legos:
            img = cv2.imread(f"data/legos/{name}.jpg")
            hist = cv2.calcHist(
                [img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256]
            )
            hist = cv2.normalize(hist, hist).flatten()
            self.histograms.append(hist)

    def predict_pieces(
        self, image: str | object, range_pieces: tuple | list, coordenadas
    ) -> list[str]:
        # Carga la imagen
        img = image
        # cv2.imshow("Imagen Next_hla", img)
        # cv2.waitKey(0)
        if isinstance(image, str):
            img = cv2.imread(image)
        # Divide la imagen en num_pieces piezas y clasifica cada una
        pieces = []
        a, b = range_pieces
        #print(f"num_pieces: {b} rangos: {a} - {b}")
        y1, y2, x1, x2 = coordenadas
        h = y2 - y1
        imagen_next= None
        for i in range(a, b + 1):
            imagen_next = img[y1 + int(h * ((i - 1) / 5)) :
                    y1 + int(h * ((i) / 5))
                    , x1:x2]
            # if a==5 and b==5:
            #     imagen_next = img[y1 + int(h * ((i - 1) / 5)) :
            #         y1 + int(h * ((i) / 5) -(h* 0.05))
            #         , x1:x2]
            #     cv2.imshow("Imagen Next", imagen_next)
            #     cv2.waitKey(0)

            pieces.append(self.predict_piece(imagen_next))

            #print(f"Predecir color lego: ", pieces[i - a])
            # cv2.imshow("Imagen Next", imagen_next)
            # cv2.waitKey(0)
        # #print(pieces)
        return pieces
    


    def predict_piece(self, piece_img) -> str:
        hist = self.calculate_histogram(piece_img)
        distances = [
            cv2.compareHist(hist, lego_hist, cv2.HISTCMP_CHISQR)
            for lego_hist in self.histograms
        ]
        predicted_color = self.legos[np.argmin(distances)]
        return predicted_color

    def calculate_histogram(self, img):
        mask = cv2.inRange(img, np.array([1, 1, 1]), np.array([250, 250, 250]))
        hist = cv2.calcHist([img], [0, 1, 2], mask, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist


# #ejemplo de uso
# classifier = Classifier()
# predicted_colors = classifier.predict_piece(cv2.imread('./tests/predecir1.jpg'))

# #print(predicted_colors)
