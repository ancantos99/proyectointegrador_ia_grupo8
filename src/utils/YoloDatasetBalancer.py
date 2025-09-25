import os
import glob
import shutil
import random
from collections import Counter, defaultdict
from sklearn.base import BaseEstimator, TransformerMixin
import logging

class YoloDatasetBalancer(BaseEstimator, TransformerMixin):
    def __init__(self,
                 input_path,
                 output_path,
                 oversample=True,
                 undersample=True,
                 split="train",
                 undersample_factor=2):
        """
        input_path: ruta del dataset original
        output_path: ruta del dataset balanceado
        oversample: aplicar oversampling a clases minoritarias
        undersample: aplicar undersampling a clases mayoritarias
        split: conjunto a balancear (train, val o test)
        undersample_factor: clase mayoritaria se reduce a min_count * factor
        """
        self.input_path = input_path
        self.output_path = output_path
        self.oversample = oversample
        self.undersample = undersample
        self.split = split
        self.undersample_factor = undersample_factor
        self.class_counts_ = Counter()
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger por clase
        self.logger.propagate = True
        self.logger.info(f"Se ha configurado un YoloDatasetBalancer con repo_path={self.input_path} \n"
                         f"output_path={self.output_path} y \n"
                         f"oversample={self.oversample} y \n"
                         f"undersample={self.undersample}"
                         f"split={self.split} y \n"
                         f"undersample_factor={self.undersample_factor} y \n")

    def fit(self, X=None, y=None):
        """
        Calcula distribución de clases en el split definido.
        """
        labels_path = os.path.join(self.input_path, self.split, "labels")
        label_files = glob.glob(os.path.join(labels_path, "*.txt"))
        class_counts = Counter()

        for file in label_files:
            with open(file, "r") as f:
                for line in f:
                    class_id = int(line.strip().split()[0])
                    class_counts[class_id] += 1

        self.class_counts_ = class_counts
        self.logger.info(f"Distribución inicial de clases: {dict(class_counts)}")
        self.logger.info("Fit YoloDatasetBalancer completado")
        return self

    def transform(self, X=None):
        """
        Copia el dataset y aplica balanceo en el split definido.
        """
        # 1. Copiar dataset completo
        #print("📂 Copiando dataset original...")
        self.logger.info("Copiando dataset original...")
        for s in ["train"]: #, "val", "test"]: #Solo copio la carpeta Train
            for folder in ["images", "labels"]:
                os.makedirs(os.path.join(self.output_path, s, folder), exist_ok=True)
                src = os.path.join(self.input_path, s, folder)
                dst = os.path.join(self.output_path, s, folder)
                for file in glob.glob(os.path.join(src, "*")):
                    shutil.copy(file, dst)

        # 2. Solo balanceamos el split elegido
        labels_path = os.path.join(self.output_path, self.split, "labels")
        images_path = os.path.join(self.output_path, self.split, "images")

        image_to_classes = defaultdict(set)
        label_files = glob.glob(os.path.join(labels_path, "*.txt"))

        for file in label_files:
            img_name = os.path.splitext(os.path.basename(file))[0]
            with open(file, "r") as f:
                for line in f:
                    class_id = int(line.strip().split()[0])
                    image_to_classes[img_name].add(class_id)

        max_count = max(self.class_counts_.values())
        min_count = min(self.class_counts_.values())

        # 3. Oversampling
        if self.oversample:
            #print("\n🔼 Aplicando oversampling...")
            self.logger.info("Aplicando oversampling...")
            for img_name, classes in image_to_classes.items():
                for cls in classes:
                    if self.class_counts_[cls] < max_count:
                        deficit = max_count - self.class_counts_[cls]
                        img_file = os.path.join(images_path, img_name + ".jpg")
                        if not os.path.exists(img_file):
                            img_file = os.path.join(images_path, img_name + ".png")
                        label_file = os.path.join(labels_path, img_name + ".txt")

                        if os.path.exists(img_file) and os.path.exists(label_file):
                            for i in range(deficit // len(classes)):
                                new_img = os.path.join(images_path, f"{img_name}_dup{i}.jpg")
                                new_label = os.path.join(labels_path, f"{img_name}_dup{i}.txt")
                                shutil.copy(img_file, new_img)
                                shutil.copy(label_file, new_label)
                        break

        # 4. Undersampling
        if self.undersample:
            #print("\n🔽 Aplicando undersampling...")
            self.logger.info("Aplicando undersampling...")
            majority_class = max(self.class_counts_, key=self.class_counts_.get)
            target_size = min_count * self.undersample_factor

            images_with_majority = [
                img for img, classes in image_to_classes.items() if majority_class in classes
            ]
            to_remove = random.sample(
                images_with_majority,
                max(0, len(images_with_majority) - target_size)
            )

            for img_name in to_remove:
                img_file = os.path.join(images_path, img_name + ".jpg")
                if not os.path.exists(img_file):
                    img_file = os.path.join(images_path, img_name + ".png")
                label_file = os.path.join(labels_path, img_name + ".txt")
                if os.path.exists(img_file): os.remove(img_file)
                if os.path.exists(label_file): os.remove(label_file)

        #print("\n✅ Dataset balanceado generado en:", self.output_path)
        self.logger.info(f"Dataset balanceado generado en: {self.output_path}")
        return self.output_path
