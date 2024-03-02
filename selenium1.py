from selenium import webdriver

# Inicializa el driver del navegador (en este caso, Chrome)
driver = webdriver.Edge()

# Maximiza la ventana del navegador
driver.maximize_window()

# Abre la URL que quieres
driver.get('https://tetr.io/')

# Toma una captura de pantalla y la guarda como 'screenshot.png'
driver.save_screenshot('screenshot.png')

# Cierra el navegador
driver.quit()