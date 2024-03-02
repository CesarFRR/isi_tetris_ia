from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Inicializa el driver del navegador (en este caso, Chrome)
driver = webdriver.Edge()



class Controls:
    def __init__(self):
        # Inicializa el driver del navegador (en este caso, Chrome)
        self.driver = webdriver.Edge()           
        # Maximiza la ventana del navegador
        self.driver.maximize_window()
        self.driver.execute_script("document.body.style.zoom='70%'")
        print("driver inicializado, zoom a 70%")

        # Abre la URL que quieres
        #self.driver.get('https://tetr.io/')
        self.driver.get('https://google.com/')

    def drop_hard(self):
        # Presiona la tecla Space para realizar una caída rápida
        self.driver.find_element(By.ID, 'body').send_keys(Keys.SPACE)
    def drop_soft(self):
        # Presiona la tecla Space para realizar una caída rápida
        self.driver.find_element(By.ID, 'body').send_keys(Keys.ARROW_DOWN)
    def spin_left(self):
        # Presiona la tecla Z para girar a la izquierda
        self.driver.find_element(By.ID, 'body').send_keys('z')
    def spin_right(self):
        # Presiona la tecla x para girar a la derecha
        self.driver.find_element(By.ID, 'body').send_keys('x')
    def move_left(self):
        # Presiona la tecla izquierda para mover la pieza a la izquierda
        self.driver.find_element(By.ID, 'body').send_keys(Keys.ARROW_LEFT)
    def move_right(self):
        # Presiona la tecla derecha para mover la pieza a la derecha
        self.driver.find_element(By.ID, 'body').send_keys(Keys.ARROW_RIGHT)
    def hold_move(self):
        # Presiona la tecla c para guardar la pieza actual
        self.driver.find_element(By.ID, 'body').send_keys('c')
    def spin_180(self):
        # Presiona la tecla a para girar la pieza a 180 grados
        self.driver.find_element(By.ID, 'body').send_keys('a')
    

c1 = Controls()


time.sleep(7)

c1.drop_hard()
c1.hold_move()
c1.spin_180()
c1.spin_left()

print("teclas presionadas")
time.sleep(7)
