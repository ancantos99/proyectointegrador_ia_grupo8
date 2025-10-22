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

#### *Observaciones*
Hay Clases sin elementos, para nuestro proyecto las clases más importantes son Link, button e input (estas interactuan más con el RPA)

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

#### *Observaciones*
El porcentaje de sitios web que nos interesa ( Aplicaciones web ) es 15%, un poco bajo

### Distribución de objetos por Subconjunto
<img width="790" height="490" alt="image" src="https://github.com/user-attachments/assets/d28b5e8b-3924-4f04-a314-06d3cbde5869" />

## Análisis Descriptivo de las Instancias de Clases (Train)

| Métrica | Valor | Observaciones |
|---------|-------|-------|
| Media (Mean) | 1,499.88 | Por sí sola, sugiere un tamaño de entrenamiento adecuado, pero es engañosa porque está inflada por una clase muy grande que es link  
| Mediana (Median) | 48.00 | Valor central. Significa que la mitad de tus clases tienen 48 instancias o menos en el conjunto de entrenamiento (la mayoría de las clases son minoritarias) |
| Moda (Mode) | 0 | Indica que una o más clases no tienen ninguna instancia (bounding box) |
| Desv. Estándar (Std Dev) | 3,835.55 | El alto valor (más del doble de la Media) indica que los conteos de clase están extremadamente dispersos alrededor de la media (hay un desbalance, el modelo aprenderá muy bien la clase mayoritaria e ignorará o fallará en las minoritarias)
| Rango (Range) | 15,583.00 | Muestra una diferencia de 15,583 instancias entre la clase más grande y la más pequeña |
| Mínimo (Min) | 0.00 | La clase menos representada tiene 0 instancias. El modelo no podrá aprender a detectar estas clases, y su recall (capacidad de encontrar positivos) será cero para ellas.|
| Máximo (Max) | 15,583.00 | La clase más representada tiene más de 15 mil instancias (link) |

### Observación Clave sobre el Desbalance en TRAIN (Original)

| Aspecto | Descripción |
|---------|-------------|
| ⚠️ **Clases No Representadas en TRAIN** | `select`, `image`, `text` (0 instancias) |
| **Desbalance Máximo** | La clase más frecuente (**link** con 15,583 instancias) tiene **1,947.88** veces más instancias que la menos frecuente (**toggle** con 8 instancias) en TRAIN |
| 🚨 **Conclusión** | **Desbalance SIGNIFICATIVO**: Se requiere aplicar técnicas robustas de balanceo (*oversampling*, *pérdida ponderada* o *Data Augmentation* avanzada) |

## 📊 Visualizaciones del EDA (mínimo 5-6 gráficos relevantes)



## 🔎 Identificación de patrones, correlaciones, outliers
## 🧹 Decisiones de preprocesamiento justificadas
## 🛠️ Manejo de datos faltantes o desbalanceados
