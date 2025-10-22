# Consideraciones éticas
> **Detección de cambios en interfaces web para procesos RPA utilizando Inteligencia Artificial**
>
> Aunque este proyecto se enfoca en la automatización de la detección de cambios en interfaces web mediante IA, es fundamental abordar las implicaciones éticas relacionadas con la privacidad, el uso responsable de datos y el impacto en los usuarios y trabajadores involucrados en procesos RPA.

## 1️⃣ Análisis de sesgos:

Esta tabla presenta de manera clara y estructurada los principales sesgos identificados en el dataset, junto con sus implicaciones prácticas para el proyecto.

| Tipo de Sesgo | Diagnóstico basado en el Análisis | Implicaciones/Grupos Perjudicados |
|---------|-----------------------------------|-----------------------------------|
| **Sesgo Estructural (Clases)** | **Sesgo de Desbalance Severo**: La clase `link` domina con **64.48%** de las instancias, creando un ratio de desbalance de **1,947.88×** respecto a la clase minoritaria (`toggle`). | El modelo tendrá un rendimiento excelente en `link` (clase mayoritaria), pero un pobre recall y precisión en clases minoritarias pero críticas para RPA, como `toggle`, `textarea` e `input`. |
| **Sesgo Geográfico/Cultural** | El dataset proviene de "más de 300 sitios web populares". Estos son predominantemente anglosajones, existe un sesgo de diseño y lenguaje. | El modelo podría fallar en la detección de elementos que sigan convenciones de diseño o estén escritos en idiomas con alfabetos no latinos, comprometiendo la robustez del RPA en entornos internacionales. |
| **Sesgo de Datos Faltantes** | Tres clases (`select`, `image`, `text`) tienen **0 instancias** en el conjunto de entrenamiento. | El modelo no podrá detectar estas clases. Los procesos RPA que dependan de la detección de un elemento `<select>` o una imagen interactiva no estarán cubiertos. |

## 2️⃣ Equidad y fairness:

Esta tabla presenta las estrategias implementadas para mitigar los sesgos revisados en el punto 1 y garantizar un tratamiento más equitativo de todas las clases en el modelo.

| Aspecto | Evaluación y Estrategias Implementadas |
|---------|----------------------------------------|
| **Tratamiento Equitativo** | **Injusto por Diseño**: El modelo, sin mitigación, no trata a todas las clases de forma equitativa, favoreciendo la clase dominante (`link`). |
| **Métricas de Fairness** | La métrica clave de fairness es el **mAP por clase** (Average Precision). Se debe monitorear que el mAP de las clases críticas minoritarias (ej. `input`, `textarea`, `button`) no caiga por debajo de un umbral aceptable (ej. **mAP ≥ 0.5** para ellas). |
| **Estrategias de Mitigación** | **1. Pérdida Ponderada**: Se usará en el entrenamiento para asignar un mayor peso a los errores de las clases minoritarias (ej. `toggle`, `clickable`), forzando al modelo a aprender mejor estas clases.<br><br>**2. Data Augmentation Avanzada**: Aplicar sobremuestreo (*oversampling*) y técnicas como MixUp o Copy-Paste específicamente a las clases con menos instancias. |

### Con respecto a la equidad del uso del sistema

- **¿El sistema reduce o aumenta desigualdades existentes?** El sistema busca mejorar la eficiencia y confiabilidad de los bots RPA, lo que puede reducir desigualdades operativas entre empresas con procesos automatizados avanzados y aquellas con menos capacidad técnica.
- **¿Quién se beneficia?** Los principales beneficiarios son empresas medianas y grandes que cuentan con infraestructura RPA y personal capacitado, así como los equipos técnicos responsables del mantenimiento de los bots, quienes experimentan menor carga laboral y mayor confiabilidad operativa.
- **¿Todos tienen igual acceso al sistema?** Actualmente, el acceso no es equitativo, ya que la solución inicial depende de plataformas específicas y licencias comerciales. Esto limita la adopción por parte de organizaciones pequeñas o con menor inversión tecnológica
- **¿Qué grupos podrían ser excluidos?** Las empresas que no han comenzado su transformación digital podrían quedar excluidas, al no contar con infraestructura, licencias de software ni personal capacitado para implementar soluciones de RPA e IA

## 3️⃣ Privacidad:

