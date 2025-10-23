import streamlit as st
from ultralytics import YOLO
import cv2
from PIL import Image
import pyodbc
import io
import numpy as np
import types
import os

try:
    from src.utils import ComparadorVersiones
except ImportError:
    # Si la importación falla, intentar ajustar el path (común en entornos Streamlit)
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from src.utils import ComparadorVersiones


#======================
#CONEXIÓN A LA BASE DE DATOS (con caché)
#======================
@st.cache_resource
def get_connection():
    db_config = (
        "DRIVER={SQL Server};"
        "SERVER=localhost;"
        "DATABASE=BD_TEST;"
        "UID=sa;"
        "PWD=Runever19"
    )
    conn = pyodbc.connect(db_config)
    return conn

conn = get_connection()
cursor = conn.cursor()

#======================
#CARGAR MODELO YOLO
#======================
model = YOLO("../models/best_model.pt")

#======================
#INTERFAZ STREAMLIT
#======================
st.title("🧠 Prueba de modelo YOLOv8l Para Detección de Interfaces Web en RPA")

# Creamos st.session_state para almacenar los inputs y poder acceder a ellos con el botón
if 'save_to_db' not in st.session_state:
    st.session_state.save_to_db = False
if 'interfaz_id' not in st.session_state:
    st.session_state.interfaz_id = ""
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'comparar_db' not in st.session_state:
    st.session_state.comparar_db = None

st.session_state.comparar_db = st.checkbox("¿Comparar con una interfaz de la base de datos?")
st.session_state.save_to_db = st.checkbox("¿Guardar las detecciones en la base de datos?")

#interfaz_id = None
if st.session_state.save_to_db or st.session_state.comparar_db:
    st.session_state.interfaz_id = st.text_input("🆔 Ingresa el Identificador de la interfaz:")

st.write("Sube una imagen de una interfaz web para realizar la detección:")
st.session_state.uploaded_file = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])

