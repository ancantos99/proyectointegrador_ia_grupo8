import os
import importlib
import logging
import sys
import data_processing
from ultralytics import YOLO
from tools.YOLODatasetManager import YOLODatasetManager
from tools.YOLOMetricasVisualizar import YOLOMetricasVisualizar
from data_processing import Data_processing


datasetmanager = YOLODatasetManager("../data/raw")
datasetmanager.yaml_cambiar_carpeta(split="train",nuevaruta="train")
counts = datasetmanager.compute_class_distribution("train")
print("Distribución:", counts)
##datasetmanager.plot_distribution()
"""# APLICAR SOBREMUESTREO"""
processor = Data_processing("../data/raw")
antes = processor.count_class_distribution("Antes")
processor.oversample_rare_classes()
despues = processor.count_class_distribution("Despues")
## 3️⃣ **Entrenamiento del modelo**

#datasetmanager.yaml_cambiar_carpeta(split="train",nuevaruta="train")
#Entrenar YOLO de manera clásica con el dataset train, para eso modifico la ruta en el dataset.yaml
model = YOLO("yolov8l.pt")  # yolov8l.pt.
# Cargar dataset usando YOLOv8 Dataset
carpeta_salida = "exp_5" #carpeta donde se van a guardar los resultados del entrenamiento de YOLO y el modelo
model.train(data=datasetmanager.ruta_yaml,
    epochs=100,         #epocas 100
    imgsz= (1920,1080), #tamaño a los que se redimensionara la imagen de entrada #(1920,1080) - 640
    batch=6,            #tamaño del batch (ajustarlo según Vram)
    optimizer="AdamW", #AdamW
    #momentum =0.72765,      # será ignorado si usa Adam/AdamW
    weight_decay = 0.00808107114573286,
    lr0= 0.00004694921598565255,
    lrf= 0.46315,
    name= carpeta_salida,   # nombre del run
    exist_ok=False,         # sobrescribe si ya existe
    project="/content/drive/MyDrive/MIA/Entrenamientos", #En Drive
    patience=15
)
"""## 4️⃣ **Generación de todas las curvas y Evaluación**"""
# Crear objeto Visualizador
visualizer = YOLOMetricasVisualizar(f"/content/drive/MyDrive/MIA/Entrenamientos/{carpeta_salida}/results.csv",
                                    f"/content/drive/MyDrive/MIA/Entrenamientos/{carpeta_salida}/weights/best.pt",datasetmanager.ruta_yaml)
visualizer.plot_loss() # Graficar Loss
visualizer.gap_entretrainyval() # Graficar Gap
visualizer.plot_map()  # Graficar mAP
visualizer.plot_precision_recall_f1() # Graficar Precision, Recall, F1
visualizer.print_final_metrics() # Mostrar métricas finales
#Metricas por Clase
df = visualizer.metrics_por_clase_tabla()   # Imprime Precision, Recall, F1 y mAP50 por clase
#display(df)

from ultralytics import YOLO
import cv2
from PIL import Image
from matplotlib import pyplot as plt

ruta_modelo = "/content/drive/MyDrive/MIA/Entrenamientos/exp_5/weights/best.pt"
ruta_imagen = "/content/drive/MyDrive/MIA/webs_prueba/web_senescyt.png";

model = YOLO(ruta_modelo)
results = model.predict(ruta_imagen,conf=0.35)
res = results[0] if isinstance(results, list) else results
res.show()

ruta_modelo = "/content/drive/MyDrive/MIA/Entrenamientos/exp_4_1/weights/best.pt"
ruta_imagen = "/content/drive/MyDrive/MIA/webs_prueba/web_senescyt.png";

model = YOLO(ruta_modelo)
results = model.predict(ruta_imagen,conf=0.35)
res = results[0] if isinstance(results, list) else results
res.show()