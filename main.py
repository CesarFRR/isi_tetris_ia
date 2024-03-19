# ARCHIVO main.py, el "botón que inicia el programa"
import os
from view.ScreenShot import ScreenShot
import cv2
import numpy as np
from model.Grid import Grid
import model.Pieces
from controller.Managers import GridManager, NextManager, HoldManager
from  view.Texts import *
from dotenv import load_dotenv
load_dotenv()




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

            if best_option[2] ==2:
                actions.append("spin_180")
                piece.set_current_shape(2)
                break
            if best_option[2] == 3:
                actions.append("spin_left")
                piece.set_current_shape(3)
                break

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


def start():
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
    hold_m.grid_m = grid_m
    hold_m.ctr = ctr
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
    status = {"Used Pieces: ":0, "remaining holes: ":0, 'remaining height: ':0, "full rows: ":0}

    time.sleep(8.5)
    print("COMENZANDO A JUGAR")
    print("Desde aqui se empieza a jugar, los tiempos y el time de 9s son necesarios, no removerlos")
    print("=========================================")
    # time.sleep(0.5)
    play= True
    win = False
    print('next list: ', next_m.get_next_list())

    current_piece = next_m.pop_piece()
    current_piece_2 = next_m.pop_piece()
    piece = getattr(model.Pieces, current_piece)()
    hold_m.swap(piece)
    hold_m.update()
    
    next_m.update([4, 5])
    print('next list + (4,5): ', next_m.get_next_list())
    
    current_piece = current_piece_2
    print('POP!!!##=====>', current_piece)
    print("current_piece: ", current_piece)
    
    piece = getattr(model.Pieces, current_piece)()
    #print("piece: ", piece, type(piece))
    best_choice= grid_m.get_best_choice(piece)
    score, pos, rotation, indices= best_choice
    print("best choice: ", best_choice)
    actions = generate_actions(best_choice, piece, grid_m.grid)
   # print("actions: ", actions)
    ctr.perform_actions(actions)
    grid_m.place_piece(piece, best_choice[1], best_choice[2])
    grid_m.update_grid()
    #time.sleep(0.1)
    next_m.update()
    view_grid = np.array(grid_m.grid.grid.copy(), dtype=object)
    for r, c in indices:
        view_grid[r, c] = 'X'
    print('grid_m.grid: \n')
    print_grid(view_grid)
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

        if hold_m.get_score() > best_choice[0]:
            print("swapping")
            piece = hold_m.swap(piece)
            
            best_choice= hold_m.best_choice
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
        hold_m.update()
        next_m.update()
        view_grid = np.array(grid_m.grid.grid.copy(), dtype=object)
        for r, c in indices:
            view_grid[r, c] = 'X'
        print('grid_m.grid: \n')
        print_grid(view_grid)
        #time.sleep(0.1)
        if ctr.check_you_win():
            play= False
            win = True
            print(txt_you_win)
            break

        if ctr.check_game_over():
            play= False
            print(txt_game_over)
            break
        #print('\nh_pieces:\n', grid_m.grid.h_pieces)
        #print_grid(99)
        #time.sleep(0)
    if win:
        status["Used Pieces: "] = next_m.popped_pieces
        status["remaining holes: "] = grid_m.grid.find_holes()
        status['remaining height: '] = grid_m.grid.find_h_piece_sum()
        status["full rows: "] = grid_m.grid.full_rows_removed
        print(status)



    time.sleep(5)


start()