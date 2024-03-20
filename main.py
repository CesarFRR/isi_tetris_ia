# ARCHIVO main.py, el "botón que inicia el programa"
def main():
    from controller.MainController import MainController
    main = MainController().start()

if __name__ == "__main__":
    main()