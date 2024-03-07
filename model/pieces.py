import numpy as np


legos = {
    "Cian_l": [
                [[0,0,0,0], 
                 [0,0,0,0], 
                 [1,1,1,1], 
                 [0,0,0,0]],

                [[0,1,0,0],
                 [0,1,0,0],
                 [0,1,0,0],
                 [0,1,0,0]],

                [[0,0,0,0], 
                 [1,1,1,1], 
                 [0,0,0,0], 
                 [0,0,0,0]],

                [[0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0],
                 [0,0,1,0]]
                 ],
    "Fucsia_T":[
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
          
    ],
    "Green_S": [
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
    ],
    "Orange_L":[
        [[0,0,0],
         [0,0,1],
         [1,1,1]],

        [[0,1,1],
         [0,0,1],
         [0,0,1]],

        [[1,1,1],
         [1,0,0],
         [0,0,0]],
         
        [[1,0,0],
         [1,0,0],
         [1,1,0]],
    ],
    "Purple_L":[
        [[0,0,0],
         [1,0,0],
         [1,1,1]],

        [[0,0,1]
        ,[0,0,1]
        ,[0,1,1]],

        [[1,1,1]
        ,[0,0,1]
        ,[0,0,0]],

        [[1,1,0]
        ,[1,0,0]
        ,[1,0,0]],
    ],

    "Red_Z":[
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
       
    ],
    "Yellow_sq":[
        [[1,1],
         [1,1]]
    ]
        
}


class Piece:
    current_shape = 0
    def __init__(self):
        self.shapes = np.array([[]])

    def get_shape(self, i=None):
        if i is not None:
            return self.__get_i_shape(i)
        return self.shapes[self.current_shape if i is None else i]

    def __get_i_shape(self, i):
        # print('i: ', i, type(i), ' len shapes: ', len(self.shapes), type(self.shapes))
        if len(self.shapes) == 0 or i < 0 or i >= len(self.shapes):
            return None
        return self.shapes[i]

    def get_len_shapes(self):
        return len(self.shapes)

    def spin_left(self):
        self.current_shape = (self.current_shape - 1) % len(self.shapes)
        return self

    def spin_right(self):
        self.current_shape = (self.current_shape + 1) % len(self.shapes)
        return self
    
    def spin_180(self):
        self.current_shape = (self.current_shape + 2) % len(self.shapes)
        return self

    def __str__(self, i=None):
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
        self.shapes = np.array(
            legos[self.__class__.__name__]
        )

class Fucsia_T(Piece):
    def __init__(self):
        self.shapes = np.array(
            legos[self.__class__.__name__]
        )

class Green_S(Piece):
    def __init__(self):
        self.shapes = np.array(
            legos[self.__class__.__name__]
        )

class Orange_L(Piece):
    def __init__(self):
        self.shapes = np.array(
            legos[self.__class__.__name__]
        )

class Purple_L(Piece):
    def __init__(self):
        self.shapes = np.array(
            legos[self.__class__.__name__]
        )

class Red_Z(Piece):
    def __init__(self):
        self.shapes = np.array(
            legos[self.__class__.__name__]
        )


class Yellow_sq(Piece):
    def __init__(self):
        self.shapes = np.array(
            legos[self.__class__.__name__]
        )




c1 = Cian_l()
# print(c1.current_shape)

print(c1)


# A2= [[0, 0, 0, 0],[0, 0, 0, 0],[1, 1, 1, 1],[0, 0, 0, 0]]

# A2_l= len(A2)

# print(A2_l)
# index = 0

# print('reset para -1: ', (-1) % len(A2))
