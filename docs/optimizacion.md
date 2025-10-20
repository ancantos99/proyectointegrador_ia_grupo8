# Optimización de Hiperparámetros para YOLOV8 con Weights & Biases 
> Optimización de Hiperparámetros para YOLOv8 con Optimización Bayesiana y usando la plataforma Weights & Biases 
## ⚙️ Proceso
Cuando se aborda la detección de objetos, la eficiencia del modelo es primordial. Esto nos obliga a afinar la configuración mediante la selección precisa de hiperparámetros. En este artículo, detallo cómo se logró maximizar el desempeño de YOLOv8 **utilizando la plataforma Weights & Biases (W&B).**
- Se utilizó Optimización Bayesiana
- Se busca Maximizar mAP50
- Se probaron 50 combinaciones
- Idea general: Hacer un sweep rápido a baja resolución y batch grande (640 y 16 fijos) para encuentrar buenas combinaciones de hiperparámetros rápido. Esto te ahorra muchísimo tiempo y GPU.
- Luego transferir y afinar esas configuraciones en el entrenamiento final a alta resolución y batch ( (1920,1080) y 2 ) ya que usar la resolución original de la imágen ha dado buenos resultados.
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

## 📋 Resultados e Implicaciones

#### Análisis de Sensibilidad

<table style="width: 100%; text-align: left; vertical-align: top;">
  <tr>
    <td>
      <h4>Hiperparámetro 1: Optimizer</h4>
      <img src="../results/figures/docs_optimizacion_optimizer.png" style="width: 100%;">
      <span>
      <b>a) Patrón observado: </b>
      <ul>
        <li>AdamW tiene el mejor desempeño promedio (mayor mAP50 y menor variabilidad).</li>
        <li>Adam es similar, pero con más dispersión.</li>
        <li>SGD tiene el rendimiento más bajo.</li>        
      </ul>
      <b>b) Comparación con configuración actual: </b>
      <p>Estoy usando Adam, Cambiar de Adam a AdamW mejoraría el mAP50.</p>
      <b>c) Sensibilidad: </b>
      <p>🔴 CRÍTICO → El optimizador influye fuertemente en el rendimiento.</p>
      </span>
    </td>
    <td style="width: 50%; vertical-align: top;">
      <h4>Hiperparámetro 2: Lr0 (Tasa de aprendizaje inicial)</h4>
      <img src="../results/figures/docs_optimizacion_lro.png" style="width: 100%;">
      <span>
      <b>a) Patrón observado: </b>
      <ul>
        <li>Relación negativa fuerte: a mayor lr0, menor mAP50.</li>
        <li>El mejor desempeño está en valores bajos (~0.001–0.005).</li>
        <li>R² ≈ 0.30 indica una correlación clara.</li>        
      </ul>
      <b>b) Comparación con configuración actual: </b>
      <p>Usamos un lr0 bajo (0.001), estamos en la zona óptima, pero se puede mejorar usando valores menores (~0.00010)</p>
      <b>c) Sensibilidad: </b>
      <p>🔴 CRÍTICO → Cambios pequeños pueden alterar fuertemente el rendimiento.</p>
      </span>
    </td>  
  </tr>
  <tr>
    <td style="width: 49%; vertical-align: top;">
      <h4>Hiperparámetro 3: Momentum</h4>
      <img src="../results/figures/docs_optimizacion_momentum.png" style="width: 100%;">
      <span>
      <b>a) Patrón observado: </b>
      <ul>
        <li>No hay una relación lineal clara, pero valores intermedios (~0.72–0.78) parecen concentrar mAP50 más altos.</li>
        <li>A valores altos (> 0.86 ) el rendimiento tiende a bajar, pero no es una tendencia marcada</li>
      </ul>
      <b>b) Comparación con configuración actual: </b>
      <p>Inicialmente no se usaba, este parámetro se utiliza cuando el Optimizador es SVG. si se elige SVG usar un valor bajo (≈0.72-0.78)</p>
      <b>c) Sensibilidad: </b>
      <p>🟡 MODERADO → Tiene efecto, pero no cambia drásticamente el resultado.</p>
      </span>
    </td>
    <td style="width: 50%; vertical-align: top;">
      <h4>Hiperparámetro 4: Lrf (learning rate final ratio)</h4>
      <img src="../results/figures/doc_optimizacion_lfr.png" style="width: 100%;">
      <span>
      <b>a) Patrón observado: </b>
      <ul>
        <li>Correlación muy débil (R² ≈ 0.02), sin patrón claro.</li>
        <li>Los puntos están dispersos sin tendencia definida.</li>
      </ul>
      <b>b) Comparación con configuración actual: </b>
      <p>Cualquier valor dentro del rango usado funcionaría similar; no se observa ventaja clara.</p>
      <b>c) Sensibilidad: </b>
      <p>🟡 MODERADO → Tiene poca o nula influencia sobre el resultado.</p>
      </span>
    </td>   
  </tr>
  <tr>
    <td style="width: 49%; vertical-align: top;">
      <h4>Hiperparámetro 5: Weight Decay</h4>
      <img src="../results/figures/docs_optimizacion_weightdecay.png" style="width: 100%;">
      <span>
      <b>a) Patrón observado: </b>
      <ul>
        <li>Tendencia ligeramente positiva: mAP50 mejora conforme aumenta weight_decay</li>
        <li>No es lineal fuerte, pero se observa una correlación débil (R² ≈ 0.13).</li>
      </ul>
      <b>b) Comparación con configuración actual: </b>
      <p>No se utiliza, pero se podría utilizar con valores entre (≈0.007–0.009).</p>
      <b>c) Sensibilidad: </b>
      <p>🟡 MODERADO → Tiene efecto, pero no cambia drásticamente el resultado.</p>
      </span>
    </td>
    <td style="width: 50%; vertical-align: top;">
      <h4>Hiperparámetro 6: Augment (Aumento de datos)</h4>
      <img src="../results/figures/docs_optimizacion_augment.png" style="width: 100%;">
      <span>
      <b>a) Patrón observado: </b>
      <ul>
        <li>Las corridas con augment=True muestran ligeramente mayor mAP50 y menor dispersión que augment=False.</li>
        <li>Ambos obtuvieron un mAP50(B) muy similar</li>
      </ul>
      <b>b) Comparación con configuración actual: </b>
      <p>Se utiliza pero con transformaciones muy leves, sin alterar la geometría solo brillo, saturación, etc. Y no tiene un incremento significativo en la mejora de la métrica </p>
      <b>c) Sensibilidad: </b>
      <p>🟢 BAJA → Afecta el rendimiento, pero no de forma dramática. (El aumento ayuda, pero no es el único factor determinante.)</p>
      </span>
    </td>   
  </tr>
