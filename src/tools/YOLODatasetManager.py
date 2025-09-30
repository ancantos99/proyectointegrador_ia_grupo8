import os
import yaml
import matplotlib.pyplot as plt
from collections import Counter
import shutil
import logging
from tqdm import tqdm

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
        #self.class_names = [data_cfg['names'][i] for i in range(len(data_cfg['names']))]
        self.class_names = {int(k): v for k, v in data_cfg['names'].items()}
        # Guardar cambios en el Yaml
        with open(self.ruta_yaml, "w") as f:
            yaml.dump(data_cfg, f, default_flow_style=False)
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger por clase
        self.logger.propagate = True

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
            if self.splitconsultar != "train_balanced":
                if splitconsultar not in self.splits: raise ValueError(f"Split '{splitconsultar}' no válido. Usa {self.splits}")
            self._read_labels_from_split(splitconsultar)
        # Crear dict completo con todas las clases
        full_counts = {str(i): self.classes_counter.get(str(i), 0) for i in range(len(self.class_names))}
        return full_counts

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
        #indices = list(range(len(self.class_names)))
        indices = sorted(self.class_names.keys())
        values = [counts.get(str(i), 0) for i in indices]
        labels = [f"{i}:{self.class_names[i]}" for i in indices]

        plt.figure(figsize=(12, 6))
        plt.bar(labels, values, color="skyblue")
        plt.xlabel("Clases")
        plt.ylabel("Frecuencia")
        plt.title(f"Distribución de Clases en el Dataset [{self.splitconsultar}]")
        plt.xticks(rotation=45)
        plt.show()

    def eliminar_clases_yaml(self, clases_a_eliminar):
        """
        Elimina clases del dataset.yaml sin modificar los IDs de las otras clases.
        Parámetros:
            ruta_yaml (str): Ruta al archivo dataset.yaml.
            clases_a_eliminar (list): Lista de IDs (int) de clases a eliminar.
        """
        # Leer YAML
        with open(self.ruta_yaml, "r") as f:
            data_cfg = yaml.safe_load(f)
        # Filtrar las clases
        data_cfg['names'] = {k: v for k, v in data_cfg['names'].items() if int(k) not in clases_a_eliminar}
        # Actualizar número de clases (opcional, útil para YOLO)
        data_cfg['nc'] = len(data_cfg['names'])
        # Guardar YAML modificado
        with open(self.ruta_yaml, "w") as f:
            yaml.dump(data_cfg, f, default_flow_style=False)
        print(f"Clases {clases_a_eliminar} eliminadas correctamente de {self.ruta_yaml}.")

    def aplicar_sobremuestreo(self, split = "train", cantidad_seleccion_minoritaria=500):
        # Contar instancias por clase
        counts = self.compute_class_distribution(splitconsultar=split)
        self.logger.info(f"Distribución original: {counts}")
        # Carpeta balanceada
        ruta_balanceada = os.path.join(self.ruta_raiz_dataset, split + "_balanced")
        os.makedirs(os.path.join(ruta_balanceada, "images"), exist_ok=True)
        os.makedirs(os.path.join(ruta_balanceada, "labels"), exist_ok=True)
        # Copiar todas las imágenes primero
        img_dir = os.path.join(self.ruta_raiz_dataset, split, "images")
        lbl_dir = os.path.join(self.ruta_raiz_dataset, split, "labels")
        for img_file in os.listdir(img_dir):
            shutil.copy(os.path.join(img_dir, img_file),os.path.join(ruta_balanceada, "images", img_file))
            lbl_file = img_file.rsplit(".", 1)[0] + ".txt"
            shutil.copy(os.path.join(lbl_dir, lbl_file),os.path.join(ruta_balanceada, "labels", lbl_file))
        # Sobremuestreo: duplicar imágenes de clases minoritarias
        max_count = max(counts.values()) #clase dominante
        # Sobremuestreo por clase
        for clase, count in counts.items():
            if count == 0 or count == max_count:
                continue  # ignorar clase dominante o sin datos
            if count  > cantidad_seleccion_minoritaria: #Seleccionar clases minoritarias
                continue #Saltar al Siguiente, solo pasan los que tienen más de la cantidad_seleccion_minoritaria
            # Factor de duplicación
            factor = (max_count // count) - 1  # cuántas veces duplicar cada imagen
            # Listar imágenes que contienen la clase
            imgs_clase = []
            for lbl_file in os.listdir(lbl_dir):
                lbl_path = os.path.join(lbl_dir, lbl_file)
                if not os.path.isfile(lbl_path):
                    continue
                with open(lbl_path, "r") as f:
                    lineas = f.readlines()
                    clases_en_img = [line.strip().split()[0] for line in lineas]
                    if clase in clases_en_img:
                        imgs_clase.append(lbl_file.rsplit(".", 1)[0])

            for base_name  in tqdm(imgs_clase, desc=f"Dup clase {clase}", leave=False):
                img_file = base_name + ".png"
                lbl_file = base_name + ".txt"
                img_path = os.path.join(img_dir, img_file)
                lbl_path = os.path.join(lbl_dir, lbl_file)
                if not os.path.exists(os.path.join(lbl_dir, lbl_file)):
                    continue  # saltar si no existe etiqueta

                for i in range(factor):
                    new_img = base_name + f"_dup{i}.png"
                    shutil.copy(img_path, os.path.join(ruta_balanceada, "images", new_img))
                    shutil.copy(lbl_path, os.path.join(ruta_balanceada, "labels", new_img.replace(".png", ".txt")))

        self.logger.info(f"Dataset balanceado con SobreMuestreo y guardado en: {ruta_balanceada}")

