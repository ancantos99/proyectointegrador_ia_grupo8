import os
import yaml
from collections import Counter
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
        class_counts = {split: Counter() for split in self.splits}

        for split in self.splits:
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

        all_counts = {class_id: sum(class_counts[s].get(class_id, 0) for s in self.splits)
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
        """Calcula y presenta el análisis descriptivo principal (global y por split)."""

        data = []
        for class_id in range(self.num_classes):
            data.append({
                'Class ID': class_id,
                'Class Name': self.class_names.get(class_id, 'N/A'),
                'Train': class_counts['train'].get(class_id, 0),
                'Val': class_counts['val'].get(class_id, 0),
                'Test': class_counts['test'].get(class_id, 0),
                'Total': sum(class_counts[s].get(class_id, 0) for s in self.splits)
            })

        df = pd.DataFrame(data)

        # Calcular Estadísticas Globales
        global_counts = df['Total'].values
        global_stats = self._calculate_stats(global_counts)

        # Calcular Estadísticas por Split
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

    # --- Funciones de Visualización ---
    def plot_class_distribution(self, df, column, title):
        """Genera un gráfico de barras para la distribución de clases (Total o por Split)."""

        if df.empty:
            print(f"No hay datos para graficar la distribución de clases en {title}.")
            return

        plt.figure(figsize=(12, 6))

        # Solución a la advertencia de Seaborn
        sns.barplot(
            x='Class Name',
            y=column,
            data=df,
            palette='viridis',
            hue='Class Name',
            legend=False
        )

        plt.title(title, fontsize=16)
        plt.xlabel("Clase de Objeto", fontsize=12)
        plt.ylabel(f"Número de Instancias ({column})", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def plot_split_counts(self, class_counts):
        """Genera un gráfico de barras para mostrar el número total de objetos por split."""

        counts = {split: sum(class_counts[split].values()) for split in self.splits}
        df_split = pd.DataFrame(list(counts.items()), columns=['Split', 'Total_Objects'])

        plt.figure(figsize=(8, 5))
        ax = sns.barplot(
            x='Split',
            y='Total_Objects',
            data=df_split,
            palette=['#4c72b0', '#55a868', '#c44e52'],
            hue='Split',
            legend=False
        )

        for p in ax.patches:
            ax.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=10, color='black', xytext=(0, 5),
                        textcoords='offset points')

        plt.title("Distribución de Objetos por Subconjunto (Train, Val, Test)", fontsize=14)
        plt.xlabel("Subconjunto del Dataset", fontsize=12)
        plt.ylabel("Número Total de Instancias (Bounding Boxes)", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    # --- Manejo del Desbalance (MODIFICADO para enfocarse en 'Train') ---
    def check_imbalance(self, df_counts, title_suffix):
        """Verifica y reporta el ratio de desbalance, enfocado en el conjunto TRAIN."""

        print("\n" + "=" * 80)
        print(f"Observación clave sobre el desbalance en **TRAIN** {title_suffix}:")

        # 1. Usar solo la columna 'Train'
        df_train = df_counts[['Class Name', 'Train']].rename(columns={'Train': 'Count'})

        # 2. Identificar clases con 0 instancias en TRAIN
        zero_counts = df_train[df_train['Count'] == 0]['Class Name'].tolist()

        if zero_counts:
            print(f"⚠️ **Clases No Representadas en TRAIN (0 instancias)**: {', '.join(zero_counts)}")

            # 3. Filtrar para calcular el ratio solo con las clases que sí tienen instancias en TRAIN
            df_filtered = df_train[df_train['Count'] > 0]

            if df_filtered.empty:
                print(
                    "No hay instancias en ninguna clase en TRAIN (el conjunto de entrenamiento está vacío o solo tiene clases con 0 instancias).")
                print("=" * 80)
                return
        else:
            df_filtered = df_train
            print("✅ Todas las clases están representadas en TRAIN (Min > 0).")

        min_count = df_filtered['Count'].min()
        max_count = df_filtered['Count'].max()

        if min_count > 0:
            ratio = max_count / min_count
            max_class = df_filtered[df_filtered['Count'] == max_count]['Class Name'].iloc[0]
            min_class = df_filtered[df_filtered['Count'] == min_count]['Class Name'].iloc[0]

            print(
                f"La clase más frecuente (**{max_class}** con {max_count:,} instancias) tiene **{ratio:,.2f}** veces más instancias que la menos frecuente (**{min_class}** con {min_count:,} instancias) en TRAIN.")

            if ratio > 5:
                print(
                    "🚨 **Desbalance SIGNIFICATIVO**: Se requiere aplicar técnicas robustas de balanceo (*oversampling*, *pérdida ponderada* o *Data Augmentation* avanzada).")
            elif ratio > 2:
                print(
                    "⚠️ **Desbalance Moderado**: Se recomienda considerar técnicas de balanceo para mejorar la robustez del modelo en las clases minoritarias.")
            else:
                print("✅ Distribución de Clases relativamente EQUILIBRADA entre las clases representadas en TRAIN.")
        else:
            print(
                "No se puede calcular el ratio de desbalance (error de filtrado o todas las clases restantes tienen 0 instancias en TRAIN).")
        print("=" * 80)

    # --- Ejecución del Análisis ---
    def run_analysis(self, title_suffix="(Original)"):
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
        self.plot_class_distribution(df_counts, 'Total', f"Distribución de Clases (Total) {title_suffix}")

        # 6. Gráfico: Distribución de Objetos por Subconjunto
        self.plot_split_counts(class_counts)

        # 7. Gráficos: Distribución de Clases por Subconjunto
        for split in self.splits:
            self.plot_class_distribution(df_counts, split.capitalize(),
                                         f"Distribución de Clases ({split.upper()}) {title_suffix}")

        # 8. Evaluación del Desbalance (AHORA SOLO EN TRAIN)
        self.check_imbalance(df_counts, title_suffix)