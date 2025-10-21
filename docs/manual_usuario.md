# Detección de cambios en interfaces web para procesos RPA utilizando Inteligencia Artificial
## MANUAL DE USUARIO

###  TRAZABILIDAD DEL DOCUMENTO
| Versión | Preparado Por                                      | Fecha    | Revisado por         | Descripción     |
|---------|----------------------------------------------------|----------|-----------------------|------------------|
| 1       | Andrés Martín Cantos Rivadeneira, María Paola Mendoza Mendieta | 24-10-25 | PhD. Gladys Villegas  | Versión Inicial |

1.  ## Información General del Proceso

    1.  ### Descripción del Problema

En los entornos de automatización robótica de procesos (RPA) que
interactúan con páginas web, la principal vulnerabilidad proviene de
cambios visuales en los elementos de la interfaz. Los bots suelen
depender de localizadores tradicionales (XPATH, ID, CSS) para
interactuar con controles como campos de entrada (input), enlaces
(links), botones, menús desplegables (select), casillas de verificación
(checkbox), radio buttons, imágenes y tablas.

Esta dependencia limita la robustez y escalabilidad de las
automatizaciones, generando costos adicionales en mantenimiento y
afectando la continuidad de los procesos automatizados.

El proyecto busca abordar esta problemática mediante el desarrollo de un
módulo basado en Visión por Computadora y Redes Neuronales
Convolucionales (CNN), capaz de detectar cambios visuales en las
interfaces web y notificar oportunamente las alteraciones que puedan
comprometer el funcionamiento del bot. Con ello, se pretende reducir la
vulnerabilidad de los procesos RPA ante modificaciones en las
aplicaciones y mejorar su fiabilidad y autonomía.

## Resultados esperados de la solución e indicadores de éxito

Este proyecto tiene como objetivo detectar automáticamente cambios
visuales en interfaces web que puedan afectar procesos RPA. Su
funcionalidad principal incluye la detección de modificaciones en la
estructura, posición o apariencia de elementos visuales; la comparación
con versiones anteriores para generar alertas en caso de diferencias
significativas.

## Programas para utilizar

| Aplicación / Sistema | Módulo                    | Tipo de Interfaz | Solicita Claves | Estabilidad |
|----------------------|---------------------------|------------------|------------------|-------------|
| SQL Server           | Base de datos             | Escritorio       | Sí               | Alta        |
| Electroneek          | Herramienta RPA           | Escritorio       | Sí               | Alta        |
| Microsoft Service    | Gestor de Correo          | Web              | Sí               | Alta        |
| Google Chrome        | Navegador Web con acceso a SRI y Senescyt           | Escritorio       | No               | Alta        |
| Python               | Desarrollo IA               | Escritorio       | No               | Alta        |

## Usuarios requeridos por el bot

| Usuario                                                 | Perfil/Propietario |
|----------------------------------------------------------|---------------------|
| Cuenta de correo electrónico con permisos                | Paola Mendoza       |
| Credenciales de acceso a base de datos                   | Andrés Cantos       |
| Credenciales de acceso al SRI                            | Paola Mendoza       |

4.  **Fuera del alcance**

Este proyecto no contempla dentro de su alcance la implementación de
acciones reactivas o correctivas dentro de los procesos de
automatización ante posibles cambios en la página web.

# 2. Diseño detallado

## 2.1. Diagrama de arquitectura
<img width="921" height="460" alt="image" src="https://github.com/user-attachments/assets/c6164263-aa90-4cb2-b65c-f857a77c902a" />

## 2.2. Flujo del proceso detallado

