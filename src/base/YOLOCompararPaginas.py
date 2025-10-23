import math

class YOLOComparadorResultados:

    def _iou(self, box1, box2):
        xA = max(box1[0], box2[0])
        yA = max(box1[1], box2[1])
        xB = min(box1[2], box2[2])
        yB = min(box1[3], box2[3])

        interArea = max(0, xB - xA) * max(0, yB - yA)
        box1Area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2Area = (box2[2] - box2[0]) * (box2[3] - box2[1])

        if box1Area + box2Area - interArea == 0:
            return 0
        return interArea / (box1Area + box2Area - interArea)

    def _tipo_cambio(self, box_db, box_pred, clase_db, clase_pred,
                      umbral_iou=0.3, umbral_dim=0.25, umbral_centro=150):
        """Determina el tipo de cambio de un objeto"""
        if clase_db != clase_pred:
            return 'nuevo'

        iou = self._iou(box_db, box_pred)

        ancho_db, alto_db = box_db[2] - box_db[0], box_db[3] - box_db[1]
        ancho_pred, alto_pred = box_pred[2] - box_pred[0], box_pred[3] - box_pred[1]
        diff_ancho = abs(ancho_db - ancho_pred) / max(ancho_db, ancho_pred)
        diff_alto = abs(alto_db - alto_pred) / max(alto_db, alto_pred)

        cx_db, cy_db = (box_db[0] + box_db[2]) / 2, (box_db[1] + box_db[3]) / 2
        cx_pred, cy_pred = (box_pred[0] + box_pred[2]) / 2, (box_pred[1] + box_pred[3]) / 2
        dist_centro = math.sqrt((cx_db - cx_pred)**2 + (cy_db - cy_pred)**2)

        mismo_tamano = diff_ancho < umbral_dim and diff_alto < umbral_dim
        misma_posicion = iou > umbral_iou or dist_centro < umbral_centro

        if mismo_tamano and misma_posicion:
            return 'igual'
        elif mismo_tamano and not misma_posicion:
            return 'movido'
        elif not mismo_tamano:
            return 'modificado'

        return 'nuevo'

    def comparar_paginas(self, db_results, pred_results, conf_thresh=0.5,
                         umbral_iou=0.3, umbral_dim=0.25, umbral_centro=150):
        """
        Compara resultados guardados en BD con predicciones YOLO.
        Empareja 1 a 1 los elementos (cada pred solo se usa una vez)
        """
        cambios = []
        nuevos = []

        # Filtrar predicciones con baja confianza
        pred_results = [r for r in pred_results if r['confianza'] >= conf_thresh]

        usados_pred = set()  # para evitar reutilizar una predicción

        # Comparar cada objeto de la BD con su mejor coincidencia
        for db_r in db_results:
            mejor_pred = None
            mejor_iou = 0
            mejor_tipo = 'eliminado'
            mejor_idx = None

            for j, pred in enumerate(pred_results):
                if j in usados_pred:
                    continue  # ya fue emparejada con otro

                tipo = self._tipo_cambio(
                    [db_r['x1'], db_r['y1'], db_r['x2'], db_r['y2']],
                    [pred['x1'], pred['y1'], pred['x2'], pred['y2']],
                    db_r['clase'], pred['clase'],
                    umbral_iou, umbral_dim, umbral_centro
                )
                if tipo in ['igual', 'movido', 'modificado']:
                    iou = self._iou(
                        [db_r['x1'], db_r['y1'], db_r['x2'], db_r['y2']],
                        [pred['x1'], pred['y1'], pred['x2'], pred['y2']]
                    )
                    # nos quedamos con el que tenga mayor IOU
                    if iou > mejor_iou:
                        mejor_iou = iou
                        mejor_pred = pred
                        mejor_tipo = tipo
                        mejor_idx = j

            if mejor_pred:
                usados_pred.add(mejor_idx)

            if mejor_tipo != 'igual':
                cambio = {
                    'id': db_r.get('id'),
                    'clase': db_r['clase'],
                    'confianza': db_r['confianza'],
                    'estado': mejor_tipo
                }
                if mejor_pred:
                    cambio['posicion_anterior'] = {
                        'x1': db_r['x1'], 'y1': db_r['y1'],
                        'x2': db_r['x2'], 'y2': db_r['y2']
                    }
                    cambio['posicion_actual'] = {
                        'x1': mejor_pred['x1'], 'y1': mejor_pred['y1'],
                        'x2': mejor_pred['x2'], 'y2': mejor_pred['y2']
                    }
                cambios.append(cambio)

        # Detectar objetos nuevos (predicciones no usadas)
        # Cambio 22 oct : A los elementos nuevos no se los tomara en cuenta para el analisis de cambio
        for j, pred in enumerate(pred_results):
            if j not in usados_pred:
                nuevos.append({
                    'id': None,
                    'clase': pred['clase'],
                    'confianza': pred['confianza'],
                    'estado': 'nuevo',
                    'posicion_actual': {
                        'x1': pred['x1'], 'y1': pred['y1'],
                        'x2': pred['x2'], 'y2': pred['y2']
                    }
                })

        pagina_cambio = len(cambios) > 0

        return {
            'cambios': cambios,
            'nuevos': nuevos,
            'pagina_cambio': pagina_cambio
        }
