import numpy as np
from Pieces import Piece
class Grid:
    def __init__(self, grid=None, h_pieces=None):
        self.width = 10
        self.max_height = 20
        self.h_pieces = np.zeros(self.width, dtype=np.int8) if h_pieces is None else h_pieces
        initial_height = min(np.max(self.h_pieces) + 4, self.max_height)
        print('initial_height:',initial_height , self.h_pieces, np.min(self.h_pieces))
        self.grid = np.zeros((initial_height, self.width), dtype=np.int8) if grid is None else grid
        self.print_shape()

    def add_rows(self, n):
        if self.grid.shape[0] + n <= self.max_height:
            new_rows = np.zeros((n, self.width), dtype=np.int8)
            self.grid = np.concatenate((new_rows, self.grid), axis=0)

    def update_h_pieces(self):
        # Actualiza h_pieces para cada columna
        for col in range(self.width):
            # Si la columna está vacía (todos ceros), la altura es 0
            if np.all(self.grid[:, col] == 0):
                self.h_pieces[col] = 0
            else:
                # De lo contrario, la altura es la fila del primer 1 desde abajo
                self.h_pieces[col] = np.argmax(self.grid[::-1, col] != 0)

    def get_h_pieces(self):
        # Devuelve una copia de h_pieces para evitar la modificación externa
        return self.h_pieces.copy()
    def print_shape(self):
        print(self.grid.shape)
    
    def get_full_rows(self):
        # Encuentra las filas que están completamente llenas de unos
        full_rows = np.all(self.grid == 1, axis=1)
        # Devuelve los índices de las filas llenas
        return np.where(full_rows)[0]
    
    # def calculate_iterations(self, piece: Piece, x):
    #     # Calcula la posición y de la pieza
    #     p = piece.get_optimized_current_shape()
    #     w_piece = p.shape[0] if p.ndim == 1 else p.shape[1]

    #    return self.width - (w_piece -1)
    def remove_full_rows(self):
        # Usa get_full_rows para encontrar las filas llenas
        full_rows = self.get_full_rows()

        # Si no hay filas llenas, no hay nada que hacer
        if full_rows.size == 0:
            return

        # Crea un nuevo array sin las filas llenas y con nuevas filas de ceros en la parte superior
        num_full_rows = full_rows.size
        remaining_rows = np.delete(self.grid, full_rows, axis=0)
        new_rows = np.zeros((num_full_rows, self.grid.shape[1]))
        self.grid = np.concatenate((new_rows, remaining_rows), axis=0)

        # Actualiza h_pieces
        self.update_h_pieces()






g1 = Grid()
# Añade algunas piezas de Tetris en la parte inferior de la cuadrícula
print(g1.grid)
g1.print_shape()
g1.update_h_pieces()
print (g1.get_h_pieces())
  # [15 20 20 20 20 20 14 20 20 20]
    
print (g1.get_full_rows()) # [18]
print('\n')
print(g1.grid)
g1.print_shape()
print('\n')
g1.remove_full_rows()
print(g1.grid)
g1.print_shape()
print('\n')