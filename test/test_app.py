import pytest
import types
import numpy as np
from PIL import Image

import sys, os
# Asegurar que se pueda importar src.app.app
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import app


def test_get_connection(monkeypatch):
    """Prueba que la función get_connection se ejecute sin error (mockeando pyodbc)."""
    class DummyConn:
        def cursor(self): return "cursor"
    monkeypatch.setattr(app.pyodbc, "connect", lambda _: DummyConn())

    conn = app.get_connection()
    assert conn.cursor() == "cursor"


def test_dibujar_boxes_imagen_sin_boxes():
    """Debe devolver la misma imagen si no hay boxes."""
    image = Image.new("RGB", (100, 100), "white")
    result = types.SimpleNamespace(boxes=types.SimpleNamespace(xyxy=np.array([])))
    output = app.dibujar_boxes_imagen(image, result)
    assert isinstance(output, np.ndarray)
    assert output.shape[0] == 100  # altura
    assert output.shape[1] == 100  # ancho





@pytest.mark.database
def test_dibujar_boxes_imagen_con_datos_bd():
    """
    Prueba la función dibujar_boxes_imagen usando los datos reales de la base de datos
    para la interfaz con ID 'sen1'.
    """
    web_id = "sen1"
    result = app.get_results_por_web(web_id)

    # Si no hay registros, el test falla con mensaje claro
    assert result is not None, f"No se encontraron registros en BD para el ID '{web_id}'"
    assert hasattr(result, "boxes"), "El objeto result no tiene atributo 'boxes'"

    # Crear una imagen vacía solo para dibujar encima
    image = Image.new("RGB", (800, 600), "white")

    # Dibujar las detecciones de la BD sobre la imagen
    output = app.dibujar_boxes_imagen(image, result)

    # Validaciones básicas
    assert isinstance(output, np.ndarray), "La salida no es una imagen NumPy"
    assert output.shape[0] == 600  # altura
    assert output.shape[1] == 800  # ancho

    # Validar que hay boxes
    num_boxes = len(result.boxes.xyxy)
    assert num_boxes > 0, f"No se dibujaron cajas (boxes) para {web_id}"

    print(f"✅ Se dibujaron {num_boxes} boxes para la interfaz '{web_id}' correctamente.")
