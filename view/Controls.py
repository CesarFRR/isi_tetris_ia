from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from model.Pieces import Piece
import time
import os

options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')  # Esto ajusta el nivel de registro a ERROR

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""
"""Script de javascript para arrastrar y soltar un archivo en un elemento HTML.
Nota: Es el único método que funciona para arrastrar y soltar archivos del equipo al nevegador en Selenium (Marzo-2024)"""


class Controls:
    def __init__(self, url = 'https://tetr.io/', OS = 'Windows'):
        # Inicializa el self.driver del navegador (en este caso, Chrome)
        self.url = url
        self.OS = OS
        self.browser_time = os.getenv('BROWSER_TIME_LOADING')
        # Inicializa el self.driver de Selenium correspondiente
        self.browser_name = os.getenv('BROWSER')
        self.driver = self.get_browser()
        self.driver.maximize_window()

        # Navega a la página web
        self.driver.execute_script(F"document.body.style.zoom='80%'")
        self.driver.get('https://tetr.io/')
        # Espera n segundos
        time.sleep(int(self.browser_time))
        zoom = os.getenv('BROWSER_ZOOM')
        # Ejecuta un script JavaScript para ajustar el nivel de zoom al 70%
        self.driver.execute_script(F"document.body.style.zoom='{zoom if zoom is not None else 100}%'")
        # Ejecuta un script JavaScript para obtener el nivel de zoom actual
        zoom_level = self.driver.execute_script("return document.body.style.zoom")

        # Imprime el nivel de zoom
        print(f"Nivel de zoom: {zoom_level}")
        time.sleep(1)

    def get_browser(self):
        driver = None
        if self.OS == 'Linux' and not self.browser_name:
            options = webdriver.FirefoxOptions()
            options.add_argument('--private')
            # Ajusta el nivel de registro a ERROR para Firefox
            options.log.level = 'error'
            driver = webdriver.Firefox(options=options)
            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        if self.OS == 'Windows' and not self.browser_name:
            options = webdriver.EdgeOptions()
            options.add_argument('--incognito')
            options.add_argument('--log-level=3')  # Ajusta el nivel de registro a ERROR para Edge

            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
            return driver


        if self.browser_name == 'EDGE':
            options = webdriver.EdgeOptions()
            options.add_argument('--incognito')
            options.add_argument('--log-level=3')  # Ajusta el nivel de registro a ERROR para Edge

            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
        elif self.browser_name == 'CHROME':
            options = webdriver.ChromeOptions()
            options.add_argument('--log-level=3')  # Ajusta el nivel de registro a ERROR para Chrome
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
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
                options.add_argument('--incognito')
                options.binary_location = bp
                driver_version = cv
                driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version).install()), options=options)
            else:
                options.add_argument('--log-level=3')  # Ajusta el nivel de registro a ERROR para Edge
                driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
        return driver
    
    def check_game_over(self):
        try:
            list_request_scroller = self.driver.find_element(By.ID, "list_request_scroller")
            # Verifica si el elemento está visible
            if list_request_scroller.is_displayed():
                # Si el elemento aparece y está visible, establece play en False
                return True
            else:
                return False
        except Exception:
            return False
        
    def check_you_win(self):
        try:
            you_win = self.driver.find_element(By.ID, "result_header")
            # Verifica si el elemento está visible
            if you_win.is_displayed():
                # Si el elemento aparece y está visible, establece play en False
                return True
            else:
                return False
        except Exception:
            return False
        
    def login(self):
        # Localiza el elemento con el ID 'entry_username'
        
        username_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'entry_username'))
        )

        # Introduce 'CESAR12345' y presiona ENTER
        username_input.send_keys('CESAR12345' + Keys.ENTER)

        # Espera a que aparezca el elemento con el ID 'askregister_anon'
        register_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'askregister_anon'))
        )

        # Hace clic en el elemento con el ID 'askregister_anon' utilizando JavaScript
        self.driver.execute_script("arguments[0].click();", register_button)
        time.sleep(1)

    def drag_and_drop_file(self, drop_target, path):
        driver = drop_target.parent
        file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
        file_input.send_keys(path)

    def play_40_l(self):
        # Encuentra el div con id 'play_solo' y haz clic en él
        # Ruta del archivo a arrastrar
        
        ruta_archivo = os.path.abspath("./data/tetris_custom_settings.ttc")  # Reemplaza con la ruta real de tu archivo

        # Buscar el elemento destino en el navegador
        drop_target = self.driver.find_element(By.ID, "home_menu")

        # Arrastrar el archivo al elemento destino
        self.drag_and_drop_file(drop_target, ruta_archivo)
        
        xpath_expression = "/html/body/div[44]/div/div/div[2]"
        
        import_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_expression)))
        self.driver.execute_script("arguments[0].click();", import_button)

        play_solo_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'play_solo')))
        self.driver.execute_script("arguments[0].click();", play_solo_button)
        
        # Espera hasta que aparezca el div con id 'game_40l'
        game_40l_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'game_40l')))
        self.driver.execute_script("arguments[0].click();", game_40l_button)
        # Espera 3 segundos
        

        # Espera hasta que aparezca el div con id 'start_40l' y haz clic en él
        start_40l_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'start_40l')))
        self.driver.execute_script("arguments[0].click();", start_40l_button)
        
        self.focus()
        time.sleep(1.5)


    def focus(self):
        # Espera hasta que aparezca el elemento con id 'nofocus'
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('f')
        
    def drop_hard(self):
        # Presiona la tecla Space para realizar una caída rápida
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        #print("tecla espacio") 
    def drop_soft(self):
        # Presiona la tecla Space para realizar una caída rápida
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_DOWN)
        #print("tecla  arrow down") 

    def spin_left(self):
        # Presiona la tecla Z para girar a la izquierda
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('z')
        #print("tecla z") 

    def spin_right(self):
        # Presiona la tecla x para girar a la derecha
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('x')
        #print("tecla x") 

    def move_left(self):
        # Presiona la tecla izquierda para mover la pieza a la izquierda
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_LEFT)
        #print("tecla arrow left") 

    def move_right(self):
        # Presiona la tecla derecha para mover la pieza a la derecha
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
        #print("tecla arrow right")
    def hold_move(self):
        # Presiona la tecla c para guardar la pieza actual
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('c')
        #print("tecla c")
    def spin_180(self):
        # Presiona la tecla a para girar la pieza a 180 grados
        self.driver.find_element(By.TAG_NAME, 'body').send_keys('a')
        #print("tecla a")
        
    def perform_actions(self, actions):
        for action in actions:
            # Obtén el método con el nombre de acción y llámalo
            method = getattr(self, action)
            method()
            # time.sleep(0.5)

    def generate_actions(self, best_option, piece: Piece):
        """Genera las acciones necesarias para mover la pieza a la mejor opción."""
        actions = []
        piece.set_current_shape(0)
        
        # Rotaciones
        while best_option[2] != piece.current_shape:

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

        # Movimientos laterales
        if best_option[1] < piece.grid_position:
            grid_pos = piece.grid_position
            while best_option[1] != grid_pos:
                actions.append("move_left")
                grid_pos -= 1

        elif best_option[1] > piece.grid_position:
            grid_pos = piece.grid_position
            while best_option[1] != grid_pos:
                actions.append("move_right")
                grid_pos += 1
        # Bajar la pieza
        actions.append("drop_hard")
        return actions