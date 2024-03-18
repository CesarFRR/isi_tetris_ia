from cgi import test
from view.Classifier import Classifier
from view.Framer import Framer
from view.ScreenShot import ScreenShot
from model.Grid import Grid
from model.Pieces import Fucsia_T, Piece, Orange_L, Green_S, Yellow_sq, Purple_L, Red_Z, Cian_l
from controller.Managers import HoldManager, NextManager, GridManager
import numpy as np


def generate_actions(best_option, piece:Piece, grid:Grid):
    """Genera las acciones necesarias para mover la pieza a la mejor opción."""
    actions = []
    # Mover la pieza a la izquierda o derecha
    #print("best_option: ", best_option, "piece.grid_position: ", piece.grid_position, "piece.current_shape: ", piece.current_shape)
    # Rotar la pieza
    current = piece.current_shape

    while best_option[2] != current:
        #print('current: ', current, 'best_option[2]: ', best_option[2])
        if best_option[2] < current:
            actions.append("spin_left")
            current = (current - 1) % 4
        elif best_option[2] > current:
            actions.append("spin_right")
            current = (current + 1) % 4

    
        #print('while 0')
        #print('current: ', current, 'best_option[2]: ', best_option[2])
    piece.set_current_shape(current)

    if best_option[1] < piece.grid_position:
        grid_pos = piece.grid_position
        while best_option[1] != grid_pos:
            #print('while 1')
            #print('grid_pos: ', grid_pos, 'best_option[1]: ', best_option[1])
            actions.append("move_left")
            grid_pos -= 1
        #print('grid_pos: ', grid_pos, 'best_option[1]: ', best_option[1])

    elif best_option[1] > piece.grid_position:
        grid_pos = piece.grid_position
        while best_option[1] != grid_pos:
            #print('while 2')
            #print('grid_pos: ', grid_pos, 'best_option[1]: ', best_option[1])
            actions.append("move_right")
            grid_pos += 1
       # print('grid_pos: ', grid_pos, 'best_option[1]: ', best_option[1])
    # Bajar la pieza
    actions.append("drop_hard")
    return actions


grid_test = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
])
# #print(grid_test)
h_pieces = np.array([6, 5, 4, 6, 6, 3, 5, 1, 0, 6], dtype=np.int8)
g= Grid()
g.grid = grid_test
grid_m = GridManager()
grid_m.set_grid(g)

#grid_m.grid.update_h_pieces()


p = Cian_l()
full_rows = 0
holes = 0
gaps = 6
aggregate_height = 13
props = {"full_rows": full_rows, "holes": holes, "gaps": gaps, "aggregate_height": aggregate_height, "h_pieces": h_pieces}
def print_props(props):
    for i, j in props.items():
        print(i+':')
        print(j)
print('=======================================')

print('test grid')

print('=======================================')

print('Grid antes:\n')
print(grid_m.get_grid())
print('props:')
print_props(props)


print('h_pieces Grid class:')

grid_m.grid.update_h_pieces()

print(grid_m.grid.h_pieces)

print('Aplicando get_best_choice:')

results_1 = grid_m.get_best_choice(p)

print(results_1)


print(generate_actions(results_1, p, grid_m.grid))

def print_grid(grid):
    for row in grid:
        for col in row:
            print(col, end=" ")
        print()
g2= np.array(grid_test.copy(), dtype=object)
g2[0][0] = 'X'

print_grid(g2)