Esta tabla presenta de manera clara las consideraciones de privacidad y los mecanismos de protección necesarios para el uso responsable del sistema en entornos con datos sensibles.

| Aspecto | Consideración y Mecanismos de Protección |
|---------|------------------------------------------|
| **Uso de Datos Sensibles** | **Indirectamente**: El input son capturas de pantalla web. Si el proceso RPA se ejecuta en un ambiente con datos sensibles (ej. formularios de salud, datos bancarios), la captura podría contener información personal visible. |
| **Protección de la Privacidad** | La responsabilidad recae en el **preprocesamiento de la captura** antes de enviarla al modelo. Se requiere que el software RPA aplique técnicas de **anonimización o enmascaramiento** (blurring de áreas sensibles, placeholder de campos de texto) antes de que la imagen sea procesada por el modelo YOLOv8l. |
| **Cumplimiento de Regulaciones** | El modelo no almacena información personal sensible. Sin embargo, su entorno de ejecución (el RPA) debe ser compatible con regulaciones (GDPR, AI Act de la Unión Europea) si maneja datos de usuarios protegidos, asegurando el **no almacenamiento** de las capturas de pantalla de inferencia. |

## 4️⃣ Transparencia y explicabilidad:

A continuación se presenta las limitaciones de interpretabilidad del modelo y las técnicas implementadas para mejorar la transparencia del sistema.

| Aspecto | Diagnóstico de Explicabilidad |
|---------|-------------------------------|
| **Interpretabilidad** | **Baja (Modelo Black Box)**: YOLOv8l es una red neuronal profunda. No es intrínsecamente interpretable. El modelo indica *qué* detectó, pero no *por qué* (qué características visuales utilizó). Aunque si muestra un % de confianza de cada interpretación. |
| **Entendimiento del Usuario** | Los operadores de RPA pueden entender la salida del modelo (un bounding box con etiqueta y confianza). Sin embargo, se necesita **documentación clara** sobre las limitaciones de detección (ej. "el modelo tiende a confundir `button` y `link` si tienen el mismo tamaño"). |
| **Técnicas de explicabilidad Implementadas** | La técnica principal de explicabilidad es la **Visualización del Output**: mostrar el bounding box con su score de confianza sobre la imagen original. Para el diagnóstico de fallas, se puede considerar como futura mejora la aplicación de técnicas de **Activación (Grad-CAM)** para identificar las regiones de la imagen que guiaron la predicción errónea.<br><br>Además se envía un correo indicando que la comparación no fué exitosa.|

## 5️⃣ Impacto social:

| Tipo de Impacto | Aspecto | Descripción |
|---------|----------------------------|-------------|
| **Impacto Positivo** | **(+) Robustez y Confiabilidad** | Aumenta drásticamente la resiliencia de los procesos RPA de alto valor. Reduce el tiempo de inactividad de la automatización causado por cambios inesperados en la UI. |
|  | **(+) Fomento de la innovación tecnológica y formación en IA** | El desarrollo del proyecto impulsa la adopción de tecnologías emergentes, como visión por computadora y redes neuronales convolucionales, dentro de un contexto práctico de automatización.<br><br>Esta integración de Inteligencia Artificial con RPA promueve la capacitación del personal en competencias digitales avanzadas, fortaleciendo sus habilidades técnicas y contribuyendo al desarrollo de talento especializado  |
| **Impacto Negativo** | **(-) Riesgo de reemplazo o desplazamiento laboral** | Los operadores de RPA podrían ver una reducción en tareas de bajo valor (mantenimiento de bots por fallas de UI), reduciendo la necesidad de personal técnico que actualmente realiza tareas de mantenimiento manual de RPA.<br><br>Grupos vulnerables: Los grupos vulnerables son el personal técnico con baja especialización<br><br>Sin embargo, este riesgo puede mitigarse mediante programas de capacitación en IA y automatización, transformando el rol del personal hacia funciones de supervisión, análisis o desarrollo más avanzado de RPA. |
|   | **(-) Dependencia tecnológica y riesgo de exclusión digital** | La solución, en su versión inicial, depende de la plataforma de automatización RPA ElectroNeek, lo que puede generar una dependencia tecnológica significativa. Esta limitación podría restringir su adopción por parte de organizaciones que utilicen otros entornos de automatización o que no cuenten con licencias activas del software. <br><br>Grupos vulnerables: Las PYMES e instituciones pequeñas son los principales grupos vulnerables, dada su capacidad económica y técnica reducida.<br><br>Este riesgo puede mitigarse mediante la modularización del sistema, permitiendo su integración con diversas plataformas RPA, y utilizando librerías open-source|
| **Beneficiarios** | **Empresas y Desarrolladores de RPA** | Se benefician de una mayor eficiencia operativa y menores costos de mantenimiento. |
| **Potenciales Perjudicados** | **Operadores de RPA (por cambio de rol)** | Aquellos cuyo trabajo se centraba en el mantenimiento reactivo de fallas de UI. |

