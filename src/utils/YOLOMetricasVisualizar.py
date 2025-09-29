import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from ultralytics import YOLO
import numpy as np

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

    def print_metrics_por_clase(self):
        """Imprime Precision, Recall, F1, mAP50 por clase usando ap_class_index"""
        if self.metric_por_clase is None or self.class_names is None:
            print("No se han calculado métricas por clase. Asegúrate de pasar model_path y data_yaml_path.")
            return

        metric = self.metric_por_clase
        print("Métricas por clase:")

        # ap_class_index indica a qué clase corresponde cada valor de p, r, f1
        for i, class_idx in enumerate(metric.ap_class_index):
            cls_name = self.class_names[class_idx]
            precision = metric.p[i]
            recall = metric.r[i]
            f1 = metric.f1[i]
            map50 = metric.ap50[i] if hasattr(metric, "ap50") else 0
            print(f"{cls_name}: Precision={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f}, mAP50={map50:.3f}")

    def plot_confusion_matrix(self):
        """Grafica confusion matrix por clase"""
        if self.metric_por_clase is None:
            print("No se puede generar confusion matrix. Asegúrate de pasar model_path y data_yaml_path.")
            return
        cm = self.metric_por_clase.confusion_matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=self.class_names, yticklabels=self.class_names)
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title("Confusion Matrix por Clase")
        plt.show()

    def plot_iou_por_clase(self):
        """Grafica IoU promedio por clase"""
        if self.metric_por_clase is None:
            print("No se puede generar IoU por clase. Asegúrate de pasar model_path y data_yaml_path.")
            return
        iou_per_class = np.array(self.metric_por_clase.iou) if hasattr(self.metric_por_clase, "iou") else np.zeros(len(self.class_names))
        plt.figure(figsize=(12, 6))
        sns.barplot(x=self.class_names, y=iou_per_class)
        plt.ylabel("IoU promedio")
        plt.xlabel("Clase")
        plt.title("IoU promedio por clase")
        plt.xticks(rotation=45)
        plt.show()
