# Optimización de Hiperparámetros para YOLOV8 con Weights & Biases 
> Optimización de Hiperparámetros para YOLOv8 con Optimización Bayesiana y usando la plataforma Weights & Biases 
## ⚙️ Proceso
Cuando se aborda la detección de objetos, la eficiencia del modelo es primordial. Esto nos obliga a afinar la configuración mediante la selección precisa de hiperparámetros. En este artículo, detallo cómo se logró maximizar el desempeño de YOLOv8 **utilizando la plataforma Weights & Biases (W&B).**
- Se utilizó Optimización Bayesiana
- Se busca Maximizar mAP50
- Se probaron 50 combinaciones
### ¿Por qué Optimización Bayesiana?
Optimización Bayesiana (BO) es un enfoque inteligente para buscar hiperparámetros cuando:
- El espacio de hiperparámetros es grande o costoso de evaluar.
- Cada entrenamiento tarda mucho (como en YOLOv8).
### ¿Por qué Maximizar mAP50?
mAP50 significa Precisión Media Promedio con un IoU de 0.5. En términos simples, evalúa cuán bien las cajas delimitadoras predichas por nuestro modelo se superponen con las cajas delimitadoras reales. Maximizar mAP50 significa que nuestro modelo no solo está detectando objetos, sino que también está ubicándolos con precisión.
¿Por qué elegí maximizar mAP50 sobre mAP50-95? Al entrenar nuestro modelo por primera vez con hiperparámetros predeterminados, observamos que mAP50 alcanzó su valor óptimo alrededor de la marca de 50 épocas, mientras que mAP50-95 tomó más tiempo, estabilizándose pasada las 70 épocas

## ✍️ Hiperparámetros explorados y rangos
El modelo YOLOv8 (You Only Look Once) es ampliamente utilizado en tareas de detección de objetos debido a su alta eficiencia. Su rendimiento depende de varios hiperparámetros. En este análisis se considerarán 8 de ellos, de los cuales dos (imgsz y batch) ya se conocen sus valores óptimos para obtener un mejor desempeño. Además, se evita modificar estos parámetros porque hacerlo incrementa significativamente el costo computacional y el tiempo de entrenamiento.
| # | Hiperparámetro | Descripción | Rango |
| :--- | :--- | :--- | :--- |
| **1** | **imgsz** |Tamaño de imagen: Afecta la resolución de las imágenes introducidas en el modelo.  | para la optimización de hiperparámetros se redimensionará a 640. Pero hemos descubierto que los mejores resultados se obtienen con el tamaño original de la imágen (1920,1080) aunque usar esta resolución consume más recursos computacionales y eleva el tiempo de entrenamiento |
| **2** | **batch** | Tamaño del lote: Determina la cantidad de muestras procesadas antes de que el modelo actualice sus pesos | ara la optimización de hiperparámetros se utilizará un lote de 16 ya que al redimensionar la imágen con 640 no cosume mucha vram, pero cuando se utiliza (1920,1080) hay que utilizar un batch de 1 o max 2 ya que puede llegar a consumar hasta 30Gb de Vram  |
| **3** | **optimizer** | Es el algoritmo encargado de actualizar los pesos del modelo durante el entrenamiento para que la red aprenda a detectar objetos correctamente. | 'SGD', 'Adam', 'AdamW' |
| **4** | **momentum** | es un parámetro del optimizador (Solo se usa cuando se prueba con SGD) que acelera el aprendizaje y suaviza las actualizaciones de los pesos del modelo durante el entrenamiento | {'min': 0.7, 'max': 0.97} |
| **5** | **augment** | Indica si introducir o no cambios aleatorios en los datos de entrada aumenta la robustez del modelo | [True, False] |
| **6** | **lr0** | Tasa de aprendizaje: Controla cuánto ajustar el modelo en respuesta al error estimado cada vez que se actualizan los pesos del modelo | "min": 1e-5, "max": 1e-1 |
| **7** | **lrf** | lrf define la tasa de aprendizaje final al final del entrenamiento (en la última época). YOLOv8 ajusta la tasa de aprendizaje de forma exponencial o cosenoidal desde el valor inicial (lr0) hasta lr0 * lrf. | "min": 0.01, "max": 1.0 |
| **8** | **weight_decay** | Factor de regularización L2 para evitar el sobreajuste. Los valores más grandes imponen una regularización más fuerte | 'min': 0.0001, 'max': 0.01 |

## Configuración y Redimiento Inicial

<table style="width: 100%;">
<tr>
  <td style="width: 33%; vertical-align: top;"><h4 align="center">Hiperparámetros Iniciales</h4></td>
  <td style="width: 33%; vertical-align: top;"><h4 align="center">Métricas de Rendimiento Inicial General</h4></td>
  <td style="width: 33%; vertical-align: top;"><h4 align="center">Métricas de Rendimiento Inicial Por Clase</h4></td>
</tr>
<tr>
  <td style="width: 33%; vertical-align: top;">   
    <ul>
      <li><b>imgsz</b> : (1920,1080)</li>
      <li><b>batch</b> : 1</li>
      <li><b>optimizer</b> : Adam</li>
      <li><b>lr0</b> : 0.001</li>
      <li><b>lrf</b> : 0.01</li>
      <li><b>patience</b> : 15</li>
    </ul>
  </td>
  <td style="width: 33%; vertical-align: top;">
    <ul>
      <li><b>Precision</b> :  0.4764</li>
      <li><b>Recall</b> : 0.1636  </li>
      <li><b>F1-score</b> : 0.2436 </li>
      <li><b>mAP@50</b> : 0.159</li>   
    </ul>
  </td>
  <td style="width: 33%; vertical-align: top;">
    <table>
      <tr><th>Clase</th><th>Precision</th><th>Recall</th><th>F1-score</th><th>mAP@50</th></tr>
      <tr><th>0-link</th><td>0.468352</td><td>0.375569</td><td>0.41686</td><td>0.332972</td></tr>
      <tr><th>1-button</th><td>0.457078</td><td>0.444254</td><td>0.450574</td><td>0.394805</td></tr>
      <tr><th>2-input</th><td>0.718178</td><td>0.388889</td><td>0.504561</td><td>0.454618</td></tr>
    </table>
  </td>
</tr>
</table>

## 📋 Resultados del análisis de sensibilidad

#### Imágenes

#### Tabla resumen
| # | Hiperparámetro | Nivel de Sensibilidad | Valor Actual | Valor Óptimo | Mejora Potencial |
| :--- | :--- | :--- | :--- |:--- |:--- |
| **optimizer** | 🔴 Crítico | Adadm | 
| **momentum** | 🟡 Moderado |
| **lr0** | 🔴 Crítico |
| **lrf** | 🔴 Crítico |
| **weight_decay** | 🔴 Crítico |
| **augment** | 🟢 Bajo |

Ejemplo de imagen:
![Captura de pantalla de la aplicación](ruta/a/tu/imagen.png)

***

## 🚀 Empezando

Estas instrucciones te guiarán para obtener una copia de este proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

### 📋 Prerrequisitos

Enumera el software y las herramientas que necesitas tener instaladas antes de comenzar (ej. Node.js, Python, Docker, etc.).

```bash
# Ejemplo de un prerrequisito:
Node.js versión 18+
