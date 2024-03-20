from model.IA import Tetris_IA
from view.ScreenShot import ScreenShot
import model.Pieces
from controller.Managers import GridManager, NextManager, HoldManager
from  view.Texts import txt_game_over, txt_you_win
from view.Controls import Controls
from view.Framer import Framer    

import time, platform, os
from dotenv import load_dotenv
load_dotenv()

class MainController:

    def __init__(self) -> None:
        pass

    def start(self):

        ctr = Controls(OS=platform.system())
        
        ss = ScreenShot()

        ctr.login()
        time.sleep(1)

        ctr.play_40_l()


        # aqui comienza el screenshot y los managers
        img_0= ss.capture()
        fr = Framer(img=img_0)
        fr.encontrar_bordes_centrales()

        next_m, grid_m= NextManager(img_0, fr.obtener_next()), GridManager()
        hold_m = HoldManager(ctr)
        IA = Tetris_IA(grid_m.grid, hold_m, next_m)
        hold_m.ia = IA

        status = {"Used Pieces: ":0, "remaining holes: ":0, 'remaining height: ':0, "full rows: ":0}

        time.sleep(8.5)
        print("COMENZANDO A JUGAR")
        print("Desde aqui se empieza a jugar, los tiempos y el time de 9s son necesarios, no removerlos")
        print("=========================================")
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
        best_choice= IA.get_best_choice(piece)
        score, pos, rotation, indices= best_choice
        print("best choice: ", best_choice)
        actions = ctr.generate_actions(best_choice, piece)
        ctr.perform_actions(actions)
        grid_m.place_piece(piece, best_choice[1], best_choice[2])
        grid_m.update_grid()
        next_m.update()

        #grid_m.print_grid(indices)
        while(play):
            print('\n\nnext list: ', next_m.get_next_list())
            current_piece = next_m.pop_piece()
            print('POP!!!=====>', current_piece)
            print("\ncurrent_piece: ", current_piece)
            piece = getattr(model.Pieces, current_piece)()
            best_choice= IA.get_best_choice(piece)
            score, pos, rotation, indices= best_choice
            best_choice = (score, pos, rotation)

            if hold_m.get_score() > best_choice[0]:
                print("swapping")
                piece = hold_m.swap(piece)
                
                best_choice= hold_m.best_choice
                score, pos, rotation, indices= best_choice
                best_choice = (score, pos, rotation)

            print("best choice: ", piece,  best_choice)
            actions = ctr.generate_actions(best_choice, piece)
            print("actions: ", actions)
            ctr.perform_actions(actions)
            grid_m.place_piece(piece, pos, rotation)
            grid_m.update_grid()
            hold_m.update()
            next_m.update()
            
            if ctr.check_you_win():
                play= False
                win = True
                print(txt_you_win)
                break

            if ctr.check_game_over():
                play= False
                print(txt_game_over)
                break
            self.clear_console()
            
        if win:
            status["Used Pieces: "] = next_m.popped_pieces
            status["remaining holes: "] = grid_m.grid.find_holes()
            status['remaining height: '] = grid_m.grid.find_h_piece_sum()
            status["full rows: "] = grid_m.grid.full_rows_removed
            print(status)
            grid_m.print_grid(indices)
            

        print("\nEl navegador se cerrará en 20 segundos, por favor no cerrar manualmente\n")

        time.sleep(20)

    def clear_console(self):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)


