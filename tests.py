from calendar import c
import os
from view.ScreenShot import ScreenShot
import cv2
import numpy as np
from model.Grid import Grid
import model.Pieces
from controller.Managers import GridManager, NextManager, HoldManager
import time
from  view.Texts import *
from dotenv import load_dotenv
load_dotenv()

def framer_test():
    from view.Framer import Framer
    from view.Classifier import Classifier
    import cv2

    # Ejemplo de uso
    fr = Framer()
    imagen = cv2.imread("./data/tests/tetris_ss.jpg")
    bordes_central = fr.encontrar_bordes_centrales(imagen)

    # Guardar la imagen recortada
    # cv2.imwrite("imagen_tetris_recortada.jpg", imagen_recortada)
    #print(f"Bordes central: {bordes_central}")
    cv2.imshow(
        "Imagen recortada",
        imagen[
            bordes_central[0] : bordes_central[1], bordes_central[2] : bordes_central[3]
        ],
    )
    cv2.waitKey(0)

    # # Ejemplo de uso
    coordenadas_next = fr.obtener_next(bordes_central)

    next_img = imagen[
        coordenadas_next[0] : coordenadas_next[1], coordenadas_next[2] : coordenadas_next[3]
    ]


    # cv2.imshow("Imagen Next_0", next_img)
    # cv2.waitKey(0)
    cls = Classifier()

    predichas =  cls.predict_pieces(imagen, [3, 4], coordenadas_next)

    #print('PREDICHAS 2 A 4: ', predichas)

    # for i in range(1, 6):

    #     print(f"Coordenadas del Next: {coordenadas_next}")
    #     imagen_next = imagen[
    #         coordenadas_next[0]
    #         + int(
    #             (coordenadas_next[1] - coordenadas_next[0]) * ((i - 1) / 5)
    #         ) : coordenadas_next[0]
    #         + int((coordenadas_next[1] - coordenadas_next[0]) * (i / 5)),
    #         coordenadas_next[2] : coordenadas_next[3],
    #     ]

    #     # Calcula las coordenadas del centro de la imagen
    #     centro_y, centro_x = imagen_next.shape[0] // 2, imagen_next.shape[1] // 2

    #     # Pone un pixel blanco en el centro de la imagen
    #     print(f"color centro: {imagen_next[centro_y, centro_x]}")
    #     imagen_next[centro_y, centro_x] = [255, 255, 255]
    #     print(f"precedir color lego: ", cls.predict_piece(imagen_next))
    #     cv2.imshow("Imagen Next", imagen_next)
    #     cv2.waitKey(0)

    # cls.predict_pieces(imagen, 5, coordenadas_next)

    coordenadas_grid = fr.obtener_grid(bordes_central)
    #print(f"Coordenadas del Grid: {coordenadas_grid}")
    imagen_grid = imagen[coordenadas_grid[0]:coordenadas_grid[1],
                                coordenadas_grid[2]:coordenadas_grid[3]]
    cv2.imshow("Imagen Grid", imagen_grid)
    cv2.waitKey(0)

    # # Ejemplo de uso

    # coordenadas_hold = fr.obtener_hold(bordes_central)
    # print(f"Coordenadas del Hold: {coordenadas_hold}")
    # imagen_hold = imagen[coordenadas_hold[0]:coordenadas_hold[1],
    #                             coordenadas_hold[2]:coordenadas_hold[3]]
    # cv2.imshow("Imagen Hold", imagen_hold)
    # cv2.waitKey(0)

def generate_actions(best_option, piece:model.Pieces.Piece, grid:Grid):
    """Genera las acciones necesarias para mover la pieza a la mejor opción."""
    actions = []
    # Mover la pieza a la izquierda o derecha
    #print("best_option: ", best_option, "piece.grid_position: ", piece.grid_position, "piece.current_shape: ", piece.current_shape)
    # Rotar la pieza
    piece.set_current_shape(0)
    
    while best_option[2] != piece.current_shape:
        #print('current: ', current, 'best_option[2]: ', best_option[2])
        
        if best_option[2] > piece.current_shape:
            actions.append("spin_right")
            piece.spin_right()
        #print('while 0')
        #print('current: ', current, 'best_option[2]: ', best_option[2])
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


