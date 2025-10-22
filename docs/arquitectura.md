# Arquitectura
> **Detección de cambios en interfaces web para procesos RPA utilizando Inteligencia Artificial**
>
> Arquitectura enfocada en la implementación de YOLOv8l para la detección de elementos de interfaz de usuario (UI) en el contexto de RPA.

## 🤖 Tipo de modelo seleccionado y justificación

<img width="200" height="100" alt="image" src="https://github.com/user-attachments/assets/fb536832-50e5-4ed2-9534-5b7d65ff30e4" />

### Se seleccionó el modelo YOLOV8l

- YOLO es un modelo y marco unificado de visión artificial desarrollado por Ultralytics
- Se basa en redes neuronales convolucionales (CNNs).
- Está especializado en la detección de objetos en tiempo real.
- Tipo de Aprendizaje: Supervisado (En el entrenamiento se usan imágenes junto con sus anotaciones)

| Modelo | Tamaño / Parámetros | Velocidad y precisión | Uso típico |
|--------|---------------------|-----------------------|------------|
| YOLOv8l<br>Large(l)| ~47M    | Más lento - Precisión Alta| Alta precisión en objetos pequeños, se necesita GPU potente |

### Justificación

| Aspecto | Modelo Seleccionado | Justificación |
|---------|---------------------|---------------|
| **Modelo Base** | **YOLOv8l (Large)** | Se selecciona la variante Large (`l`) para un equilibrio óptimo entre precisión (mAP) y velocidad de inferencia. Dado que las imágenes son de alta resolución (1920 × 1080 px) y el sistema debe detectar múltiples objetos por pantalla (media de 43.47 objetos/imagen), se necesita un modelo con una capacidad de aprendizaje robusta para diferenciar clases minoritarias y manejar la complejidad del entorno web. |
| **Paradigma** | **Anchor-Free** | YOLOv8 es un detector anchor-free. Esto simplifica el diseño, ya que no requiere la configuración o el ajuste de anchor boxes predefinidas, mejorando la robustez y la generalización. |
| **Tarea Principal** | **Detección de Objetos en Tiempo Real** | Es la elección estándar para Visión por Computadora debido a su alta velocidad y capacidad para funcionar en producción, clave para la detección de cambios rápidos en procesos RPA. |

## 🏗️ Arquitectura detallada (capas, parámetros, etc.)

La red neuronal de YOLOv8l se divide conceptualmente en tres componentes interconectados:

### Arquitectura de YOLOv8: Componentes Clave

| Componente | Rol | Estructura Clave | Relevancia para el Proyecto |
|------------|-------------------|------------------|------------------------------|
| **Backbone** (CSPDarknet Modificado) | Extraer características ricas y de diferentes niveles de abstracción de la imagen de entrada. | Bloques `C2f` (similar a C3 en versiones anteriores, pero más eficiente), que mejoran el flujo de gradientes y la reutilización de características. | Es vital para extraer características de objetos de tamaños extremos: desde links minúsculos hasta grandes áreas de texto o inputs. |
| **Neck** (FPN + PAN) | Fusionar y propagar la información extraída a través de múltiples escalas. | Una combinación de *Feature Pyramid Network* (FPN) para la información semántica (Top-Down) y *Path Aggregation Network* (PAN) para la información de localización (Bottom-Up). | Esta estructura multi-escala permite la detección robusta de la diversidad de tamaños de bounding boxes observada en el EDA, desde pequeños íconos hasta elementos de gran ancho. |
| **Head** (Decoupled Head) | Generar las predicciones finales (localización y clasificación). | **Anchor-Free**: Separa las ramas de Clasificación (qué objeto es) y Regresión (dónde está) para mejorar el rendimiento. Predice el centro (x_center, y_center) y las dimensiones (width, height) normalizadas de los objetos. | Simplifica la predicción y mejora la precisión en la detección de elementos UI con proporciones variables, especialmente objetos horizontales y de múltiples escalas. |

### Configuración de Entrenamiento e Hiperparámetros

La fase de entrenamiento de YOLOv8l se configura para maximizar el rendimiento en la detección de elementos de UI en un entorno web complejo y desbalanceado. Los hiperparámetros seleccionados buscan un equilibrio entre la velocidad de convergencia y la capacidad de generalización del modelo.

