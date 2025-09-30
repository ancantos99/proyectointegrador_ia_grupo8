import pandas as pd
import matplotlib.pyplot as plt
import yaml
from ultralytics import YOLO
import numpy as np
import seaborn as sns

class YOLOMetricasVisualizar:
    def __init__(self, csv_path: str, model_path: str = None, data_yaml_path: str = None):
        """
        Inicializa la clase para visualizar métricas de YOLOv8.

        Args:
            csv_path (str): Ruta al archivo results.csv de YOLOv8.
            model_path (str, optional): Ruta al modelo entrenado (.pt).
            data_yaml_path (str, optional): Ruta al dataset YAML para obtener nombres de clases y evaluación por clase.
        """
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

        # Calcular F1-score promedio
        self.df['F1'] = 2 * (self.df["metrics/precision(B)"] * self.df["metrics/recall(B)"]) / \
                        (self.df["metrics/precision(B)"] + self.df["metrics/recall(B)"])

        self.model_path = model_path
        self.data_yaml_path = data_yaml_path
        self.class_names = None
        self.metric_por_clase = None

        # Cargar nombres de clases si se proporcionó YAML
        if data_yaml_path:
            with open(data_yaml_path, "r") as f:
                data_yaml = yaml.safe_load(f)
                self.class_names = [data_yaml['names'][i] for i in range(len(data_yaml['names']))]

        # Evaluar métricas por clase si se proporcionó modelo
        if model_path and data_yaml_path:
            self._calcular_metricas_por_clase()

    # ================= MÉTRICAS PROMEDIO =================
    def plot_loss(self):
        """Grafica Box, Cls y DFL Loss (train vs validation)"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.df["epoch"], self.df["train/box_loss"], label="Train Box Loss")
        plt.plot(self.df["epoch"], self.df["val/box_loss"], label="Val Box Loss")
        plt.plot(self.df["epoch"], self.df["train/cls_loss"], label="Train Cls Loss")
        plt.plot(self.df["epoch"], self.df["val/cls_loss"], label="Val Cls Loss")
        plt.plot(self.df["epoch"], self.df["train/dfl_loss"], label="Train DFL Loss")
        plt.plot(self.df["epoch"], self.df["val/dfl_loss"], label="Val DFL Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Training vs Validation Loss (Box, Cls, DFL)")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_map(self):
        """Grafica mAP50 y mAP50-95 (validación)"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.df["epoch"], self.df["metrics/mAP50(B)"], label="Val mAP@50")
        plt.plot(self.df["epoch"], self.df["metrics/mAP50-95(B)"], label="Val mAP@50-95")
        plt.xlabel("Epoch")
        plt.ylabel("mAP")
        plt.title("Validation Accuracy mAP (mAP@50 y mAP@50-95)")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_precision_recall_f1(self):
        """Grafica Precision, Recall y F1-score (validación)"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.df["epoch"], self.df["metrics/precision(B)"], label="Precision")
        plt.plot(self.df["epoch"], self.df["metrics/recall(B)"], label="Recall")
        plt.plot(self.df["F1"], label="F1-score")
        plt.xlabel("Epoch")
        plt.ylabel("Score")
        plt.title("Precisión, Recall y F1-score (Validación)")
        plt.legend()
        plt.grid()
        plt.show()

    def print_final_metrics(self):
        """Muestra las métricas finales promedio de validación"""
        precision = self.df["metrics/precision(B)"].iloc[-1]
        recall = self.df["metrics/recall(B)"].iloc[-1]
        f1 = self.df["F1"].iloc[-1]
        print(f"Final Metrics (last epoch):")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-score:  {f1:.4f}")

    # ================= MÉTRICAS POR CLASE =================
    def _calcular_metricas_por_clase(self):
        """Evalúa el modelo en el dataset de validación para obtener métricas por clase"""
        model = YOLO(self.model_path)
        results = model.val(data=self.data_yaml_path, verbose=False)
        self.metric_por_clase = results.box  # objeto Metric con listas p, r, f1, all_ap, ap_class_index

    def metrics_por_clase_tabla(self):
        """Muestra Precision, Recall, F1 y mAP50 para todas las clases en una tabla"""
        if self.class_names is None:
            print("No se han cargado nombres de clases. Asegúrate de pasar data_yaml_path.")
            return

        if self.metric_por_clase is None:
            print("No se han calculado métricas por clase. Asegúrate de pasar model_path y data_yaml_path.")
            return

        metric = self.metric_por_clase
        idx_map = {cls_idx: i for i, cls_idx in enumerate(metric.ap_class_index)}

        data = []
        for i, cls_name in enumerate(self.class_names):
            if i in idx_map:
                pos = idx_map[i]
                precision = metric.p[pos]
                recall = metric.r[pos]
                f1 = metric.f1[pos]
                map50 = metric.ap50[pos] if hasattr(metric, "ap50") else 0
                data.append([cls_name, precision, recall, f1, map50])
            else:
                data.append(
                    [cls_name, "clase sin métricas", "clase sin métricas", "clase sin métricas", "clase sin métricas"])

        df_tabla = pd.DataFrame(data, columns=["Clase", "Precision", "Recall", "F1", "mAP50"])
        #display(df_tabla)  # en Jupyter/Colab
        return df_tabla

    def plot_confusion_matrix(self, iou_threshold=0.5):
        """
        Genera y grafica la matriz de confusión por clase usando IoU threshold.

        Args:
            iou_threshold (float): Umbral de IoU para considerar una predicción correcta.
        """
        if self.model_path is None or self.data_yaml_path is None:
            print("Se requiere model_path y data_yaml_path para calcular la matriz de confusión.")
            return

        model = YOLO(self.model_path)
        results = model.val(data=self.data_yaml_path, verbose=False)

        num_classes = len(self.class_names)
        cm = np.zeros((num_classes, num_classes), dtype=int)

        # Función para calcular IoU entre dos cajas
        def iou(box1, box2):
            x1 = max(box1[0], box2[0])
            y1 = max(box1[1], box2[1])
            x2 = min(box1[2], box2[2])
            y2 = min(box1[3], box2[3])
            inter_area = max(0, x2 - x1) * max(0, y2 - y1)
            box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
            box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
            union_area = box1_area + box2_area - inter_area
            return inter_area / union_area if union_area > 0 else 0

        # Recorrer resultados por imagen
        for r in results:
            # Ground-truth
            gt_boxes = r.boxes.xyxy.numpy() if hasattr(r.boxes, 'xyxy') else np.array([])
            gt_cls = r.boxes.cls.numpy() if hasattr(r.boxes, 'cls') else np.array([])

            # Predicciones
            pred_boxes = r.pred[0].boxes.xyxy.numpy() if hasattr(r.pred[0].boxes, 'xyxy') else np.array([])
            pred_cls = r.pred[0].boxes.cls.numpy() if hasattr(r.pred[0].boxes, 'cls') else np.array([])

            for t_idx, t_box in enumerate(gt_boxes):
                t_class = int(gt_cls[t_idx])
                ious = np.array([iou(t_box, p_box) for p_box in pred_boxes])
                # Encontrar predicción con IoU máxima
                if len(ious) > 0 and ious.max() >= iou_threshold:
                    p_idx = ious.argmax()
                    p_class = int(pred_cls[p_idx])
                    cm[t_class, p_class] += 1
                else:
                    # No se detectó correctamente
                    cm[t_class, t_class] += 0  # opcional: contar como FN

        # Graficar
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', xticklabels=self.class_names,
                    yticklabels=self.class_names, cmap='Blues')
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title(f"Matriz de Confusión por Clase (IoU ≥ {iou_threshold})")
        plt.show()
        return cm
