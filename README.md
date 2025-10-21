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
El proyecto resuelve la vulnerabilidad principal de los procesos RPA que interactúan con páginas web, la cual surge de los cambios visuales o estructurales en los elementos de la interfaz. Estos cambios (como el reposicionamiento, modificaciones en IDs o clases HTML) pueden provocar interrupciones imprevistas en la ejecución de los bots, ya que estos dependen de localizadores tradicionales (XPATH, ID, CSS) que se vuelven frágiles.

### 3.2. ¿Por qué es importante?  
La dependencia de localizadores tradicionales limita la robustez y escalabilidad de las automatizaciones, generando costos adicionales en mantenimiento. La solución propuesta, al utilizar IA, permite a los bots detectar cambios, comprender su naturaleza e, idealmente, adaptarse. Esto garantiza la continuidad operativa, reduce el tiempo de inactividad de los bots y aumenta la tasa de éxito de la automatización.

### 3.3. ¿Quiénes son los usuarios objetivo?  
Los usuarios objetivo son principalmente los Desarrolladores y operadores de RPA (quienes mantienen y ajustan los bots en la plataforma ElectroNeek) y los Clientes (organizaciones que usan la solución en procesos contables y tributarios y que buscan datos confiables y reducción de errores).