</table>

## Importancia de hiperparámetros

Estos resultados provienen del panel de Importancia de Parámetros (Parameter Importance) de Weights & Biases (W&B), generado después de ejecutar una búsqueda de hiperparámetros (Sweep) para un modelo de detección de objetos (probablemente YOLOv8).

El gráfico tiene como objetivo mostrar cuáles de los hiperparámetros que probaste tuvieron el mayor impacto en la métrica objetivo, que en este caso es el metrics/mAP50 (Mean Average Precision al umbral de IoU 0.50).

![Optimización 1](../results/figures/docs_optimizacion1.png)

- **Columna Importancia:** Cuanto más larga sea la barra azul, más influyente fue ese parámetro en el resultado final del rendimiento (mAP50).
- **Columna Correlation:** Esta columna visualiza la relación direccional (positiva o negativa) entre el parámetro y la métrica mAP50.
  - Barra Verde (Positiva 🟢): A medida que el valor del parámetro aumenta, el mAP50 tiende a aumentar (relación directa).
  - Barra Roja (Negativa 🔴): A medida que el valor del parámetro aumenta, el mAP50 tiende a disminuir (relación inversa).

## Conclusiones para la Optimización

1. **Runtime:** Es el parámetro más influyente en el gráfico. Puede indicar que el tiempo de ejecución (o la cantidad de épocas/pasos realizados) es el factor dominante, o que W&B usó esta variable proxy para medir el impacto de la duración del entrenamiento.
2. **Enfocarse en la Tasa de Aprendizaje (lr0):** Dado que es el hiperparámetro con mayor impacto (y tiene una fuerte correlación negativa), debes priorizar probar valores más pequeños de lr0 en futuras búsquedas.
3. **Regularización (weight_decay):** Este parámetro también es importante. Su correlación positiva sugiere que podrías probar valores ligeramente más altos para mejorar el rendimiento.
4. **Optimizador:** La correlación negativa de optimizer: SGD y la positiva de optimizer:value_AdamW (aunque con baja importancia) sugieren que AdamW podría ser una mejor opción inicial que SGD para tu modelo y conjunto de datos.
5. **lrf:** La correlación negativa de optimizer: SGD y la positiva de optimizer:value_AdamW (aunque con baja importancia) sugieren que AdamW podría ser una mejor opción inicial que SGD para tu modelo y conjunto de datos.
6. **Parámetros Menos Importantes:** se puede gastar menos tiempo en ajustar parámetros con baja importancia (como momentum o augment), ya que cambiarlos probablemente no generará una mejora dramática en el rendimiento. El parámetro momentum solo tiene sentido usarlo si se utiliza el Optimizador SGD
7. **imgsz o lrf:** en el entrenamiento final utilizar el tamaño real de la imágen que ha dado buenos resultados Pero incrementa la cantidad de 

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


lr_0 = 0.01, batch_proxy=16, batch_final=2 → lr_final = 0.01 * (2/16) = 0.00125.

Exp3
results_dict: {'metrics/precision(B)': 0.7964556325233887, 'metrics/recall(B)': 0.21359048200126907, 'metrics/mAP50(B)': 0.2523554905035456, 'metrics/mAP50-95(B)': 0.20580211889200103, 'fitness': 0.20580211889200103}

Final Metrics (last epoch):
Precision: 0.6704
Recall:    0.2338
F1-score:  0.3467

Clase	Precision	Recall	F1	mAP50
0	link	0.796361	0.485337	0.603112	0.56649
1	button	0.830692	0.493997	0.619555	0.599194
2	input	0.955417	0.666667	0.785341	0.757747



results_dict: {'metrics/precision(B)': 0.707373496530193, 'metrics/recall(B)': 0.2434078433420458, 'metrics/mAP50(B)': 0.27167244196342755, 'metrics/mAP50-95(B)': 0.21281179895108382, 'fitness': 0.21281179895108382}

Final Metrics (last epoch):
Precision: 0.6722
Recall:    0.2489
F1-score:  0.3633
Clase	Precision	Recall	F1	mAP50
0	link	0.765659	0.565302	0.6504	0.601146
1	button	0.781648	0.536878	0.636544	0.608453
2	input	0.882485	0.69544	0.777877	0.740863
