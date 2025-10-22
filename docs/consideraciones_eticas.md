# Consideraciones éticas
> **Detección de cambios en interfaces web para procesos RPA utilizando Inteligencia Artificial**
>
> Aunque este proyecto se enfoca en la automatización de la detección de cambios en interfaces web mediante IA, es fundamental abordar las implicaciones éticas relacionadas con la privacidad, el uso responsable de datos y el impacto en los usuarios y trabajadores involucrados en procesos RPA.

## 1️⃣ Análisis de sesgos:
### ¿El dataset tiene sesgos demográficos, culturales o de otro tipo?

| Aspecto | Diagnóstico basado en el Análisis | Implicaciones/Grupos Perjudicados |
|---------|-----------------------------------|-----------------------------------|
| **Sesgo Estructural (Clases)** | **Sesgo de Desbalance Severo**: La clase `link` domina con **64.48%** de las instancias, creando un ratio de desbalance de **1,947.88×** respecto a la clase minoritaria (`toggle`). | El modelo tendrá un rendimiento excelente en `link` (clase mayoritaria), pero un pobre recall y precisión en clases minoritarias pero críticas para RPA, como `toggle`, `textarea` e `input`. |
| **Sesgo Geográfico/Cultural** | El dataset proviene de "más de 300 sitios web populares". Si estos son predominantemente anglosajones, existe un sesgo de diseño y lenguaje. | El modelo podría fallar en la detección de elementos que sigan convenciones de diseño o estén escritos en idiomas con alfabetos no latinos, comprometiendo la robustez del RPA en entornos internacionales. |
| **Sesgo de Datos Faltantes** | Tres clases (`select`, `image`, `text`) tienen **0 instancias** en el conjunto de entrenamiento. | El modelo **NO** podrá detectar estas clases. Los procesos RPA que dependan de la detección de un elemento `<select>` o una imagen interactiva NO estarán cubiertos. |

### ¿Cómo podrían afectar estos sesgos las predicciones?
### ¿Qué grupos podrían ser perjudicados?
## 2️⃣ Equidad y fairness:
• ¿El modelo trata a todos los grupos de forma equitativa?
• Métricas de fairness evaluadas (si aplica)
• Estrategias implementadas para mitigar inequidades
## 3️⃣ Privacidad:
• ¿Se utilizan datos personales o sensibles?
• ¿Cómo se protege la privacidad de los usuarios?
• Cumplimiento con regulaciones (GDPR, CCPA, etc.)
## 4️⃣ Transparencia y explicabilidad:
• ¿El modelo es interpretable?
• ¿Los usuarios entienden cómo funciona?
• Técnicas de explicabilidad implementadas (SHAP, LIME, etc.)
## 5️⃣ Impacto social:
• ¿Qué impacto positivo puede tener el proyecto?
• ¿Qué impactos negativos podrían surgir?
• ¿Quiénes se benefician? ¿Quiénes podrían ser perjudicados?
## 6️⃣ Responsabilidad:
• ¿Quién es responsable si el modelo falla?
• ¿Qué mecanismos de accountability existen?
• Plan de monitoreo y actualización del modelo
## 7️⃣ Uso dual y mal uso:
• ¿Podría el modelo usarse con fines maliciosos?
• ¿Qué salvaguardas se han implementado?
• Limitaciones de uso claramente documentadas
## 8️⃣ Limitaciones reconocidas:
• ¿En qué casos NO debe usarse el modelo?
• ¿Qué advertencias deben darse a los usuarios?
• Casos límite donde el modelo no es confiable
