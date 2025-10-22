# Planificación 
> **Detección de cambios en interfaces web para procesos RPA utilizando Inteligencia Artificial**
> 
> Este proyecto aborda un desafío crítico en la automatización robótica de procesos (RPA): la fragilidad de los bots ante los cambios en la interfaz de usuario (UI) de las aplicaciones web

## ✍🏻 Definición del problema y objetivos

A pesar de los avances en la automatización de procesos robóticos (RPA) y la aplicación de la inteligencia artificial, persiste una brecha crítica. Las soluciones actuales de RPA dependen en gran medida de localizadores de elementos de interfaz de usuario (cómo selectores css o Ids), lo que las hace muy vulnerables a los cambios en el diseño o la estructura de las páginas web.

El éxito de la RPA a gran escala se ve constantemente limitado por la fragilidad de las interfaces de usuario. Las organizaciones pierden incontables horas de productividad cuando los bots dejan de funcionar debido a cambios o fallos en dichas interfaces.

### Objetivos

| Tipo | Objetivo |
| :--- | :--- | 
| **Objetivo General** | Desarrollar un modelo de Inteligencia Artificial que sea capaz de detectar y clasificar cambios significativos en la UI de una página web relevante para un proceso RPA, con el fin de alertar al equipo de mantenimiento y así evitar tiempos perdidos por rupturas de los procesos |
| **Objetivos Específicos** | 1. **Captura y Almacenamiento:** Implementar un mecanismo para capturar y almacenamiento de instantáneas (screenshots) de las interfaces web objetivo.  <br/><br/>2. **Detección de Cambios Visuales:** Entrenar y Aplicar modelos de Visión por Computadora para identificar diferencias visuales en los screenshots entre versiones. <br/><br/>3. **Clasificación de elementos Estructurales:** Entrenar un modelo de CNN (YoloV8), para identificar y clasificar modificaciones en los selectores clave utilizados por el RPA. <br/><br/>4. **Clasificación y Alerta:** Realizar una comparación entre el los resultados del modelo con la nueva interfaz y la guardada en la base de datos previamente. si se detectan cambios estructurales ( por ej. movimiento de elementos ) generar una alerta oportuna.|

## 📝 Justificación de la relevancia del proyecto

Si bien existen investigaciones que proponen la detección de cambios utilizando visión por computadora, no abordan directamente el problema de detección en tiempo real de los cambios para los bots de RPA. El gap identificado es la falta de un módulo basado únicamente en la visión por computadora (CNN), que permita a un Bot de RPA detectar cambios visuales y operar sin depender de los localizadores tradicionales, mejorando así su autonomía y fiabilidad.

### Relevancia

1. **Mejora de la Resiliencia Operacional:** Transforma el mantenimiento de RPA de un modelo reactivo —en el que los errores se abordan solo después de que alguien los detecta y ya han afectado las operaciones durante un tiempo— a un modelo proactivo, donde el sistema identifica los cambios en la interfaz y alerta al equipo de inmediato. Esto permite una respuesta rápida ante posibles interrupciones, reduciendo el impacto y asegurando la continuidad de los procesos críticos del negocio.
   
2. **Innovación Tecnológica:** Integra técnicas avanzadas de Inteligencia Artificial (Visión por Computadora y CNN) para resolver un problema que las herramientas de RPA tradicionales manejan de forma deficiente, posicionando la solución como un avance estratégico en el campo de la RPA asistida por IA (AI-powered RPA).

3. **Impacto Económico Directo:** Al reducir el número de fallos de bots en producción y el tiempo de inactividad (Downtime), se logra un ahorro sustancial en costos operativos y de mantenimiento.

## 🎯 Alcance (qué incluye y qué NO incluye)

## Alcance del Proyecto de Detección de Cambios en Interfaces Web para RPA

| Categoría | Incluye (Enfoque del Proyecto) | NO Incluye (Restricciones y Exclusiones) |
| :--- | :--- | :--- |
| **Monitoreo** | Desarrollo de scripts para la **captura** de **screenshots** de la página web con la que está trabajando el bot, esta captura será enviada al modelo para su detección o clasificación | **Autorreparación del Bot (Auto-Healing):** El proyecto no incluye la lógica para modificar o reconfigurar automáticamente el bot de RPA después de detectar un cambio. Solo se limita a la detección y alerta. |
| **Análisis** | Implementación de modelos (IA o algorítmicos) para comparar y detectar cambios **visuales** (screenshots). | **Análisis de Seguridad o Rendimiento:** No se analizarán los cambios en el rendimiento de la aplicación web ni vulnerabilidades de seguridad. |
| **Clasificación** | Un modelo de CNN (YOloV8) para detecta **los elementos estructurales de la interfaz web** en relación con la ejecución del bot de RPA. | **Detección en Aplicaciones de Escritorio:** El enfoque está estrictamente en interfaces **Web (navegadores)**. |
| **Alerta** |  **notificación simple por correo** para mostrar los cambios detectados, una alerta con la versión inicial y con cambios de la interaz, la imágen muestra el elemento con su % de confianza detectado. | **Integración en Plataformas RPA Comerciales:** El output será una **prueba de concepto (PoC)**, no un plugin totalmente integrado en plataformas RPA específicas (e.g., UiPath, Automation Anywhere), aunque los principios serán aplicables. |

