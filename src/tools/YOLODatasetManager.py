import os
import yaml
import matplotlib.pyplot as plt
from collections import Counter

class YOLODatasetManager:
    def __init__(self, ruta_raiz_dataset = "/content/dataset"):
        """
        root_path: ruta al dataset YOLOv8 que contiene train/, val/, test/
        """
        self.ruta_raiz_dataset = ruta_raiz_dataset
        self.splits = ["train", "val", "test"]
        self.classes_counter = Counter()

        self.ruta_yaml = "/content/dataset/dataset.yaml"
        # Cargar yaml existente
        with open(self.ruta_yaml, "r") as f:
            data_cfg = yaml.safe_load(f)
        # Modificar (ejemplo: cambiar número de clases y nombres)
        data_cfg["path"] = self.ruta_raiz_dataset

    def _read_labels_from_split(self, split):
        """
        Lee todas las anotaciones de un split y actualiza el contador de clases.
        """
        labels_dir = os.path.join(self.ruta_raiz_dataset, split, "labels")
        if not os.path.exists(labels_dir):
            return
        for file in os.listdir(labels_dir):
            if file.endswith(".txt"):
                with open(os.path.join(labels_dir, file), "r") as f:
                    for line in f:
                        class_id = line.strip().split()[0]  # primera columna es la clase
                        self.classes_counter[class_id] += 1

    def compute_class_distribution(self):
        """
        Calcula distribución de clases en train/val/test.
        """
        self.classes_counter.clear()
        for split in self.splits:
            self._read_labels_from_split(split)
        return self.classes_counter

    def plot_distribution(self, class_names=None):
        """
        Genera gráfico de barras con la distribución de clases.
        class_names: lista opcional con los nombres de las clases
        """
        counts = dict(self.classes_counter)
        if not counts:
            print("Primero ejecute compute_class_distribution().")
            return

        keys = list(counts.keys())
        values = list(counts.values())

        # Mapeo a nombres de clases si está disponible
        if class_names:
            keys = [class_names[int(k)] for k in keys]

        plt.figure(figsize=(10, 6))
        plt.bar(keys, values, color="skyblue")
        plt.xlabel("Clases")
        plt.ylabel("Frecuencia")
        plt.title("Distribución de Clases en el Dataset")
        plt.xticks(rotation=45)
        plt.show()