En este capítulo se describe de forma detallada el proceso en formato
TO-BE (como será), donde se describe paso a paso las actividades a
desarrollar, así como el proceder de cada una para permitir al
desarrollador configurar el proces
| Actividad | Pasos Detallados |
|-----------|------------------|
| **Navegación y obtención de datos de SENESCYT** | 1. Ir a la URL: https://www.senescyt.gob.ec/web/guest/consultas<br>2. Se captura la pantalla actual (predicción)<br>3. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>4. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br>5. Datos de entrada requeridos:<br>&nbsp;&nbsp;&nbsp;&nbsp;a. Cédula de identidad<br>&nbsp;&nbsp;&nbsp;&nbsp;b. Resolver Captcha<br>📷 Imagen de referencia |
| **Descarga de facturas** | 1. Ingresar al portal del SRI: https://srienlinea.sri.gob.ec/<br>2. Se captura la pantalla actual del login (predicción)<br>3. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>4. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br>📷 Imagen de referencia<br>5. Realiza el inicio de sesión en el SRI:<br>&nbsp;&nbsp;&nbsp;&nbsp;a. RUC/C.I./Pasaporte<br>&nbsp;&nbsp;&nbsp;&nbsp;b. Clave<br>&nbsp;&nbsp;&nbsp;&nbsp;c. Clic en Ingresar<br>6. Valida si inició sesión<br>7. Se captura la pantalla actual del inicio de sesión (predicción)<br>8. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>9. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br>📷 Imagen de referencia<br>10. Ir a la sección de facturas recibidas: FACTURACIÓN ELECTRÓNICA → Comprobantes electrónicos recibidos<br>11. Se captura la pantalla actual (facturas recibidas, predicción)<br>12. Se valida si la pantalla tiene cambios (validar imagen original y predicción)<br>13. Si se detectan cambios en la ventana de la página, se envía una notificación incluyendo la imagen original y la nueva ventana de predicción. En caso contrario, se envía una notificación indicando que la ventana de la página no presenta cambios, acompañada de la imagen original.<br>📷 Imagen de referencia<br>14. Realizar consulta de las facturas:<br>&nbsp;&nbsp;&nbsp;&nbsp;a. Seleccionar Ruc/Cédula/Pasaporte<br>&nbsp;&nbsp;&nbsp;&nbsp;b. Periodo de emisión (mes actual y anterior; el mes anterior se descarga solo hasta un día específico del mes actual)<br>&nbsp;&nbsp;&nbsp;&nbsp;c. Tipo de comprobante (Factura, Notas de crédito, Notas de débito, Retenciones y Liquidación de compra de bienes y prestación de servicios)<br>&nbsp;&nbsp;&nbsp;&nbsp;d. Consultar (resolución de captcha requerida previamente)<br>&nbsp;&nbsp;&nbsp;&nbsp;e. Clic en Descargar reporte<br>15. Descargar TXT de facturas. |


# 3. Uso de librería de IA

Este componente permite detectar y comparar visualmente los cambios en
una página web a partir de dos capturas de pantalla: una imagen base
(original) y una imagen actual (prediccion).

El sistema utiliza un modelo de inteligencia artificial YOLOv8 para
identificar los elementos visuales presentes en cada imagen y determinar
si hubo modificaciones en la interfaz, como movimiento, eliminación o
aparición de nuevos componentes.

El proceso está compuesto por dos scripts principales:

-   **YOLOPredictor.py:** ejecuta la detección de objetos en las
    imágenes.

-   **YOLOCompararPaginas.py:** analiza los resultados de detección para
    identificar diferencias entre ambas imágenes.

## 3.1. Requisitos previos

Antes de ejecutar los módulos, deben instalarse las siguientes librerías
en el entorno Python:

-   pip install ultralytics opencv-python pillow matplotlib

Si se utiliza una base de datos para almacenar los resultados, también
es necesario configurar la clase YOLOResultsDB en la carpeta base y
tener instaladas las dependencias correspondientes (por ejemplo,
pyodbc).

## 3.2. Flujo funcional del proceso

**Paso 1. Ejecución del detector YOLOv8**

El archivo **YOLOPredictor.py** permite procesar una imagen para
detectar los elementos presentes en la interfaz.

-   **Entrada:** ruta de la imagen capturada.

-   **Salida:** imagen con detecciones visuales y archivo con los
    resultados (lista de objetos detectados). Cada resultado contiene la
    información de los objetos detectados (clase, nivel de confianza y
    coordenadas).

**Paso 2. Comparación de resultados**

El archivo **YOLOCompararPaginas.py** permite comparar las detecciones
obtenidas entre la imagen original y la nueva.

-   **Entrada:** resultados de detección de ambas imágenes.

-   **Salida:** listado de diferencias y un indicador que confirma si
    hubo o no cambios.

**Paso 3. Interpretación de resultados**

El resultado de la comparación incluye un indicador principal:

-   pagina_cambio = True → se detectaron diferencias.

-   pagina_cambio = False → no se encontraron cambios.

## 3.3. Consideraciones de uso

-   Utilizar imágenes con la misma resolución para garantizar una
    comparación precisa.

-   Mantener el umbral de confianza (conf) entre 0.4 y 0.6 para evitar
    falsos positivos.

-   Guardar las imágenes procesadas con las detecciones para fines de
    auditoría o evidencia.

-   Si se utiliza conexión a base de datos, cerrar la sesión con
    close_db() al finalizar el proceso.

## 3.4. Resultado esperado

Al finalizar la ejecución:

-   Se generan dos imágenes con las detecciones visuales realizadas por
    el modelo YOLOv8.

-   Se produce un informe estructurado de los cambios detectados entre
    ambas versiones de la página.

-   El bot notifica si la página presenta modificaciones significativas
    respecto a la imagen original.

# 4. Estructura de Base de Datos

La base de datos almacena los resultados generados por el modelo de
inteligencia artificial YOLOv8, utilizados por el asistente para
detectar los elementos visuales presentes en las páginas web.\
Cada registro representa una detección individual realizada sobre una
imagen, incluyendo su posición, clase, nivel de confianza y metadatos
asociados al proceso.

## 4.1. Esquema General

**Nombre de la base de datos:** BD_TEST\
**Tabla principal:** DeteccionesYolo\
**Motor de base de datos sugerido:** SQL Server

**4.1. Detalle de la Tabla DeteccionesYolo**

