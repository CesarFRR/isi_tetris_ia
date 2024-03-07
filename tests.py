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
    
    c1 = Controls()


    # time.sleep(7)

    # c1.drop_hard()
    # c1.hold_move()
    
    # c1.spin_left()

    # print("teclas presionadas")
    # time.sleep(7)


    c1.login()
    time.sleep(1)

    c1.play_40_l()
    print("login!!")

    time.sleep(10)
    for i in range(15):
        c1.spin_180()
        if i % 2 == 0:
            c1.spin_left()
            c1.move_left()
            c1.spin_left()
            c1.move_left()
            c1.spin_left()
            c1.move_left()
            c1.move_right()
            c1.move_right()
        else:
            c1.spin_right()
            c1.move_right()
            c1.spin_right()
            c1.move_right()
            c1.spin_right()
            c1.move_right()
            c1.move_left()
            c1.move_left()
        
        c1.spin_180()
        
        c1.spin_180()
        c1.drop_hard()



#controls_test()
framer_test()

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
