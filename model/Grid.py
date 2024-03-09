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
            #Si la columna está vacía (todos ceros), la altura es 0
            if np.all(self.grid[:, col] == 0):
                self.h_pieces[col] = 0
            else:
               # De lo contrario, la altura es la fila del primer 1 desde abajo
                self.h_pieces[col] = np.argmin(self.grid[::-1, col] == 1)

        # Verifica cuántas filas de ceros hay desde la fila 0 hacia abajo
        zero_rows = np.all(self.grid == 0, axis=1)
        num_zero_rows = np.sum(zero_rows)

        # Si hay menos de 4 filas de ceros, agrega filas de ceros hasta que haya 4
        if num_zero_rows < 4:
            self.add_rows(4 - num_zero_rows)

    def get_h_pieces(self):
        # Devuelve una copia de h_pieces para evitar la modificación externa
        return self.h_pieces.copy()
    def print_shape(self):
        print(self.grid.shape)
    
    def find_full_rows(self):
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
        full_rows = self.find_full_rows()

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

    def find_holes(self):
        # Crea una copia de la cuadrícula y añade una fila de ceros en la parte superior
        grid = np.vstack([np.zeros((1, self.grid.shape[1])), self.grid]).astype(np.int8)

        # Inicializa el contador de huecos
        count = 0

        # Recorre cada columna
        for col in range(grid.shape[1]):
            # Encuentra los índices de los bloques (1s) en la columna
            block_indices = np.argwhere(grid[:, col] == 1)

            # Si la columna contiene bloques
            if block_indices.size > 0:
                # Encuentra los índices de los huecos (0s que tienen al menos un bloque por encima de ellos)
                hole_indices = np.argwhere((grid[:, col] == 0) & (np.arange(grid.shape[0]) > np.min(block_indices)))

                # Cambia los valores de los huecos a -1 en la copia de la cuadrícula
                grid[hole_indices, col] = -1

                # Incrementa el contador de huecos por el número de huecos en la columna
                count += hole_indices.size

        # Imprime la copia de la cuadrícula con los huecos representados por -1
        print(grid)

        return count
    
    def find_gaps(self):
        # usa self.h_pieces para encontrar las diferencias entre las alturas de las columnas para cada elemento abs(n - (n+1))
        return np.sum(np.abs(self.h_pieces[:-1] - self.h_pieces[1:]))
    def find_h_piece_sum(self):
        # devuelve la suma de las alturas de las columnas
        return np.sum(self.h_pieces)



g1 = Grid()
# Añade algunas piezas de Tetris en la parte inferior de la cuadrícula
print(g1.grid)

g1.print_shape()
print('\n')

grid_test = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
])
print(grid_test)
h_pieces = np.zeros(grid_test.shape[1], dtype=np.int8)
for col in range(grid_test.shape[1]):
    h_pieces[col] = np.argmin(grid_test[::-1, col] == 1)

print('grid local: h_pieces: \n',h_pieces)
g1.grid = grid_test
#g1.h_pieces = h_pieces
print('\n')

g1.print_shape()
print('\n')
print(g1.h_pieces)
g1.update_h_pieces()
print(g1.h_pieces)
print('\n')
print(g1.grid)
g1.print_shape()


print('\n')
holes = g1.find_holes()
print('huecos: ', holes)
print(g1.get_h_pieces())



print(g1.grid)

print(g1.find_gaps()) 
print(g1.find_h_piece_sum())