## 🗓️ Cronograma de desarrollo (planificado vs real)

La implementación se centrará en la detección de cambios visuales
El proyecto se realizará en un plazo de 5 semanas con un alcance inicial de 2 a 3 aplicaciones web, suficiente para demostrar la viabilidad de la solución

### Cronograma Planificado

<img width="1777" height="706" alt="Presentacion Pitch" src="https://github.com/user-attachments/assets/54ea7bea-884d-4efe-a8cc-52cab39c16ce" />

Originalmente, el proyecto se estructuró en **4 Sprints** planificados para un total de cinco semanas. El diseño inicial contemplaba el **Sprint 1 (Investigación y Diseño)** cubriendo las Semanas 1 y 2, el **Sprint 2 (Desarrollo Core) en la Semana 3**, **el Sprint 3 (Optimización) en la Semana 4**, y el **Sprint 4 (Documentación) en la Semana 5**.

Sin embargo, para cumplir con el plazo de entrega y optimizar los recursos, fue necesario realizar un ajuste en la última fase. Finalmente, los **Sprints 3 y 4 se fusionaron**, dedicando la Semana 5 a una fase integral de Optimización, Validación, y Documentación final."

### Cronograma Real

| Semana | Fase Definida | Sprints Incluidos |
| :---: | :--- | :--- |
| **Semana 1** | Planificación y recopilación de datos | **Sprint 1 (Parte I)**: Investigación y Diseño Inicial |
| **Semana 2** | Preparación del dataset etiquetado | **Sprint 1 (Parte II)**: Preparación del Entorno y Dataset |
| **Semana 3** | Desarrollo del prototipo IA | **Sprint 2 (Parte I)**: Implementación Core del Modelo |
| **Semana 4** | Integración, Pruebas y Correcciones | **Sprint 2 (Parte II)**: Integración y Pruebas Iniciales |
| **Semana 5** | Evaluación y Documentación | **Sprint 3 y 4 (Fusionados)**: Optimización, Validación y Documentación final |

### Detalle de Sprints

#### Sprint 1: Investigación, Diseño y Preparación

