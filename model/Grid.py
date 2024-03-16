import os
import numpy as np
from model.Pieces import Piece

class Grid:
    def __init__(self, grid=None, h_pieces=None):
        self.width = 10
        self.max_height = 20
        self.h_pieces = np.zeros(self.width, dtype=np.int8) if h_pieces is None else h_pieces
        initial_height = min(np.max(self.h_pieces) + 4, self.max_height)
        ##print('initial_height:',initial_height , self.h_pieces, np.min(self.h_pieces))
        self.grid = np.zeros((initial_height, self.width), dtype=np.int8) if grid is None else grid
        # self.print_shape()
    def __str__(self) -> str:
        return str(self.grid)

    def add_rows(self, n):
        if self.grid.shape[0] + n <= self.max_height:
            new_rows = np.zeros((n, self.width), dtype=np.int8)
            self.grid = np.concatenate((new_rows, self.grid), axis=0)


    def update_h_pieces(self):
        print('current h_pieces: \n', self.h_pieces, '\n', self.grid)

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
        print('after h_pieces: \n', self.h_pieces, '\n', self.grid)

    def get_h_pieces(self):
        # Devuelve una copia de h_pieces para evitar la modificación externa
        return self.h_pieces.copy()
    def get_grid_matrix(self):
        return self.grid
    
    def print_shape(self):
        print(self.grid.shape)
    
    def find_full_rows(self):
        # Encuentra las filas que están completamente llenas de unos
        full_rows = np.all(self.grid == 1, axis=1)
        # Devuelve los índices de las filas llenas
        return np.where(full_rows)[0]
    
    # def calculate_iterations(self, piece: Piece, x):
    #     # Calcula la posición y de la pieza
    #     p = piece.get_optimized_current_matrix()
    #     w_piece = p.shape[0] if p.ndim == 1 else p.shape[1]

    #    return self.width - (w_piece -1)
    def remove_full_rows(self, update_h_pieces=True):
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
        if update_h_pieces:
            self.update_h_pieces()
            
    def update_grid(self):
        #self.remove_full_rows()
        self.update_h_pieces()
        return self

    def find_holes(self)-> int:
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
        ##print(grid)

        return count
    
    def find_gaps(self)-> int:
        # usa self.h_pieces para encontrar las diferencias entre las alturas de las columnas para cada elemento abs(n - (n+1))
        return np.sum(np.abs(self.h_pieces[:-1] - self.h_pieces[1:]))
    
    def find_h_piece_sum(self):
        # devuelve la suma de las alturas de las columnas
        return int(np.sum(self.h_pieces))
    
    def get_piece_indexes(self, piece:Piece, index):
        """Calcula donde caerá la pieza en la cuadrícula y devuelve los indices de la cuadrícula que la pieza va a ocupar (solo los indices donde la pieza tiene 1)"""
        # Asume que la pieza es una matriz 3x3 y que quieres colocarla en la primera columna
        index =index
        piece_width = piece.get_optimized_current_matrix().shape[1]
        piece_height = piece.get_optimized_current_matrix().shape[0]
        heights = self.h_pieces[index:index + piece.get_optimized_current_matrix().shape[1]]
        #print('shape del grid: ', self.grid.shape , '\n')
        # Encuentra la altura más alta
        local_h_pieces = max(heights) if max(heights) > 0 else 0
        if local_h_pieces == 0:
            #print('no hay nada debajo, simplemente se pone la pieza:\n')
            indices = set((a + self.grid.shape[0] - piece_height, b+index) for a in range(piece_height) for b in range(piece_width) if piece.get_optimized_current_matrix()[a, b] == 1)
            return indices
        
        
            # Calcula los índices de la cuadrícula que la pieza va a ocupar
        # indices = [(row+i, index+j) for j in range(piece.shape[1]) for i in range(piece.shape[0]) if piece[i, j] == 1]

        indices = set()
        # Este doble FOR tiene como maximo 16 iteraciones de acuerdo a la pieza mas larga (4x4)
        for a, i in enumerate(range(local_h_pieces-piece.get_optimized_current_matrix().shape[0], local_h_pieces)):
            for b,j in enumerate(range(index, index + piece.get_optimized_current_matrix().shape[1])):
                #print('i:', i, 'j:', j)
                if piece.get_optimized_current_matrix()[a, b] == 1:
                    indices.add((i, j))

        
        while True:
            # Comprueba si la pieza puede moverse hacia abajo
            if any(i+1 < self.grid.shape[0] and self.grid[i+1, j] == 1 for i, j in indices):
                break

            # Mueve la pieza hacia abajo
            indices = [(i+1, j) for i, j in indices]
        return indices


    def place_piece(self, piece: Piece,index,  indices: tuple = None, update_h_pieces=False):
        """Coloca la pieza en la cuadrícula"""
        if indices is not None:
            self.__place_piece(indices)
        else:
            # Calcula los índices de la cuadrícula que la pieza va a ocupar
            indices = self.get_piece_indexes(piece,index)

            # Coloca la pieza en la cuadrícula
            self.__place_piece(indices)
        if update_h_pieces:
            self.update_h_pieces()

    def place_piece_final(self, piece: Piece, index:int, rotation:int):
        """Coloca la pieza en la cuadrícula en la columna y rotacion dada"""
        piece.set_current_shape(rotation)
        #self.update_grid()
        indices = self.get_piece_indexes(piece, index)
        self.__place_piece(indices)
        self.update_h_pieces()
        #print('place piece final, grid: ', self.grid)
        return self
    
        
    def unplace_piece(self, indices, update_h_pieces=False):
        """Quita la pieza de la cuadrícula"""
        for i, j in indices:
            self.grid[i, j] = 0
        if update_h_pieces:
            self.update_h_pieces()

    def calculate_heuristics(self, piece:Piece, index=0)-> tuple:
        ##print('calculate_heuristics: indice:', index, '\npiece:', piece.get_matrix(), '\nh_pieces:', self.h_pieces, '\ngrid:', self.grid, '\nshape:', self.grid.shape, '\nwidth:', self.width, '\nmax_height:', self.max_height, '\nindex: ', index)
        print(f'grid calculate_heuristics - {0}:', self.grid)
        indices = self.get_piece_indexes(piece, index)
        print(f'grid calculate_heuristics - {1}:', self.grid)
        cache_h_pieces = self.h_pieces.copy()
        self.place_piece(piece,index=index, update_h_pieces=False)
        
        ones_count = np.sum(piece.get_optimized_current_matrix() == 1, axis=0)
        self.h_pieces[index:index+piece.get_optimized_current_matrix().shape[1]] += ones_count

        print(f'grid calculate_heuristics - {2}:', self.grid)
        # aqui se calculan heristicas, 
        # se puede devolver un diccionario.
        # (aggregate_height, complete_lines, holes, gaps)
        # if index==1:
        #         print('index:', index, 'piece:', piece.get_optimized_current_matrix(), 'grid: ', self.grid)
        a= float(os.environ.get("H_A"))
        b= float(os.environ.get("H_B"))
        c= float(os.environ.get("H_C"))
        d= float(os.environ.get("H_D"))
        #print('grid con la pieza colocada:', self.grid)
        H = (a*self.find_h_piece_sum(), b*self.find_full_rows().size,
              c*self.find_holes(), d*self.find_gaps())
        print(f'grid calculate_heuristics - {3}:', self.grid)
        # ===================================#
        #print('la suma da esto======: ', sum(H))

        # Quita la pieza de la cuadrícula
        self.unplace_piece(indices, update_h_pieces=False)
        self.h_pieces = cache_h_pieces
        print(f'grid calculate_heuristics - {4}:', self.grid)
        return H

    def __place_piece(self, indices):
        """Coloca la pieza en la cuadrícula"""
        ##print('indices:', indices)
        for i, j in indices:
            self.grid[i, j] = 1


