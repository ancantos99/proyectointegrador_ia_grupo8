# 🗂️ Descripción del Dataset

Para nuestro proyecto, vamos a entrenar una Red Neuronal YOLOV8.

Nuestro dataset, es diferente a un dataset tabular clásico (Con columnas numéricas, categóricas, filas, etc..) en YOLO el dataset tiene un formato específico y consiste en:
- Imágenes (.jpg, .png …).
- Labels (.txt) con anotaciones en formato YOLO: class x_center y_center width height.
- dataset.yaml con paths y clases.

### Estructura de la raiz del Dataset
```
Dataset/
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

