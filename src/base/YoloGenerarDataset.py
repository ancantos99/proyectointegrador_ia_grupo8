import os
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
# Importaciones necesarias para las esperas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time # Para una espera de último recurso (opcional)

# CONFIGURACIÓN
urls = [
    "https://www.senescyt.gob.ec/web/guest/consultas",
    "https://lugarvotacion.cne.gob.ec/",
    "https://pq.biess.fin.ec/pq-concesion-web/pages/concesion/roles.jsf",
    "https://facturadorsri.sri.gob.ec/portal-facturadorsri-internet/pages/inicio.html",
    "https://portal-sd.securitydata.net.ec/",
    "https://apc.arcotel.gob.ec/aplicaciones_senatel/concesion/consulta_no_adeudar.php",
    "https://consultas.atm.gob.ec/PortalWEB/paginas/clientes/clp_criterio_consulta.jsp",
    "https://servicios.axiscloud.ec/AutoServicio/inicio.jsp?ps_empresa=22&ps_accion=P55"
]
output_dir = "C:/MIA/datasetec"
images_dir = os.path.join(output_dir, "images")
labels_dir = os.path.join(output_dir, "labels")
classes = ["link", "button", "input"]  # Agrega más clases si quieres

os.makedirs(images_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)

# Guardar archivo de clases
with open(os.path.join(output_dir, "classes.txt"), "w") as f:
    for c in classes:
        f.write(f"{c}\n")

# Configuración de Selenium headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080") #1920,1080
tmp_dir = tempfile.mkdtemp()
chrome_options.add_argument(f"--user-data-dir={tmp_dir}")

driver = webdriver.Chrome(options=chrome_options)

# Configuración del objeto de espera explícita
# Esperará un máximo de 15 segundos para que se cumpla cualquier condición
wait = WebDriverWait(driver, 15)

for idx, url in enumerate(urls, start=1):
    try:
        driver.get(url)
        # -------------------------------------------------------------
        # 1. ESPERA EXPLÍCITA CRÍTICA: Esperar a que un elemento CLAVE esté visible
        # La mejor manera de asegurar la carga visual es esperar por un elemento que sepa que siempre existe.
        # Aquí esperamos por el tag <body>, que es el último en cargarse visualmente.
        # Si la página usa un div principal (ej: id="main-content"), úsalo en su lugar.
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

        # 2. ESPERA ADICIONAL: Esperar a que el estado del DOM sea 'completo'
        # Esto asegura que todo el JavaScript inicial se ha ejecutado.
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # 3. PAUSA FINAL DE SEGURIDAD (Opcional, pero muy útil en sitios complejos)
        # Permite que los elementos cargados asincrónicamente (como animaciones o pop-ups) se terminen de renderizar.
        time.sleep(2)

        # Captura screenshot
        screenshot = driver.get_screenshot_as_png()
        img = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR)
        h, w, _ = img.shape

        # Guardar imagen
        image_name = f"img_{idx}.png"
        image_path = os.path.join(images_dir, image_name)
        cv2.imwrite(image_path, img)

        # Crear archivo de labels YOLO
        label_path = os.path.join(labels_dir, f"img_{idx}.txt")
        with open(label_path, "w") as f:
            # Detectar inputs
            inputs = driver.find_elements("tag name", "input")
            for inp in inputs:
                loc = inp.location
                size = inp.size
                x_center = (loc['x'] + size['width'] / 2) / w
                y_center = (loc['y'] + size['height'] / 2) / h
                width = size['width'] / w
                height = size['height'] / h
                f.write(f"2 {x_center} {y_center} {width} {height}\n")

            # Detectar buttons
            buttons = driver.find_elements("tag name", "button")
            for btn in buttons:
                loc = btn.location
                size = btn.size
                x_center = (loc['x'] + size['width'] / 2) / w
                y_center = (loc['y'] + size['height'] / 2) / h
                width = size['width'] / w
                height = size['height'] / h
                f.write(f"1 {x_center} {y_center} {width} {height}\n")
    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")
        # Continuar con la siguiente URL si falla

driver.quit()
print("Dataset YOLO generado en:", output_dir)