| Campo     | Tipo de Dato             | Descripción                                                                 |
|-----------|--------------------------|------------------------------------------------------------------------------|
| id        | INT (PK, autoincremental)| Identificador único de la detección.                                        |
| web       | VARCHAR(100)             | Código o nombre de la página web o proceso donde se realizó la detección.   |
| clase     | VARCHAR(50)              | Tipo de objeto detectado por el modelo (botón, texto, imagen, campo, etc.). |
| confianza | FLOAT                    | Nivel de certeza de la predicción realizada por el modelo YOLOv8.           |
| x1        | INT                      | Coordenada X inicial del rectángulo delimitador del objeto detectado.       |
| y1        | INT                      | Coordenada Y inicial del rectángulo delimitador.                            |
| x2        | INT                      | Coordenada X final del rectángulo delimitador.                              |
| y2        | INT                      | Coordenada Y final del rectángulo delimitador.                              |

## 4.2. Consideraciones Técnicas

-   Esta tabla se alimenta automáticamente desde el módulo
    YOLOPredictor.py mediante la función save_results() de la clase
    YOLOResultsDB.

-   Los datos registrados pueden ser consultados para comparar
    resultados entre diferentes ejecuciones.

-   En caso de errores de conexión o escritura, validar la configuración
    de conexión (server, database, user, password) en el archivo de
    configuración del bot.

# 5. Notificaciones 

El asistente emite dos notificaciones dependiendo del escenario:
## 5. Notificaciones

| ID   | Asunto                                 | Cuerpo                                                                                                                                                                                                                                                                                                                                                          | Usuario                     |
|------|----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| N001 | RPAI: Cambios en el [nombrePagina]     | Estimados usuarios,  
Se informa que la página web del [nombrePagina] ha presentado cambios en el [nombreVentana]. Esta actualización podría afectar temporalmente el funcionamiento de algunas funcionalidades automatizadas.  
Se adjuntan la imagen original y la imagen con la predicción generada (nueva).  
*Esta es una notificación automática, por favor no responder a este mensaje.*  
Saludos cordiales. | Usuarios funcionales técnico. |
| N002 | RPAI: Sin cambios en el [nombrePagina] | Estimados usuarios,  
Se informa que, tras la revisión realizada, no se han detectado cambios en el proceso de [nombreVentana] página web del [nombrePagina]. Las funcionalidades automatizadas continúan operando con normalidad.  
Se adjunta la imagen original.  
*Esta es una notificación automática, por favor no responder a este mensaje.*  
Saludos cordiales. | Usuarios funcionales técnico. |
# 6. Usuarios de soporte

El proceso ha sido desarrollado:

| Nombre         | Rol              | Teléfono   | Correo                         |
|----------------|------------------|------------|--------------------------------|
| Paola Mendoza  | Desarrollador IA/RPA | 0998615087 | maria.mendozam@uees.edu.ec     |
| Andrés Cantos  | Desarrollador IA/RPA | 0981794940 | andres.cantos@uees.edu.ec      |

# 7. Escalabilidad

En caso de presentarse inconvenientes en el funcionamiento o la
ejecución del asistente y de la solución basada en inteligencia
artificial, la primera línea de atención será el equipo de soporte
técnico indicado en este manual.

# 8. Incidentes frecuentes y acción para la solución

| Incidente                                           | Acción                                                                                                                                                                                                 |
|-----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| La IA no detecta correctamente los elementos de la página web. | Revisar que la imagen capturada tenga buena resolución y sea consistente con el entrenamiento del modelo. Si el error persiste, ajustar el umbral de confianza (`conf`) en el archivo `YOLOPredictor.py` o reentrenar el modelo YOLOv8 con nuevas muestras. |
| La IA detecta cambios inexistentes entre dos imágenes. | Verificar que ambas capturas correspondan al mismo entorno (misma resolución, sin variaciones de zoom ni scroll). Reducir el umbral de similitud (`umbral_iou`) en el archivo `YOLOCompararPaginas.py` para disminuir falsos positivos. |
| La IA no genera resultados de comparación.          | Comprobar que existan resultados válidos de detección en ambas imágenes (original y nueva). Si las listas de resultados están vacías, revisar la ruta de las imágenes y el funcionamiento del modelo YOLO. |
| Error en la ejecución del modelo YOLOv8.            | Validar que el archivo del modelo (`.pt`) exista en la ruta configurada y que la versión de `ultralytics` esté correctamente instalada. En caso necesario, reinstalar con `pip install --upgrade ultralytics`. |
| El asistente no encuentra los archivos insumos.     | Verificar que los archivos insumos existan en las rutas configuradas y que no se hayan modificado sus nombres o ubicaciones. En caso de cambios, actualizar las rutas en la configuración del bot. |
| El Bot no pudo navegar en los portales web          | Validar la disponibilidad del portal y confirmar que no existan modificaciones en su estructura o URL. Si el portal se encuentra en mantenimiento, reintentar la ejecución una vez restablecido el servicio. |
  
