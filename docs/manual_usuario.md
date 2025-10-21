**Detección de cambios en interfaces web para procesos RPA utilizando
Inteligencia Artificial**

**MANUAL DE USUARIO**

#  TRAZABILIDAD DEL DOCUMENTO
| Versión | Preparado Por                        | Fecha    | Revisado por         | Descripción     |
|---------|--------------------------------------|----------|-----------------------|------------------|
| 1       | Andrés Martín Cantos Rivadeneira     | 24-10-25 | PhD. Gladys Villegas  | Versión Inicial |
|         | María Paola Mendoza Mendieta         |          |                       |                  |

# CONTENIDO

[CARATULA
[1](#comunicado-oficial---uees---universidad-espíritu-santo)](#comunicado-oficial---uees---universidad-espíritu-santo)

[TRAZABILIDAD DEL DOCUMENTO
[2](#trazabilidad-del-documento)](#trazabilidad-del-documento)

[CONTENIDO [3](#contenido)](#contenido)

[1. Información General del Proceso
[4](#información-general-del-proceso)](#información-general-del-proceso)

[1.1. Descripción del Problema
[4](#descripción-del-problema)](#descripción-del-problema)

[1.1. Resultados esperados de la solución e indicadores de éxito
[4](#resultados-esperados-de-la-solución-e-indicadores-de-éxito)](#resultados-esperados-de-la-solución-e-indicadores-de-éxito)

[1.2. Programas para utilizar
[4](#programas-para-utilizar)](#programas-para-utilizar)

[1.3. Usuarios requeridos por el bot
[5](#usuarios-requeridos-por-el-bot)](#usuarios-requeridos-por-el-bot)

[2. Diseño detallado [6](#diseño-detallado)](#diseño-detallado)

[2.1. Diagrama de arquitectura
[6](#diagrama-de-arquitectura)](#diagrama-de-arquitectura)

[2.2. Flujo del proceso detallado
[6](#flujo-del-proceso-detallado)](#flujo-del-proceso-detallado)

[3. Uso de librería de IA
[1](#uso-de-librería-de-ia)](#uso-de-librería-de-ia)

[3.1. Requisitos previos [1](#requisitos-previos)](#requisitos-previos)

[3.2. Flujo funcional del proceso
[1](#flujo-funcional-del-proceso)](#flujo-funcional-del-proceso)

[3.3. Consideraciones de uso
[2](#consideraciones-de-uso)](#consideraciones-de-uso)

[3.4. Resultado esperado [2](#resultado-esperado)](#resultado-esperado)

[4. Estructura de Base de Datos
[2](#estructura-de-base-de-datos)](#estructura-de-base-de-datos)

[4.1. Esquema General [2](#esquema-general)](#esquema-general)

[4.2. Consideraciones Técnicas
[3](#consideraciones-técnicas)](#consideraciones-técnicas)

[5. Notificaciones [3](#notificaciones)](#notificaciones)

[6. Usuarios de soporte [4](#usuarios-de-soporte)](#usuarios-de-soporte)

[7. Escalabilidad [5](#escalabilidad)](#escalabilidad)

[8. Incidentes frecuentes y acción para la solución
[5](#incidentes-frecuentes-y-acción-para-la-solución)](#incidentes-frecuentes-y-acción-para-la-solución)

1.  # Información General del Proceso

    1.  ## Descripción del Problema

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

  ------------- ------------------------- ------------ ------------- -------------
  Aplicación /  Módulo                    Tipo de      Solicita      Nivel de
  Sistema                                 Interfaz de  Claves de     Estabilidad
                                          Usuario      Acceso        

  SQL Server    Base de datos             Escritorio   SI            ALTA

  Electroneek   Herramienta RPA           Escritorio   SI            ALTA

  Servicio de   Gestor de Correo          Servicio web SI            ALTA
  Microsoft                                                          

  Google Chome  Navegador Web con acceso  Escritorio   NO            ALTA
                a SRI y Senescyt                                     

  Python        Herramienta de desarrollo Escritorio   NO            ALTA
  ------------- ------------------------- ------------ ------------- -------------

## Usuarios requeridos por el bot

  ------------------------------------------------------- --------------------
  Usuario                                                 Perfil/Propietaria

  Cuenta de Correo electrónico y contraseña (debe tener   Paola Mendoza
  permisos para acceso a aplicaciones de terceros)        

  Credenciales de acceso para base de datos               Andrés Cantos

  Credenciales de acceso al SRI                           Paola Mendoza
  ------------------------------------------------------- --------------------

4.  **Fuera del alcance**

Este proyecto no contempla dentro de su alcance la implementación de
acciones reactivas o correctivas dentro de los procesos de
automatización ante posibles cambios en la página web.

# 2. Diseño detallado

## 2.1. Diagrama de arquitectura

![Interfaz de usuario gráfica El contenido generado por IA puede ser
incorrecto.](media/image2.png){width="6.1375in"
height="3.067361111111111in"}

## 2.2. Flujo del proceso detallado

En este capítulo se describe de forma detallada el proceso en formato
TO-BE (como será), donde se describe paso a paso las actividades a
desarrollar, así como el proceder de cada una para permitir al
desarrollador configurar el proces

+--------+--------------------------------------------------+---------+
| *      | > **Pasos Detallados**                           | **      |
| *Activ |                                                  | Errores |
| idad** |                                                  | Pr      |
|        |                                                  | obables |
|        |                                                  | y       |
|        |                                                  | P       |
|        |                                                  | rocedim |
|        |                                                  | iento** |
+--------+--------------------------------------------------+---------+
| Nave   | 1.  Ir a la URL:                                 |         |
| gación |     > <                                          |         |
| y      | https://www.senescyt.gob.ec/web/guest/consultas> |         |
| obt    |                                                  |         |
| ención | 2.  Se captura la pantalla actual (predicción)   |         |
| de     |                                                  |         |
| datos  | 3.  Se valida si la pantalla tiene cambios       |         |
| de     |     > (validar imagen original y predicción)     |         |
| SE     |                                                  |         |
| NESCYT | 4.  Si se detectan cambios en la ventana de la   |         |
|        |     > página, se envía una notificación          |         |
|        |     > incluyendo la imagen original y la nueva   |         |
|        |     > ventana de predicción. En caso contrario,  |         |
|        |     > se envía una notificación indicando que la |         |
|        |     > ventana de la página no presenta cambios,  |         |
|        |     > acompañada de la imagen original.          |         |
|        |                                                  |         |
|        | 5.  Datos de entrada requeridos:                 |         |
|        |                                                  |         |
|        |     a.  Cédula de identidad                      |         |
|        |                                                  |         |
|        |     ```{=html}                                   |         |
|        |     <!-- -->                                     |         |
|        |     ```                                          |         |
|        |     a.  Resolver Captcha                         |         |
|        |                                                  |         |
|        | !                                                |         |
|        | [](media/image3.png){width="5.786893044619423in" |         |
|        | height="2.761791338582677in"}                    |         |
+--------+--------------------------------------------------+---------+
| De     | 1.  Ingresar al portal del SRI:                  |         |
| scarga |     [https://srienlinea.sri.gob.ec/](https://sr  |         |
| de     | ienlinea.sri.gob.ec/auth/realms/Internet/protoco |         |
| fa     | l/openid-connect/auth?client_id=app-sri-claves-a |         |
| cturas | ngular&redirect_uri=https%3A%2F%2Fsrienlinea.sri |         |
|        | .gob.ec%2Fsri-en-linea%2F%2Fcontribuyente%2Fperf |         |
|        | il&state=857feb78-ff75-4f56-8517-167fdbb872db&no |         |
|        | nce=e708edc4-280c-42be-9e3a-1fdd2da99f32&respons |         |
|        | e_mode=fragment&response_type=code&scope=openid) |         |
|        |                                                  |         |
|        | 2.  Se captura la pantalla actual del login      |         |
|        |     (predicción)                                 |         |
|        |                                                  |         |
|        | 3.  Se valida si la pantalla tiene cambios       |         |
|        |     (validar imagen original y predicción)       |         |
|        |                                                  |         |
|        | 4.  Si se detectan cambios en la ventana de la   |         |
|        |     página, se envía una notificación incluyendo |         |
|        |     la imagen original y la nueva ventana de     |         |
|        |     predicción. En caso contrario, se envía una  |         |
|        |     notificación indicando que la ventana de la  |         |
|        |     página no presenta cambios, acompañada de la |         |
|        |     imagen original.                             |         |
|        |                                                  |         |
|        | > !                                              |         |
|        | [](media/image4.png){width="6.187412510936133in" |         |
|        | > height="2.801442475940507in"}                  |         |
|        |                                                  |         |
|        | 5.  Realiza el inicio de sesión en el SRI        |         |
|        |                                                  |         |
|        |     a.  RUC/C.I./Pasaporte                       |         |
|        |                                                  |         |
|        |     b.  Clave                                    |         |
|        |                                                  |         |
|        |     c.  Clic en Ingresar                         |         |
|        |                                                  |         |
|        | ![Interfaz de usuario gráfica, Aplicación        |         |
|        | Descripción generada                             |         |
|        | automáticamente                                  |         |
|        | ](media/image5.png){width="1.6935192475940508in" |         |
|        | height="1.9644827209098863in"}                   |         |
|        |                                                  |         |
|        | 6.  Valida si inicio sesión                      |         |
|        |                                                  |         |
|        | 7.  Se captura la pantalla actual del inicio de  |         |
|        |     sesión (predicción)                          |         |
|        |                                                  |         |
|        | 8.  Se valida si la pantalla tiene cambios       |         |
|        |     (validar imagen original y predicción)       |         |
|        |                                                  |         |
|        | 9.  Si se detectan cambios en la ventana de la   |         |
|        |     página, se envía una notificación incluyendo |         |
|        |     la imagen original y la nueva ventana de     |         |
|        |     predicción. En caso contrario, se envía una  |         |
|        |     notificación indicando que la ventana de la  |         |
|        |     página no presenta cambios, acompañada de la |         |
|        |     imagen original.                             |         |
|        |                                                  |         |
|        | >                                                |         |
|        | ![](media/image6.png){width="5.77950021872266in" |         |
|        | > height="2.6261876640419946in"}                 |         |
|        |                                                  |         |
|        | 10. Ir a la sección de facturas recibidas:       |         |
|        |     FACTURACIÓN ELECTRÓNICA 🡪 Comprobantes       |         |
|        |     electrónicos recibidos                       |         |
|        |                                                  |         |
|        | 11. Se captura la pantalla actual facturas       |         |
|        |     recibidas(predicción)                        |         |
|        |                                                  |         |
|        | 12. Se valida si la pantalla tiene cambios       |         |
|        |     (validar imagen original y predicción)       |         |
|        |                                                  |         |
|        | 13. Si se detectan cambios en la ventana de la   |         |
|        |     página, se envía una notificación incluyendo |         |
|        |     la imagen original y la nueva ventana de     |         |
|        |     predicción. En caso contrario, se envía una  |         |
|        |     notificación indicando que la ventana de la  |         |
|        |     página no presenta cambios, acompañada de la |         |
|        |     imagen original.                             |         |
|        |                                                  |         |
|        | !                                                |         |
|        | [](media/image7.png){width="6.294622703412074in" |         |
|        | height="2.849983595800525in"}                    |         |
|        |                                                  |         |
|        | 14. Realizar consulta de las facturas            |         |
|        |                                                  |         |
|        |     a.  Seleccionar Ruc/Cédula/Pasaporte         |         |
|        |                                                  |         |
|        |     b.  Periodo de emisión (mes actual y         |         |
|        |         anterior, el mes anterior se descarga    |         |
|        |         solo hasta un día específico del mes     |         |
|        |         actual)                                  |         |
|        |                                                  |         |
|        |     c.  Tipo de comprobante (Factura, Notas de   |         |
|        |         crédito, Notas de débito, Retenciones y  |         |
|        |         Liquidación de compra de bienes y        |         |
|        |         prestación de servicios)                 |         |
|        |                                                  |         |
|        |     d.  Consultar. NOTA: Previo a realizar la    |         |
|        |         consulta se debe hacer una resolución de |         |
|        |         captcha                                  |         |
|        |                                                  |         |
|        |     e.  Clic en Descargar reporte                |         |
|        |                                                  |         |
|        | ![Interfaz de usuario gráfica, Aplicación        |         |
|        | Descripción generada                             |         |
|        | automáticamente                                  |         |
|        | ](media/image8.png){width="3.0315824584426947in" |         |
|        | height="2.3633552055993in"}                      |         |
|        |                                                  |         |
|        | 15. Descargar TXT de facturas.                   |         |
+--------+--------------------------------------------------+---------+

# 

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

**3. Detalle de la Tabla DeteccionesYolo**

  --------------------------------------------------------------------------
  **Campo**   **Tipo de Dato**    **Descripción**
  ----------- ------------------- ------------------------------------------
  id          INT (PK,            Identificador único de la detección.
              autoincremental)    

  web         VARCHAR(100)        Código o nombre de la página web o proceso
                                  donde se realizó la detección.

  clase       VARCHAR(50)         Tipo de objeto detectado por el modelo
                                  (botón, texto, imagen, campo, etc.).

  confianza   FLOAT               Nivel de certeza de la predicción
                                  realizada por el modelo YOLOv8.

  x1          INT                 Coordenada X inicial del rectángulo
                                  delimitador del objeto detectado.

  y1          INT                 Coordenada Y inicial del rectángulo
                                  delimitador.

  x2          INT                 Coordenada X final del rectángulo
                                  delimitador.

  y2          INT                 Coordenada Y final del rectángulo
                                  delimitador.
  --------------------------------------------------------------------------

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

+-----+--------------+-----------------------------------+-------------+
| **I | **Asunto**   | **Cuerpo**                        | **Usuario** |
| d** |              |                                   |             |
+-----+--------------+-----------------------------------+-------------+
| N   | RPAI:        | Estimados usuarios,               | Usuarios    |
| 001 | Cambios en   |                                   | funcionales |
|     | el           | Se informa que la página web del  | técnico.    |
|     | \[no         | \[nombrePagina\] ha presentado    |             |
|     | mbrePagina\] | **cambios en el**                 |             |
|     |              | \[nombreVentana\]. Esta           |             |
|     |              | actualización podría afectar      |             |
|     |              | temporalmente el funcionamiento   |             |
|     |              | de algunas funcionalidades        |             |
|     |              | automatizadas.                    |             |
|     |              |                                   |             |
|     |              | Se adjuntan la imagen original y  |             |
|     |              | la imagen con la predicción       |             |
|     |              | generada (nueva).                 |             |
|     |              |                                   |             |
|     |              | *Esta es una notificación         |             |
|     |              | automática, por favor no          |             |
|     |              | responder a este mensaje.*        |             |
|     |              |                                   |             |
|     |              | Saludos cordiales,                |             |
|     |              |                                   |             |
|     |              | ![](me                            |             |
|     |              | dia/image9.png){width="3.10625in" |             |
|     |              | height="1.0993055555555555in"}    |             |
+-----+--------------+-----------------------------------+-------------+
| N   | RPAI: Sin    | **Estimados usuarios,**           | Usuarios    |
| 002 | cambios en   |                                   | funcionales |
|     | el           | Se informa que, tras la revisión  | técnico.    |
|     | \[no         | realizada, no se han detectado    |             |
|     | mbrePagina\] | cambios en el proceso de          |             |
|     |              | \[nombreVentana\] página web del  |             |
|     |              | \[nombrePagina\]. Las             |             |
|     |              | funcionalidades automatizadas     |             |
|     |              | continúan operando con            |             |
|     |              | normalidad.                       |             |
|     |              |                                   |             |
|     |              | Se adjuntan la imagen original    |             |
|     |              |                                   |             |
|     |              | *Esta es una notificación         |             |
|     |              | automática, por favor no          |             |
|     |              | responder a este mensaje.*        |             |
|     |              |                                   |             |
|     |              | Saludos cordiales,                |             |
|     |              |                                   |             |
|     |              | ![](media/image10                 |             |
|     |              | .png){width="2.223468941382327in" |             |
|     |              | height="1.4622134733158356in"}    |             |
+-----+--------------+-----------------------------------+-------------+

# 6. Usuarios de soporte

El proceso ha sido desarrollado:

  -----------------------------------------------------------------------------
  Nombre            Rol               Teléfono     Correo
  ----------------- ----------------- ------------ ----------------------------
  Paola Mendoza     Desarrollador IA/ 0998615087   maría.mendozam@uees.edu.ec
                    RPA                            

  Andrés Cantos     Desarrollador IA/ 0981794940   andres.cantos@uees.edu.ec
                    RPA                            
  -----------------------------------------------------------------------------

# 7. Escalabilidad

En caso de presentarse inconvenientes en el funcionamiento o la
ejecución del asistente y de la solución basada en inteligencia
artificial, la primera línea de atención será el equipo de soporte
técnico indicado en este manual.

# 8. Incidentes frecuentes y acción para la solución

  ----------------------------- -----------------------------------------
  Incidente                     Acción

  La IA no detecta              Revisar que la imagen capturada tenga
  correctamente los elementos   buena resolución y sea consistente con el
  de la página web.             entrenamiento del modelo. Si el error
                                persiste, ajustar el umbral de confianza
                                (conf) en el archivo YOLOPredictor.py o
                                reentrenar el modelo YOLOv8 con nuevas
                                muestras.

  La IA detecta cambios         Verificar que ambas capturas correspondan
  inexistentes entre dos        al mismo entorno (misma resolución, sin
  imágenes.                     variaciones de zoom ni scroll). Reducir
                                el umbral de similitud (umbral_iou) en el
                                archivo YOLOCompararPaginas.py para
                                disminuir falsos positivos.

  La IA no genera resultados de Comprobar que existan resultados válidos
  comparación.                  de detección en ambas imágenes (original
                                y nueva). Si las listas de resultados
                                están vacías, revisar la ruta de las
                                imágenes y el funcionamiento del modelo
                                YOLO.

  Error en la ejecución del     Validar que el archivo del modelo (.pt)
  modelo YOLOv8.                exista en la ruta configurada y que la
                                versión de ultralytics esté correctamente
                                instalada. En caso necesario, reinstalar
                                con pip install \--upgrade ultralytics.

  El asistente no encuentra los Verificar que los archivos insumos
  archivos insumos.             existan en las rutas configuradas y que
                                no se hayan modificado sus nombres o
                                ubicaciones. En caso de cambios,
                                actualizar las rutas en la configuración
                                del bot.

  El Bot no pudo navegar en los Validar la disponibilidad del portal y
  portales web                  confirmar que no existan modificaciones
                                en su estructura o URL. Si el portal se
                                encuentra en mantenimiento, reintentar la
                                ejecución una vez restablecido el
                                servicio.
  ----------------------------- -----------------------------------------