| Hiperparámetro | Valor Definido | Justificación para el Proyecto |
|----------------|----------------|--------------------------------|
| `epochs` | **100** | Número estándar de épocas. Suficiente para la convergencia inicial del modelo, con un margen de seguridad, pero sujeto a la detección temprana por `patience`. |
| `imgsz` | **(1920, 1080)** | Se utiliza la resolución original de las imágenes para el entrenamiento. Esto es crucial para preservar los detalles finos de los elementos de UI pequeños (íconos, links) y evitar la pérdida de información que podría ocurrir al redimensionar a 640 × 640. |
| `batch` | **6** | El tamaño de lote se ajusta a un valor bajo/moderado (6) para adaptarse a la restricción de memoria de la GPU, especialmente al trabajar con una resolución de entrada tan alta (1920 × 1080). |
| `optimizer` | **AdamW** | Optimización de alto rendimiento, preferida sobre SGD en muchos escenarios de visión por computadora. Incluye regularización L2 (*Weight Decay*), esencial para prevenir el sobreajuste en las clases minoritarias. |
| `patience` | **15** | Implementa parada temprana (*early stopping*). Si la métrica de validación (típicamente mAP) no mejora después de 15 épocas consecutivas, el entrenamiento se detiene automáticamente. |

Los siguientes hiperparámetros de regularización y tasa de aprendizaje son críticos y no deben ser seleccionados al azar debido al severo desbalance de clases y la alta complejidad del dataset.

la determinación de los hiperparámetros debe realizarse mediante algún tipo de Optimizanción, en nuestro caso utilizaremos Optimización Bayesiana (utilizando la plataforma W&B ):

| Hiperparámetro | Rango de Valores según Documentación | Rol y Justificación |
|----------------|--------------------------------------|---------------------|
| `weight_decay` (Decaimiento de Peso) | **(0.0, 0.001)** | **Regularización**. Controla la complejidad del modelo. Un valor en este rango es un estándar de la industria. Un valor más alto podría ser beneficioso para evitar que el modelo sobreajuste a la clase mayoritaria (`link`) o a las pocas instancias de las clases minoritarias (`toggle`, `clickable`). |
| `lr0` (Tasa de Aprendizaje Inicial) | **(1e-5, 1e-1)** | **Velocidad de Convergencia**. Define el tamaño del primer paso en el espacio de parámetros. 0.01 es un punto de partida común para optimizadores como AdamW, pero la Optimización Bayesiana es necesaria para encontrar el óptimo exacto. |
| `lrf` (Factor de Tasa de Aprendizaje Final) | **(0.01, 1.0)** | **Estrategia de Programación**. Define el factor por el cual se reduce la tasa de aprendizaje final (ej. si lr0=0.01 y lrf=0.01, el lr final será 0.0001). Un valor bajo asegura que el modelo converja finamente al final del entrenamiento. |

## 🔁 Diagrama de flujo del sistema completo

<img width="2840" height="2700" alt="Blank diagram" src="https://github.com/user-attachments/assets/d896f956-e5d2-41d4-846b-0ad8bd1aeadb" />
    
## 🐘 Pipeline de datos (desde input hasta output)

El pipeline describe la secuencia de pasos que transforman la captura de pantalla web (Input) en una decisión binaria de RPA (Output: Continuar o Alertar) basada en la detección y comparación de elementos UI.

## Pipeline de Validación RPA con YOLOv8l