# g1 = Grid()
# # Añade algunas piezas de Tetris en la parte inferior de la cuadrícula
# ##print(g1.grid)

# g1.#print_shape()
# ##print('\n')

# grid_test = np.array([
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
#     [1, 1, 0, 1, 1, 1, 1, 0, 0, 0]
# ])
# ##print(grid_test)
# h_pieces = np.zeros(grid_test.shape[1], dtype=np.int8)
# for col in range(grid_test.shape[1]):
#     h_pieces[col] = np.argmin(grid_test[::-1, col] == 1)

# ##print('grid local: h_pieces: \n',h_pieces)
# g1.grid = grid_test
# g1.h_pieces = h_pieces
# g1.update_h_pieces()
# ##print('\n')
# ##print(g1.grid)
# p1 = Green_S()

# gm = GridManager()
# gm.set_grid(g1)
# heuristics_list = gm.compute_piece(p1)




# g1.place_piece(p1)
# ##print('\n')
# ##print(g1.grid)
# g1.#print_shape()
# ##print('\n')
# ##print(g1.h_pieces)
# g1.update_h_pieces()
# ##print(g1.h_pieces)
# ##print('\n')
# ##print(g1.grid)
# g1.#print_shape()


# ##print('\n')
# holes = g1.find_holes()
# ##print('huecos: ', holes)
# ##print(g1.get_h_pieces())



# ##print(g1.grid)

# ##print(g1.find_gaps()) 
# ##print(g1.find_h_piece_sum())

