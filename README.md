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

---

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