## 6️⃣ Responsabilidad:
### ¿Quién es responsable si el modelo falla?

La gestión ética y técnica del sistema se sustenta en una cadena de responsabilidad
claramente definida, donde cada rol cumple funciones específicas de implementación,
control y supervisión:

| Rol | Responsabilidades | Rendición de Cuentas |
|-----|-------------------|----------------------|
| **Desarrolladores**| • Garantizar la correcta implementación técnica del sistema, incluyendo la integración del modelo YOLOv8, validaciones y mecanismos de detección<br>• Integración con el Software RPA (ElectroNeek)<br>• Cumplimiento de métricas: **precisión ≥ 0.75**, **recall ≥ 0.50** | • **Revisión de Sprints**: Inspección del incremento y obtención de feedback<br>• Pruebas de integración y pruebas unitarias, verificables y documentadas |
| **Data Scientists** | • Asegurar la calidad de los datos, el equilibrio de clases y la mitigación de sesgos durante el entrenamiento y validación del modelo | • **Auditorías de sesgo**: Análisis documentado de la frecuencia de clases e impacto del desbalance de clases en el rendimiento del modelo<br>• **Trazabilidad del dataset**: Mantenimiento de una bitácora que registre cada actualización del dataset |
| **Product Owner**| • Tomar decisiones de diseño, priorizar funcionalidades y documentar los compromisos entre precisión, recall y explicabilidad del modelo | • **Documentación de decisiones**: Justificación de la priorización de recall sobre precisión<br>• **Cumplimiento de hitos**: Seguimiento y reporte del progreso del proyecto conforme al cronograma y los entregables definidos |
| **Organización** | • Proveer gobernanza, recursos y cumplimiento ético<br>• Supervisar la correcta aplicación de políticas de privacidad, transparencia y seguridad | • Revisiones periódicas y aprobación formal de los entregables clave<br>• Establecimiento de acuerdos formales (ej. acuerdos de confidencialidad)<br>• Reuniones periódicas de seguimiento con retroalimentación continua sobre los resultados verificables del proyecto |


### ¿Qué mecanismos de accountability existen?


| Dimensión | Mecanismos | Aplicación en el Proyecto |
|-----------|------------|---------------------------|
| **Documentación** | • **Model Card**: Elaboración de fichas técnicas que indiquen las capacidades y limitaciones del modelo YOLOv8 entrenado<br>• **Datasheet**: Plan de Adquisición de datos documentado<br>• **Declaración de ética**: Informes de "Impacto Social y Responsabilidad" | • Se elaborará un **Model Card** completo del modelo YOLOv8 entrenado<br>• Se detallan el origen, los pasos del preprocesamiento, normalización, limpieza y formatos de imágenes (dataset en formato YOLO)<br>• Análisis documentado de posibles riesgos y estrategias de mitigación |
| **Supervisión** | • **Revisión Humana en decisiones críticas**<br>• **Proceso de Apelación para Usuarios**<br>• **Auditoría Periódica** | • La solución genera **alertas** revisadas por Desarrolladores/Operadores de RPA, quienes analizan el cambio detectado para depurar y ajustar el bot<br>• Cuando el RPA se auto-configure impulsado por IA, debe **notificar el cambio** para supervisión<br>• Usuarios técnicos pueden reportar fallos o decisiones incorrectas mediante **correo electrónico**<br>• **Auditorías trimestrales** para evaluar desempeño y cumplimiento ético |
| **Monitoreo Continuo** | • **Métricas de Fairness Trackeadas**<br>• **Alertas por Drift o Anomalías**<br>• **Reportes de Incidentes** | • Monitoreo del impacto del desbalance de clases, priorizando **precisión y recall por clase** como garantía de equidad funcional<br>• **Alertas automáticas** ante desviaciones o reducción no aceptable de métricas<br>• Registro y análisis de incidentes donde la solución no detectó cambios, para **aprendizaje organizacional** |
| **Transparencia** | • **Información clara sobre uso de IA**<br>• **Comunicación de limitaciones**<br>• **Acceso a explicaciones de decisiones** | • Documentación detallada del modelo CNN, procedimientos de uso e integración con RPA<br>• Información explícita sobre limitaciones del modelo, entrenamiento y dificultades de balanceo del dataset<br>• Cada predicción incluye: elementos detectados, ubicación, **% de confianza**<br>• Alertas de cambio contienen **comparación visual** con la interfaz inicial |

