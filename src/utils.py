import numpy as np
import types


class ComparadorVersiones:
    """
    Compara los resultados de detección (boxes) obtenidos de una base de datos
    (versión antigua) con los de una nueva predicción YOLO (versión actual).
    """

    # ----------------------------------------------------
    # Parámetros de umbral ajustables
    # ----------------------------------------------------
    # IoU mínimo para considerar que un box de la base coincide con uno de la predicción.
    IOU_UMBRAL = 0.85
    # Cambio máximo permitido en el centro del box (en porcentaje del tamaño de la imagen)
    # para considerarlo 'movido' en lugar de 'nuevo' o 'diferente'.
    MOVIMIENTO_UMBRAL_PIXEL = 5  # 5 píxeles de desplazamiento máximo
    # Cambio máximo permitido en la confianza para considerarlo 'igual'.
    CONFIANZA_UMBRAL = 0.05

    def __init__(self, umbral_iou=0.85, umbral_movimiento_pixel=10, umbral_confianza=0.08):
        """Inicializa la clase con umbrales personalizados."""
        self.IOU_UMBRAL = umbral_iou
        self.MOVIMIENTO_UMBRAL_PIXEL = umbral_movimiento_pixel
        self.CONFIANZA_UMBRAL = umbral_confianza

    # ----------------------------------------------------
    # Métodos Auxiliares de Cálculo
    # ----------------------------------------------------

    @staticmethod
    def _calcular_iou(box1, box2):
        """Calcula Intersección sobre Unión (IoU) entre dos boxes [x1, y1, x2, y2]."""
        x_a = max(box1[0], box2[0])
        y_a = max(box1[1], box2[1])
        x_b = min(box1[2], box2[2])
        y_b = min(box1[3], box2[3])

        inter_area = max(0, x_b - x_a) * max(0, y_b - y_a)

        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

        union_area = float(box1_area + box2_area - inter_area)
        if union_area == 0:
            return 0.0
        return inter_area / union_area

    @staticmethod
    def _calcular_centro(box):
        """Calcula el centro de un box [x_c, y_c]."""
        return np.array([
            (box[0] + box[2]) / 2,
            (box[1] + box[3]) / 2
        ])

    @staticmethod
    def _get_boxes_data(result):
        if result is None or not hasattr(result, 'boxes') or len(result.boxes.xyxy) == 0:
            # Si no hay resultados o boxes, simplemente retorna la imagen original
            return np.array([]), np.array([]), np.array([])
        # YOLOv8 puede devolver tensores 0-dim
        # Manejar ambos casos: si viene de YOLO (con .cpu().numpy()) o de la DB (ya en NumPy)
        if isinstance(result.boxes.xyxy, np.ndarray):
            boxes = result.boxes.xyxy.astype(int)  # Nx4, ya en numpy
            cls = result.boxes.cls.astype(int)  # N, ya en numpy
            conf = result.boxes.conf  # N, ya en numpy
        else:  # Asumir que son tensores de YOLO
            # Los resultados de YOLO vienen como tensores
            boxes = result.boxes.xyxy.cpu().numpy().astype(int)  # Nx4
            cls = result.boxes.cls.cpu().numpy().astype(int)  # N
            conf = result.boxes.conf.cpu().numpy()  # N

        #conf = conf.astype(float)
        return boxes, cls, conf

    # ----------------------------------------------------
    # Método Principal de Comparación
    # ----------------------------------------------------

    def comparar_base_con_prediccion(self, result_base, result_prediccion):
        """
        Compara los boxes de la versión base con los de la predicción.

        :param result_base: Objeto result de la base de datos (get_results_por_web).
        :param result_prediccion: Objeto result de la predicción YOLO.
        :return: Tupla (pagina_cambio, nuevos, cambios)
        """

        # Extraer datos de la base (antigua)
        boxes_base, cls_base, conf_base = self._get_boxes_data(result_base)
        names_base = result_base.names if result_base else {}

        # Extraer datos de la predicción (nueva)
        boxes_pred, cls_pred, conf_pred = self._get_boxes_data(result_prediccion)
        names_pred = result_prediccion.names if result_prediccion else {}

        # ----------------------------------------------------------------------
        # Caso 1: No hay boxes en la base
        # ----------------------------------------------------------------------
        if len(boxes_base) == 0:
            pagina_cambio = len(boxes_pred) > 0  # Hay cambio si hay algo nuevo
            nuevos = []
            for i in range(len(boxes_pred)):
                nuevos.append(
                    {"tipo": "nuevo", "box": boxes_pred[i].tolist(),
                     "clase": names_pred.get(cls_pred[i], 'Desconocido'), "confianza": conf_pred[i]}
                )
            return (pagina_cambio, nuevos, [])

        # ----------------------------------------------------------------------
        # Inicialización de resultados y marcadores
        # ----------------------------------------------------------------------

        # Array de marcadores para boxes de la predicción (True si ya se han emparejado)
        emparejado_pred = np.zeros(len(boxes_pred), dtype=bool)

        cambios = []
        pagina_cambio = False

        # ----------------------------------------------------------------------
        # Iterar sobre la BASE para encontrar emparejamientos en la PREDICCIÓN
        # ----------------------------------------------------------------------
        for i in range(len(boxes_base)):
            box_b = boxes_base[i]
            cls_b = names_base.get(cls_base[i], 'Desconocido')
            conf_b = conf_base[i]
            centro_b = self._calcular_centro(box_b)

            mejor_iou = -1
            mejor_idx_pred = -1

            # 1. Buscar el mejor box de la predicción con un IoU alto y la misma clase
            for j in range(len(boxes_pred)):
                if emparejado_pred[j]: continue  # Saltar boxes de predicción ya usados

                cls_p = names_pred.get(cls_pred[j], 'Desconocido')
                if cls_b != cls_p: continue  # Debe ser la misma clase

                iou = self._calcular_iou(box_b, boxes_pred[j])

                if iou >= self.IOU_UMBRAL and iou > mejor_iou:
                    mejor_iou = iou
                    mejor_idx_pred = j

            # 2. Procesar el emparejamiento
            if mejor_idx_pred != -1:
                j = mejor_idx_pred
                box_p = boxes_pred[j]
                conf_p = conf_pred[j]
                #conf_p_py = conf_p.item()
                centro_p = self._calcular_centro(box_p)

                # Marcar como usado
                emparejado_pred[j] = True
                # Calcular la distancia de movimiento entre centros
                distancia_movimiento = np.linalg.norm(centro_b - centro_p)
                # Determinar el tipo de cambio
                tipo_cambio = "igual"
                if abs(conf_p - conf_b) > self.CONFIANZA_UMBRAL:
                    # Si cambia la confianza, es una modificación
                    tipo_cambio = "modificado"
                if distancia_movimiento > self.MOVIMIENTO_UMBRAL_PIXEL:
                    # Si se mueve (a pesar de tener buen IoU)
                    tipo_cambio = "movido"
                if tipo_cambio != "igual":
                    pagina_cambio = True

                cambios.append({
                    "tipo": tipo_cambio,
                    "clase": cls_b,
                    "base": {"box": box_b.tolist(), "confianza": float(conf_b)},
                    "prediccion": {"box": box_p.tolist(), "confianza_p": float(conf_p)}
                })

            else:
                # El box de la base no fue encontrado: se considera ELIMINADO (un tipo de cambio relevante)
                pagina_cambio = True
                cambios.append({
                    "tipo": "eliminado",
                    "clase": cls_b,
                    "base": {"box": box_b.tolist(), "confianza": float(conf_b)},
                    "prediccion": None
                })

        # ----------------------------------------------------------------------
        # Caso 3: Boxes NUEVOS (los que quedaron sin emparejar en la PREDICCIÓN)
        # ----------------------------------------------------------------------
        nuevos = []
        for j in range(len(boxes_pred)):
            if not emparejado_pred[j]:
                #pagina_cambio = True
                nuevos.append(
                    {"tipo": "nuevo", "box": boxes_pred[j].tolist(),
                     "clase": names_pred.get(cls_pred[j], 'Desconocido'), "confianza": float(conf_pred[j])}
                )

        return (pagina_cambio, nuevos, cambios)