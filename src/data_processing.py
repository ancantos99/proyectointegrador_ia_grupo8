import os
import yaml
from collections import Counter, defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Data_processing:
    """
    Clase para realizar el análisis de estadísticas descriptivas del dataset YOLOv8.
    """

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        yaml_path = os.path.join(dataset_path, "dataset.yaml")
        with open(yaml_path, 'r') as file:
            dataset_config = yaml.safe_load(file)
        self.class_names = dataset_config['names']
        self.num_classes = dataset_config['nc']


    # --- Función para contar las etiquetas (basada en tu código) ---
    def count_class_distribution(self, title_suffix=""):
        """Cuenta las instancias de cada clase en los splits train, val y test."""
        splits = ['train', 'val', 'test']
        class_counts = {split: Counter() for split in splits}

        for split in splits:
            labels_dir = os.path.join(self.dataset_path, split, 'labels')
            # Verifica la existencia de las carpetas (importante para evitar errores)
            if not os.path.exists(labels_dir):
                print(f"Advertencia: Directorio de etiquetas no encontrado: {labels_dir}")
                continue

            for label_file in os.listdir(labels_dir):
                if label_file.endswith('.txt'):
                    with open(os.path.join(labels_dir, label_file), 'r') as f:
                        for line in f:
                            if len(line.strip()) > 0:
                                try:
                                    # La primera columna es el class_id
                                    class_id = int(line.strip().split()[0])
                                    class_counts[split][class_id] += 1
                                except ValueError:
                                    # Manejo de líneas vacías o mal formadas
                                    continue

        self._print_class_table(class_counts, title_suffix)
        return class_counts

    def _print_class_table(self, class_counts, title_suffix):
        """Imprime la tabla descriptiva de conteo de clases."""
        print(f"\nDistribución Detallada de Clases {title_suffix}:")
        print("=" * 80)
        print(f"{'ID':>4} {'Clase':<20} {'Train':>8} {'Val':>8} {'Test':>8} {'Total':>8} {'% Total':>8}")
        print("-" * 80)

        all_counts = {class_id: sum(class_counts[s].get(class_id, 0) for s in ['train', 'val', 'test'])
                      for class_id in range(self.num_classes)}
        grand_total = sum(all_counts.values())

        for class_id in range(self.num_classes):
            train_count = class_counts['train'].get(class_id, 0)
            val_count = class_counts['val'].get(class_id, 0)
            test_count = class_counts['test'].get(class_id, 0)
            total_count = all_counts[class_id]

            percentage = (total_count / grand_total) * 100 if grand_total > 0 else 0

            print(f"{class_id:>4} {self.class_names.get(class_id, 'N/A'):<20} "
                  f"{train_count:>8} {val_count:>8} {test_count:>8} "
                  f"{total_count:>8} {percentage:>8.2f}%")
        print("=" * 80)
        print(
            f"{'TOTAL INSTANCIAS':<25} {sum(class_counts['train'].values()):>8} {sum(class_counts['val'].values()):>8} {sum(class_counts['test'].values()):>8} {grand_total:>8} {'100.00%':>8}")

    # --- Función para el Análisis Estadístico Descriptivo ---
    def get_descriptive_stats(self, class_counts):
        """Calcula y presenta el análisis descriptivo principal."""

        # 1. Preparar los datos para un DataFrame
        data = []
        for class_id in range(self.num_classes):
            data.append({
                'Class ID': class_id,
                'Class Name': self.class_names.get(class_id, 'N/A'),
                'Train': class_counts['train'].get(class_id, 0),
                'Val': class_counts['val'].get(class_id, 0),
                'Test': class_counts['test'].get(class_id, 0),
                'Total': sum(class_counts[s].get(class_id, 0) for s in ['train', 'val', 'test'])
            })

        df = pd.DataFrame(data)

        # 2. Calcular Estadísticas (MTC y MD)
        all_counts = df['Total'].values

        if len(all_counts) > 0:
            stats = {
                'Media (Mean)': np.mean(all_counts),
                'Mediana (Median)': np.median(all_counts),
                'Moda (Mode)': df['Total'].mode().tolist(),
                'Desv. Estándar (Std Dev)': np.std(all_counts),
                'Rango (Range)': np.ptp(all_counts),
                'Mínimo (Min)': np.min(all_counts),
                'Máximo (Max)': np.max(all_counts)
            }
        else:
            stats = {}

        return df, stats

    # --- Función para la Visualización ---
    def plot_class_distribution(self, df, title="Distribución de Clases del Dataset YOLOv8"):
        """Genera un gráfico de barras para visualizar la distribución de clases."""

        if df.empty:
            print("No hay datos para graficar.")
            return

        plt.figure(figsize=(12, 6))
        sns.barplot(x='Class Name', y='Total', data=df, palette='viridis')
        plt.title(title, fontsize=16)
        plt.xlabel("Clase de Objeto", fontsize=12)
        plt.ylabel("Número Total de Instancias (Bounding Boxes)", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    # --- Ejecución del Análisis ---
    def run_analysis(self, title_suffix=""):
        """Ejecuta todos los pasos del análisis descriptivo."""

        # 1. Conteo de Clases
        class_counts = self.count_class_distribution(title_suffix)

        # 2. Análisis Estadístico Descriptivo
        df_counts, stats = self.get_descriptive_stats(class_counts)

        print("\nAnálisis Descriptivo de las Instancias de Clases (Totales):")
        print("=" * 60)
        for name, value in stats.items():
            if isinstance(value, list):
                print(f"{name:<25}: {', '.join(map(str, value))}")
            else:
                print(f"{name:<25}: {value:,.2f}")
        print("=" * 60)

        # 3. Visualización
        self.plot_class_distribution(df_counts,
                                     title=f"Distribución de Clases {title_suffix}")

        # 4. Evaluación del Desbalance
        print("\nObservación clave sobre el desbalance:")
        # Calcular el desbalance (ej. Ratio Max/Min)
        if len(df_counts) > 0 and df_counts['Total'].min() > 0:
            ratio = df_counts['Total'].max() / df_counts['Total'].min()
            print(f"La clase más frecuente tiene {ratio:,.2f} veces más instancias que la menos frecuente.")
            if ratio > 5:
                print(
                    "⚠️ **Alerta**: Este ratio indica un Desbalance de Clases SIGNIFICATIVO. Debe considerarse el uso de técnicas como *oversampling*, *undersampling* o pérdida ponderada.")
            elif ratio > 2:
                print(
                    "⚠️ **Advertencia**: Existe un Desbalance de Clases notable. Puede impactar el rendimiento del modelo en las clases minoritarias.")
            else:
                print("✅ Distribución de Clases relativamente EQUILIBRADA.")
        else:
            print("No se puede calcular el ratio de desbalance (posiblemente hay clases con 0 instancias).")