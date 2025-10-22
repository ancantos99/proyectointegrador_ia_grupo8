import os
import yaml
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Data_processing:
    """
    Clase para realizar el análisis de estadísticas descriptivas y EDA del dataset YOLOv8.
    """

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        yaml_path = os.path.join(dataset_path, "dataset.yaml")
        with open(yaml_path, 'r') as file:
            dataset_config = yaml.safe_load(file)
        self.class_names = dataset_config['names']
        self.num_classes = dataset_config['nc']
        self.splits = ['train', 'val', 'test']

    # --- Funciones Auxiliares de Lectura de Datos ---

    def _load_all_labels(self):
        """Carga todos los bounding boxes y metadatos de los splits train, val, test."""
        all_data = []
        objects_per_image = Counter()

        for split in self.splits:
            labels_dir = os.path.join(self.dataset_path, split, 'labels')
            if not os.path.exists(labels_dir): continue

            for label_file in os.listdir(labels_dir):
                if label_file.endswith('.txt'):
                    image_id = label_file.replace('.txt', '')
                    object_count = 0
                    with open(os.path.join(labels_dir, label_file), 'r') as f:
                        for line in f:
                            parts = line.strip().split()
                            if len(parts) == 5:
                                try:
                                    class_id = int(parts[0])
                                    # Formato YOLO: class_id x_center y_center width height (normalizados de 0 a 1)
                                    x_center, y_center, w, h = map(float, parts[1:])
                                    all_data.append({
                                        'split': split,
                                        'class_id': class_id,
                                        'class_name': self.class_names.get(class_id, 'N/A'),
                                        'x_center': x_center,
                                        'y_center': y_center,
                                        'width': w,
                                        'height': h,
                                        'area': w * h,  # Agregamos el área para un mejor análisis
                                        'aspect_ratio': w / h if h > 0 else 0
                                    })
                                    object_count += 1
                                except ValueError:
                                    continue
                    objects_per_image[f"{split}_{image_id}"] = object_count

        df_labels = pd.DataFrame(all_data)
        return df_labels, objects_per_image

    # --- Métodos de Estadística Descriptiva (existentes) ---

    def count_class_distribution(self, title_suffix=""):
        # ... (código de conteo existente, no se modifica)
        class_counts = {split: Counter() for split in self.splits}
        # Lógica de conteo...
        df_labels, _ = self._load_all_labels()
        for _, row in df_labels.iterrows():
            class_counts[row['split']][row['class_id']] += 1

        self._print_class_table(class_counts, title_suffix)
        return class_counts

    def _print_class_table(self, class_counts, title_suffix):
        # ... (código de impresión de tabla existente)
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

    def get_descriptive_stats(self, class_counts):
        # ... (código de estadísticas existente)
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

        global_stats = self._calculate_stats(df['Total'].values)

        split_stats = {}
        for split in ['Train', 'Val', 'Test']:
            split_stats[split] = self._calculate_stats(df[split].values)

        return df, global_stats, split_stats

    # ... (resto de funciones _calculate_stats, _print_stats, plot_class_distribution, plot_split_counts, check_imbalance existentes)

    # FUNCIONES DE ESTADÍSTICA DESCRIPTIVA Y VISUALIZACIÓN YA DEFINIDAS

    # --- Nuevas Funciones de EDA (Análisis Exploratorio de Datos) ---

    def plot_bbox_dimensions(self, df_labels):
        """Visualiza la distribución de ancho (width) y alto (height) de los bounding boxes."""

        # Filtrar valores atípicos (outliers) para una mejor visualización (ej. 99% de los datos)
        w_max = df_labels['width'].quantile(0.99)
        h_max = df_labels['height'].quantile(0.99)
        df_filtered = df_labels[(df_labels['width'] < w_max) & (df_labels['height'] < h_max)]

        print("\nAnálisis de Dimensiones de Bounding Boxes (EDA):")
        print(
            f"Nota: Se filtró el 1% superior de objetos por tamaño (W > {w_max:.4f}, H > {h_max:.4f}) para mejor visualización.")

        # 1. Gráfico de dispersión (Scatter Plot)
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x='width', y='height', data=df_filtered, hue='class_name', size='area', alpha=0.6,
                        sizes=(20, 200))
        plt.title('Distribución de Ancho vs. Alto de Bounding Boxes (Normalizado)', fontsize=16)
        plt.xlabel('Ancho Normalizado (W)', fontsize=12)
        plt.ylabel('Alto Normalizado (H)', fontsize=12)
        plt.legend(title='Clase', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

        # 2. Histograma 2D (Joint Plot)
        sns.jointplot(x='width', y='height', data=df_filtered, kind="hist", bins=50,
                      marginal_kws=dict(bins=50, fill=True))
        plt.suptitle('Densidad de Dimensiones de Bounding Boxes (W vs H)', y=1.02, fontsize=14)
        plt.show()

        # Interpretación
        print("\nInterpretación de Dimensiones:")
        print(
            "La agrupación de puntos en el gráfico de dispersión (Scatter Plot) indica los tamaños de objetos que predominan en tu dataset.")
        print(
            "Estos clusters se usan para determinar los **Anclajes (Anchors)** óptimos que debe usar el modelo YOLOv8 para una detección más precisa.")

    def plot_bbox_centers(self, df_labels):
        """Visualiza la distribución de las coordenadas centrales de los bounding boxes."""

        plt.figure(figsize=(8, 8))
        # 1. Histograma 2D (Heatmap) para mostrar la densidad de centros
        plt.hist2d(df_labels['x_center'], df_labels['y_center'], bins=50, cmap='inferno')
        plt.colorbar(label='Densidad de Bounding Boxes')
        plt.title('Distribución de Coordenadas Centrales (x, y)', fontsize=16)
        plt.xlabel('Coordenada X Central Normalizada', fontsize=12)
        plt.ylabel('Coordenada Y Central Normalizada', fontsize=12)

        # Añadir un punto central para referencia
        plt.plot(0.5, 0.5, 'w*', markersize=10, label='Centro de la Imagen')
        plt.legend()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

        print("\nInterpretación de Centros de Bounding Boxes:")
        print(
            "Muestra si los objetos tienden a aparecer en ciertas áreas de la interfaz web (p. ej., barras laterales o pie de página).")
        print(
            "Si la densidad se concentra en los bordes, puede justificar un *Data Augmentation* que simule recortes de pantalla.")

    def plot_objects_per_image(self, objects_per_image):
        """Visualiza la distribución del número de objetos por imagen."""

        if not objects_per_image:
            print("No hay datos de conteo de objetos por imagen.")
            return

        counts = np.array(list(objects_per_image.values()))

        # Filtrar el 99% superior para mejor visualización del histograma
        max_count = np.percentile(counts, 99)
        counts_filtered = counts[counts <= max_count]

        plt.figure(figsize=(10, 5))
        sns.histplot(counts_filtered, bins=30, kde=True, color='skyblue')
        plt.title('Distribución del Número de Objetos por Imagen (Máx. 99%)', fontsize=16)
        plt.xlabel('Número de Objetos por Imagen', fontsize=12)
        plt.ylabel('Frecuencia (Número de Imágenes)', fontsize=12)
        plt.axvline(np.mean(counts), color='red', linestyle='--', label=f'Media: {np.mean(counts):.2f}')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

        print("\nInterpretación de Objetos por Imagen:")
        print(f"Media de objetos por imagen: {np.mean(counts):.2f}")
        print(
            "La media y la forma del histograma (sesgo a la izquierda o derecha) indican si tu modelo debe ser rápido (pocas detecciones) o exhaustivo (muchas detecciones).")

    # --- Ejecución del Análisis (MODIFICADA) ---
    def run_analysis(self, title_suffix="(Original)"):
        """Ejecuta todos los pasos del análisis descriptivo y EDA."""

        # 1. Cargar todas las etiquetas y metadatos (necesario para EDA)
        df_labels, objects_per_image = self._load_all_labels()

        if df_labels.empty:
            print("Error: El dataset no contiene etiquetas válidas.")
            return

        # 2. Conteo de Clases y Tabla de Distribución
        class_counts = {s: Counter(df_labels[df_labels['split'] == s]['class_id']) for s in self.splits}
        self._print_class_table(class_counts, title_suffix)

        # 3. Análisis Estadístico Descriptivo (Global y por Split)
        df_counts, global_stats, split_stats = self.get_descriptive_stats(class_counts)

        # 4. Imprimir Estadísticas
        self._print_stats(f"Análisis Descriptivo de las Instancias de Clases (GLOBALES) {title_suffix}", global_stats)
        for split, stats in split_stats.items():
            self._print_stats(f"Análisis Descriptivo de las Instancias de Clases ({split})", stats)

        # 5. Visualizaciones de Distribución de Clases
        self.plot_class_distribution(df_counts, 'Total', f"Distribución de Clases (Total) {title_suffix}")
        self.plot_split_counts(class_counts)
        for split in self.splits:
            self.plot_class_distribution(df_counts, split.capitalize(),
                                         f"Distribución de Clases ({split.upper()}) {title_suffix}")

        # 6. Evaluación del Desbalance
        self.check_imbalance(df_counts, title_suffix)

        # 7. NUEVAS VISUALIZACIONES EDA
        print("\n" + "#" * 30 + " ANÁLISIS EXPLORATORIO DE DATOS (EDA) " + "#" * 30)
        self.plot_bbox_dimensions(df_labels)
        self.plot_bbox_centers(df_labels)
        self.plot_objects_per_image(objects_per_image)

    # FUNCIONES DE ESTADÍSTICA DESCRIPTIVA YA DEFINIDAS

    def _calculate_stats(self, counts):
        # ... (código existente)
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
        # ... (código existente)
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

    def plot_class_distribution(self, df, column, title):
        # ... (código existente)
        if df.empty:
            print(f"No hay datos para graficar la distribución de clases en {title}.")
            return

        plt.figure(figsize=(12, 6))

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
        # ... (código existente)
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

    def check_imbalance(self, df_counts, title_suffix):
        # ... (código existente)
        print("\n" + "=" * 80)
        print(f"Observación clave sobre el desbalance en **TRAIN** {title_suffix}:")

        df_train = df_counts[['Class Name', 'Train']].rename(columns={'Train': 'Count'})
        zero_counts = df_train[df_train['Count'] == 0]['Class Name'].tolist()

        if zero_counts:
            print(f"⚠️ **Clases No Representadas en TRAIN (0 instancias)**: {', '.join(zero_counts)}")
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