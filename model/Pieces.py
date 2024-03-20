import numpy as np


legos = {
    "Cian_l": np.array([
                [[0,0,0,0], 
                 [0,0,0,0], 
                 [1,1,1,1], 
                 [0,0,0,0]],

                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]],

                [[0,0,0,0], 
                 [1,1,1,1], 
                 [0,0,0,0], 
                 [0,0,0,0]],

                [[0,1,0,0],
                 [0,1,0,0],
                 [0,1,0,0],
                 [0,1,0,0]],


                 ], dtype=np.int8),
    "Fucsia_T":np.array([
        [[0,1,0],
         [1,1,1],
         [0,0,0]],

        [[0,1,0],
         [0,1,1],
         [0,1,0]],

        [[0,0,0],
         [1,1,1],
         [0,1,0]],

        [[0,1,0],
         [1,1,0],
         [0,1,0]],
          
    ], dtype=np.int8),
    "Green_S": np.array([
        [[0,0,0],
         [0,1,1],
         [1,1,0]],

        [[0,1,0],
         [0,1,1],
         [0,0,1]],

        [[0,1,1],
         [1,1,0],
         [0,0,0]],

        [[1,0,0],
         [1,1,0],
         [0,1,0]]
    ],  dtype=np.int8),
    "Orange_L":np.array([
        [[0,0,1],
         [1,1,1],
         [0,0,0]],
         
        [[0,1,0],
         [0,1,0],
         [0,1,1]],

        [[0,0,0],
         [1,1,1],
         [1,0,0]],

        [[1,1,0],
         [0,1,0],
         [0,1,0]],

    ], dtype=np.int8),
    "Purple_L":np.array([
        [[1,0,0],
         [1,1,1],
         [0,0,0]],

        [[0,1,1],
         [0,1,0],
         [0,1,0]],

        [[0,0,0],
         [1,1,1],
         [0,0,1]],

        [[0,1,0]
        ,[0,1,0]
        ,[1,1,0]],


    ], dtype=np.int8),

    "Red_Z": np.array([
        [[0,0,0],
         [1,1,0],
         [0,1,1]],

        [[0,0,1]
        ,[0,1,1]
        ,[0,1,0]],

        [[1,1,0]
        ,[0,1,1]
        ,[0,0,0]],

        [[0,1,0]
        ,[1,1,0]
        ,[1,0,0]]
       
    ], dtype=np.int8),
    "Yellow_sq": np.array([
                [[0,0,0,0], 
                 [0,1,1,0], 
                 [0,1,1,0], 
                 [0,0,0,0]],
    ], dtype=np.int8)
        
}


class Piece:


    current_shape = 0
    """Indica el shape actual que se esta utilizando, entiendase por shape al estado (en que está girado) actual de la pieza (matriz 2D)"""
    computable_shapes=1
    """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
    zero_columns = None
    shapes = None
    optimized_current_shape = None
    grid_position = 3
    """Importante: Da la posicion (de 0 a 9 en el tablero) en la que se encuentra la pieza, esto es importante para el calculo de los estados, ya que se debe saber en que posicion se encuentra la pieza en el tablero para calcular los estados posibles de la pieza en el tablero. La mayoria de piezas lo tienen en 3 (pos 4 de las 10 columnas)"""
    def __init__(self):
        pass

    def set_current_shape(self, i):
        if i != self.current_shape:
            self.current_shape = i
            self.optimized_current_shape = self.trim_zeros()
        return self
    
    def trim_zeros(self, i=None):
        # Obtén el shape actual

        shape = self.shapes[self.current_shape if i == None else i]

        # Encuentra los índices de los elementos no cero
        indices = np.argwhere(shape)

        # Encuentra los límites de las filas y columnas
        row_start, col_start = indices.min(axis=0)
        row_end, col_end = indices.max(axis=0) + 1

        # Crea un nuevo array con los elementos no cero
        trimmed_shape = shape[row_start:row_end, col_start:col_end]

        if col_start == 0:
            self.grid_position = 3
        else:
            self.grid_position = 3 + col_start

        return trimmed_shape
    def get_optimized_current_matrix(self, i=None):
        if i is not None:
            return self.trim_zeros(i)
        return self.optimized_current_shape
    
    def update_grid_position(self):
        self.grid_position = 3 + self.__get_first_nonzero_column(self.shapes[self.current_shape])
        return self
    
    def calculate_iterations(self):
        # Calcula la posición y de la pieza
        p = self.get_optimized_current_shape()
        w_piece = p.shape[0] if p.ndim == 1 else p.shape[1]
        return 10 - (w_piece -1)
    
    def __get_first_nonzero_column(self, shape):
        return np.argmax(np.any(shape, axis=0))
    
    def __get_first_nonzero_column_reverse(self, shape):
        return np.argmax(np.any(np.fliplr(shape), axis=0))



    def get_matrix(self, i=None):
        if i is not None:
            return self.__get_i_shape(i)
        return self.shapes[self.current_shape]

    def __get_i_shape(self, i):
        # #print('i: ', i, type(i), ' len shapes: ', len(self.shapes), type(self.shapes))
        if len(self.shapes) == 0 or i < 0 or i >= len(self.shapes):
            return None
        return self.shapes[i]

    def get_len_shapes(self):
        return len(self.shapes)
    
    def get_computable_shapes(self):
        return self.computable_shapes

    def spin_left(self):
        self.current_shape = (self.current_shape - 1) % len(self.shapes)
        self.optimized_current_shape = self.trim_zeros()
        return self

    def spin_right(self):
        self.current_shape = (self.current_shape + 1) % len(self.shapes)
        self.optimized_current_shape = self.trim_zeros()
        return self
    
    def spin_180(self):
        self.current_shape = (self.current_shape + 2) % len(self.shapes)
        self.optimized_current_shape = self.trim_zeros()
        return self

    def __str__(self, i=None, class_name=None):
        if class_name is not None:
            return " " + class_name + "\n"
        shape_str = (
            str(self.__get_i_shape(self.current_shape if i == None else i))
            if len(self.shapes) > 0
            else " []"
        )
        return " " + shape_str[1:-1] + "\n"

    def print_shape(self, i=None):
        print(self.__str__(i))

class Cian_l(Piece):
    def __init__(self):
        self.shapes = legos[self.__class__.__name__].copy()
        
        self.computable_shapes=2
        """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
        self.optimized_current_shape = self.trim_zeros()
    def __str__(self):
        return super().__str__(class_name=self.__class__.__name__)
    

