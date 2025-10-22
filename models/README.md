# 🗂️ Descripción del Dataset

Para nuestro proyecto, vamos a entrenar una Red Neuronal YOLOV8.

Nuestro dataset, es diferente a un dataset tabular clásico (Con columnas numéricas, categóricas, filas, etc..) en YOLO el dataset tiene un formato específico y consiste en:
- Imágenes (.png).
- Labels (.txt) con Anotaciones o labels en formato **YOLO**: **class_id xcenter ycenter ancho alto**
- dataset.yaml con paths y clases.
- utilizaremos el **"UI Elements Detection Dataset"** de Hugging Face.
  * **Fuente:** [YashJain/UI-Elements-Detection-Dataset](https://huggingface.co/datasets/YashJain/UI-Elements-Detection-Dataset)
  * **Contenido:** Imágenes de interfaces de usuario web con anotaciones de objetos (Bounding Boxes) para la detección de elementos comunes de UI (botones, barras de búsqueda, texto, etc.).
  * **Formato de Anotación:** Las coordenadas de los *bounding boxes* están **normalizadas** (valores entre 0 y 1)

### Estructura de la raiz del Dataset
```
raw/
├── train/
│    ├── images/ imagenes.png ...
│    ├── labels/ architos.txt ...
├── val/
│    ├── images/ imagenes.png ...
│    ├── labels/ architos.txt ...
└── test/
│    ├── images/ imagenes.png ...
│    ├── labels/ architos.txt ...
└── dataset.yaml (archivo de configuración)

