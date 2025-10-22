<p align="center">
  <h1> Detección de Cambios en Interfaces Web para Procesos RPA utilizando Inteligencia Artificial</h1>
</p>

**Integrantes**
- Andrés Martín Cantos Rivadeneira
- María Paola Mendoza Mendieta

## 📌 Descripción

Este proyecto aborda la fragilidad de los procesos de Automatización Robótica de Procesos (RPA) frente a cambios visuales en interfaces web.  
Propone un módulo basado en Visión por Computadora y Redes Neuronales Convolucionales (CNN) que detecta automáticamente dichas alteraciones, sin depender de localizadores tradicionales.  
Esto permite identificar y notificar cambios relevantes en la interfaz, mejorando la fiabilidad del monitoreo y reduciendo el tiempo de diagnóstico e intervención manual.

## 🧰 Tecnologías Clave

- **Lenguaje principal:** Python 3.8+
- **Librerías:** 
  - **Ultralytics** (para detección avanzada con modelos YOLO)
  - OpenCV  
  - Tesseract OCR  
  - Pandas  
  - NumPy  
  - TensorFlow / Keras
- **Plataforma RPA:** [ElectroNeek](https://electroneek.com/)  
  *(Licencia temporal otorgada por una empresa con carta de autorización)*


## ⚙️ Funcionalidades Destacadas

- 🔍 Comparación automática de interfaces web mediante detección de diferencias visuales.
- 🧠 Clasificación de cambios mediante Redes Neuronales Convolucionales (CNN).
- 📝 Extracción de texto en pantallas con OCR (Tesseract).
- 🚨 Generación de alertas o acciones correctivas para flujos RPA afectados.
- ✅ Mejora en la resiliencia y autonomía de bots RPA.
  
---
## 2. Tabla de contenido
[3. Descripción del Problema](#3-descripción-del-problema)

[4. Dataset](#4-dataset)
## 3. Descripción del Problema

### 3.1. ¿Qué problema resuelve el proyecto?  
El proyecto aborda la fragilidad de los procesos RPA en aplicaciones web, donde cambios
en la interfaz pueden afectar su ejecución. Propone un módulo basado Visión por
Computadora y Redes Neuronales Convolucionales (CNN) que identifique estos cambios
visuales y los notifique, sin depender de localizadores tradicionales, mejorando así la
fiabilidad de los procesos automatizados.

### 3.2. ¿Por qué es importante?  
La dependencia de localizadores tradicionales limita la robustez y escalabilidad de las automatizaciones, generando costos adicionales en mantenimiento. La solución propuesta, al utilizar IA, permite a los bots detectar y notificar cambios en la interfaz, facilitando una rápida identificación de problemas. Esto ayuda a reducir el tiempo de inactividad al acelerar la intervención humana y mejora la gestión del mantenimiento, contribuyendo a una mayor continuidad operativa y tasa de éxito en la automatización.

### 3.3. ¿Quiénes son los usuarios objetivo?  
- Desarrolladores y operadores de RPA: Aquellos que mantienen y ajustan los
bots en la plataforma ElectroNeek.
- Clientes (empresas): Organizaciones que utilizarán la solución en procesos
contables y tributarios y que buscan datos confiables y reducción de errores.

## 4. Dataset

### 4.1. Descripción de los Datos Utilizados

El dataset consiste en un conjunto completo de datos de elementos de interfaz de usuario web recopilados de los sitios web más visitados del mundo. Este conjunto de datos está diseñado específicamente para entrenar modelos de IA que detecten y clasifiquen componentes de la interfaz de usuario, lo que permite realizar pruebas automatizadas de la interfaz de usuario, análisis de accesibilidad y estudios de diseño de interfaz.


### 4.2. Fuente y licencia de los datos

El dataset fue descargado desde Hugging Face. La fuente específica es: YashJain/UI-Elements-Detection-Dataset.
Está disponible bajo la licencia MIT (o la que aplique), lo que permite su uso con fines académicos y comerciales.
Además, se planificó la recolección de capturas de pantalla de portales públicos de Ecuador (SRI, MSP, SENESCYT, Fiscalía), siendo el portal del SRI el recomendado como dataset principal debido a su relevancia analítica y contable.

### 4.3. Características principales

- Más de 300 sitios web populares muestreados
- 15 clases esenciales de elementos de interfaz de usuario
- Capturas de pantalla de alta resolución (1920x1080)
- Metadatos de accesibilidad enriquecidos
- Anotaciones en formato YOLO
- Distribución equilibrada de clases 
- En el contexto YOLO, los datos de las coordenadas (`x_center`, `y_center`, `width`, `height`) están normalizados entre 0 y 1.

### 4.4. Link a los datos públicos

El dataset base es accesible en Hugging Face:  
[https://huggingface.co/datasets/YashJain/UI-Elements-Detection-Dataset](https://huggingface.co/datasets/YashJain/UI-Elements-Detection-Dataset)

## 5. Metodología

### 5.1. Tipo de Modelo Utilizado y Justificación

- **Modelos utilizados:** El proyecto utilizó variantes del modelo de detección de objetos **YOLOv8**. Se probaron específicamente las versiones **YOLOv8n**, **YOLOv8m** y **YOLOv8l**. Los entrenamientos más exitosos emplearon **YOLOv8l**.
- **Justificación:**  
  El escalado del modelo desde versiones más ligeras (YOLOv8n) hacia modelos más grandes (YOLOv8l) mostró mejoras consistentes en **precisión** y **mAP@50**, con mayor capacidad de generalización y menor pérdida en validación.  
  Además, los entrenamientos con YOLOv8l, junto con ajustes de hiperparámetros y técnicas de **data augmentation seguro**, lograron mejoras significativas sin comprometer la semántica visual.

### 5.2. Preprocesamiento Aplicado

Se implementaron las siguientes estrategias de preprocesamiento y manejo de datos:

1. **Balanceo y Estratificación del Dataset**  
   Se evaluaron tres versiones del dataset: original, balanceado y estratificado.  
   Aunque el balanceo mejoró levemente el recall, los modelos más robustos rindieron mejor con el dataset original.

2. **Data Augmentation Seguro**  
   Se aplicó un aumento de datos limitado a color y brillo, para mantener la semántica visual.  
   Esta técnica mejoró la **generalización** del modelo sin afectar negativamente la **precisión** de clases clave.

3. **Reducción de Clases**  
   En un entreanamiento, el dataset fue reducido a solo 3 clases principales: `input`, `button`, y `link`, lo que mejoró el rendimiento específico en casos de uso relevantes.


### 5.3. Técnicas de Optimización Empleadas

La metodología fue experimental, iterativa y comparativa, centrada en la **optimización de hiperparámetros**.

#### 1. Plataforma y Técnica

- Se utilizó **Weights & Biases (W&B)** para realizar **optimización bayesiana** de hiperparámetros del modelo YOLOv8.

#### 2. Estrategia de Entrenamiento en Fases

- **Fase Exploratoria Rápida:**  
  Entrenamiento con baja resolución (`imgsz=640`) y batch grande (`batch=16`) para acelerar la búsqueda de combinaciones viables.

- **Fase de Ajuste Final:**  
  Entrenamiento con los mejores hiperparámetros a **resolución real (1920x1080)** y `batch=6`.

#### 3. Ajustes Críticos de Hiperparámetros

- Los hiperparámetros **`lr0`** (learning rate inicial) y **`optimizer`** fueron los más determinantes.
- Rango óptimo de `lr0`:
  - **Adam / AdamW:** muy bajos (`< 0.005`)
  - **SGD:** más altos (`0.05 – 0.065`)
- **Mejor combinación final:**
  - imgsz = (1920x1080)
  - batch = 6
  - optimizer="AdamW"
  - weight_decay = 0.00808107114573286
  - lr0= 0.00004694921598565255
  - lrf=0.46315