| Característica | Detalle |
| :--- | :--- |
| **Duración** | Semana 1 - 2 |
| **Objetivo** | Realizar una investigación exhaustiva, definir la arquitectura de la solución y preparar el dataset inicial, dejando el entorno de desarrollo listo. |
| **Definition of Done (DoD)** | Encontrar 3 metodologías y seleccionar la arquitectura final. Entorno de desarrollo funcional y comenzar el repositorio en GitHub. Dataset inicial listo y páginas web seleccionadas. |
| **Riesgo** | La investigación se extiende y retrasa la definición de la arquitectura (se encontraron dos modelos posibles YOLOv8  Y Siamese, probamos ambos) |
| **Mitigación** | Asignar un tiempo fijo para la definición y realizar una sesión de decisión final al inicio de la Semana 2. (Nos decidimos por el Modelo YoloV8 |
| **Historias de Usuario** |  (Analizar 20 papers), (Definir métricas de éxito),  (Configurar repositorio y entorno), (Investigar arquitecturas de CNN), (Preparar el dataset inicial). |

### Sprint 2: Desarrollo Core e Integración

| Característica | Detalle |
| :--- | :--- |
| **Duración** | Semana 3 - 4 |
| **Objetivo** | Implementar el algoritmo principal de detección (Modelo CNN) y los componentes de integración necesarios (pipeline) para interactuar con el RPA. |
| **Definition of Done (DoD)** | Modelo CNN entrenado en su versión inicial. Script funcional de integración con Electroneek que envíe capturas al modelo. Pruebas de integración exitosas. |
| **Riesgo** | El modelo CNN no logra un rendimiento aceptable en las primeras iteraciones. |
| **Mitigación** | Preparar scripts para el pre-procesamiento de datos y establecer puntos de control para el ajuste de hiperparámetros, revisar documentación sobre entrenamientos con YOLO (Se descubrió que el rendimiento mejoraba usando la dimensión original de las imágenes) |
| **Historias de Usuario** | (Implementar y entrenar Modelo CNN),  (Implementar script/pipeline de integración con Electroneek), (Pruebas de integración Modelo/Script). |

### Sprint 3,4: Optimización, Validación y Finalización (Fusionado)

| Característica | Detalle |
| :--- | :--- |
| **Duración** | Semana 5 |
| **Objetivo** | Optimizar el rendimiento del modelo (ajuste de hiperparámetros), validar los resultados finales, exportar el modelo funcional, integración final con Electroneek, comparación, envío de notificación por correo  y realizar la documentación del proyecto. |
| **Definition of Done (DoD)** | Modelo alcanza los umbrales de éxito técnicos aceptables. Sistema automatizado completo con éxito de 2 casos de uso. Código y Documentación técnica completa subida a GitHub. |
| **Riesgo** | Los resultados de las pruebas de validación no son satisfactorios y/o surgen bugs críticos durante las pruebas finales. |
| **Mitigación** | Planificar iteraciones o entrenamientos adicionales para ajustar el modelo. Dividir al equipo: un integrante prioriza la solución de bugs mientras el segundo realiza la documentación. |
| **Historias de Usuario** | (Ajuste de hiperparámetros), (Validar el modelo contra dataset de pruebas),  (Pruebas integrales de extremo a extremo),  (Documentación técnica y versionado), (Preparación de la Presentación final). |

## 🛠️ Recursos necesarios (datos, hardware, software)

| Categoría | Recurso Específico | Propósito |
| :--- | :--- | :--- |
| 🌐<br/>**Datos** | Datos de Entrenamiento | Muestras de interfaces web **screenshots** con etiquetas de clasificación en Formato YOLO. **Propósito:** Entrenamiento del modelo de IA para detección. |
|  | Sitios Web de Prueba | **URLs** de aplicaciones web de libre acceso (e.g., sri, senescyt). **Propósito:** Pruebas en tiempo real y simulación del entorno RPA. |
| --- | --- | --- |
| 🖥️<br/>**Hardware** | **Máquina Local:** Laptop AMD Ryzen 7, 16 GB RAM. |Edición y gestión de código, scripts de captura web inicial y ejecución de pruebas locales. |
|   | **Entorno de Procesamiento IA:** Google Colab (uso de 200 Unidades de Procesamiento). | Entrenamiento y ejecución de modelos de IA a gran escala, aprovechando la aceleración GPU |
|   | **Aceleradores Gráficos:** GPU T4 (15GB VRAM) y GPU A100 (40GB VRAM) (disponibles en Colab). | Aceleración del entrenamiento de modelos de Visión por Computadora (T4) y pruebas de alto rendimiento con imágenes sin redimensionar (A100). |
| --- | --- | --- |
| </><br/>**Software** | Lenguaje de Desarrollo: **Python.** | Desarrollo principal de toda la lógica del sistema. |
|  | **Modelo de Visión por Computadora (CNN):** Librería Ultralytics con modelo YoloV8.| Detección de objetos (elementos UI) y clasificación visual de cambios en los screenshots.|
|  | **Herramienta de Edición y Ejecución:** Google Colab. | Entorno de desarrollo para edición de código y ejecución de modelos en la nube. |
|  | **Librería de Análisis de Datos:** Pandas. | Análisis y procesamiento de las métricas de YoloV8 (archivos results.csv) y datos de cambio estructural. |
|  | **Plataforma de MLOps:** Weights & Biases (W&B). | Visualización de los runs de entrenamiento, tracking de métricas y optimización de hiperparámetros (Optimización Bayesiana) |
|  | **Control de Versiones:** Git y Github | Control de Cambios y documentación |

## 🚨 Riesgos identificados y mitigación

| Riesgo Identificado | Descripción del Riesgo | Mitigación Propuesta |
| :--- | :--- | :--- |
| **Falta de Datos Etiquetados** | Sesgo de detección por desbalance de clases en el dataset | Centrar el análisis a las 3 clases más críticas link, button e imput. Ampliar y equilibrar dataset con data augmentation con cambios que no alteren la geometría de la imágen |
| **Elevado requerimiento computacional** | El entrenamiento del modelo de YoloV8 puede ser lento y costoso. | Comprar unidades de procesamiento en Google Colab    |
| **Falsos positivos / Negativos** | El sistema detecta un cambio menor como crítico (falso positivo) o ignora un cambio crítico (falso negativo), minando la confianza en el sistema. | Validación Rigurosa, Utilizar Weights & Biases (W&B) para el tracking eficiente y la Optimización Bayesiana para encontrar los mejores hiperparámetros |
