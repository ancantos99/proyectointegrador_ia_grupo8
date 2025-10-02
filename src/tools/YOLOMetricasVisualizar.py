import pandas as pd
import matplotlib.pyplot as plt
import yaml
from ultralytics import YOLO
import numpy as np
import seaborn as sns
import os
from PIL import Image


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

    def gap_entretrainyval(self):
        train_box = self.df['train/box_loss']
        val_box = self.df['val/box_loss']
        train_cls = self.df['train/cls_loss']
        val_cls = self.df['val/cls_loss']
        train_dfl = self.df['train/dfl_loss']
        val_dfl = self.df['val/dfl_loss']

        # Gap
        gap_cls = val_cls - train_cls
        gap_dfl = val_dfl - train_dfl
        gap_box = val_box - train_box

        plt.figure(figsize=(10, 4))
        plt.plot(gap_cls, label='Gap Cls (val - train)')
        plt.plot(gap_dfl, label='Gap DFL (val - train)')
        plt.plot(gap_box, label='Gap Box (val - train)')
        plt.xlabel("Epoch")
        plt.ylabel("Gap")
        plt.legend()
        plt.grid(True)
        plt.title("Brecha por componente de pérdida")
        plt.show()

    def comparar_resultados(self, ruta_inicial, ruta_final, ruta_intermedia=None,
                            label_inicial="Prueba Inicial",
                            label_intermedia="Prueba Intermedia",
                            label_final="Prueba Final",
                            graficoamostrar="todos"):


        # ==============================
        # 1) Cargar resultados
        # ==============================
        prueba_inicial = pd.read_csv(ruta_inicial)
        prueba_final = pd.read_csv(ruta_final)
        prueba_intermedia = pd.read_csv(ruta_intermedia) if ruta_intermedia and os.path.exists(
            ruta_intermedia) else None

        # ==============================
        # Función auxiliar para graficar varias curvas
        # ==============================
        def plot_metric(metric, ylabel, title):
            plt.figure(figsize=(10, 6))
            plt.plot(prueba_inicial["epoch"], prueba_inicial[metric], label=label_inicial)
            if prueba_intermedia is not None:
                plt.plot(prueba_intermedia["epoch"], prueba_intermedia[metric], label=label_intermedia)
            plt.plot(prueba_final["epoch"], prueba_final[metric], label=label_final)
            plt.xlabel("Epoch")
            plt.ylabel(ylabel)
            plt.title(title)
            plt.legend()
            plt.show()

        # ==============================
        # 2) Curvas de pérdida (Box Loss)
        # ==============================
        if graficoamostrar=="boxloss" or graficoamostrar=="todos":
            plt.figure(figsize=(10, 6))
            plt.plot(prueba_inicial["epoch"], prueba_inicial["train/box_loss"], label=f"{label_inicial} - train_box")
            plt.plot(prueba_inicial["epoch"], prueba_inicial["val/box_loss"], label=f"{label_inicial} - val_box")

            if prueba_intermedia is not None:
                plt.plot(prueba_intermedia["epoch"], prueba_intermedia["train/box_loss"],
                         label=f"{label_intermedia} - train_box")
                plt.plot(prueba_intermedia["epoch"], prueba_intermedia["val/box_loss"],
                         label=f"{label_intermedia} - val_box")

            plt.plot(prueba_final["epoch"], prueba_final["train/box_loss"], label=f"{label_final} - train_box")
            plt.plot(prueba_final["epoch"], prueba_final["val/box_loss"], label=f"{label_final} - val_box")

            plt.xlabel("Epoch")
            plt.ylabel("Box Loss")
            plt.title("Comparación de Box Loss")
            plt.legend()
            plt.show()

        # ==============================
        # 3) mAP@[.5:.95]
        # ==============================
        if graficoamostrar == "map" or graficoamostrar == "todos":
            plot_metric("metrics/mAP50-95(B)", "mAP@[.5:.95]", "Comparación de mAP durante entrenamiento")

        # ==============================
        # 4) Precisión, Recall y mAP50
        # ==============================
        if graficoamostrar == "prmap" or graficoamostrar == "todos":
            fig, ax = plt.subplots(1, 3, figsize=(18, 5))

            # Precisión
            ax[0].plot(prueba_inicial["epoch"], prueba_inicial["metrics/precision(B)"], label=label_inicial)
            if prueba_intermedia is not None:
                ax[0].plot(prueba_intermedia["epoch"], prueba_intermedia["metrics/precision(B)"], label=label_intermedia)
            ax[0].plot(prueba_final["epoch"], prueba_final["metrics/precision(B)"], label=label_final)
            ax[0].set_title("Precisión")
            ax[0].set_xlabel("Epoch");
            ax[0].set_ylabel("Precision");
            ax[0].legend()

            # Recall
            ax[1].plot(prueba_inicial["epoch"], prueba_inicial["metrics/recall(B)"], label=label_inicial)
            if prueba_intermedia is not None:
                ax[1].plot(prueba_intermedia["epoch"], prueba_intermedia["metrics/recall(B)"], label=label_intermedia)
            ax[1].plot(prueba_final["epoch"], prueba_final["metrics/recall(B)"], label=label_final)
            ax[1].set_title("Recall")
            ax[1].set_xlabel("Epoch");
            ax[1].set_ylabel("Recall");
            ax[1].legend()

            # mAP50
            ax[2].plot(prueba_inicial["epoch"], prueba_inicial["metrics/mAP50(B)"], label=label_inicial)
            if prueba_intermedia is not None:
                ax[2].plot(prueba_intermedia["epoch"], prueba_intermedia["metrics/mAP50(B)"], label=label_intermedia)
            ax[2].plot(prueba_final["epoch"], prueba_final["metrics/mAP50(B)"], label=label_final)
            ax[2].set_title("mAP50")
            ax[2].set_xlabel("Epoch");
            ax[2].set_ylabel("mAP50");
            ax[2].legend()
            plt.suptitle("Comparación de Precisión, Recall y mAP50", fontsize=14)
            plt.show()

        if graficoamostrar == "barras" or graficoamostrar == "todos":
            # ==============================
            # 5) Gráfico final comparativo (barras)
            # ==============================
            final_inicial = prueba_inicial.iloc[-1]
            final_final = prueba_final.iloc[-1]
            final_intermedia = prueba_intermedia.iloc[-1] if prueba_intermedia is not None else None

            metrics = ["metrics/mAP50-95(B)", "metrics/mAP50(B)", "metrics/precision(B)", "metrics/recall(B)"]
            labels = ["mAP@[.5:.95]", "mAP50", "Precision", "Recall"]

            values_inicial = [final_inicial[m] for m in metrics]
            values_final = [final_final[m] for m in metrics]
            values_intermedia = [final_intermedia[m] for m in metrics] if final_intermedia is not None else None

            x = range(len(metrics))
            plt.figure(figsize=(10, 6))
            plt.bar([i - 0.25 for i in x], values_inicial, width=0.25, label=label_inicial)
            if values_intermedia is not None:
                plt.bar([i for i in x], values_intermedia, width=0.25, label=label_intermedia)
                plt.bar([i + 0.25 for i in x], values_final, width=0.25, label=label_final)
            else:
                plt.bar([i for i in x], values_final, width=0.25, label=label_final)

            plt.xticks(x, labels)
            plt.ylabel("Valor")
            plt.title("Comparación de métricas finales")
            plt.legend()
            plt.show()

        if graficoamostrar == "gap" or graficoamostrar == "todos":
            # ==============================
            # 6) GAP entre train y val en Box Loss
            # ==============================
            def plot_boxloss_gap(prueba, label):
                gap = prueba["val/box_loss"] - prueba["train/box_loss"]
                plt.plot(prueba["epoch"], gap, label=label)

            plt.figure(figsize=(10, 6))
            plot_boxloss_gap(prueba_inicial, label_inicial)
            if prueba_intermedia is not None:
                plot_boxloss_gap(prueba_intermedia, label_intermedia)
            plot_boxloss_gap(prueba_final, label_final)

            plt.axhline(0, color="gray", linestyle="--")
            plt.xlabel("Epoch")
            plt.ylabel("Gap (Train - Val) Box Loss")
            plt.title("Comparación de GAP en Box Loss")
            plt.legend()
            plt.show()