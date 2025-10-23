<p align="center">
  <h1> Detección de Cambios en Interfaces Web para Procesos RPA utilizando Inteligencia Artificial</h1>
</p>

## 📌 Descripción

Este proyecto aborda la fragilidad de los procesos de Automatización Robótica de Procesos (RPA) frente a cambios visuales en interfaces web.  
Propone un módulo basado en Visión por Computadora y Redes Neuronales Convolucionales (CNN) que detecta automáticamente dichas alteraciones, sin depender de localizadores tradicionales.  
Esto permite identificar y notificar cambios relevantes en la interfaz, mejorando la fiabilidad del monitoreo y reduciendo el tiempo de diagnóstico e intervención manual.

## 🧰 Tecnologías Clave

- **Lenguaje principal:** Python 3.8+
- **Librerías principales:** 
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

[5. Metodología](#5-metodología)

[6. Resultados](#6-resultados)

[7. Instalación y Uso](#7-instalación-y-uso)

[8. Diseño detallado de automatización e IA](#8-diseño-detallado-de-automatización-e-ia)

[9. Estructura del proyecto](#9-estructura-del-proyecto)

[10. Consideraciones Éticas](#10-consideraciones-éticas)

[11. Autores y Contribuciones](#11-autores-y-contribuciones)

[12. Licencia](#12-licencia)

[13. Agradecimientos y Referencias](#13-agradecimientos-y-referencias) 
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
    
## 6. Resultados

### 📈 Métricas Finales del Modelo (YOLOv8 Optimizado)

A continuación, se presentan los resultados obtenidos tras aplicar un proceso de optimización de hiperparámetros al modelo YOLOv8 utilizando Optimización Bayesiana y la plataforma Weights & Biases (W&B).

<table style="width: 100%;">
<tr>
  <td style="width: 33%; vertical-align: top;"><h4 align="center">Hiperparámetros Iniciales</h4></td>
  <td style="width: 33%; vertical-align: top;"><h4 align="center">Métricas de Rendimiento Inicial General</h4></td>
  <td style="width: 33%; vertical-align: top;"><h4 align="center">Métricas de Rendimiento Inicial Por Clase</h4></td>
</tr>
<tr>
  <td style="width: 33%; vertical-align: top;">   
    <ul>
      <li><b>epochs</b>: 100</li>
      <li><b>imgsz</b> : (1920,1080)</li>
      <li><b>batch</b> : 6</li>
      <li><b>optimizer</b> : AdamW</li>
      <li><b>lr0</b> :0.00004694921598565255</li>
      <li><b>lrf</b> : 0.46315</li>
      <li><b>weight_decay</b> : 0.00808107114573286</li>
      <li><b>patience</b> : 15</li>
    </ul>
  </td>
  <td style="width: 33%; vertical-align: top;">
    <ul>
      <li><b>Precision</b> : 0.7616</li>
      <li><b>Recall</b> :   0.2383</li>
      <li><b>F1-score</b> :  0.3630</li>
      <li><b>mAP@50</b> : 0.268</li>   
    </ul>
  </td>
  <td style="width: 33%; vertical-align: top;">
    <table>
      <tr><th>Clase</th><th>Precision</th><th>Recall</th><th>F1-score</th><th>mAP@50</th></tr>
      <tr><th>0-link</th><td>0.788805</td><td>0.507472</td><td>0.61761</td><td>0.581007</td></tr>
      <tr><th>1-button</th><td>0.785473</td><td>0.685185</td><td>0.631176</td><td>0.598784</td></tr>
      <tr><th>2-input</th><td>0.841365</td><td>0.685185</td><td>0.755286</td><td>0.737391</td></tr>
    </table>
  </td>
</tr>
</table>


### 🔁 Comparación con Baseline

La comparación se realizó contra dos líneas base:

| Aspecto | Configuración Original | Configuración Optimizada | Cambio | 
| :--- | :--- | :--- | :--- |
| Métrica principal mAP50(B) | 0.1636 | 0.268 | +63.81% |
| Precision | 0.4764 |  0.7616 | +59.86% |
| Recall | 0.1636 |   0.2383 | +45.05% |
| Tiempo de entrenamiento | 8591.96 minutos (100 épocas con early stopping 15: se corrieron 63 épocas)| 6891.00 minutos (100 épocas con early stopping 15: se corrieron 100 épocas) | -19.79% |
| Tamaño del modelo | 83.8 MB | 83.8 MB | 0% |
| Gpu Utilizada | GPU t4 | GPU A100 | N/A |
| Complejidad del modelo |  Alta |  Alta|  N/A |

> La optimización de hiperparámetros en YOLOv8 generó una mejora sustancial del 63.81% en mAP@50, incrementando también precisión y recall sin modificar la arquitectura del modelo. El uso de una GPU A100 permitió reducir el tiempo de entrenamiento en casi 20%, a pesar de completar más épocas. El modelo mantiene su tamaño (83.8 MB) y complejidad, pero con un rendimiento significativamente superior. Estos resultados validan la efectividad de ajustar parámetros clave como lr0, optimizer y weight_decay. La mejora se logra con la misma arquitectura, pero con un aprendizaje mucho más eficiente.

### 📊 Visualización del Rendimiento

Para evaluar la efectividad y rendimiento del modelo de detección visual implementado con YOLOv8, se realizaron múltiples ejecuciones de entrenamiento con distintas configuraciones. El gráfico a continuación muestra la evolución del rendimiento del modelo en función del métrico mAP@0.5 (mean Average Precision con umbral IoU de 0.5), que es un estándar en tareas de detección de objetos.
Cada línea representa una variante de entrenamiento identificada por su nombre de ejecución, y permite visualizar cómo mejora la precisión del modelo a lo largo de los pasos de entrenamiento. Este análisis es clave para:
- Comparar el desempeño entre diferentes configuraciones.
- Identificar ejecuciones con mayor estabilidad y precisión.
- Seleccionar el modelo más robusto para integrarlo en el asistente RPA.
El gráfico evidencia una tendencia general de mejora, lo que valida la efectividad del enfoque basado en visión por computadora para detectar cambios en interfaces web.

<img width="1910" height="961" alt="image" src="https://github.com/user-attachments/assets/3a65c9c7-b2e6-4151-8e6d-3dae9a8fda15" />

## 7. Instalación y Uso

Este componente de IA utiliza la librería **YOLOv8** para la detección de elementos visuales, y su uso está integrado en el flujo de la herramienta de Automatización Robótica de Procesos (RPA) **ElectroNeek**.

### 🖥️ Requisitos del sistema

Para que el proyecto funcione correctamente, se requiere la instalación y configuración de varias aplicaciones y sistemas, además de contar con los permisos de acceso necesarios:

| Requisito             | Tipo                 | Detalles                                                                 |
|-----------------------|----------------------|--------------------------------------------------------------------------|
| Python                | Herramienta de desarrollo | Se utiliza como lenguaje base para la lógica de IA.                  |
| SQL Server            | Base de datos         | Utilizado para almacenar los resultados generados por el modelo (deteccionesYolo). |
| ElectroNeek           | Herramienta RPA       | Plataforma principal de automatización con la que se integra el sistema. |
| Servicio de Microsoft | Gestor de Correo      | Se requiere para el envío de notificaciones automáticas.                |
| Google Chrome         | Navegador Web         | Necesario para acceder a los portales públicos de validación (SRI y Senescyt). |
| Credenciales de Acceso| Usuarios              | Se requieren credenciales para la Base de Datos (**Andrés Cantos**), correo electrónico y acceso al SRI (**Paola Mendoza**). |

### ⚙️ Instrucciones paso a paso para instalar

La instalación se centra principalmente en configurar el entorno de Python para que pueda ejecutar el modelo de Visión por Computadora (**YOLOv8**):

1. **Instalar Librerías Python (Requisitos Previos):**  
   Antes de ejecutar el proyecto, asegúrate de instalar las siguientes librerías con `pip`:

| Paquete | Paquete | Paquete |
|----------|----------|----------|
| certifi | charset-normalizer | contourpy |
| cycler | filelock | fonttools |
| fsspec | idna | Imagegrab |
| Jinja2 | kiwisolver | MarkupSafe |
| matplotlib | mpmath | networkx |
| numpy | opencv-python | packaging |
| pillow | pip | polars |
| polars-runtime-32 | psutil | pyodbc |
| pyparsing | python-dateutil | pywin32 |
| PyYAML | requests | scipy |
| setuptools | six | sympy |
| torch | torchvision | typing_extensions |
| ultralytics | ultralytics-thop | urllib3 |


**2. Configuración de Base de Datos (Opcional)**

Si se utiliza una base de datos para almacenar los resultados (como SQL Server):

- Configura la clase `YOLOResultsDB` ubicada en la carpeta base del proyecto.
- Asegúrate de instalar el conector ODBC de Python para SQL Server ejecutando

**3. Verificación del Modelo**

Se debe validar que el archivo del modelo (.pt) exista en la ruta configurada y que la versión de ultralytics esté correctamente instalada. En caso de error, se recomienda reinstalar con pip install --upgrade ultralytics.

**4. Requisito de Instalación y Acceso a la Plataforma RPA ElectroNeek**
El proyecto está diseñado para operar dentro del ecosistema de la plataforma RPA ElectroNeek. Por lo tanto, esta herramienta no es una dependencia secundaria, sino el entorno principal de ejecución del Bot:
1. Necesidad de Instalación en el Equipo:
    ◦ ElectroNeek está clasificado como una Herramienta RPA cuya Interfaz de Usuario es de tipo Escritorio.
    ◦ Dado su tipo de interfaz, se requiere que la plataforma esté instalada y configurada en el equipo donde operará el Bot para que los desarrolladores y operadores de RPA puedan mantener y ajustar los bots.
2. Necesidad de Licencia y Acceso por Claves:
    ◦ ElectroNeek es un software que Solicita Claves de Acceso. Esto significa que, para acceder y utilizar la plataforma, se necesita una licencia (en las referencias se adjunto link de herramienta).
    ◦ La integración y estabilidad del sistema con ElectroNeek está respaldada por una carta de licencia.
    ◦ El equipo reconoce que la dependencia de esta plataforma de automatización puede generar una dependencia tecnológica significativa y un riesgo de exclusión digital.

### Comandos para Ejecutar el Proyecto

El proceso de detección y comparación se maneja a través de dos scripts principales de Python que son invocados dentro del flujo del bot de RPA:

**1. `YOLOPredictor.py` (Ejecución del detector YOLOv8)**

- **Función:** Ejecuta la detección de objetos en una imagen capturada.
- **Entrada:** La ruta de la imagen capturada.
- **Salida:** 
  - Imagen con las detecciones visuales.
  - Archivo con los resultados, incluyendo:
    - Clase detectada.
    - Nivel de confianza.
    - Coordenadas de cada objeto.
  - Este módulo también alimenta automáticamente la tabla `DeteccionesYolo` en la base de datos mediante la función `save_results()`.

**2. `YOLOCompararPaginas.py` (Comparación de resultados)**

- **Función:** Analiza los resultados de detección de objetos para identificar diferencias significativas entre la imagen base (original) y la nueva imagen (predicción).
- **Entrada:** Resultados de detección de ambas imágenes.
- **Salida:** 
  - Un listado de diferencias.
  - Indicador principal `pagina_cambio` (`True` o `False`).

### Ejemplos de Uso

El módulo de IA está integrado en el flujo de ejecución del bot de RPA, sirviendo como un validador de interfaz tras cada acción crítica.

** Flujo Funcional General (3 pasos)**

1. **Ejecución del Detector** (`YOLOPredictor.py`): Procesa la imagen actual de la interfaz para detectar elementos visuales.
2. **Comparación de Resultados** (`YOLOCompararPaginas.py`): Compara los objetos detectados entre la imagen base y la imagen nueva.
3. **Interpretación y Notificación:** 
   - Si `pagina_cambio = True`: Se detectaron cambios → se genera notificación `N001` con ambas imágenes.
   - Si `pagina_cambio = False`: No se detectaron cambios → se genera notificación `N002`.

#### Ejemplo de Uso Operacional: Consulta de personas titulados en el Senescyt

El proceso de detección se ejecuta en el inicio del flujo del bot:
- ✅ **Validación de página inicial:** Después de cargar el portal del Senescyt, el bot captura la pantalla actual y la compara con la imagen original.
  
#### Ejemplo de Uso Operacional: Descarga de Facturas del SRI

El proceso de detección se ejecuta en varios puntos críticos del flujo del bot:
- ✅ **Validación de Login:** Después de cargar el portal del SRI y antes de iniciar sesión, el bot captura la pantalla actual y la compara con la imagen original.
- ✅ **Validación de Pantalla de Inicio:** Tras el login exitoso, se valida la pantalla de inicio contra la original.
- ✅ **Validación de Secciones Internas:** En la sección "facturas recibidas", se compara la pantalla actual antes de realizar la consulta o descarga de facturas.

#### Consideraciones Importantes para el Uso Adecuado

- 📐 Usar imágenes con la **misma resolución, en este caso 1920*1080** para garantizar comparaciones precisas .
- 🎯 Mantener el **umbral de confianza (`conf`) entre 0.4 y 0.6** para minimizar falsos positivos.
- 🗃️ Guardar las imágenes procesadas con sus detecciones para fines de auditoría.
- ⚠️ **Advertencia:** Si se detectan cambios inexistentes (falsos positivos), reducir el umbral de similitud (`umbral_iou`) en el archivo `YOLOCompararPaginas.py`.

## 8. Diseño detallado de Automatización e IA
### 8.1. Flujo del proceso detallado

A continuación se describe de forma detallada el proceso que realiza la solución RPA + IA.
| Actividad | Pasos Detallados |
|-----------|------------------|
| **Navegación en SENESCYT** | 1. Ir a la URL: https://www.senescyt.gob.ec/web/guest/consultas<br>2. Se captura la pantalla actual (predicción)<br>3. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>4. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br>5. Datos de entrada requeridos:<br>&nbsp;&nbsp;&nbsp;&nbsp;a. Cédula de identidad<br>&nbsp;&nbsp;&nbsp;&nbsp;b. Resolver Captcha<br><img width="868" height="414" alt="image" src="https://github.com/user-attachments/assets/432f0e62-3fba-4e0c-a063-4c34053b1087" />|
| **Navegación en SRI** | 1. Ingresar al portal del SRI: https://srienlinea.sri.gob.ec/<br>2. Se captura la pantalla actual del login (predicción)<br>3. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>4. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br><img width="928" height="420" alt="image" src="https://github.com/user-attachments/assets/284f69e3-c786-41c6-88b2-dbef76d457fc" /><br>5. Realiza el inicio de sesión en el SRI:<br>&nbsp;&nbsp;&nbsp;&nbsp;a. RUC/C.I./Pasaporte<br>&nbsp;&nbsp;&nbsp;&nbsp;b. Clave<br>&nbsp;&nbsp;&nbsp;&nbsp;c. Clic en Ingresar<br>6. Valida si inició sesión<br>7. Se captura la pantalla actual del inicio de sesión (predicción)<br>8. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>9. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br><img width="866" height="394" alt="image" src="https://github.com/user-attachments/assets/b79a19d9-7f35-4d62-84de-e3574f309a18" /><br>10. Ir a la sección de facturas recibidas: FACTURACIÓN ELECTRÓNICA → Comprobantes electrónicos recibidos<br>11. Se captura la pantalla actual (facturas recibidas, predicción)<br>12. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>13. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br><img width="944" height="427" alt="image" src="https://github.com/user-attachments/assets/46d56e25-e587-4092-9c70-95eb3135a129" /><br>14. Realizar consulta de las facturas:<br>&nbsp;&nbsp;&nbsp;&nbsp;a. Seleccionar Ruc/Cédula/Pasaporte<br>&nbsp;&nbsp;&nbsp;&nbsp;b. Periodo de emisión (mes actual y anterior; el mes anterior se descarga solo hasta un día específico del mes actual)<br>&nbsp;&nbsp;&nbsp;&nbsp;c. Tipo de comprobante (Factura, Notas de crédito, Notas de débito, Retenciones y Liquidación de compra de bienes y prestación de servicios)<br>&nbsp;&nbsp;&nbsp;&nbsp;d. Consultar (resolución de captcha requerida previamente)<br>&nbsp;&nbsp;&nbsp;&nbsp;e. Clic en Descargar reporte<br>15. Descargar TXT de facturas. |

### 8.3. Link a demo en vivo 

https://vimeo.com/1130007790?fl=ip&fe=ec

### 8.4. Instrucciones de notificaciones del bot
El asistente emite dos notificaciones dependiendo del escenario:

| Id   | Asunto                              | Cuerpo                                                                                                                                                                                                                                                                                                         | Usuario                          |
|------|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| N001 | RPAI: Cambios en el [nombrePagina]  | Estimados usuarios,<br><br>Se informa que la página web del [nombrePagina] ha presentado cambios en el [nombreVentana]. Esta actualización podría afectar temporalmente el funcionamiento de algunas funcionalidades automatizadas.<br><br>Se adjuntan la imagen original y la imagen con la predicción generada (nueva).<br><br>Esta es una notificación automática, por favor no responder a este mensaje.<br><br>Saludos cordiales,<img width="466" height="165" alt="image" src="https://github.com/user-attachments/assets/65424adf-76f3-4f82-9dbf-70e63179071b" />| Usuarios funcionales y técnicos. |
| N002 | RPAI: Sin cambios en el [nombrePagina] | Estimados usuarios,<br><br>Se informa que, tras la revisión realizada, no se han detectado cambios en el proceso de [nombreVentana] página web del [nombrePagina]. Las funcionalidades automatizadas continúan operando con normalidad.<br><br>Se adjuntan la imagen original.<br><br>Esta es una notificación automática, por favor no responder a este mensaje.<br><br>Saludos cordiales,   <img width="333" height="165" alt="image" src="https://github.com/user-attachments/assets/e9302870-4889-4bd6-b50a-527ccff8ea01" />| Usuarios funcionales y técnicos. |

El **objetivo principal** de estas notificaciones es **mantener informados a los usuarios funcionales y técnicos** sobre el estado de las interfaces web monitoreadas por el sistema de **IA/RPA**, asegurando la **continuidad operativa** y la **detección temprana de cambios** que puedan afectar los procesos automatizados.

>### 🔔 N001 (Cambios detectados)
>Notifica automáticamente cuando el modelo de visión por computadora detecta **modificaciones en la estructura visual o funcional** de una página web (por ejemplo, cambio de botones o enlaces).  
>Esto permite al equipo técnico **anticiparse a posibles fallos** en la automatización y **ajustar el bot o el flujo correspondiente**.

>### ✅ N002 (Sin cambios)
>Informa que, tras el análisis, **no se han encontrado variaciones significativas** entre la página base y la actual.  
>Esto confirma que los procesos automatizados **siguen funcionando correctamente**, brindando **tranquilidad operativa** y **trazabilidad del monitoreo**.

## 9. Estructura del proyecto:
El presente repositorio contiene las siguientes carpetas:

| Carpeta      | Descripción                                                                 |
|---------------|------------------------------------------------------------------------------|
| **docs/**     | Documentación del proyecto (planificación, análisis, arquitectura, ética, manual de usuario, etc.) en formarto .md. |
| **data/**     | Conjuntos de datos utilizados, tanto originales como procesados.            |
| **notebooks/**| Jupyter notebooks con las etapas del flujo de trabajo (EDA, modelado, evaluación). |
| **src/**      | Código fuente modular (procesamiento, modelos, entrenamiento, evaluación y utilidades). |
| **models/**   | Modelos entrenados y versiones anteriores con su descripción.               |
| **app/**      | Fuente del proyecto incluye automatización y solución IA.             |
| **tests/**    | Pruebas unitarias para validar el funcionamiento del código.                |
| **results/**  | Resultados finales, métricas, figuras y reportes generados.                 |

## 10. Consideraciones Éticas

### 🔎 Resumen de Aspectos Éticos Considerados

Se identificaron y abordaron cuatro riesgos éticos clave relacionados con el uso de IA para detectar cambios visuales en interfaces web:

1. **Riesgo de Sesgo y Equidad (Fairness)**  
   - **Riesgo:** Sesgo de detección debido a desbalance en las clases del dataset. La clase `link` (con 15.583 instancias) domina, mientras que clases críticas como `input` o `button` tienen menos de 50 ejemplos.  
   - **Mitigación:** Se aplicó **undersampling**, **data augmentation** específico y **ajuste de pesos por clase**. Además, se priorizó el **recall por clase** en la evaluación, no solo el promedio.

2. **Riesgo de Seguridad y Fiabilidad Operacional**  
   - **Riesgo:** Un **falso negativo crítico** podría hacer que el RPA no reconozca un cambio funcional, provocando fallas graves.  
   - **Mitigación:** Se priorizó el **Recall** sobre la Precisión y se reentrenó el modelo con solo las 3 clases más críticas: `input`, `button`, `link`.

3. **Riesgo de Privacidad**  
   - **Riesgo:** Las capturas de pantalla pueden contener **información sensible o personal** si se toman durante sesiones activas.  
   - **Mitigación:** Se recomienda un paso obligatorio de **anonimización o pseudonimización** antes de almacenar o usar imágenes en el modelo. 

4. **Riesgo de Transparencia ("Caja Negra")**  
   - **Riesgo:** Las redes CNN como YOLOv8 tienen baja explicabilidad, dificultando entender por qué se genera una alerta.  
   - **Mitigación:** Se proyecta integrar **mapas de calor (heatmaps)** y un **porcentaje de similitud** para visualizar y justificar las decisiones del sistema.

### 📉 Limitaciones Conocidas del Modelo

El sistema tiene limitaciones inherentes que deben ser consideradas:

1. **Baja Explicabilidad Inherente**  
   Las CNN funcionan como “caja negra”, dificultando entender la lógica de decisiones. Esto puede reducir la confianza si no se explican bien los resultados.

2. **Sesgo Persistente en Clases Minoritarias**  
   A pesar de los ajustes, el desequilibrio original del dataset puede generar **memorization** en lugar de **generalización**, afectando la equidad funcional.

3. **Dependencia Tecnológica (Exclusión Digital)**  
   El bot depende actualmente de **ElectroNeek**, lo que puede excluir a organizaciones que no tengan acceso a esta plataforma.

4. **Riesgo Residual de Error**  
   Siempre existe un margen de error inherente a cualquier sistema de IA. Falsos positivos o negativos podrían requerir revisión constante.

### ⚠️ Advertencias sobre Uso Inadecuado

1. **Falso Negativo Crítico**  
   El sistema está diseñado para minimizar estos errores, pero no los elimina. La tolerancia máxima aceptada para errores críticos es de **≤ 5%**.

2. **La IA es un Soporte, No un Reemplazo**  
   El módulo de IA debe ser supervisado. Cualquier alerta debe ser **revisada por un operador humano** antes de ejecutar acciones automáticas.

3. **Anonimización Obligatoria**  
   La captura de imágenes sin anonimizar representa un riesgo. El sistema exige que este filtro esté **activado por defecto** en producción.

4. **Cumplimiento de Transparencia**  
   Se requiere mantener actualizada la documentación técnica (como model cards, flujos, umbrales de decisión) para cumplir con normativas como el **AI Act de la UE** o principios éticos institucionales.

## 11. Autores y Contribuciones

| Nombre                         | Rol Principal       | Rol Secundario / Contribución                                                                                     |
|-------------------------------|---------------------|--------------------------------------------------------------------------------------------------------------------|
| **Andrés Martín Cantos Rivadeneira** | Desarrollador IA/RPA | Implementador técnico, Analista de datos, Data Scientist (calidad de datos, balance, mitigación de sesgos), Desarrollador core técnico, Scrum Master. |
| **María Paola Mendoza Mendieta**     | Desarrollador IA/RPA | Implementadora técnica, Desarrollador core técnico, Product Owner (diseño, priorización de funcionalidades, documentación), Project Manager. |
| **PhD. Gladys Villegas**             | Patrocinador Académico | Revisora oficial, Supervisora metodológica, Asesora en IA y visión por computadora.                                |


## 12. Licencia

- El proyecto fue desarrollado en el entorno basado en la nube **Google Colab**, utilizando herramientas y librerías de código abierto, tales como:
  - `Python` (lenguaje principal)
  - `OpenCV` (procesamiento de imágenes)
  - `Tesseract OCR` (reconocimiento óptico de caracteres)
  - `Pandas` (manipulación de datos)
  - `Ultralytics` (`YOLOv8` para detección de objetos)

- La plataforma de Automatización Robótica de Procesos (**ElectroNeek**) fue utilizada con una **licencia temporal**, prestada y documentada mediante una **carta de autorización oficial** (ver anexo https://github.com/ancantos99/proyectointegrador_ia_grupo8/blob/main/licencia.pdf).

## 13. Agradecimientos y Referencias

### 🙏 Agradecimientos

Queremos expresar nuestro más sincero agradecimiento a todas las personas y entidades que hicieron posible este proyecto:

- A **Dios**, por darnos sabiduría, fortaleza y propósito durante todo este proceso.
- A nuestras **familias y amigos**, por su paciencia, apoyo constante y motivación incondicional.
- A nuestra **profesora PhD. Gladys Villegas**, por su guía, revisión académica y asesoría técnica en Inteligencia Artificial y Visión por Computadora.
- A nuestro compañero de maestría, por su colaboración, compañerismo y contribuciones al desarrollo del proyecto.

### 📚 Referencias

- **Ultralytics YOLOv8**:  
  Ultralytics. (2023). YOLOv8 – SOTA Real-Time Object Detection.  
  Repositorio oficial: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)

- **Dataset de Elementos UI (Hugging Face)**:  
  Yash Jain. (2023). UI-Elements-Detection-Dataset.  
  Disponible en: [https://huggingface.co/datasets/YashJain/UI-Elements-Detection-Dataset](https://huggingface.co/datasets/YashJain/UI-Elements-Detection-Dataset)

- **ElectroNeek RPA Platform**:  
  ElectroNeek Robotics Inc. (2023). ElectroNeek Automation Platform – Intelligent RPA for Business Automation.  
  Sitio web oficial: [https://electroneek.com](https://electroneek.com)
