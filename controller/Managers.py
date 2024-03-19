
import re
import cv2
from model.Pieces import Piece
from view.Classifier import Classifier
from view.Framer import Framer
from view.ScreenShot import ScreenShot
from model.Grid import Grid
import numpy as np
fr = Framer()


class HoldManager:
    def __init__(self):
        self.hold = None
        self.score = 0
        self.position = None
        self.rotation = None
        self.indices = None
        self.best_choice = None
        self.ctr = None
        self.grid_m=None

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
        self.best_choice = self.grid_m.get_best_choice(self.hold)
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

    def compute_piece(self, piece:Piece):
        """Calcula todas las heuristicas de la pieza para cada columna de grid, sin rotar la pieza"""
        ##print('AQUI ES LA PIEZA: \n', piece.get_optimized_current_matrix(), '\n', piece.get_optimized_current_matrix().shape,'\n')
        #print('alturas de la grilla: \n', self.grid.h_pieces)
        h_list = np.array([float for i in range(11-piece.get_optimized_current_matrix().shape[1])], dtype=object)
        max_value = float('-inf')
        max_index = -1
        max_value_0 = float('-inf')
        max_index_0 = -1
        #print(f'grid compute_piece - {0}: \n', self.grid.grid)
        #print('pieza actual:\n', piece.get_optimized_current_matrix())
        indices = None
        max_indices = None
        for i in range(len(h_list)):
            current, indices, current_0 = self.grid.calculate_heuristics(piece, i)
            current = sum(current)
            current_0 = sum(current_0)
            h_list[i]= current
            ###print('heurisrica de i:', i, h_list[i], '\npara la pieza:', piece.get_optimized_current_matrix())
            
            if current > max_value:
                max_value = current
                max_index = i
                max_indices = indices
            if current_0 > max_value_0:
                max_value_0 = current_0
                max_index_0 = i
            
        #print(f'grid compute_piece - {1}: \n', self.grid.grid)
        #print('AQUI ES LAS HEURISTICAS: \n', h_list)
        return (max_value, max_index,max_indices)
    
    def compute_piece_all_rotations(self, piece:Piece):
        """Calcula todas las heuristicas de la pieza para cada columna de grid, rotando la pieza"""
        h_list_all = np.array( [np.array for _ in range(piece.computable_shapes)], dtype=object)
       # print(f'grid compute_piece_all_rotations - {0}: \n', self.grid.grid)
        for i in range(len(h_list_all)):
            piece.set_current_shape(i)
            max_v, max_i, max_indices = self.compute_piece(piece)
            h_list_all[i]=(max_v, max_i, max_indices)
            
            ###print('heurisricas de i:', i, h_list_all[i], '\npara la matrix de la pieca:', piece.get_optimized_current_matrix(), '\nNumero: ', piece.current_shape, '\n')
        
        ##print('\nHeuristicas de todas las rotaciones!!: \n', h_list_all)
        
        #print(f'grid compute_piece_all_rotations - {1}: \n', self.grid.grid)
        piece.set_current_shape(0)
       # print(f'grid compute_piece_all_rotations - {2}: \n', self.grid.grid)
        return h_list_all
    
    def get_best_choice(self, piece:Piece):
        """Calcula la mejor columna para la pieza actual.

        returns: (max_value, max_index, max_rotation)
        
        max_value: el valor maximo de la heuristica
        max_index: la columna donde se encuentra el valor maximo
        max_rotation: la rotacion que tiene la pieza con la que se obtuvo el valor maximo"""
        #print('GRID ANTES DEL BEST CHOICE: \n', self.grid.grid)
        h_list= self.compute_piece_all_rotations(piece)
        max_index, max_value = max(enumerate(h_list), key=lambda x: x[1][0])
        #print('max_value:', max_value, 'max_index:', max_index)
        #print('GRID DESPUES DEL BEST CHOICE: \n', self.grid.grid)
        print('best_choice:',(max_value[0], max_value[1], max_index))
        return (max_value[0], max_value[1], max_index, max_value[2])
    
    def place_piece(self, piece:Piece, column:int, rotation:int):
        """Coloca la pieza en la columna y rotacion dada"""
        self.grid.place_piece_final(piece, column, rotation)
        #print('\ngrid despues de poner pieza:\n', self.grid)
        
       
    def update_grid(self):
        """Actualiza el grid, eliminando las filas completas y actualizando las heuristicas"""
        self.grid.update_grid()
        #print('\ngrid despues de actaulizarse:\n', self.grid)

      
  


    def __str__(self):
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.grid)