| Etapa | Descripción | Componente del Diagrama |
|-------|-------------|-------------------------|
| **1. Input/Adquisición** | El proceso de RPA inicia y toma una **Captura de Pantalla WEB** de la interfaz a validar. | Inicio de Proceso RPA → Captura de Pantalla WEB |
| **2. Preprocesamiento** | Se aplica un **Preprocesamiento** inicial a la imagen capturada, específicamente para eliminar la cabecera del navegador. Esto reduce el ruido y enfoca el modelo YOLOv8l en el contenido relevante de la UI. | Preprocesamiento: eliminar cabecera navegador |
| **3. Inferencia (YOLOv8l)** | La imagen preprocesada se pasa al modelo entrenado YOLOv8l para la **Predicción o Inferencia**. El modelo detecta todos los elementos UI (links, botones, etc.). | Predicción o Inferencia con YOLOv8l |
| **4. Generación de Output Crudo** | El resultado de la inferencia es una **Lista de Bounding Boxes** que contiene las coordenadas, clases y % confianza de todos los objetos detectados en la captura actual. | Resultado: Lista de Bounding Boxes |
| **5. Comparación (Decisión Central)** | Se realiza una **Consulta a la BD** para obtener los Bounding Boxes de la "versión inicial" (línea base). Estos boxes recuperados se comparan con los boxes detectados por YOLOv8l en la captura actual. | Consulta a la BD → Comparación de Bounding boxes detectados con los recuperados de la base |
| **6. Output/Acción RPA** | Basado en la etapa de comparación (¿Son Iguales?), el pipeline bifurca hacia una de dos acciones finales: | **Decisión**: ¿Son Iguales? |
| **6a. Sin Cambios (Éxito)** | Si la interfaz es estable (bounding boxes son iguales o aproximadamente iguales), el **Proceso RPA continúa la interacción** esperada. Se envía un correo informativo (académico). | ✅ Proceso RPA continúa interacción |
| **6b. Con Cambios (Fallo)** | Si se detecta una diferencia (No son Iguales), se **Genera Correo de Alerta** a operadores RPA para reajuste, indicando que la interfaz ha cambiado y requiere intervención. | ⚠️ Generar Correo de Alerta para reajuste |
| **7. Fin del Proceso** | El pipeline concluye su ejecución de validación. | Fin del Proceso |

## 📚 Tecnologías y librerías utilizadas con versiones

La implementación del proyecto se basa en un stack de código abierto, con YOLOv8l como núcleo de inteligencia artificial y Electroneek como plataforma de Automatización Robótica de Procesos (RPA).

## Stack Tecnológico del Proyecto

| Tecnología/Librería | Categoría | Propósito en el Proyecto | Versión (Actual) |
|---------------------|-----------|--------------------------|------------------|
| **YOLOv8l** | Modelo de Detección de Objetos | Modelo principal de Deep Learning para la detección rápida y precisa de los 15 elementos de UI (como `link`, `button`, `input`) en las interfaces web. Se accede mediante la librería `ultralytics`. | `ultralytics==8.3.50` |
| **Electroneek** | Plataforma RPA | Motor de Automatización que ejecuta el proceso, toma la captura de pantalla web (Input) y actúa según el Output del modelo de IA (continuar o alertar). | Versión específica de la implementación |
| **Python** | Lenguaje de Programación | Lenguaje base para el desarrollo del pipeline de datos, el entrenamiento del modelo y la integración de las librerías. | `3.10.12` (Colab default) |
| **pandas** | Análisis de Datos | Creación y manipulación de DataFrames para el análisis descriptivo del dataset (conteo y tablas de distribución de clases). | `2.2.2` |
| **NumPy** | Computación Numérica | Manejo eficiente de tensores y vectores para cálculos estadísticos (Media, Desviación Estándar) y la manipulación de las coordenadas de los bounding boxes. | `1.26.4` |
| **Matplotlib / Seaborn** | Visualización (EDA) | Generación de gráficos descriptivos (distribución de clases) y análisis exploratorio de datos (EDA) para dimensiones y relación de aspecto de los bounding boxes. | `3.8.0` / `0.13.2` |
| **opencv-python** (cv2) | Visión por Computadora | Manejo de imágenes, incluyendo las funciones de preprocesamiento (ej. resize, recorte para "eliminar cabecera navegador") y manipulación durante la inferencia. | `4.10.0.84` |
| **yaml** | Configuración | Lectura y gestión del archivo de configuración del dataset (`dataset.yaml`), que contiene las rutas y los nombres de las 15 clases de elementos UI. | `6.0.2` (PyYAML) |
| **collections** (Counter) | Utilidad de Datos | Utilizado para realizar el conteo eficiente de las instancias de cada clase a través de los splits (`train`, `val`, `test`) durante el análisis descriptivo. | Incluido en Python stdlib |

