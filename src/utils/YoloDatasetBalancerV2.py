import os
import glob
import random
from collections import Counter, defaultdict
from sklearn.base import BaseEstimator, TransformerMixin
import logging
import torch
from torch.utils.data import Sampler


class BalancedYoloSampler(Sampler):
    """
    Sampler balanceado para datasets YOLOv8.
    No copia ni borra archivos, solo ajusta los índices de muestreo.
    """
    def __init__(self, indices, labels, oversample=True, undersample=True, undersample_factor=2, logger=None):
        self.indices = indices
        self.labels = labels
        self.oversample = oversample
        self.undersample = undersample
        self.undersample_factor = undersample_factor
        self.logger = logger or logging.getLogger(self.__class__.__name__)

        # Contar ocurrencias por clase
        self.class_counts = Counter(labels)
        self.max_count = max(self.class_counts.values())
        self.min_count = min(self.class_counts.values())

        self.logger.info(f"Distribución inicial de clases en sampler: {dict(self.class_counts)}")
        self.logger.info(f"oversample={self.oversample}, undersample={self.undersample}, factor={self.undersample_factor}")

        # Generar lista balanceada de índices
        self.balanced_indices = self._balance_indices()
        self.logger.info(f"Sampler balanceado generado con {len(self.balanced_indices)} ejemplos")

    def _balance_indices(self):
        indices_by_class = defaultdict(list)
        for idx, cls in zip(self.indices, self.labels):
            indices_by_class[cls].append(idx)

        balanced = []

        # Oversampling
        if self.oversample:
            self.logger.info("Aplicando oversampling a clases minoritarias...")
            for cls, idxs in indices_by_class.items():
                deficit = self.max_count - len(idxs)
                if deficit > 0:
                    idxs = idxs + random.choices(idxs, k=deficit)
                balanced.extend(idxs)
        else:
            for idxs in indices_by_class.values():
                balanced.extend(idxs)

        # Undersampling
        if self.undersample:
            self.logger.info("Aplicando undersampling a clase mayoritaria...")
            majority_class = max(self.class_counts, key=self.class_counts.get)
            target_size = self.min_count * self.undersample_factor
            majority_idxs = [i for i in balanced if self.labels[self.indices.index(i)] == majority_class]

            if len(majority_idxs) > target_size:
                self.logger.info(f"Reduciendo clase {majority_class} de {len(majority_idxs)} a {target_size} ejemplos")
                majority_idxs = random.sample(majority_idxs, target_size)

            balanced = [i for i in balanced if self.labels[self.indices.index(i)] != majority_class]
            balanced.extend(majority_idxs)

        random.shuffle(balanced)
        return balanced

    def __iter__(self):
        return iter(self.balanced_indices)

    def __len__(self):
        return len(self.balanced_indices)


class YoloDatasetBalancer(BaseEstimator, TransformerMixin):
    def __init__(self, input_path, split="train", oversample=True, undersample=True, undersample_factor=2):
        self.input_path = input_path
        self.split = split
        self.oversample = oversample
        self.undersample = undersample
        self.undersample_factor = undersample_factor
        self.class_counts_ = Counter()
        self.labels_ = []
        self.indices_ = []
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.propagate = True

        self.logger.info(f"Se ha configurado un YoloDatasetBalancer con: \n"
                         f"input_path={self.input_path} \n"
                         f"split={self.split} \n"
                         f"oversample={self.oversample} \n"
                         f"undersample={self.undersample} \n"
                         f"undersample_factor={self.undersample_factor}")

    def fit(self, X=None, y=None):
        """
        Leer anotaciones y calcular distribución de clases.
        """
        labels_path = os.path.join(self.input_path, self.split, "labels")
        label_files = glob.glob(os.path.join(labels_path, "*.txt"))

        indices, labels = [], []
        idx = 0
        for file in label_files:
            with open(file, "r") as f:
                for line in f:
                    cls = int(line.strip().split()[0])
                    labels.append(cls)
                    indices.append(idx)
            idx += 1

        self.labels_ = labels
        self.indices_ = indices
        self.class_counts_ = Counter(labels)

        self.logger.info(f"Distribución inicial de clases: {dict(self.class_counts_)}")
        self.logger.info("Fit YoloDatasetBalancer completado")
        return self

    def transform(self, X=None):
        """
        Devuelve un sampler balanceado para usar en DataLoader.
        """
        self.logger.info("Generando sampler balanceado...")
        sampler = BalancedYoloSampler(
            indices=self.indices_,
            labels=self.labels_,
            oversample=self.oversample,
            undersample=self.undersample,
            undersample_factor=self.undersample_factor,
            logger=self.logger
        )
        self.logger.info("Sampler listo para entrenamiento")
        return sampler
