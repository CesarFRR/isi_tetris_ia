import numpy as np
from Pieces import Piece
class Grid:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.h_pieces=np.zeros(self.width, dtype=int)


    def update_h_pieces(self):
        # Actualiza h_pieces para cada columna
        for col in range(self.width):
            # Si la columna está vacía (todos ceros), la altura es 0
            if np.all(self.grid[:, col] == 0):
                self.h_pieces[col] = 0
            else:
                # De lo contrario, la altura es la fila del primer 1 desde arriba
                self.h_pieces[col] = np.argmax(self.grid[:, col] != 0)

    def get_h_pieces(self):
        # Devuelve una copia de h_pieces para evitar la modificación externa
        return self.h_pieces.copy()
    
    def get_full_rows(self):
        # Encuentra las filas que están completamente llenas de unos
        full_rows = np.all(self.grid == 1, axis=1)
        # Devuelve los índices de las filas llenas
        return np.where(full_rows)[0]
    
    # def calculate_iterations(self, piece: Piece, x):
    #     # Calcula la posición y de la pieza
    #     p = piece.get_optimized_current_shape()
    #     w_piece = p.shape[0] if p.ndim == 1 else p.shape[1]

        return self.width - (w_piece -1)
    def remove_full_rows(self):
        # Usa get_full_rows para encontrar las filas llenas
        full_rows = self.get_full_rows()

        # Si no hay filas llenas, no hay nada que hacer
        if full_rows.size == 0:
            return

        # Usa get_h_pieces para encontrar la fila más alta con un 1
        highest_piece_row = min(self.get_h_pieces())

        # Mueve todas las filas por encima de la fila llena más alta hacia abajo
        self.grid[highest_piece_row+1:] = self.grid[:highest_piece_row+1]

        # Llena las filas superiores con ceros
        self.grid[:highest_piece_row+1] = 0

        # Actualiza h_pieces
        self.update_h_pieces()

grid = np.zeros((20, 10), dtype=int)

# Añade algunas piezas de Tetris en la parte inferior de la cuadrícula
grid[18, 3:6] = 1  # Pieza horizontal
grid[17, 5:8] = 1  # Pieza horizontal
grid[16:20, 8] = 1  # Pieza vertical
grid[15:20, 1] = 1  # Pieza vertical
grid[14:20, 6] = 1  # Pieza vertical
grid[18, 0:10] =1
grid[16, 0:10] =1



g1 = Grid()
g1.grid = grid
print(g1.grid)
g1.update_h_pieces()
print (g1.get_h_pieces())
  # [15 20 20 20 20 20 14 20 20 20]
    
print (g1.get_full_rows()) # [18]


g1.remove_full_rows()
print(g1.grid)