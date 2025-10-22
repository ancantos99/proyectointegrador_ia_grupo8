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
  - OpenCV  
  - Tesseract OCR  
  - Pandas  
  - NumPy  
  - TensorFlow / Keras
  - **Ultralytics** (para detección avanzada con modelos YOLO)
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
- [3. Descripción del Problema](#3-descripción-del-problema)

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

El dataset fue descargado desde Hugging Face. La fuente específica es: [YashJain/UI-Elements-Detection-Dataset](https://huggingface.co/datasets/YashJain/UI-Elements-Detection-Dataset).  
Adicionalmente, se planificó la recolección de capturas de pantalla de portales públicos de Ecuador (SRI, MSP, SENESCYT, Fiscalía), siendo el portal del SRI el recomendado como dataset principal debido a su relevancia analítica y contable.

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