#======================
#FUNCIÓN PARA GUARDAR INTERACCION CON BASE DE DATOS
#======================
def save_results(identificador_web, results):
    for box in results.boxes:
        clase = results.names[int(box.cls)]
        conf = float(box.conf)
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        query = """
            INSERT INTO [dbo].[DeteccionesYolo] ([web],[clase],[confianza],[x1],[y1],[x2],[y2])
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, identificador_web, clase, conf, x1, y1, x2, y2)
    conn.commit()

def get_results_por_web(web_id):
    cursor.execute("""
        SELECT clase, confianza, x1, y1, x2, y2 FROM [dbo].[DeteccionesYolo] WHERE web = ?
    """, web_id)
    registros = cursor.fetchall()
    if not registros:
        st.warning(f"No se encontraron detecciones para web '{web_id}'")
        return None
    # Crear objeto result
    result = types.SimpleNamespace()
    # Diccionario de clases
    clases_unicas = list({r[0] for r in registros})
    result.names = {i: nombre for i, nombre in enumerate(clases_unicas)}
    # Crear arrays directamente, sin listas
    boxes = types.SimpleNamespace()
    boxes.xyxy = np.array([[r[2], r[3], r[4], r[5]] for r in registros], dtype=int)  # Nx4
    boxes.cls   = np.array([clases_unicas.index(r[0]) for r in registros], dtype=int) # N
    boxes.conf  = np.array([r[1] for r in registros], dtype=float)                  # N

    result.boxes = boxes
    return result
##===============================
##FUNCION PARA GRAFICAR LA IMAGEN
##===============================
def dibujar_boxes_imagen(image_pil, result):
    # Convertir PIL -> BGR para OpenCV
    image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    # Comprobar si hay boxes usando la longitud del array xyxy
    if result is None or not hasattr(result, 'boxes') or len(result.boxes.xyxy) == 0:
        # Si no hay resultados o boxes, simplemente retorna la imagen original
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # YOLOv8 puede devolver tensores 0-dim
    # Manejar ambos casos: si viene de YOLO (con .cpu().numpy()) o de la DB (ya en NumPy)
    if isinstance(result.boxes.xyxy, np.ndarray):
        boxes = result.boxes.xyxy.astype(int)  # Nx4, ya en numpy
        cls_ids = result.boxes.cls.astype(int)  # N, ya en numpy
        confs = result.boxes.conf  # N, ya en numpy
    else:  # Asumir que son tensores de YOLO
        # Los resultados de YOLO vienen como tensores
        boxes = result.boxes.xyxy.cpu().numpy().astype(int)  # Nx4
        cls_ids = result.boxes.cls.cpu().numpy().astype(int)  # N
        confs = result.boxes.conf.cpu().numpy()  # N

    for i in range(len(boxes)):
        x1, y1, x2, y2 = map(int, boxes[i])
        cls_id = int(cls_ids[i])
        conf = float(confs[i])
        label = f"{result.names[cls_id]} {conf:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    # Convertir BGR -> RGB para Streamlit
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# =======================
# LÓGICA DE COMPARACION ENCAPSULADA EN UNA FUNCIÓN
# =======================
def ejecutar_comparacion(uploaded_file, interfaz_id):
    if not uploaded_file:
        st.error("❌ Por favor, sube una imagen antes de comparar.")
        return
    if not interfaz_id:
        st.error("❌ Por favor, ingresa un Identificador de interfaz (ID) antes de comparar.")
        return

    image = Image.open(uploaded_file)
    #st.image(image, caption="📸 Imagen original para análisis", use_container_width=True)
    # 1. Cargar la versión BASE (anterior) de la DB
    rbase = get_results_por_web(interfaz_id)
    img_rgb = dibujar_boxes_imagen(image, rbase)
    st.image(img_rgb, caption="📸 Boxes originales de la base de datos sobre la nueva imagen", use_container_width=True)

    with st.spinner("🤖 Realizando predicción YOLO y comparando con la base de datos..."):
        # Realizar predicción con YOLO sobre la imagen subida
        results = model.predict(image, conf=0.5)
        result_yolo = results[0] if isinstance(results, list) else results
        # 2. COMPARACIÓN
        comparador = ComparadorVersiones( )
        pagina_cambio, boxes_nuevos, boxes_cambiados = comparador.comparar_base_con_prediccion(rbase, result_yolo)

        # 3. Mostrar Resultados de Comparación
        st.header("Análisis de Cambios")
        if pagina_cambio:
            st.warning("⚠️ ¡La interfaz ha CAMBIADO! Registrando nueva versión.")
            st.json({"Nuevos Boxes": boxes_nuevos, "Cambios": boxes_cambiados})
            img_rgb = dibujar_boxes_imagen(image, result_yolo)  # Dibuja la nueva versión
        else:
            st.success("🎉 No se detectaron cambios relevantes. Se mantiene la versión de la base.")
            img_rgb = dibujar_boxes_imagen(image, rbase if rbase is not None else result_yolo)

        st.image(img_rgb, caption="🎯 Detecciones de la Versión Final", use_container_width=True)


if st.session_state.comparar_db:
    if st.button("Comprobar Cambios", type="primary"):
        ejecutar_comparacion(st.session_state.uploaded_file, st.session_state.interfaz_id)
else:
    # Lógica de detección simple si no se activa la comparación con DB
    if st.session_state.uploaded_file:
        image = Image.open(st.session_state.uploaded_file)
        st.image(image, caption="📸 Imagen original", use_container_width=True)
        # Realizar predicción
        results = model.predict(image, conf=0.5)
        result = results[0] if isinstance(results, list) else results

        # Guardar si se habilitó la opción y hay un ID
        if st.session_state.save_to_db and st.session_state.interfaz_id:
            save_results(st.session_state.interfaz_id, result)
            st.success(f"✅ Detecciones guardadas en la base de datos con ID '{st.session_state.interfaz_id}'.")

            rbase = get_results_por_web(st.session_state.interfaz_id)
            img_rgb = dibujar_boxes_imagen(image, rbase)
            st.image(img_rgb, caption="🎯 Detecciones YOLOv8", use_container_width=True)
        else:
            # img = result.plot()
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = dibujar_boxes_imagen(image, result)
            st.image(img_rgb, caption="🎯 Detecciones YOLOv8", use_container_width=True)

