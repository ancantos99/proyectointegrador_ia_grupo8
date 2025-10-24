# 🚀 Proceso de Entrenamiento de la Red Siamese

Este documento detalla el proceso para entrenar una red siamesa para la detección de cambios en imágenes, basándose en el código proporcionado. El proceso se divide en etapas clave, desde la preparación de los datos hasta la evaluación del modelo final.

## 1. Preparación de Datos: SiameseUIDataset

Se crea una clase de PyTorch, SiameseUIDataset, para gestionar los pares de imágenes.

**Pares de Imágenes:** Los datos se cargan desde un archivo CSV con el formato img_a,img_b,label. El label indica si las imágenes son un par positivo (0, imágenes similares) o un par negativo (1, imágenes diferentes).

**Carga de Imágenes:** La clase lee las rutas de las imágenes, las carga usando la librería PIL y las convierte al formato RGB para asegurar la consistencia.

**DataSet Utilizado:** A partir de los datos del repositorio de huggingface (YashJain/UI-Elements-Detection-Dataset) se armó un data set de pruebas con la estructura:
```
pairs/
├── train/
│    ├── pos_0_a.png, pos_0_b.png, ...
│    ├── neg_0_a.png, neg_0_b.png, ...
├── val/
│    ├── ...
└── test/
     ├── ...
```
Se utilizó:
- label = 0 → similar → distancia debería ser pequeña.
- label = 1 → distinto → distancia debería ser grande.
  
## 2. Preprocesamiento de Imágenes: Transforms

Se utiliza una secuencia de transformaciones para preparar las imágenes antes de la entrada a la red, lo que mejora la robustez del modelo.

**Cambio de Tamaño y Recorte:** Se redimensionan las imágenes a 256x256 y luego se realiza un recorte aleatorio a 224x224.

**Aumentación de Datos:** Se aplican transformaciones aleatorias para simular variaciones del mundo real:

- **Volteo Horizontal:** Con una probabilidad del 10%.
- **Ajuste de Color:** Se modifica el brillo, contraste, saturación y tono.

**Normalización:** Las imágenes se convierten a tensores de PyTorch y se normalizan usando la media y desviación estándar de la base de datos ImageNet, lo cual es una práctica estándar con modelos pre-entrenados.

## 3. Arquitectura de la Red Siamés: SiameseNet

La red neuronal utiliza un modelo pre-entrenado como columna vertebral para la extracción de características.

**Backbone:** Se usa ResNet-50, un modelo de visión por computadora potente y pre-entrenado en ImageNet. El uso de este modelo permite que la red se beneficie de la capacidad de ResNet para extraer características visuales complejas. Se eliminó la capa final para adaptarla a la tarea de incrustación. Se elimin贸 la capa final para adaptarla a la tarea de incrustaci贸n.
**Head:** Se añade un head personalizado compuesto por capas lineales y una función de activación ReLU para proyectar las características del backbone a un espacio de incrustación (embedding) de 512 dimensiones.
**Función forward_once:** Procesa una sola imagen, la pasa a través del backbone y el head, y normaliza el vector de incrustación resultante para que tenga una longitud unitaria. Esto es crucial para la métrica de distancia.
**Función forward:** Toma un par de imágenes, las procesa a través de la red y devuelve sus respectivos vectores de incrustación, listos para calcular la distancia.

## 4. Función de Pérdida: ContrastiveLoss

La función de pérdida contrastiva es fundamental para entrenar la red siamesa.

**Cálculo de la Distancia:** Mide la distancia euclidiana entre los dos vectores de incrustación.
**Lógica de Pérdida:**
- Para pares **positivos o iguales (label = 0)**, la pérdida busca minimizar la distancia entre las incrustaciones, acercándolas.
- Para pares **negativos o distintas (label = 1)**, la pérdida solo se activa si la distancia es menor que un margen (margin = 1.0). Esto empuja las incrustaciones de imágenes diferentes a estar lo suficientemente separadas en el espacio.

## 5. Proceso de Entrenamiento y Evaluación

**Entrenamiento (train_siamese):** Se utiliza el optimizador Adam y un scheduler para ajustar la tasa de aprendizaje. El modelo se entrena en un bucle donde se calcula la pérdida y se actualizan los pesos del modelo.
**Evaluación (evaluate_embeddings):** El rendimiento del modelo se mide utilizando el Área Bajo la Curva ROC (AUC). También se calcula un umbral óptimo para la inferencia, basado en el índice de Youden, que maximiza la diferencia entre la tasa de verdaderos positivos y la tasa de falsos positivos.

## 6. Inferencia (detect_change)

**Uso del Modelo:** Una vez entrenado, el modelo se puede usar para comparar dos nuevas imágenes.
**Decisión:** La función calcula la distancia entre las incrustaciones de las dos imágenes. Si esta distancia es mayor que el umbral óptimo, el modelo determina que ha habido un cambio.

## 7. Evaluación de Métricas
Los mejores resultados se obtuvieron con:
- embedding_size =  512.
- resnet50 en el Backbone

Se obtuvieron las siguientes métricas:
- **AUC:** 0.9130
- **Accuracy:** 0.8300
- **Precision:** 0.8056
- **Recall:** 0.8700
- **F1:** 0.8365
- **Threshold usado:** 0.5169

### 7.1. Interpretación de métricas
- **AUC: 0.9130**
Significa que el modelo tiene un 91.3% de probabilidad de rankear correctamente un par positivo (similar) por debajo de un par negativo (distinto).
→ En otras palabras, el modelo distingue muy bien entre pares similares y distintos.

- **Accuracy: 0.8300 (83%)**
En promedio, 8 de cada 10 pares fueron clasificados correctamente.

- **Precision: 0.8056 (81%)**
Cuando el modelo dice "estos dos son similares", acierta en un 81% de los casos.
→ Baja precisión puede indicar que aún hay algunos falsos positivos (pares distintos clasificados como similares).

- **Recall: 0.8700 (87%)**
De todos los pares realmente similares, el modelo detectó el 87%.
→ Es bastante alto, o sea que el modelo casi no se le escapan los pares correctos.

- **F1: 0.8365 (83.6%)**
Es el balance entre precision y recall, y muestra un desempeño sólido y equilibrado.

- **Threshold usado: 0.5169**
Ese es el punto de corte que mejor separa “similar” y “distinto” para tu dataset de test.

### 7.2. Visualización de la distribución de distancias
<img width="534" height="413" alt="image" src="https://github.com/user-attachments/assets/204fa8e1-04c4-43fc-8bb9-2b74bf88c8ca" />

## 8. Conclusiones generales
- La Red Neuronal Siamese está funcionando bien: el AUC alto muestra que aprendió a separar pares similares/distintos.
- El threshold está bien ajustado, porque Accuracy, Precision, Recall y F1 están todos en un rango alto y equilibrado.
- El modelo es mejor recuperando pares similares (recall alto) que evitando falsos positivos (precision un poco más baja).
→ Esto puede ser positivo (ej: detectar cambios relevantes en webs aunque arrastre algunos falsos positivos).



