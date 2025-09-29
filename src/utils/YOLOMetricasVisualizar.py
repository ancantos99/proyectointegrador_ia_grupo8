import pandas as pd
import matplotlib.pyplot as plt


class YOLOMetricasVisualizar:
    def __init__(self, csv_path: str):
        """
        Inicializa la clase cargando el CSV de resultados de YOLOv8.

        Args:
            csv_path (str): Ruta al archivo results.csv de YOLOv8.
        """
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

        # Calcular F1-score
        self.df['F1'] = 2 * (self.df["metrics/precision(B)"] * self.df["metrics/recall(B)"]) / \
                        (self.df["metrics/precision(B)"] + self.df["metrics/recall(B)"])

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

