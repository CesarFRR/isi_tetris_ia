from view.ScreenShot import ScreenShot
import cv2
import numpy as np
from model.Grid import Grid
from model.Pieces import Green_S
from control.Managers import GridManager
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
    print(f"Bordes central: {bordes_central}")
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

    print('PREDICHAS 2 A 4: ', predichas)

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
    print(f"Coordenadas del Grid: {coordenadas_grid}")
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


def controls_test():
    from view.Controls import Controls
    import time
    from view.Framer import Framer
    from view.Classifier import Classifier
    
    ctr = Controls()
    fr = Framer()
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
    ss = ScreenShot()
    ctr.focus()
    #imagenFile = cv2.imread("./data/tests/tetris_full4.jpg")
    #print("\nimagenFile dimensiones: ", imagenFile.shape)

    imgagen_mss= ss.capture()
    print("\nimagen_mss dimensiones: ",imgagen_mss.shape)
    print("\n")
    fr.encontrar_bordes_centrales(imgagen_mss)
    coord_next = fr.obtener_next(fr.encontrar_bordes_centrales(imgagen_mss))
    predichas = cls.predict_pieces(imgagen_mss, [1, 5], coord_next)
    print('PREDICHAS_control test:\n\n ', predichas)
    #coord_next_2= fr.obtener_next(fr.encontrar_bordes_centrales(imagenFile))
    #predichas2 = cls.predict_pieces(imagenFile, [1, 5], coord_next_2)

    #print('PREDICHAS_ tetris full 4--> :\n\n ', predichas)
    cv2.imshow("imagen", imgagen_mss)
    cv2.waitKey(0)
    # print("login!!")
    # time.sleep(2)

    time.sleep(10)
    print("sleep de 10 superado!")

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



#controls_test()
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




g1 = Grid()
# Añade algunas piezas de Tetris en la parte inferior de la cuadrícula
print(g1.grid)

g1.print_shape()
print('\n')

grid_test = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 0, 0, 0]
])
print(grid_test)
h_pieces = np.zeros(grid_test.shape[1], dtype=np.int8)
for col in range(grid_test.shape[1]):
    h_pieces[col] = np.argmin(grid_test[::-1, col] == 1)

print('grid local: h_pieces: \n',h_pieces)
g1.grid = grid_test
g1.h_pieces = h_pieces
g1.update_h_pieces()
print('\n')
print(g1.grid)
p1 = Green_S()

gm = GridManager()
gm.set_grid(g1)
heuristics_list = gm.compute_piece(p1)
