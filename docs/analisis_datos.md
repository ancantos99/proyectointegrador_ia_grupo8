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

### Contenido del dataset

- Capturas de pantalla de sitios web: se afirma que provienen de más de 300 sitios web populares.
- Resolución de las imágenes: 1920×1080 px
- Formato de anotaciones: anotaciones en formato YOLO.
- Metadatos adicionales: incluye metadata de accesibilidad (“rich accessibility metadata”)

### Clases / categorías de elementos

- El dataset define 15 clases principales de elementos de UI. Se agrupan en varias categorías conceptuales:

- **1.- Interactive Elements** (elementos interactivos)
- **2.- Structural Elements** (elementos estructurales)
- **3.- Form Elements** (elementos de formulario
- **clases:** 0: link, 1: button, 2: input, 3: select, 4: textarea, 5: label, 6: checkbox, 7: radio, 8: dropdown, 9: slider, 10: toggle, 11: menu_item, 12: clickable, 13: icon, 14: image, 15: text

## 📋 Estadísticas descriptivas


### Distribución Detallada de Clases (Total)

| ID | Clase | Train | Val | Test | Total | % Total |
|----|-------|-------|-----|------|-------|---------|
| 0 | link | 15583 | 1563 | 2222 | 19368 | 64.48% |
| 1 | button | 5101 | 627 | 877 | 6605 | 21.99% |
| 2 | input | 354 | 54 | 44 | 452 | 1.50% |
| 3 | select | 0 | 0 | 0 | 0 | 0.00% |
| 4 | textarea | 26 | 8 | 3 | 37 | 0.12% |
| 5 | label | 1032 | 59 | 37 | 1128 | 3.76% |
| 6 | checkbox | 42 | 0 | 9 | 51 | 0.17% |
| 7 | radio | 54 | 6 | 16 | 76 | 0.25% |
| 8 | dropdown | 799 | 88 | 93 | 980 | 3.26% |
| 9 | slider | 15 | 2 | 1 | 18 | 0.06% |
| 10 | toggle | 8 | 0 | 0 | 8 | 0.03% |
| 11 | menu_item | 820 | 103 | 115 | 1038 | 3.46% |
| 12 | clickable | 23 | 5 | 1 | 29 | 0.10% |
| 13 | icon | 141 | 55 | 49 | 245 | 0.82% |
| 14 | image | 0 | 0 | 0 | 0 | 0.00% |
| 15 | text | 0 | 0 | 0 | 0 | 0.00% |
| **TOTAL** | **INSTANCIAS** | **23998** | **2570** | **3467** | **30035** | **100.00%** |

Nota: Hay Clases sin elementos, para nuestro proyecto las clases más importantes son Link, button e input (estas interactuan más con el RPA)

### Distribución por Categoría de Sitio Web

| Categoría | Porcentaje |
|----------|------------|
| Sitios Más Visitados | 45% |
| Aplicaciones Web | 15% |
| Comercio Electrónico | 10% |
| Redes Sociales | 10% |
| Noticias y Medios | 10% |
| Herramientas para Desarrolladores | 5% |
| Plataformas Creativas | 5% |

Nota: El porcentaje de sitios web que nos interesa ( Aplicaciones web ) es 15%, un poco bajo

### Distribución de objetos por Subconjunto
<img width="790" height="490" alt="image" src="https://github.com/user-attachments/assets/d28b5e8b-3924-4f04-a314-06d3cbde5869" />

### Análisis Descriptivo de las Instancias de Clases (Train)

| Métrica | Valor | Observaciones |
|---------|-------|-------|
| Media (Mean) | 1,499.88 | Por sí sola, sugiere un tamaño de entrenamiento adecuado, pero es engañosa porque está inflada por una clase muy grande que es link  
| Mediana (Median) | 48.00 | Valor central. Significa que la mitad de tus clases tienen 48 instancias o menos en el conjunto de entrenamiento (la mayoría de las clases son minoritarias) |
| Moda (Mode) | 0 | Indica que una o más clases no tienen ninguna instancia (bounding box) |
| Desv. Estándar (Std Dev) | 3,835.55 | El alto valor (más del doble de la Media) indica que los conteos de clase están extremadamente dispersos alrededor de la media (hay un desbalance, el modelo aprenderá muy bien la clase mayoritaria e ignorará o fallará en las minoritarias)
| Rango (Range) | 15,583.00 | Muestra una diferencia de 15,583 instancias entre la clase más grande y la más pequeña |
| Mínimo (Min) | 0.00 | La clase menos representada tiene 0 instancias. El modelo no podrá aprender a detectar estas clases, y su recall (capacidad de encontrar positivos) será cero para ellas.|
| Máximo (Max) | 15,583.00 | La clase más representada tiene más de 15 mil instancias (link) |

<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/9f182e77-3f58-4c6d-ba9e-8160cfff9bb0" />

### Observación Clave sobre el Desbalance en TRAIN (Original)

| Aspecto | Descripción |
|---------|-------------|
| ⚠️ **Clases No Representadas en TRAIN** | `select`, `image`, `text` (0 instancias) |
| **Desbalance Máximo** | La clase más frecuente (**link** con 15,583 instancias) tiene **1,947.88** veces más instancias que la menos frecuente (**toggle** con 8 instancias) en TRAIN |
| 🚨 **Conclusión** | **Desbalance SIGNIFICATIVO**: Se requiere aplicar técnicas robustas de balanceo (*oversampling*, *pérdida ponderada* o *Data Augmentation* avanzada) |


## 📊 Visualizaciones del EDA (Análisis de Dimensiones de Bounding Boxes)

### Distribución de Ancho vs Alto de los Bounding Boxes

Nota: Se filtró el 1% superior de objetos por tamaño (W > 0.5251, H > 0.3866) para mejor visualización.
<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/3382e1f9-8d79-44aa-838d-8fdbd103b65c" />

### Densidad de Dimensiones de los Bounding Boxes

La agrupación de puntos en el Scatter Plot indica los tamaños de objetos que predominan y ayuda a optimizar los **Anclajes (Anchors)** del modelo YOLOv8.
<img width="598" height="616" alt="image" src="https://github.com/user-attachments/assets/956a32dd-778a-401c-bf23-516239e60447" />

### Distribución de Coordenadas centrales (x,y)

Este mapa de calor muestra si los objetos están sesgados a ciertas áreas de la pantalla, lo cual es común en interfaces web.
<img width="776" height="790" alt="image" src="https://github.com/user-attachments/assets/fd20ff0d-3ebc-4392-ac2d-a490286d5039" />

### Distribución de la Relación Aspecto (Ancho/Alto)

Los picos en este histograma indican las formas más comunes de los objetos (cuadrados, anchos, altos).

Esta información es vital para la selección o ajuste de los **anclajes (anchor boxes)** del modelo YOLOv8, asegurando que los anclajes predefinidos coincidan con las formas reales de los objetos en tus interfaces.
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/1ff31f91-c331-416e-b01f-7afa6fc9b75e" />

### Distribución del Número de Objetos por Imagen

Media de objetos por imagen: 43.47. Esto define si el modelo debe ser optimizado para pocas o muchas detecciones por pantalla.
<img width="989" height="490" alt="image" src="https://github.com/user-attachments/assets/8bc530bc-fcb1-4ec8-907c-ab1988e90661" />

## 🔎 Identificación de patrones, correlaciones, outliers

El EDA nos ayuda a confirmar que la arquitectura multi-escala de YOLOv8 es adecuada, ya que nuestro dataset tiene una gran variación de tamaños (desde objetos pequeños hasta grandes)

Así mismo el EDA revela patrones críticos en la distribución, tamaño y ubicación de los elementos de interfaz de usuario (UI elements), que deben guiar la configuración del modelo YOLOv8.

| Elemento Analizado | Patrones Identificados | Implicaciones para el Modelo |
|-------------------|------------------------|------------------------------|
| **Distribución de Coordenadas Centrales** | **Sesgo Posicional Extremo**: La mayor densidad de bounding boxes se concentra en los bordes horizontales (eje Y cerca de 0.0 y 1.0) y, en menor medida, en los bordes verticales. | El modelo debe ser eficiente detectando elementos comunes en los encabezados y pies de página de las páginas web (típico de menús, footers, etc.). |
| **Distribución de Ancho vs. Alto** | **Doble Agrupación**: Se observa una fuerte concentración de objetos muy pequeños y cuadrados/ligeramente horizontales (Ancho y Alto Normalizado ≈ 0.0 a 0.1). También hay dispersión de objetos de tamaño mediano y grande, especialmente en formatos anchos. | La arquitectura multi-escala de YOLO es necesaria para manejar la gran diferencia de tamaños: desde íconos minúsculos hasta barras de búsqueda o banners grandes. |
| **Relación de Aspecto (Aspect Ratio)** | **Dominio Horizontal**: El histograma muestra un pico principal claramente por debajo del Ratio 1:1 (Cuadrado) y sesgado hacia la izquierda (objetos más altos que anchos). Sin embargo, la mayor frecuencia se centra alrededor de los ratios 1:2 (Alto y Delgado) y 2:1 (Ancho y Bajo). | La mayoría de los UI elements (links, botones, inputs) son rectangulares y anchos (Horizontalmente dominantes). Esto confirma que los anchor boxes de YOLOv8 deben estar ajustados a estas proporciones. |
| **Objetos por Imagen** | **Densidad Media Alta**: La media de objetos por imagen es de 43.47. El histograma muestra que la mayoría de las imágenes tienen entre 10 y 50 objetos. | El modelo debe ser computacionalmente eficiente y optimizado para la detección de múltiples objetos simultáneamente en escenarios de alta congestión. |
| **Outliers (Tamaño)** | Se filtró el 1% superior de los objetos por tamaño (ej. W > 0.5251, H > 0.3866). | Estos outliers representan elementos de pantalla muy grandes (ej. tablas completas o grandes bloques de texto), que no deben dominar la optimización de los anchor boxes. |

## 🎯 Decisiones de preprocesamiento justificadas

Las siguientes decisiones de preprocesamiento se justifican por los patrones identificados y la naturaleza del dataset para optimizar el rendimiento del modelo en un contexto RPA:

### 1️⃣ Enfoque en Clases de Interacción
#### 📋 Justificación
El proyecto se centra en procesos RPA, donde las interacciones clave son `link`, `button` e `input`. Aunque el dataset tiene 15 clases, se priorizará el buen rendimiento en estas clases interactivas.
#### ✅ Decisión
Se considerarán estrategias de **pérdida ponderada** (*Weighted Loss*) para dar más importancia a los errores en las clases `link`, `button` e `input` que en otras clases de menor relevancia para RPA.

### 2️⃣ Manejo de la Resolución y Normalización
#### 📋 Justificación
Las imágenes tienen una resolución fija de **1920 × 1080 px**. Las coordenadas de los bounding boxes ya están normalizadas (valores entre 0 y 1).
#### ✅ Decisión
- ✔️ No se requiere preprocesamiento de normalización de coordenadas
- ✔️ El resizing estándar de YOLOv8 (típicamente **640 × 640**) se aplicará al inicio de la fase de entrenamiento para encontrar los mejores hiperparámetros
- ✔️ Se mantendrá la resolución original para los entrenamientos finales

### 3️⃣ Configuración de Anclajes (Anchors o Dimensiones)
#### 📋 Justificación
La distribución de la relación de aspecto y dimensiones apunta a un dominio de objetos horizontales y una gran variación de tamaños.
#### ✅ Decisión
se deberá ajustar los hiperparámetros relacionados con el bounding box y la pérdida, lo que afecta indirectamente cómo el modelo predice las dimensiones

## 🛠️ Manejo de datos faltantes o desbalanceados

El análisis descriptivo revela un desbalance de clases severo en el conjunto de entrenamiento (Train), lo cual es el mayor desafío para este dataset.

### Desafíos del Dataset y Estrategias de Mitigación

| Desafío | Diagnóstico de las Métricas | Estrategia de Mitigación |
|---------|----------------------------|--------------------------|
| **Desbalance Extremo** | La clase dominante (`link`) tiene 15,583 instancias, mientras que la clase menos frecuente (`toggle`) tiene solo 8 instancias. El ratio de desbalance es de **1,947.88×**. La Desviación Estándar es muy alta (3,835.55) y la Mediana es muy baja (48.00). | Aplicación de **Pérdida Ponderada** (*Weighted Loss*) en la configuración de entrenamiento de YOLOv8. Esto asignará un peso mayor a los errores de las clases minoritarias (ej. `toggle`, `clickable`), forzando al modelo a prestarles más atención. |
| **Clases con Cero Instancias (Datos Faltantes)** | Tres clases (`select`, `image`, `text`) tienen **0 instancias** en el conjunto de entrenamiento (`Train`). El Mínimo es **0.00** y la Moda es **0**. | **Exclusión o Fusión de Clases**: Se debe considerar eliminar las clases con 0 instancias (`select`, `image`, `text`) si no son críticas para el RPA, o fusionarlas si conceptualmente tienen relación (p. ej., si el RPA no necesita distinguir `image` de `icon`). |
| **Clases Minoritarias Críticas** | Clases como `toggle` (8 instancias), `clickable` (23 instancias), y `textarea` (26 instancias) son insuficientes para un entrenamiento robusto. | **Data Augmentation Avanzada**: Se aplicarán técnicas de aumento de datos (*Data Augmentation*) como MixUp o Copy-Paste específicamente en estas clases minoritarias. Esto generará nuevas imágenes de entrenamiento con más instancias de estas clases, mitigando artificialmente el desbalance. |


