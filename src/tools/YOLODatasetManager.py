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
        self.splitconsultar = "Todos"
        self.ruta_yaml = "/content/dataset/dataset.yaml"
        # Carga y modificiaciones al yaml existente
        with open(self.ruta_yaml, "r") as f:
            data_cfg = yaml.safe_load(f)
        #Modificar la ruta raiz del dataset en el yaml
        data_cfg["path"] = self.ruta_raiz_dataset
        self.class_names = [data_cfg['names'][i] for i in range(len(data_cfg['names']))]
        # Guardar cambios en el Yaml
        with open(self.ruta_yaml, "w") as f:
            yaml.dump(data_cfg, f, default_flow_style=False)

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

    def compute_class_distribution(self, splitconsultar= None):
        """
        Calcula distribución de clases en train/val/test.
        """
        self.classes_counter.clear()
        if splitconsultar is None:
            # Recorre todos los splits
            self.splitconsultar = "Train, Val, Test"
            for split in self.splits:
                self._read_labels_from_split(split)
        else:
            self.splitconsultar = splitconsultar
            if splitconsultar not in self.splits: raise ValueError(f"Split '{splitconsultar}' no válido. Usa {self.splits}")
            self._read_labels_from_split(splitconsultar)
        return self.classes_counter

    def plot_distribution(self):
        """
        Genera gráfico de barras con la distribución de clases.
        class_names: lista opcional con los nombres de las clases
        """
        counts = dict(self.classes_counter)
        if not counts:
            print("Primero ejecute compute_class_distribution().")
            return

        # Garantizar orden por índice
        indices = list(range(len(self.class_names)))
        values = [counts.get(str(i), 0) for i in indices]
        labels = [f"{i}:{self.class_names[i]}" for i in indices]

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color="skyblue")
        plt.xlabel("Clases")
        plt.ylabel("Frecuencia")
        plt.title(f"Distribución de Clases en el Dataset [{self.splitconsultar}]")
        plt.xticks(rotation=45)
        plt.show()