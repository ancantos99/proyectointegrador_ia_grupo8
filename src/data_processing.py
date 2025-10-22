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


    # --- Función para contar las etiquetas ---
    def count_class_distribution(self, title_suffix=""):
        """Cuenta las instancias de cada clase en los splits train, val y test."""
        splits = ['train', 'val', 'test']
        class_counts = {split: Counter() for split in splits}

        for split in splits:
            labels_dir = os.path.join(self.dataset_path, split, 'labels')
            if not os.path.exists(labels_dir):
                print(f"Advertencia: Directorio de etiquetas no encontrado: {labels_dir}")
                continue

            for label_file in os.listdir(labels_dir):
                if label_file.endswith('.txt'):
                    with open(os.path.join(labels_dir, label_file), 'r') as f:
                        for line in f:
                            if len(line.strip()) > 0:
                                try:
                                    class_id = int(line.strip().split()[0])
                                    class_counts[split][class_id] += 1
                                except ValueError:
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

    # --- Función para el Análisis Estadístico Descriptivo (MODIFICADA) ---
    def get_descriptive_stats(self, class_counts):
        """Calcula y presenta el análisis descriptivo principal (global y por split)."""

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

        # 2. Calcular Estadísticas Globales (sobre la columna 'Total')
        global_counts = df['Total'].values
        global_stats = self._calculate_stats(global_counts)

        # 3. Calcular Estadísticas por Split (sobre las columnas 'Train', 'Val', 'Test')
        split_stats = {}
        for split in ['Train', 'Val', 'Test']:
            split_stats[split] = self._calculate_stats(df[split].values)

        return df, global_stats, split_stats

    def _calculate_stats(self, counts):
        """Función auxiliar para calcular MTC y MD."""
        if len(counts) > 0 and sum(counts) > 0:
            stats = {
                'Media (Mean)': np.mean(counts),
                'Mediana (Median)': np.median(counts),
                'Moda (Mode)': pd.Series(counts).mode().tolist(),
                'Desv. Estándar (Std Dev)': np.std(counts),
                'Rango (Range)': np.ptp(counts),
                'Mínimo (Min)': np.min(counts),
                'Máximo (Max)': np.max(counts)
            }
        else:
            stats = {}
        return stats

    def _print_stats(self, title, stats):
        """Imprime las estadísticas formateadas."""
        print(f"\n{title}:")
        print("=" * 60)
        if stats:
            for name, value in stats.items():
                if isinstance(value, list):
                    print(f"{name:<25}: {', '.join(map(str, value))}")
                else:
                    print(f"{name:<25}: {value:,.2f}")
        else:
            print("No hay datos para calcular estadísticas.")
        print("=" * 60)

    # --- Función para la Visualización (GRÁFICO DE BARRAS DE CLASES TOTALES) ---
    def plot_class_distribution(self, df, title="Distribución de Clases del Dataset YOLOv8 (Total)"):
        """Genera un gráfico de barras para visualizar la distribución de clases."""

        if df.empty:
            print("No hay datos para graficar.")
            return

        plt.figure(figsize=(12, 6))

        # Solución a la advertencia de Seaborn: asignar 'x' a 'hue' y legend=False
        sns.barplot(
            x='Class Name',
            y='Total',
            data=df,
            palette='viridis',
            hue='Class Name',
            legend=False
        )

        plt.title(title, fontsize=16)
        plt.xlabel("Clase de Objeto", fontsize=12)
        plt.ylabel("Número Total de Instancias (Bounding Boxes)", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    # --- Función para el nuevo gráfico de objetos por subconjunto ---
    def plot_split_counts(self, class_counts):
        """Genera un gráfico de barras para mostrar el número total de objetos por split."""

        splits = ['train', 'val', 'test']
        counts = {split: sum(class_counts[split].values()) for split in splits}
        df_split = pd.DataFrame(list(counts.items()), columns=['Split', 'Total_Objects'])

        plt.figure(figsize=(8, 5))
        sns.barplot(
            x='Split',
            y='Total_Objects',
            data=df_split,
            palette=['#4c72b0', '#55a868', '#c44e52'],  # Colores distintivos
            hue='Split',
            legend=False
        )

        # Añadir etiquetas de valor
        for index, row in df_split.iterrows():
            plt.text(row.name, row.Total_Objects, f'{row.Total_Objects:,}', color='black', ha="center", va='bottom')

        plt.title("Distribución de Objetos por Subconjunto (Train, Val, Test)", fontsize=14)
        plt.xlabel("Subconjunto del Dataset", fontsize=12)
        plt.ylabel("Número Total de Instancias (Bounding Boxes)", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    # --- Ejecución del Análisis ---
    def run_analysis(self, title_suffix=""):
        """Ejecuta todos los pasos del análisis descriptivo."""

        # 1. Conteo de Clases y Tabla de Distribución
        class_counts = self.count_class_distribution(title_suffix)

        # 2. Análisis Estadístico Descriptivo (Global y por Split)
        df_counts, global_stats, split_stats = self.get_descriptive_stats(class_counts)

        # 3. Imprimir Estadísticas Globales
        self._print_stats(f"Análisis Descriptivo de las Instancias de Clases (GLOBALES) {title_suffix}", global_stats)

        # 4. Imprimir Estadísticas por Subconjunto
        for split, stats in split_stats.items():
            self._print_stats(f"Análisis Descriptivo de las Instancias de Clases ({split})", stats)

        # 5. Visualización de Clases Totales
        self.plot_class_distribution(df_counts, title=f"Distribución de Clases (Total) {title_suffix}")

        # 6. Nuevo Gráfico: Distribución de Objetos por Subconjunto
        self.plot_split_counts(class_counts)

        # 7. Evaluación del Desbalance
        if 'Mínimo (Min)' in global_stats and global_stats['Mínimo (Min)'] > 0:
            ratio = global_stats['Máximo (Max)'] / global_stats['Mínimo (Min)']
            print("\nObservación clave sobre el desbalance:")
            print(
                f"La clase más frecuente tiene **{ratio:,.2f}** veces más instancias que la menos frecuente (Global).")
            if ratio > 5:
                print(
                    "⚠️ **Alerta**: Desbalance de Clases SIGNIFICATIVO. El modelo podría sesgarse hacia la clase mayoritaria.")
            elif ratio > 2:
                print(
                    "⚠️ **Advertencia**: Desbalance de Clases notable. Se recomienda considerar técnicas de balanceo (p. ej., *oversampling*).")
            else:
                print("✅ Distribución de Clases relativamente EQUILIBRADA.")
        else:
            print(
                "\nObservación clave sobre el desbalance: No se puede calcular el ratio de desbalance (posiblemente hay clases con 0 instancias).")