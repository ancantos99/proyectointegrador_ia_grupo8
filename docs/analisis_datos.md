# Análisis de datos
> **Detección de cambios en interfaces web para procesos RPA utilizando Inteligencia Artificial**
>
> Optimización de Hiperparámetros para YOLOv8 con Optimización Bayesiana y usando la plataforma Weights & Biases

## 🗂️ Descripción detallada del dataset

El dataset consta de las siguiente estructura:

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
```

Nuestro dataset, es diferente a un dataset tabular clásico (Con columnas numéricas, categóricas, filas, etc..) en YOLO el dataset tiene un formato específico y consiste en:
- El dataset tiene 3 carpetas /train, / val y /test
- Imágenes (.png) en la carpeta /images
- Labels (.txt) con Anotaciones en la carpeta /labels
- Los labels deben estar en formato **YOLO**: **class_id xcenter ycenter ancho alto**
- dataset.yaml con paths y clases. (archivo de configuración de rutas y clases)
- Utilizamo inicialmente el **"UI Elements Detection Dataset"** de Hugging Face.
  * **Fuente:** [YashJain/UI-Elements-Detection-Dataset](https://huggingface.co/datasets/YashJain/UI-Elements-Detection-Dataset)
  * **Contenido:** Imágenes de interfaces de usuario web con anotaciones de objetos (Bounding Boxes) para la detección de elementos comunes de UI (botones, barras de búsqueda, texto, etc.).
  * **Formato de Anotación:** Las coordenadas de los *bounding boxes* están **normalizadas** (valores entre 0 y 1)

## 📋 Estadísticas descriptivas
## 📊 Visualizaciones del EDA (mínimo 5-6 gráficos relevantes)
## 🔎 Identificación de patrones, correlaciones, outliers
## 🧹 Decisiones de preprocesamiento justificadas
## 🛠️ Manejo de datos faltantes o desbalanceados
