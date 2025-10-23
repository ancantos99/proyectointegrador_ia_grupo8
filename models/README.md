# 🛠️ Modelos
> **Detección de cambios en interfaces web para procesos RPA utilizando Inteligencia Artificial**
>
> A continuación se escribe las versiones de los modelos YOLOv8 entrenados, sus configuraciones, resultados y observaciones relevantes.
> Los modelos resultantes de YoloV8l tienen extensión .pt


## 🥇 Versión ganadora: `best_model.pt`
- **Fecha de entrenamiento:** 20 oct 2025  
- **Base:** YOLOv8l 
- **Dataset:** Detección de elementos en interfaces web con Sobremuestreo Agresivo
- **Duración entrenamiento:** 6891.00 minutos (100 épocas con early stopping 15: se corrieron 100 épocas)
- **Gpu Utilizada:** GPU A 100
- **Tamaño del modelo:** 83.8 MB
- **Configuración ganadora:** 

|epochs|imgsz|batch|optimizer|lr0|lrf|weight_decay|patience|
|------|-----|-----|---------|---|---|------------|--------|
|100 |(1920,1080)|6|AdamW|0.00004694921598565255|0.46315|0.00808107114573286|15|

- **métricas  Generales:**

|mAP50(B)|Precision |Recall |F1-score|
|--------|----------|-------|---------|
| 0.268  |0.7616    | 0.2383| 0.3630  |

- **métricas de Clases Principales:**

|Clase|mAP50(B)|Precision |Recall |F1-score|
|-----|--------|----------|-------|---------|
|0-link	 | 0.581007|0.788805	|0.507472| 0.61761 |
|1-button| 0.598784|0.785473	|0.685185| 0.631176 |
|2-input | 0.737391|0.841365	|0.685185	|0.755286	|

---

## Versión EXP3: `YoloV8l_exp3.pt`
- **Fecha de entrenamiento:** 17 oct 2025  
- **Base:** YOLOv8l 
- **Dataset:** Detección de elementos en interfaces web con Sobremuestreo Agresivo
- **Duración entrenamiento:** 8591.96 minutos (100 épocas con early stopping 15: se corrieron 63 épocas)
- **Gpu Utilizada:** GPU t4	
- **Tamaño del modelo:** 83.8 MB
- **Configuración:** 

|epochs|imgsz|batch|optimizer|lr0|lrf|weight_decay|patience|
|------|-----|-----|---------|---|---|------------|--------|
|100 |(1920,1080)|1|Adam|0.001|0.01| No se utilizó|15|

- **métricas  Generales:**

|mAP50(B)|Precision |Recall |F1-score|
|--------|----------|-------|---------|
| 0.159  |0.4764   | 0.1636| 0.2436  |

- **métricas de Clases Principales:**

|Clase|mAP50(B)|Precision |Recall |F1-score|
|-----|--------|----------|-------|---------|
|0-link	 | 0.332972|0.468352	|0.375569| 0.41686 |
|1-button| 0.394805|0.457078	|0.444254| 0.450574 |
|2-input | 0.454618|0.718178	|0.388889	|0.504561	|

---

## Versión EXP2: `YoloV8l_exp2.pt`
- **Fecha de entrenamiento:** 12 oct 2025  
- **Base:** YOLOv8l 
- **Dataset:** Detección de elementos en interfaces web y con Data Augmentations ( cambios de saturación, brillo, configurados durante el entrenamiento del YoloV8 hsv_h,hsv_s,etc..)
- **Duración entrenamiento:** 
- **Gpu Utilizada:** GPU t4	
- **Tamaño del modelo:** 83.8 MB
- **Configuración:** 

|epochs|imgsz|batch|optimizer|lr0|lrf|weight_decay|patience|
|------|-----|-----|---------|---|---|------------|--------|
|100 |(1920,1080)|1|Adam|0.001|0.01| No se Utilizó|15|

- **métricas  Generales:**

|mAP50(B)|Precision |Recall |F1-score|
|--------|----------|-------|---------|
| 0.159  |0.4764   | 0.1636| 0.2436  |

- **métricas de Clases Principales:**

|Clase|mAP50(B)|Precision |Recall |F1-score|
|-----|--------|----------|-------|---------|
|0-link	 | 0.332972|0.468352	|0.375569| 0.41686 |
|1-button| 0.394805|0.457078	|0.444254| 0.450574 |
|2-input | 0.454618|0.718178	|0.388889	|0.504561	|