class Fucsia_T(Piece):
    def __init__(self):
        self.shapes = legos[self.__class__.__name__].copy()
        self.computable_shapes=4
        """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
        self.optimized_current_shape = self.trim_zeros()
    def __str__(self):
        return super().__str__(class_name=self.__class__.__name__)
        

class Green_S(Piece):
    def __init__(self):
        self.shapes = legos[self.__class__.__name__].copy()
        self.computable_shapes=2
        """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
        self.optimized_current_shape = self.trim_zeros()
    def __str__(self):
        return super().__str__(class_name=self.__class__.__name__)
    
class Orange_L(Piece):
    def __init__(self):
        self.shapes = legos[self.__class__.__name__].copy()
        self.computable_shapes=4
        """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
        self.optimized_current_shape = self.trim_zeros()

    def __str__(self):
        return super().__str__(class_name=self.__class__.__name__)

class Purple_L(Piece):
    def __init__(self):
        self.shapes = legos[self.__class__.__name__].copy()
        self.computable_shapes=4
        """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
        self.optimized_current_shape = self.trim_zeros()

    def __str__(self):
        return super().__str__(class_name=self.__class__.__name__)

class Red_Z(Piece):
    def __init__(self):
        self.shapes = legos[self.__class__.__name__].copy()
        self.computable_shapes=2
        """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
        self.optimized_current_shape = self.trim_zeros()
        
    def __str__(self):
        return super().__str__(class_name=self.__class__.__name__)


class Yellow_sq(Piece):
    def __init__(self):
        self.shapes = legos[self.__class__.__name__].copy()
        self.computable_shapes=1
        """Indica cuales shapes son necesarios para cada calculo de estados en la busqueda, es decir que los demás shapes son redundantes y no necesarios para el calculo."""
        self.optimized_current_shape = self.trim_zeros()
        self.grid_position = 4

    def __str__(self):
        return super().__str__(class_name=self.__class__.__name__)



# def get_first_nonzero_column(shape):
#     return np.argmax(np.any(shape, axis=0))

# # def trim_zeros(arr):
# #     # Obtén el shape actual
# #     shape = arr
# #     # Encuentra los índices de los elementos no cero
# #     indices = np.argwhere(shape)

# #     # Encuentra los límites de las filas y columnas
# #     row_start, col_start = indices.min(axis=0)
# #     row_end, col_end = indices.max(axis=0) + 1

# #     # Crea un nuevo array con los elementos no cero
# #     trimmed_shape = shape[row_start:row_end, col_start:col_end]

# #     return trimmed_shape

# c1 = Red_Z ()
# #print(c1.current_shape)
# #print(c1)


# # A2= [[0, 0, 0, 0],[0, 0, 0, 0],[1, 1, 1, 1],[0, 0, 0, 0]]

# # A2_l= len(A2)

# # #print(A2_l)
# # index = 0

# # #print('reset para -1: ', (-1) % len(A2))
# # #print(c1.optimized_current_shape)
# # #print(c1.optimized_current_shape.shape)
# # c1.spin_right()
# # #print('1 vertical:\n',c1)

# # #print(c1.optimized_current_shape)
# # #print(c1.optimized_current_shape.shape)
# # #print('\n')

# #print('TRIMED: \n', c1.trim_zeros())
# #print('\n')

# #print(c1.optimized_current_shape)

# #print('\n')
# c1.spin_right()
# #print('1 vertical:\n',c1)
# #print('\n')
# #print('\nNumeor de col con ceros: ', get_first_nonzero_column(c1.get_shape()))

# # #print('TRIMED: \n', c1.trim_zeros())
# # #print('\n')


# def #print_shape(shape):
#     for row in shape:
#         #print(" ".join(str(int(cell)) for cell in row))
#     #print('\n')
# # Tu figura
# shape = np.array([[0,1,0],
#                   [1,1,1],
#                   [0,0,0]])

# # Crea una matriz 4x4 llena de ceros
# new_shape = np.array([[0,1,0,0],
#                [0,1,0,0],
#                [0,1,0,0],
#                [0,1,0,0]])

# # Posiciona la figura en la matriz 4x4
# #print_shape(new_shape)
# #print('\nNumeor de col con ceros: ', get_first_nonzero_column(new_shape))
# #print('\n')
# rot90 = np.rot90(new_shape)

# #print_shape(rot90)
# #print('\nNumeor de col con ceros: ', get_first_nonzero_column(rot90))
# rot90 = np.rot90(rot90)

# #print_shape(rot90)
# #print('\nNumeor de col con ceros: ', get_first_nonzero_column(rot90))

# rot90 = np.rot90(rot90)

# #print_shape(rot90)
# #print('\nNumeor de col con ceros: ', get_first_nonzero_column(rot90))

# rot90 = np.rot90(rot90)

# #print_shape(rot90)
# #print('\nNumeor de col con ceros: ', get_first_nonzero_column(rot90))
