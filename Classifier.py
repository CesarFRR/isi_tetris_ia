import cv2
import numpy as np
import os

class Classifier:
    def __init__(self):
        self.legos = [os.path.splitext(file)[0] for file in os.listdir('legos') if os.path.isfile(os.path.join('legos', file))]
        self.histograms = []

        for name in self.legos:
            img = cv2.imread(f'legos/{name}.jpg')
            hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            self.histograms.append(hist)

    def predict_pieces(self, image_path, num_pieces):
        img = cv2.imread(image_path)
        height, _, _ = img.shape
        piece_height = height // num_pieces

        predicted_colors = []
        for i in range(num_pieces):
            piece_img = img[i*piece_height:(i+1)*piece_height, :]
            cv2.imshow("Cropped Image", piece_img)  # Display the cropped image
            cv2.waitKey(0)
            predicted_color = self.predict_piece(piece_img)
            predicted_colors.append(predicted_color)


        return predicted_colors

    def predict_piece(self, piece_img):
        hist = self.calculate_histogram(piece_img)

        distances = [cv2.compareHist(hist, lego_hist, cv2.HISTCMP_CHISQR) for lego_hist in self.histograms]

        predicted_color = self.legos[np.argmin(distances)]

        return predicted_color
    
    def calculate_histogram(self, img):
        mask = cv2.inRange(img, np.array([1, 1, 1]), np.array([250, 250, 250]))
        hist = cv2.calcHist([img], [0, 1, 2], mask, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist
        

#ejemplo de uso
classifier = Classifier()
predicted_colors = classifier.predict_piece(cv2.imread('./tests/predecir1.jpg'))

print(predicted_colors)