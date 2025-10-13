from ultralytics import YOLO
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from src.base.YOLOResultsDB import YOLOResultsDB

class YOLOPredictor:
    def __init__(self, model_path,conf=0.5, iou=0.45,agnostic_nms=True, max_det=100, db_config =None):
        self.model = YOLO(model_path)
        self.datamodel_conf = conf  # NMS confidence threshold
        self.datamodel_iou = iou  # NMS IoU threshold
        self.datamodel_agnostic_nms = agnostic_nms  # NMS class-agnostic
        self.datamodel_max_det = max_det  # maximum number of detections per image

        self.db = None
        if db_config:
            self.db = YOLOResultsDB( server=db_config['server'], database=db_config['database'],
                                           user=db_config['user'], password=db_config['password'] )

    def predict(self, image_path, identificador_web=None, show_image=False):

        results = self.model.predict( image_path, conf=self.datamodel_conf, max_det=self.datamodel_max_det)
        res = results[0] if isinstance(results, list) else results

        img = cv2.imread(image_path)
        output_results = []

        for box in res.boxes:
            clase = res.names[int(box.cls)]
            confianza = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Dibujar caja y texto
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            cv2.putText(img, f"{clase} {confianza:.2f}", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            output_results.append({
                "clase": clase,
                "confianza": confianza,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })

        # Guardar en base de datos si está configurada
        if self.db and identificador_web:
            self.db.save_results(identificador_web, res)

        # Mostrar imagen si se requiere
        if show_image:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(12, 10))
            plt.imshow(img_rgb)
            plt.axis('off')
            plt.show()

        return output_results

    def close_db(self):
        """Cierra la conexión a la base de datos si existe."""
        if self.db:
            self.db.close()