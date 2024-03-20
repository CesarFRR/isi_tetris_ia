



from controller.Managers import HoldManager, NextManager
from model.Grid import Grid
from model.Pieces import Piece

import numpy as np

class Tetris_IA:
    def __init__(self, grid: Grid, hold_m: HoldManager, next_m: NextManager):
        self.grid = grid
        self.hold_m = hold_m
        self.next_m = next_m

    def compute_piece_expand(self, piece:Piece):
        """Calcula todas las heuristicas de la pieza para cada columna de grid, sin rotar la pieza"""
        h_list = np.array([float for i in range(11-piece.get_optimized_current_matrix().shape[1])], dtype=object)
        max_value = float('-inf')
        max_index = -1
        max_indices = None
        for i in range(len(h_list)):
            current, indices= self.grid.calculate_heuristics(piece, i)
            current = sum(current)

            h_list[i]= current
            if current > max_value:
                max_value = current
                max_index = i
                max_indices = indices

        return (max_value, max_index,max_indices)

    def compute_piece_all_rotations(self, piece:Piece):
        """Calcula todas las heuristicas de la pieza para cada columna de grid, rotando la pieza"""
        h_list_all = np.array( [np.array for _ in range(piece.computable_shapes)], dtype=object)
       # print(f'grid compute_piece_all_rotations - {0}: \n', self.grid.grid)
        for i in range(len(h_list_all)):
            piece.set_current_shape(i)
            max_v, max_i, max_indices = self.compute_piece_expand(piece)
            h_list_all[i]=(max_v, max_i, max_indices)
        piece.set_current_shape(0)
        return h_list_all
    
    def get_best_choice(self, piece:Piece):
        """Calcula la mejor columna para la pieza actual.

        returns: (max_value, max_index, max_rotation)
        
        max_value: el valor maximo de la heuristica
        max_index: la columna donde se encuentra el valor maximo
        max_rotation: la rotacion que tiene la pieza con la que se obtuvo el valor maximo"""
        h_list= self.compute_piece_all_rotations(piece)
        max_index, max_value = max(enumerate(h_list), key=lambda x: x[1][0])
        print('best_choice:',(max_value[0], max_value[1], max_index))
        return (max_value[0], max_value[1], max_index, max_value[2])

    def __str__(self):
        return self.name + " " + self.color

