import os
import glob
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, repo_path, encoding_method="frequency", numeric_method="zscore", numeric_cols=None):
        self.repo_path = repo_path
        self.encoding_method = encoding_method
        self.numeric_method = numeric_method
        self.numeric_cols = numeric_cols if numeric_cols else ["area", "aspect_ratio", "center_dist"]
        self.df_ = None
        self.scalers = {}
    #3.1 Creación de Variables Derivadas
    #Extracción de características a partir de los labels YOLO (x, y, w, h, area, aspect_ratio, center_dist).
    def _extract_features(self):
        """Extrae features derivados de los labels YOLO"""
        features = []

        for subset in ["train", "val", "test"]:
            label_dir = os.path.join(self.repo_path, subset, "labels")
            if not os.path.exists(label_dir):
                continue

            for txt in glob.glob(os.path.join(label_dir, "*.txt")):
                with open(txt, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) != 5:
                            continue

                        cls, x, y, w, h = map(float, parts)
                        area = w * h
                        aspect_ratio = w / h if h > 0 else 0
                        center_dist = np.sqrt((x - 0.5) ** 2 + (y - 0.5) ** 2)

                        features.append({
                            "subset": subset,
                            "class": int(cls),
                            "x": x,
                            "y": y,
                            "w": w,
                            "h": h,
                            "area": area,
                            "aspect_ratio": aspect_ratio,
                            "center_dist": center_dist
                        })

        self.df_ = pd.DataFrame(features)
        return self

    #3.2 Encoding de Variables Categóricas
    #Codifica categorías (class) en distintos formatos (One-Hot, Label, Frequency).
    def _encode_categories(self, method="onehot"):
        if self.df_ is None:
            raise ValueError("Primero ejecuta _extract_features()")

        if method == "onehot":
            self.df_ = pd.get_dummies(self.df_, columns=["class"], prefix="cls")
        elif method == "frequency":
            freq = self.df_["class"].value_counts().to_dict()
            self.df_["class_freq"] = self.df_["class"].map(freq)
        elif method == "label":
            self.df_["class"] = self.df_["class"].astype("category").cat.codes
        return self

    ##3.3 Transformaciones de Variables Numéricas
    #Escala variables numéricas con Min-Max o Z-score.
    def _transform_numeric(self, cols, method="minmax"):
        if self.df_ is None:
            raise ValueError("Primero ejecuta _extract_features()")

        if method == "minmax":
            scaler = MinMaxScaler()
        elif method == "zscore":
            scaler = StandardScaler()
        else:
            raise ValueError("Método no soportado")

        self.df_[[c + "_" + method for c in cols]] = scaler.fit_transform(self.df_[cols])
        self.scalers[method] = scaler
        return self

    ##3.4 Feature Selection
    #Selecciona features relevantes con Random Forest.
    def feature_selection_rf(self, target_col="class", n_features=5):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.feature_selection import SelectFromModel

        X = self.df_.drop(columns=[target_col, "subset"], errors="ignore")
        y = self.df_[target_col]

        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)

        selector = SelectFromModel(rf, max_features=n_features, prefit=True)
        selected_features = X.columns[selector.get_support()].tolist()
        return selected_features

    def get_features(self):
        return self.df_

    # Obligatorio en sklearn
    def fit(self, X=None, y=None):
            # Extraer features de labels YOLO
        self._extract_features()
        # Encoding de categorías
        self._encode_categories(method=self.encoding_method)
        # Escalamiento de numéricas
        self._transform_numeric(cols=self.numeric_cols, method=self.numeric_method)
        return self

    # Obligatorio en sklearn
    def transform(self, X=None, y=None):
        return self.df_.copy()