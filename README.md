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

---

## ⚙️ Funcionalidades Destacadas

- 🔍 Comparación automática de interfaces web mediante detección de diferencias visuales.
- 🧠 Clasificación de cambios mediante Redes Neuronales Convolucionales (CNN).
- 📝 Extracción de texto en pantallas con OCR (Tesseract).
- 🚨 Generación de alertas o acciones correctivas para flujos RPA afectados.
- ✅ Mejora en la resiliencia y autonomía de bots RPA.
  
**Estructura del Contenido**
| Fecha              | Entregable                  | Ubicación                  |
|--------------------|----------------------------------|----------------------------|
|semana1 15/sept/25  |Workshop de metodología SMART                  | [/documentacion/s1_workshop](/documentacion/s1_workshop)     |
|semana1 16/sept/25  |Presentación del Proyecto                      | [/documentacion/s1_presentacion](/documentacion/s1_presentacion)  |
|semana1 19/sept/25  |Presentación del Proyecto                      | [/documentacion/s1_presentacion](/documentacion/s1_presentacion)  |
|semana2 24/sept/25  |Análisis Comparativo de Algoritmos             | [/documentacion/s2_comparacion_modelos](/documentacion/s2_comparacion_modelos)  |
|semana2 24/sept/25  |Análisis Exploratorio de Datos (EDA)           | [/analisis_EDA/Grupo%208_EDA_YOLO.ipynb](/analisis_EDA/Grupo%208_EDA_YOLO.ipynb)  |
|semana2 26/sept/25  |Fase de Preparación y Procesamiento de Datos   | **Análisis y preprocesamiento** <br/> [/analisis_EDA/FasePreparacion_LimpiezaDatos.ipynb](/analisis_EDA/FasePreparacion_LimpiezaDatos.ipynb)  <br/> [/analisis_EDA/FasePreparacion_FeatureEngineering.ipynb](/analisis_EDA/FasePreparacion_FeatureEngineering.ipynb) <br/>  [/analisis_EDA/FasePreparacion_EstrategiasBalanceamiento.ipynb](/analisis_EDA/FasePreparacion_EstrategiasBalanceamiento.ipynb)  <br/> [/analisis_EDA/FasePreparacion_DataAugmentation.ipynb](/analisis_EDA/FasePreparacion_DataAugmentation.ipynb) <br/> [/analisis_EDA/FasePreparacion_ParticionDatos.ipynb](/analisis_EDA/FasePreparacion_ParticionDatos.ipynb) <br/> **Pipeline y componentes** <br/> [/src/PipelinePreprocesamiento.ipynb](/src/PipelinePreprocesamiento.ipynb) <br/> **pdf y Slides** <br/> [/documentacion/s2_preprocesamiento](/documentacion/s2_preprocesamiento)|
|semana3 03/oct/25  |Diagnóstico de Overfitting/Underfitting         | **Jupyter Notebook Completo** <br/> [/sric/grupo8_underfitting_analysis.ipynb](/src/grupo8_underfitting_analysis.ipynb)  <br/> **Reporte Técnico pdf** <br/> [/documentacion/s3_diagnostico](/documentacion/s3_diagnostico)|
|semana4 16/oct/25  |Workshop: Impacto Social y Responsabilidad      | **Reporte Pdf y Presentación Ejecutiva** <br/> [/documentacion/s4_workshop_etico](/documentacion/s4_workshop_etico)  |
