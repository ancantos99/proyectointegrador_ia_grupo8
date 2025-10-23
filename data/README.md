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

Datase Original de HugginFace

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

### Dataset Train con Undersampling
Estrategia Inicial (Undersampling): Se implementó la técnica de Undersampling con el objetivo de balancear el dataset, reduciendo la representación de la clase mayoritaria para igualar su tamaño con el de la clase minoritaria.

Problema Identificado: El enfoque inicial de remover las imágenes asociadas a la clase mayoritaria resultó en una pérdida no deseada de datos (incluyendo información útil de otras clases) contenida en esas mismas imágenes.

Para mitigar esta pérdida, la estrategia sería: Modificar los Labels (.txt) y Mantener las Imágenes.
El enfoque debería ser mantener todas las imágenes y, en su lugar, modificar sus etiquetas (labels) para simular el undersampling. Esto implica eliminar únicamente las anotaciones (boxes) correspondientes a la clase mayoritaria de las imágenes seleccionadas para la reducción, preservando así las anotaciones de las clases minoritarias.

```
processed/
├── train_undersampling/
│    ├── images/ imagenes.png ...
│    ├── labels/ architos.txt ...
```

### Dataset Con Sobremuestreo
Se implementó la clase Data_processing (src/Data_processing)
y el método oversample_rare_classes para implementar un sobremuestreo agresivo ( x defecto a clases con menos de 100 elementos y con un factor de duplicación de 10)
esto se aplica sobre el Dataset principal

```python
processor = Data_processing(dataset_path)
processor.count_class_distribution()
processor.oversample_rare_classes(count_threshold=100, duplication_factor=10, target_class_id=None)


Este Sobremuestreo incrementa las clases con menos representación, a continuación se muestra las 3 clases principales para nuestro proyecto:

 ID Clase                   Train inicial     Train con Sobremuestreo    
-----------------------------------------------------------------------
   0 link                    15583                   36683
   1 button                   5101                   10961
   2 input                     354                    1074
```



