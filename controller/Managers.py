
from model.Pieces import Piece
from view.Classifier import Classifier
from view.Framer import Framer
from view.ScreenShot import ScreenShot
from model.Grid import Grid
import numpy as np
fr = Framer()


class HoldManager:
    def __init__(self, ctr, ia=None):
        self.hold = None
        self.score = 0
        self.position = None
        self.rotation = None
        self.indices = None
        self.best_choice = None
        self.ctr = ctr
        self.ia=ia

    def get_hold(self):
        return self.hold
    
    def set_hold(self, hold, score=None):
        self.hold = hold
        if score is not None:
            self.score = score

        return self
    def get_score(self):
        return self.score
    def set_score(self, score):
        self.score = score
        return self
    
    def remove_hold(self):
        self.hold = None

    def swap(self, piece):
        self.ctr.hold_move()
        if self.hold is not None:
            self.hold, piece = piece, self.hold
            return piece
        
        self.hold = piece
        return None
    
    def update(self):
        self.best_choice = self.ia.get_best_choice(self.hold)
        self.score, self.position, self.rotation, self.indices = self.best_choice
        return self
    

    def __str__(self):
        return self.hold

class NextManager:
    def __init__(self, img, coordenadas_next):
        self.img = img
        self.coordenadas_next = coordenadas_next
        self.cls = Classifier()
        self.ss= ScreenShot()
        self.next_list = self.cls.predict_pieces(self.img, [1, 5], self.coordenadas_next)
        y1, y2, x1, x2 = self.coordenadas_next
        h = y2 - y1
        w = x2 - x1
        self.popped_pieces = 0
       



    def get_next_list(self):
        return self.next_list
    
    # def swap_hold(self, hold: HoldManager):
    #     if hold.get_hold() is not None:
    #         self.next_list[0], hold.hold = hold.get_hold(), self.next_list[0]
    #     else:
    #         hold.hold = self.next_list[0]
    #         self.next_list.pop(0)
    #         self.update()
    def pop_piece(self):
        new = self.next_list.pop(0)
        self.popped_pieces += 1
        return new


    def update(self, range = [5, 5]):
        """Actualiza la lista de Next haciendo captura unicamente del sector de la nueva pieza (la quinta) y clasificandola."""
        # img = self.ss.capture()
        # cv2.imshow('next', img[self.coordenadas_next[0]:self.coordenadas_next[1], self.coordenadas_next[2]:self.coordenadas_next[3]])
        # cv2.waitKey(0)
        news= self.cls.predict_pieces(self.ss.capture(), range, self.coordenadas_next)
        

        self.next_list= self.next_list + news
        # if len(self.next_list) > 5:
        #     self.next_list.pop(0)
        return self
    
    def __str__(self) -> str:
        return self.next_list



class GridManager:
    def __init__(self):
        self.grid = Grid()

    def get_grid(self):
        return self.grid
    
    def set_grid(self, grid):
        self.grid = grid

    def print_grid(self):
        print("\nGrid:\n")
        for row in self.grid:
            print(row)
        print("\n")

    def place_piece(self, piece:Piece, column:int, rotation:int):
        """Coloca la pieza en la columna y rotacion dada"""
        self.grid.place_piece_final(piece, column, rotation)
        #print('\ngrid despues de poner pieza:\n', self.grid)
        
       
    def update_grid(self):
        """Actualiza el grid, eliminando las filas completas y actualizando las heuristicas"""
        self.grid.update_grid()
        #print('\ngrid despues de actaulizarse:\n', self.grid)

        


    def print_grid(self, indices=None):
        """Muestra el grid con la pieza actual"""
        if indices is None:

            view_grid = np.array(self.grid.grid.copy(), dtype=object)
            for r, c in indices:
                view_grid[r, c] = 'X'
        else:
            view_grid = self.grid.grid
        print('grid_m.grid: \n')
        for row in view_grid:
            for col in row:
                print(col, end=" ")
            print()
        

      
  


    def __str__(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.grid)