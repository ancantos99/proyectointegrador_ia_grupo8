import os
import yaml
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import shutil


class Data_processing:
    """
    Clase para realizar el análisis de estadísticas descriptivas y EDA del dataset YOLOv8,
    con funciones de ejecución separadas.
    """

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        yaml_path = os.path.join(dataset_path, "dataset.yaml")
        with open(yaml_path, 'r') as file:
            dataset_config = yaml.safe_load(file)
        self.class_names = dataset_config['names']
        self.num_classes = dataset_config['nc']
        self.splits = ['train', 'val', 'test']
        self.original_counts = {}  # Almacena los conteos de clases (e.g., {'train': Counter(...)})

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
                                        'area': w * h,
                                        # Evitar división por cero
                                        'aspect_ratio': w / h if h > 0 else 0
                                    })
                                    object_count += 1
                                except ValueError:
                                    continue
                    objects_per_image[f"{split}_{image_id}"] = object_count

        df_labels = pd.DataFrame(all_data)
        return df_labels, objects_per_image

    # --- Métodos de Estadística Descriptiva (Conteo y Tablas) ---

    def count_class_distribution(self, title_suffix=""):
        """Cuenta las instancias de cada clase en los splits train, val y test y las imprime."""
        df_labels, _ = self._load_all_labels()
        if df_labels.empty:
            print("Error: El dataset no contiene etiquetas válidas.")
            return None, None

        class_counts = {s: Counter(df_labels[df_labels['split'] == s]['class_id']) for s in self.splits}
        self._print_class_table(class_counts, title_suffix)

        # Almacenar los conteos en la instancia para su uso posterior (e.g., sobremuestreo)
        self.original_counts = class_counts

        return class_counts, df_labels

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

    # --- Métodos de Análisis Estadístico y Gráficos (existentes) ---

    def get_descriptive_stats(self, class_counts):
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

    def _calculate_stats(self, counts):
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

    # --- Funciones de EDA (Análisis Exploratorio de Datos) ---

    def plot_bbox_dimensions(self, df_labels):
        """Visualiza la distribución de ancho (width) y alto (height) de los bounding boxes."""

        w_max = df_labels['width'].quantile(0.99)
        h_max = df_labels['height'].quantile(0.99)
        df_filtered = df_labels[(df_labels['width'] < w_max) & (df_labels['height'] < h_max)]

        print("\nAnálisis de Dimensiones de Bounding Boxes (EDA):")
        print(
            f"Nota: Se filtró el 1% superior de objetos por tamaño (W > {w_max:.4f}, H > {h_max:.4f}) para mejor visualización.")

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

        sns.jointplot(x='width', y='height', data=df_filtered, kind="hist", bins=50,
                      marginal_kws=dict(bins=50, fill=True))
        plt.suptitle('Densidad de Dimensiones de Bounding Boxes (W vs H)', y=1.02, fontsize=14)
        plt.show()

        print(
            "La agrupación de puntos en el Scatter Plot indica los tamaños de objetos que predominan y ayuda a optimizar los **Anclajes (Anchors)** del modelo YOLOv8.")

    def plot_bbox_centers(self, df_labels):
        """Visualiza la distribución de las coordenadas centrales de los bounding boxes."""

        plt.figure(figsize=(8, 8))
        plt.hist2d(df_labels['x_center'], df_labels['y_center'], bins=50, cmap='inferno')
        plt.colorbar(label='Densidad de Bounding Boxes')
        plt.title('Distribución de Coordenadas Centrales (x, y)', fontsize=16)
        plt.xlabel('Coordenada X Central Normalizada', fontsize=12)
        plt.ylabel('Coordenada Y Central Normalizada', fontsize=12)

        plt.plot(0.5, 0.5, 'w*', markersize=10, label='Centro de la Imagen')
        plt.legend()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

        print(
            "Este mapa de calor muestra si los objetos están sesgados a ciertas áreas de la pantalla, lo cual es común en interfaces web.")

    def plot_objects_per_image(self, objects_per_image):
        """Visualiza la distribución del número de objetos por imagen."""

        if not objects_per_image:
            print("No hay datos de conteo de objetos por imagen.")
            return

        counts = np.array(list(objects_per_image.values()))

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

        print(
            f"Media de objetos por imagen: {np.mean(counts):.2f}. Esto define si el modelo debe ser optimizado para pocas o muchas detecciones por pantalla.")

    def plot_aspect_ratio_distribution(self, df_labels):
        """
        Visualiza la distribución de la relación de aspecto (ancho/alto) de los bounding boxes.
        Se filtra para evitar valores extremos y asegurar la legibilidad.
        """
        # Filtrar valores extremos de aspect_ratio (ej. entre 0.1 y 10) para un mejor rango de visualización
        # También se excluyen los casos donde h=0 y aspect_ratio=0
        df_filtered_ar = df_labels[(df_labels['aspect_ratio'] > 0.05) & (df_labels['aspect_ratio'] < 20)]

        if df_filtered_ar.empty:
            print("No hay datos de relación de aspecto válidos para graficar.")
            return

        plt.figure(figsize=(10, 6))
        sns.histplot(df_filtered_ar['aspect_ratio'], bins=50, kde=True, color='orange')

        # Añadir líneas verticales para ratios comunes
        plt.axvline(1.0, color='red', linestyle='--', label='Ratio 1:1 (Cuadrado)')
        plt.axvline(0.5, color='green', linestyle=':', label='Ratio 1:2 (Alto y Delgado)')
        plt.axvline(2.0, color='blue', linestyle=':', label='Ratio 2:1 (Ancho y Bajo)')

        plt.title('Distribución de la Relación de Aspecto (Ancho/Alto)', fontsize=16)
        plt.xlabel('Relación de Aspecto (Ancho / Alto)', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xscale('log')  # Escala logarítmica para ver mejor los picos y las colas
        plt.xticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20], ['0.1', '0.2', '0.5', '1', '2', '5', '10', '20'])
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

        print("\nInterpretación de la Relación de Aspecto:")
        print("Los picos en este histograma indican las formas más comunes de los objetos (cuadrados, anchos, altos).")
        print(
            "Esta información es vital para la selección o ajuste de los **anclajes (anchor boxes)** de tu modelo YOLOv8, asegurando que los anclajes predefinidos coincidan con las formas reales de los objetos en tus interfaces.")

    # --- Métodos de Ejecución Separados ---

    def run_analysis_descriptive(self, title_suffix="(Original)"):
        """Ejecuta el análisis descriptivo y visualización de la distribución de clases."""

        print("\n" + "#" * 20 + " ANÁLISIS DESCRIPTIVO DE DISTRIBUCIÓN DE CLASES " + "#" * 20)

        result = self.count_class_distribution(title_suffix)
        if result is None:
            return None
        class_counts, df_labels = result  # df_labels es devuelto para el EDA

        df_counts, global_stats, split_stats = self.get_descriptive_stats(class_counts)

        self._print_stats(f"Análisis Descriptivo de las Instancias de Clases (GLOBALES) {title_suffix}", global_stats)
        for split, stats in split_stats.items():
            self._print_stats(f"Análisis Descriptivo de las Instancias de Clases ({split.upper()})", stats)

        self.plot_class_distribution(df_counts, 'Total', f"Distribución de Clases (TOTAL) {title_suffix}")
        self.plot_split_counts(class_counts)
        for split in self.splits:
            self.plot_class_distribution(df_counts, split.capitalize(),
                                         f"Distribución de Clases ({split.upper()}) {title_suffix}")

        self.check_imbalance(df_counts, title_suffix)

        return df_labels  # Devolvemos df_labels para que pueda ser reutilizado por EDA

    def run_analysis_eda(self):
        """Ejecuta el Análisis Exploratorio de Datos (EDA) de los bounding boxes."""

        # Cargamos los datos para EDA (si no se han cargado ya)
        df_labels, objects_per_image = self._load_all_labels()

        if df_labels.empty:
            print("\nError: No se pueden realizar visualizaciones EDA. El dataset no contiene etiquetas válidas.")
            return

        print("\n" + "#" * 35 + " ANÁLISIS EXPLORATORIO DE DATOS (EDA) " + "#" * 35)

        self.plot_bbox_dimensions(df_labels)
        self.plot_bbox_centers(df_labels)
        self.plot_aspect_ratio_distribution(df_labels)  # <-- NUEVO GRÁFICO
        self.plot_objects_per_image(objects_per_image)

    # --- NUEVO MÉTODO DE MANEJO DE DESBALANCE ---
    def oversample_rare_classes(self, count_threshold=100, duplication_factor=10, target_class_id=None):
        """
        Realiza un sobremuestreo AGRESIVO (duplicación simple de imágenes) para clases raras
        en el split de entrenamiento, copiando los archivos de imagen y etiqueta.

        Si se especifica target_class_id, solo se sobremuestrea esa clase (si es rara).
        Si no se especifica, sobremuestrea todas las clases raras por debajo del umbral.

        Parámetros:
            count_threshold (int): El umbral por debajo del cual una clase se considera 'rara'.
            duplication_factor (int): Número de veces que se duplica cada imagen que contiene la clase(s) objetivo.
            target_class_id (int, opcional): ID de una clase específica a sobremuestrear.
        """
        if not self.original_counts or 'train' not in self.original_counts:
            print("ERROR: Primero debe ejecutar run_analysis_descriptive() o solo count_class_distribution() para calcular los conteos de clases.")
            return

        print(f" Iniciando sobremuestreo AGRESIVO con factor_duplicacion={duplication_factor}...")

        train_images_path = os.path.join(self.dataset_path, 'train', 'images')
        train_labels_path = os.path.join(self.dataset_path, 'train', 'labels')

        # 1. Determinar las clases a sobremuestrear
        if target_class_id is not None:
            # Opción 1: Sobremuestrear una clase específica
            target_count = self.original_counts['train'].get(target_class_id, 0)
            if target_count > 0 and target_count < count_threshold:
                rare_classes = {target_class_id}
                print(
                    f"Modo: Sobremuestreo enfocado en la Clase {target_class_id} ({self.class_names.get(target_class_id, 'N/A')}).")
            else:
                print(
                    f"ADVERTENCIA: La clase {target_class_id} ({self.class_names.get(target_class_id, 'N/A')}) no es rara (Conteo: {target_count}) o no existe. No se realizará sobremuestreo.")
                return
        else:
            # Opción 2: Sobremuestrear todas las clases raras
            rare_classes = {cid for cid, count in self.original_counts['train'].items() if
                            count > 0 and count < count_threshold}
            if not rare_classes:
                print(" No se encontraron clases raras por debajo del umbral.")
                return
            print(f"Modo: Sobremuestreo de TODAS las clases raras (conteo original < {count_threshold}):")

        # Imprimir las clases que serán sobremuestreadas
        for cid in sorted(list(rare_classes)):
            print(
                f"  - {self.class_names.get(cid, 'N/A')} (ID: {cid}, Conteo Original: {self.original_counts['train'][cid]})")

        images_to_oversample = set()

        # 2. Identificar las imágenes que contienen al menos una clase objetivo
        for label_file in os.listdir(train_labels_path):
            if label_file.endswith('.txt'):
                if '_oversampled' in label_file: continue  # Evitar re-muestrear archivos que ya son copias

                with open(os.path.join(train_labels_path, label_file), 'r') as f:
                    for line in f:
                        if len(line.strip()) > 0:
                            try:
                                if int(line.split()[0]) in rare_classes:
                                    images_to_oversample.add(os.path.splitext(label_file)[0])
                                    break
                            except ValueError:
                                continue

        print(f"\nSe encontraron {len(images_to_oversample)} imágenes únicas con clases objetivo para duplicar.")

        num_duplicated = 0

        # 3. Realizar la duplicación
        for i in range(duplication_factor):
            for base_name in images_to_oversample:
                original_img_path, img_extension = None, None

                # Buscar la extensión de la imagen (.jpg, .jpeg, .png)
                for ext in ['.jpg', '.jpeg', '.png']:
                    path = os.path.join(train_images_path, base_name + ext)
                    if os.path.exists(path):
                        original_img_path, img_extension = path, ext
                        break

                original_label_path = os.path.join(train_labels_path, base_name + '.txt')

                if original_img_path and os.path.exists(original_label_path):
                    # Crear un nombre único para cada copia para evitar sobrescribir
                    new_base_name = f"{base_name}_oversampled_v{i + 1}"
                    new_img_path = os.path.join(train_images_path, new_base_name + img_extension)
                    new_label_path = os.path.join(train_labels_path, new_base_name + '.txt')

                    # Solo copiar si el archivo no existe
                    if not os.path.exists(new_img_path):
                        shutil.copy2(original_img_path, new_img_path)
                        shutil.copy2(original_label_path, new_label_path)
                        num_duplicated += 1

        print(f" Se crearon {num_duplicated} nuevos pares imagen/etiqueta exitosamente.")