def controls_test():
    from view.Controls import Controls
    import time
    from view.Framer import Framer
    from view.Classifier import Classifier
    
    ctr = Controls()
    
    ss = ScreenShot()
    cls = Classifier()
    # time.sleep(7)

    # c1.drop_hard()
    # c1.hold_move()
    
    # c1.spin_left()

    # print("teclas presionadas")
    # time.sleep(7)

    ctr.login()
    time.sleep(1)

    ctr.play_40_l()
    #imagenFile = cv2.imread("./data/tests/tetris_full4.jpg")
    #print("\nimagenFile dimensiones: ", imagenFile.shape)

    # aqui comienza el screenshot y los managers
    img_0= ss.capture()
    #cv2.imshow("imagen", img_0)
    cv2.waitKey(0)
    fr = Framer(img=img_0)
    fr.encontrar_bordes_centrales()

    next_m, grid_m, hold_m = NextManager(img_0, fr.obtener_next()), GridManager(), HoldManager()
    def print_grid(grid):
        for row in grid:
            for col in row:
                print(col, end=" ")
            print()
        
    # imgagen_mss= ss.capture()
    # print("\nimagen_mss dimensiones: ",imgagen_mss.shape)
    # print("\n")
    # fr.encontrar_bordes_centrales(imgagen_mss)
    # coord_next = fr.obtener_next(fr.encontrar_bordes_centrales(imgagen_mss))
    # predichas = cls.predict_pieces(imgagen_mss, [1, 5], coord_next)
    # print('PREDICHAS_control test:\n\n ', predichas)
    # #coord_next_2= fr.obtener_next(fr.encontrar_bordes_centrales(imagenFile))
    # #predichas2 = cls.predict_pieces(imagenFile, [1, 5], coord_next_2)

    # #print('PREDICHAS_ tetris full 4--> :\n\n ', predichas)
    # cv2.imshow("imagen", imgagen_mss)
    # cv2.waitKey(0)
    # # print("login!!")
    # # time.sleep(2)

    # print("sleep de 10 superado!")
    # print('next list: ', next_m.get_next_list())
    

    time.sleep(9)
    print("COMENZANDO A JUGAR")
    print("Desde aqui se empieza a jugar, los tiempos y el time de 9s son necesarios, no removerlos")
    print("=========================================")
    play= True
    current_piece = next_m.pop_piece()
    print('POP!!!##=====>', current_piece)
    print("current_piece: ", current_piece)

    piece = getattr(model.Pieces, current_piece)()
    #print("piece: ", piece, type(piece))
    best_choice= grid_m.get_best_choice(piece)
    print("best choice: ", best_choice)
    actions = generate_actions(best_choice, piece, grid_m.grid)
   # print("actions: ", actions)
    # ctr.perform_actions(actions)
    # grid_m.place_piece(piece, best_choice[1], best_choice[2])
    # grid_m.update_grid()
    # next_m.update()
    #print_grid(0)
    while(play):
        #print_grid(2)
        print('next list: ', next_m.get_next_list())
        current_piece = next_m.pop_piece()
        print('POP!!!##=====>', current_piece)
        # next_m.update()
        print("\ncurrent_piece: ", current_piece)
        piece = getattr(model.Pieces, current_piece)()
        #print_grid(3)
        best_choice= grid_m.get_best_choice(piece)
        score, pos, rotation, indices= best_choice
        best_choice = (score, pos, rotation)
        print("best choice: ", best_choice)
        actions = generate_actions(best_choice, piece, grid_m.grid)
        print("actions: ", actions)
        #time.sleep(2)
        #actions do--> TODO
        #print("actions: ", actions)
        ctr.perform_actions(actions)
        #print_grid(5)
        #grid_m.place_piece (piece, best_choice[1], best_choice[2])
        grid_m.place_piece(piece, pos, rotation)
        #print_grid(6)
        grid_m.update_grid()
        view_grid = np.array(grid_m.grid.grid.copy(), dtype=object)
        for r, c in indices:
            view_grid[r, c] = 'X'
        print('grid_m.grid: \n')
        print_grid(view_grid)
        if ctr.check_game_over():
            play= False
            print(txt_game_over)
        #print('\nh_pieces:\n', grid_m.grid.h_pieces)
        #print_grid(99)
        time.sleep(0)




    time.sleep(5)


    # for i in range(15):
    #     c1.spin_180()
    #     if i % 2 == 0:
    #         c1.spin_left()
    #         c1.move_left()
    #         c1.spin_left()
    #         c1.move_left()
    #         c1.spin_left()
    #         c1.move_left()
    #         c1.move_right()
    #         c1.move_right()
    #     else:
    #         c1.spin_right()
    #         c1.move_right()
    #         c1.spin_right()
    #         c1.move_right()
    #         c1.spin_right()
    #         c1.move_right()
    #         c1.move_left()
    #         c1.move_left()
        
    #     c1.spin_180()
        
    #     c1.spin_180()
    #     c1.drop_hard()



controls_test()
# framer_test()

# grid = [[0 for _ in range(10)] for _ in range(20)]

# # Imprimir la matriz de manera organizada
# for row in grid:
#     print(row)
        

# import numpy as np

# def print_matrix(A):
#     for row in A:
#         print(row)

# piece_L = np.array([
#     [0, 0, 0, 0],
#     [1, 1, 1, 1],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0]
# ])

# print("Original:")
# print_matrix(piece_L)

# while True:
#     input("\nPresiona Enter para rotar la matriz...")
#     piece_L = np.rot90(piece_L, 3)
#     print("\nRotada:")
#     print_matrix(piece_L)


#controls_test()



# Añade algunas piezas de Tetris en la parte inferior de la cuadrícula
#print(g1.grid)

# #g1.print_shape()
# #print('\n')

grid_test = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
])
# #print(grid_test)
h_pieces = np.array([1, 1, 2, 2, 1, 2, 2, 1, 0, 1], dtype=np.int8)

full_rows = 0
holes = 0
gaps = 6
aggregate_height = 13

print('=======================================')

print('test grid')

print('=======================================')

print('h_pieces Grid class:')



# for col in range(grid_test.shape[1]):
#     h_pieces[col] = np.argmin(grid_test[::-1, col] == 1)

# #print('grid local: h_pieces: \n',h_pieces)
# # g1.grid = grid_test
# # g1.h_pieces = h_pieces
# g1.update_h_pieces()
# #print('\n')
# #print(g1.grid)





# import mss
# g1 = Grid()
# p1 = Fucsia_T()
# gm = GridManager()
# gm.set_grid(g1)
# start_time = time.time()
# ms = mss.mss()
# for i in range(1):
#     print('=========================================\n')
#     heuristics_list = gm.get_best_choice(p1)
#     print(heuristics_list )
#     ms.grab(ms.monitors[1])
#     print('=========================================\n')
# elapsed_time = time.time() - start_time
# print(f"El tiempo transcurrido es {elapsed_time} segundos")



# print('=========================================\n')
# print('a, b, c, d = ', os.getenv('H_A'), os.getenv('H_B'), os.getenv('H_C'), os.getenv('H_D'))


