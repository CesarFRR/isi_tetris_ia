from view.Classifier import Classifier
from view.Framer import Framer
from view.ScreenShot import ScreenShot

fr = Framer()

class NextManager:
    def __init__(self, img, coordenadas_next):
        self.img = img
        self.coordenadas_next = coordenadas_next
        self.cls = Classifier()
        self.ss= ScreenShot()
        self.fr = fr
        self.next_list = self.cls.predict_pieces(self.img, [1, 5], self.coordenadas_next)
        y1, y2, x1, x2 = self.coordenadas_next
        h = y2 - y1
        w = x2 - x1
        self.new_piece_coord =  [y1 + int(h * ((4) / 5)), x1 , w, int(h)//5 ]



    def get_next_list(self):
        return self.next_list

    def update(self):
        """Actualiza la lista de Next haciendo captura unicamente del sector de la nueva pieza (la quinta) y clasificandola."""
        self.next_list[-1] = self.cls.predict_piece(self.ss.capture_in(self.new_piece_coord))
        return self
    
    def __str__(self) -> str:
        return self.next_list

class HoldManager:
    def __init__(self):
        self.hold = None

    def get_hold(self):
        return self.hold
    
    def set_hold(self, hold):
        self.hold = hold

    def remove_hold(self):
        self.hold = None
    
    def __str__(self):
        return self.hold


class GridManager:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.cls = Classifier()
        self.fr = Framer()

    def get_grid(self):
        return self.grid
    
    def set_grid(self, grid):
        self.grid = grid

    def print_grid(self):
        print("\nGrid:\n")
        for row in self.grid:
            print(row)
        print("\n")

    def __str__(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.grid)