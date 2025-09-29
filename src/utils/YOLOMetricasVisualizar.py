import pandas as pd
import matplotlib.pyplot as plt
from ultralytics import YOLO
import seaborn as sns
import numpy as np


class YOLOMetricasVisualizar:
    def __init__(self, csv_path: str, model_path: str = None, data_path: str = None):
        """
        Inicializa la clase cargando el CSV de resultados de YOLOv8.
        Opcional: cargar modelo para métricas por clase.

        Args:
            csv_path (str): Ruta al archivo results.csv de YOLOv8.
            model_path (str, optional): Ruta al modelo entrenado .pt.
            data_path (str, optional): Ruta al dataset de validación (para evaluación por clase).
        """
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

        # Calcular F1-score promedio
        self.df['F1'] = 2 * (self.df["metrics/precision(B)"] * self.df["metrics/recall(B)"]) / \
                        (self.df["metrics/precision(B)"] + self.df["metrics/recall(B)"])

        self.model_path = model_path
        self.data_path = data_path
        self.metrics_por_clase = None

        if model_path and data_path:
            self._calcular_metricas_por_clase()

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
        plt.plot(self.df["epoch"], self.df["F1"], label="F1-score")
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
        results = model.val(data=self.data_path, verbose=False)
        self.metrics_por_clase = results.box  # box contiene precision, recall, f1 y map por clase

    def print_metrics_por_clase(self):
        """Imprime Precision, Recall, F1, mAP50 por clase"""
        if self.metrics_por_clase is None:
            print("No se han calculado métricas por clase. Proporciona model_path y data_path.")
            return

        print("Métricas por clase:")
        for i, cls in enumerate(self.metrics_por_clase.cls_names):
            p = self.metrics_por_clase.pr[i]
            r = self.metrics_por_clase.re[i]
            f1 = self.metrics_por_clase.f1[i]
            map50 = self.metrics_por_clase.map50[i]
            print(f"{cls}: Precision={p:.3f}, Recall={r:.3f}, F1={f1:.3f}, mAP50={map50:.3f}")

    def plot_confusion_matrix(self):
        """Grafica confusion matrix por clase"""
        if self.metrics_por_clase is None:
            print("No se puede generar confusion matrix. Proporciona model_path y data_path.")
            return
        cm = self.metrics_por_clase.confusion_matrix  # confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title("Confusion Matrix por Clase")
        plt.show()

    def plot_iou_por_clase(self):
        """Grafica IoU promedio por clase"""
        if self.metrics_por_clase is None:
            print("No se puede generar IoU por clase. Proporciona model_path y data_path.")
            return
        iou_per_class = self.metrics_por_clase.iou  # array con IoU promedio por clase
        plt.figure(figsize=(10, 6))
        sns.barplot(x=self.metrics_por_clase.cls_names, y=iou_per_class)
        plt.ylabel("IoU promedio")
        plt.xlabel("Clase")
        plt.title("IoU promedio por clase")
        plt.xticks(rotation=45)
        plt.show()

    def print_recall_at_n(self, n=5):
        """
        Muestra Recall@N por clase (cuántos de los N objetos más confiables se detectaron correctamente)
        """
        if self.metrics_por_clase is None:
            print("No se puede generar Recall@N. Proporciona model_path y data_path.")
            return
        recall_at_n = self.metrics_por_clase.recall_at_n  # suponiendo que existe en la versión actual
        print(f"Recall@{n} por clase:")
        for i, cls in enumerate(self.metrics_por_clase.cls_names):
            print(f"{cls}: {recall_at_n[i]:.3f}")

