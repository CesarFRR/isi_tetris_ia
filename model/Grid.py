from ast import List
import os
from cv2 import add
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
        self.grid = np.zeros((20, self.width), dtype=np.int8)
        self.full_rows_removed=0
        # self.print_shape()
    def __str__(self) -> str:
        return str(self.grid)

    def add_rows(self, n):
        if self.grid.shape[0] + n <= self.max_height:
            new_rows = np.zeros((n, self.width), dtype=np.int8)
            self.grid = np.concatenate((new_rows, self.grid), axis=0)


    def update_h_pieces(self, add_zero_rows=True):
        # Verifica cuántas filas de ceros hay desde la fila 0 hacia abajo
        zero_rows = np.all(self.grid == 0, axis=1)
        num_zero_rows = np.sum(zero_rows)

        # Si hay más de 4 filas de ceros, quita filas de ceros hasta que haya 4
        # Si hay más de 4 filas de ceros, quita filas de ceros hasta que haya 4
        # if add_zero_rows and num_zero_rows > 4:
        #     rows_to_remove = num_zero_rows - 4
        #     self.grid = np.delete(self.grid, slice(0, rows_to_remove), axis=0)  # Elimina las filas superiores
        #     self.grid = np.vstack([self.grid, np.zeros((rows_to_remove, self.grid.shape[1]))])  # Añade filas de ceros en la parte inferior

        # Actualiza h_pieces para cada columna
        for col in range(self.width):
            #Si la columna está vacía (todos ceros), la altura es 0
            if np.all(self.grid[:, col] == 0):
                self.h_pieces[col] = 0
            else:
                for i in range(self.grid.shape[0]):
                    # De lo contrario, la altura es la fila del primer 1 desde abajo
                    if self.grid[i, col] == 1:
                        #print('i:', i, 'col:', col, 'grid shape:', self.grid.shape)
                        self.h_pieces[col] = self.grid.shape[0] - i
                        break

        # Si hay menos de 4 filas de ceros, agrega filas de ceros hasta que haya 4
        # if add_zero_rows:
        #     if num_zero_rows < 4:
        #         self.add_rows(4 - num_zero_rows)
       # print('after h_pieces: \n', self.h_pieces, '\n', self.grid)

    def get_h_pieces(self):
        # Devuelve una copia de h_pieces para evitar la modificación externa
        return self.h_pieces.copy()
    def get_grid_matrix(self):
        return self.grid
    
    def print_shape(self):
        print(self.grid.shape)
    
    def find_full_rows(self, indices=None):
        # Inicializa una lista para almacenar los índices de las filas llenas
        if indices is None:
            # Encuentra las filas que están completamente llenas de unos
            full_rows = np.all(self.grid == 1, axis=1)
            # Devuelve los índices de las filas llenas
            return np.where(full_rows)[0]

        full_rows = []
        # Recorre la grilla de abajo a arriba
        for i in range(self.grid.shape[0] - 1, -1, -1):
            # Asigna la fila actual al array row
            row = self.grid[i]
            # Cuenta cuántos unos hay en la fila
            ones_in_row = np.sum(row)
            # Revisa si en los índices hay tuplas que tengan como fila la que estamos visitando
            ones_in_indices = sum(1 for x, y in indices if x == i)
            # Si la suma da 10, encontramos una fila de unos
            if ones_in_row + ones_in_indices == 10:
                full_rows.append(i)
            # Si encontramos una fila de ceros, ya no hay más filas con piezas que contar
            elif ones_in_row == 0:
                break
        # Devuelve los índices de las filas llenas
        return full_rows
    
    # def calculate_iterations(self, piece: Piece, x):
    #     # Calcula la posición y de la pieza
    #     p = piece.get_optimized_current_matrix()
    #     w_piece = p.shape[0] if p.ndim == 1 else p.shape[1]

    #    return self.width - (w_piece -1)
    def remove_full_rows(self, update_h_pieces=True, count=False):
        # Usa get_full_rows para encontrar las filas llenas
        full_rows = self.find_full_rows()

        # Si no hay filas llenas, no hay nada que hacer
        if full_rows.size == 0:
            return

        # Crea un nuevo array sin las filas llenas y con nuevas filas de ceros en la parte superior
        num_full_rows = full_rows.size
        remaining_rows = np.delete(self.grid, full_rows, axis=0)
        new_rows = np.zeros((num_full_rows, self.grid.shape[1]), dtype=np.int8)
        self.grid = np.concatenate((new_rows, remaining_rows), axis=0)

        # Actualiza h_pieces
        if update_h_pieces:
            self.update_h_pieces()

        if count: self.full_rows_removed += num_full_rows
            
    def update_grid(self):
        self.remove_full_rows(count=True)
        self.update_h_pieces()
        

    def find_holes(self, indices=None) -> int:
        if indices is None:
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
        # Crea una copia de la cuadrícula y añade una fila de ceros en la parte superior
        grid = np.vstack([np.zeros((1, self.grid.shape[1])), self.grid]).astype(np.int8)

        # Inicializa el contador de huecos
        count = 0

        # Recorre cada columna
        for col in range(grid.shape[1]):
            # Encuentra los índices de los bloques (1s) en la columna
            block_indices = np.argwhere(grid[:, col] == 1)
            

            # Añade los índices adicionales que están en la misma columna
            additional_indices = [x for x, y in indices if y == col]
            additional_indices = np.array(additional_indices)[:, None]
            #print('\nblock_indices:\n', block_indices,'\nadditional_indices:\n', additional_indices)
            block_indices = np.concatenate((block_indices, additional_indices))

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
    
    def find_gaps(self, indices = None)-> int:
        # usa self.h_pieces para encontrar las diferencias entre las alturas de las columnas para cada elemento abs(n - (n+1))
        if indices is None : return np.sum(np.abs(self.h_pieces[:-1] - self.h_pieces[1:]))

        h_pieces_copy = self.h_pieces.copy()
        for i, j in indices:
            h_pieces_copy[j] += 1
            
        # Usa h_pieces_copy para encontrar las diferencias entre las alturas de las columnas
        return np.sum(np.abs(h_pieces_copy[:-1] - h_pieces_copy[1:]))
        
    def find_h_piece_sum(self, indices=None)-> int:
        # devuelve la suma de las alturas de las columnas
        if indices is None:
            # Actualiza h_pieces para cada columna
            h_p= np.zeros(self.width, dtype=np.int8)
            for col in range(self.width):
                #Si la columna está vacía (todos ceros), la altura es 0
                if np.all(self.grid[:, col] == 0):
                    h_p[col] = 0
                else:
                # De lo contrario, la altura es la fila del primer 1 desde abajo
                    h_p[col] = self.grid.shape[0] - np.argmax(self.grid[:, col] == 1)
            return np.sum(h_p)

        return np.sum(self.h_pieces) + len(indices)
    
    
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
           # print('no hay nada debajo, simplemente se pone la pieza:\n')

            indices = set((a + self.grid.shape[0] - piece_height, b+index) for a in range(piece_height) for b in range(piece_width) if piece.get_optimized_current_matrix()[a, b] == 1)
            #print('indices de la pieza cuando no hay nada abajo: ', indices)
            return indices
        
        
            # Calcula los índices de la cuadrícula que la pieza va a ocupar
        # indices = [(row+i, index+j) for j in range(piece.shape[1]) for i in range(piece.shape[0]) if piece[i, j] == 1]

        indices = set()
        # Este doble FOR tiene como maximo 16 iteraciones de acuerdo a la pieza mas larga (4x4)
        row = self.grid.shape[0] - (local_h_pieces+piece.get_optimized_current_matrix().shape[0])
        col = index
        #print('revisando indices: \n', local_h_pieces, piece.get_optimized_current_matrix().shape, (upper_limit, self.grid.shape[0]-local_h_pieces ), index, index + piece.get_optimized_current_matrix().shape[1])
        # for a, row in enumerate(range(row, row + piece.get_optimized_current_matrix().shape[0])):
        #     for b,col in enumerate(range(index, index + piece.get_optimized_current_matrix().shape[1])):
        #        # print('i:', row, 'j:', col, 'a:', a, 'b:', b)
        #         if piece.get_optimized_current_matrix()[a, b] == 1:
        #             indices.add((row, col))
        for i in range(piece.get_optimized_current_matrix().shape[0]):
            for j in range(piece.get_optimized_current_matrix().shape[1]):
                if piece.get_optimized_current_matrix()[i, j] == 1:
                    indices.add((row+i, col+j))
        #print('\n===================\nindices de la pieza antes del while: ', indices, '\n===================\n')
        if not any((i+1 < self.grid.shape[0] and self.grid[i+1, j] == 1) for i, j in indices):
            #print('\nhay que bajar los indices\n')
            pass
        while True:
            #print('while 4 get indexes')
            # Comprueba si la pieza puede moverse hacia abajo
            if any((i+1 < self.grid.shape[0] and self.grid[i+1, j] == 1) or (i+1 == self.grid.shape[0]) for i, j in indices):
                break
            
            # Mueve la pieza hacia abajo
            indices = [(i+1, j) for i, j in indices]

        #print('\n===================\nindices de la pieza: ', indices, '\n===================\n')
        return indices


    def place_piece(self, piece: Piece =None,index=None,  indices=None, update_h_pieces=False):
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
        
        #print('place piece final, grid: ', self.grid)
        
    
        
    def unplace_piece(self, indices, update_h_pieces=False):
        """Quita la pieza de la cuadrícula"""
        for i, j in indices:
            self.grid[i, j] = 0
        if update_h_pieces:
            self.update_h_pieces()

    def calculate_heuristics(self, piece:Piece, index=0)-> tuple:
        ##print('calculate_heuristics: indice:', index, '\npiece:', piece.get_matrix(), '\nh_pieces:', self.h_pieces, '\ngrid:', self.grid, '\nshape:', self.grid.shape, '\nwidth:', self.width, '\nmax_height:', self.max_height, '\nindex: ', index)
        #print(f'grid calculate_heuristics - {0}:', self.grid)
        indices = self.get_piece_indexes(piece, index)
       # print(f'grid calculate_heuristics - {1}:', self.grid)
        #print(f'grid calculate_heuristics - {1.1}:', self.grid, '\n', self.h_pieces, '\n')
        # self.place_piece(piece,index=index, update_h_pieces=False)
        # ones_count = np.sum(piece.get_optimized_current_matrix() == 1, axis=0)
        # self.update_h_pieces()
        
       # print('la pieza tiene: ', ones_count, ' unos, pieza: ', piece.get_optimized_current_matrix())
       # print(f'grid calculate_heuristics - {1.2}:', self.grid, '\n', self.h_pieces, '\n')
       # print(f'grid calculate_heuristics - {2}:', self.grid)
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
        H = (a*self.find_h_piece_sum(indices), b*len(self.find_full_rows(indices)),
              c*self.find_holes(indices), d*self.find_gaps())
        
        self.__place_piece(indices=indices)
        self.update_h_pieces(add_zero_rows=False)
        #print(f'place piece: \n', self.grid)
        H_0 = (a*self.find_h_piece_sum(), b*len(self.find_full_rows()),
              c*self.find_holes(), d*self.find_gaps())
        self.unplace_piece(indices=indices, update_h_pieces=False)
        self.update_h_pieces(add_zero_rows=False)

        H=H_0   
        #print(f'grid calculate_heuristics - {3}:\n', self.grid)
        # ===================================#
        #print('la suma da esto======: ', sum(H))
        # print('\nheuristica:\n', H)
        # print('\nheuristica_0:\n', H_0)
        # print('=======================')
        # Quita la pieza de la cuadrícula
        #self.unplace_piece(indices, update_h_pieces=False)
        #self.update_h_pieces()
        #print(f'grid calculate_heuristics - {4}:\n', self.grid)
        if indices ==  [(16, 8), (17, 8),(18, 8),(19, 8)]:
            print('indices:', indices, 'H:', H, 'sum: ', sum(H), 'H_0:', H_0, 'sum_0:', sum(H_0))
        
        return H, indices, H_0

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

