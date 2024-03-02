from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os
# Inicializa el self.driver del navegador (en este caso, Chrome)





class Controls:
    def __init__(self, url = 'https://tetr.io/'):
        load_dotenv()
        # Inicializa el self.driver del navegador (en este caso, Chrome)
        self.url = url
        self.browser_time = os.getenv('BROWSER_TIME_LOADING')
        # Inicializa el self.driver de Selenium correspondiente
        self.browser_name = os.getenv('BROWSER')
        self.driver = self.get_browser()
        print('\nBROWSER:',self.browser_name)
        # Maximiza la ventana del navegador
        self.driver.maximize_window()

        # Navega a la página web
        self.driver.get('https://tetr.io/')

        # Espera 7 segundos
        time.sleep(int(self.browser_time))
        print("aplicando zoom con script")
        zoom = os.getenv('BROWSER_ZOOM')
        # Ejecuta un script JavaScript para ajustar el nivel de zoom al 70%
        self.driver.execute_script(F"document.body.style.zoom='{zoom if zoom is not None else 100}%'")

        # Imprime un mensaje
        print("Zoom aplicado al 70%")
        
        # Ejecuta un script JavaScript para obtener el nivel de zoom actual
        zoom_level = self.driver.execute_script("return document.body.style.zoom")

        # Imprime el nivel de zoom
        print(f"Nivel de zoom: {zoom_level}")
        time.sleep(1)

    def get_browser(self):

        driver = None
        if self.browser_name == 'EDGE':
            driver = webdriver.Edge()
        elif self.browser_name == 'CHROME':
            driver = webdriver.Chrome()
        elif self.browser_name == 'FIREFOX':
            driver = webdriver.Firefox()
        elif self.browser_name == 'INTERNET_EXPLORER':
            driver = webdriver.Ie()
        elif self.browser_name == 'SAFARI':
            driver = webdriver.Safari()
        else:
            bp, cv = os.getenv('BROWSER_PATH'), os.getenv('CHROMIUM_VERSION')
            if bp != 'NONE' and cv != 'NONE':
                options = webdriver.ChromeOptions()
                options.binary_location = bp
                driver_version = cv
                driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version).install()), options=options)
            else:
                print(f'Browser "{self.browser_name}" no soportado, iniciando con Edge por defecto.')
                driver = webdriver.Edge()
        return driver
    
    def login(self):
        # Localiza el elemento con el ID 'entry_username'
        
        username_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'entry_username'))
        )

        # Introduce 'cesar12321' y presiona ENTER
        username_input.send_keys('cesar12321' + Keys.ENTER)

        # Espera a que aparezca el elemento con el ID 'askregister_anon'
        register_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'askregister_anon'))
        )

        # Hace clic en el elemento con el ID 'askregister_anon' utilizando JavaScript
        self.driver.execute_script("arguments[0].click();", register_button)
        time.sleep(1)

    

    def play_40_l(self):
        # Encuentra el div con id 'play_solo' y haz clic en él
        play_solo_button = self.driver.find_element(By.ID, 'play_solo')
        self.driver.execute_script("arguments[0].click();", play_solo_button)
        time.sleep(1)
        # Espera hasta que aparezca el div con id 'game_40l'
        game_40l_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'game_40l')))
        self.driver.execute_script("arguments[0].click();", game_40l_button)
        # Espera 3 segundos
        time.sleep(1)

        # Espera hasta que aparezca el div con id 'start_40l' y haz clic en él
        start_40l_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'start_40l')))
        self.driver.execute_script("arguments[0].click();", start_40l_button)
        print("play 40 lines !!")
        time.sleep(2)
        self.focus()


    def focus(self):
        # Espera hasta que aparezca el elemento con id 'nofocus'
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('f')
        
        print("focus!!")

    def drop_hard(self):
        # Presiona la tecla Space para realizar una caída rápida
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        print("tecla espacio") 
    def drop_soft(self):
        # Presiona la tecla Space para realizar una caída rápida
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_DOWN)
        print("tecla  arrow down") 

    def spin_left(self):
        # Presiona la tecla Z para girar a la izquierda
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('z')
        print("tecla z") 

    def spin_right(self):
        # Presiona la tecla x para girar a la derecha
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('x')
        print("tecla x") 

    def move_left(self):
        # Presiona la tecla izquierda para mover la pieza a la izquierda
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_LEFT)
        print("tecla arrow left") 

    def move_right(self):
        # Presiona la tecla derecha para mover la pieza a la derecha
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
        print("tecla arrow right")
    def hold_move(self):
        # Presiona la tecla c para guardar la pieza actual
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('c')
        print("tecla c")
    def spin_180(self):
        # Presiona la tecla a para girar la pieza a 180 grados
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('a')
        print("tecla a")
    

# c1 = Controls()


# # time.sleep(7)

# # c1.drop_hard()
# # c1.hold_move()
# # c1.spin_180()
# # c1.spin_left()

# # print("teclas presionadas")
# # time.sleep(7)


# c1.login()
# time.sleep(1)

# c1.play_40_l()
# print("login!!")

# # time.sleep(7)