### Plan de monitoreo y actualización del modelo

Gestión Proactiva de Incidentes: Este protocolo garantiza una respuesta rápida y estructurada ante fallos del sistema, minimizando el impacto operativo y convirtiendo cada incidente en una oportunidad de mejora continua.

| Fase | Acción Principal | Ejemplo Aplicado al Proyecto |
|------|------------------|------------------------------|
| **Detección** | Monitoreo automático de métricas (recall, precisión) y alertas por fallos del modelo o anomalías visuales. | El sistema detecta una caída abrupta del recall o se identifica que el modelo no emitió una alerta ante un cambio real en la interfaz. |
| **Respuesta Inmediata** | Registrar el incidente y mantener al bot en estado de pausa en el proceso RPA donde se detectó el problema, hasta revisión técnica. | El bot se detiene temporalmente solo para el RPA que descarga facturas del SRI, se genera un log del evento y se notifica al equipo. |
| **Investigación** | Análisis de logs, revisión de predicciones y trazabilidad del modelo (inputs, versiones, umbrales). | Los Data Scientists verifican si el error provino de desbalance de clases o umbral inadecuado, si el modelo falló en detectar un elemento crítico de la interfaz. |
| **Corrección** | Ajustar parámetros del modelo o actualizar dataset con ejemplos del cambio no detectado. | • Realizar un **fine-tuning** del modelo incorporando nuevas imágenes del incidente o del cambio no detectado<br>• Validar el rendimiento del modelo actualizado antes de su **redeployment** en el entorno de producción |
| **Prevención** | Registrar el caso en la base de incidentes, actualizar la documentación y ajustar el monitoreo. | Se documenta el incidente en la base de conocimiento y se refuerza el seguimiento de métricas para prevenir recurrencias similares. |

## 7️⃣ Uso dual y mal uso:

| Aspecto | Riesgo y Salvaguardas |
|---------|----------------------|
| **¿Podría el modelo usarse con fines maliciosos?** | **Riesgo Potencial**: Un detector de UI de alta precisión podría ser adaptado para automatizar web scraping ilegal o facilitar ataques de phishing al identificar elementos clave de formularios con facilidad. |
| **¿Qué salvaguardas se han implementado?** | **Restricción de Acceso**: El modelo YOLOv8l debe estar alojado en un ambiente de ejecución RPA controlado y no disponible como un servicio de API público, restringiendo su uso únicamente a los procesos RPA autorizados. |
| **Limitaciones de uso claramente documentadas** | **Prohibición de Scraping Ilegal**: Documentar claramente que el modelo no debe ser utilizado para la recolección de datos no autorizada o fuera del alcance de los procesos de la compañía. |


## 8️⃣ Limitaciones reconocidas:

| Advertencia | Descripción del Caso Límite |
|-------------|------------------------------|
| **Advertencia de Desbalance** | El modelo tiene una **confiabilidad baja** en las clases con menos de 50 instancias (ej. `toggle`, `textarea`) y **no funcionará** para las clases con cero instancias en `Train` (`select`, `image`, `text`). |
| **Advertencia de Resolución** | El modelo fue entrenado a **1920 × 1080 px**. La entrada debe mantener una resolución cercana o consistente. **No es confiable** con capturas de pantalla de móvil o resoluciones inconsistentes que el RPA no puede predecir. |
| **Casos Límite no Confiables** | **1. Interfaces Gráficas Puras**: El modelo puede tener problemas para distinguir elementos de UI incrustados en gráficos complejos (ej. infografías).<br><br>**2. Elementos Fuera de Escena**: Si el RPA tiene que hacer scroll, el modelo solo detectará los elementos visibles en la captura actual. |

