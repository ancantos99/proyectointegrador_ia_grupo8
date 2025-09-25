import os
import glob
import numpy as np
import shutil
from sklearn.base import BaseEstimator, TransformerMixin
import logging


class DataCleaner(BaseEstimator, TransformerMixin):
    def __init__(self, repo_path, nclasesmax=15,removerLabelsinvalidos=False, moverarchivosincompletos=False):
        self.repo_path = repo_path
        #cantidad de clases definidas en .yaml ej: 0: link, 1:buton, .. 15: text; entonces nclasesmax = 15
        self.nclasesmax = nclasesmax
        self.missing = []
        self.outliers = []
        self.removerLabelsinvalidos = removerLabelsinvalidos
        self.moverarchivosincompletos = moverarchivosincompletos
        self.logger = logging.getLogger(self.__class__.__name__)  # Logger por clase
        self.logger.propagate = True
        self.logger.info(f"Se ha configurado un DataCleaner con repo_path={self.repo_path} \n"
                         f"nclasesmax={self.nclasesmax} y \n"
                         f"removerLabelsinvalidos={self.removerLabelsinvalidos} y \n"
                         f"moverarchivosincompletos={self.moverarchivosincompletos}")

    #2.1 Tratamiento de Valores Faltantes
    def _check_missing(self, img_dir, label_dir, moverfaltantes = False):
      self.logger.info(f"Inicia Verificación de Valores Faltantes en: {os.path.dirname(img_dir)}")
      #Detecta imágenes sin label y labels sin imagen
      #para cada directorio extrae el nombre base del archivo en minúscula
      images = {os.path.splitext(f)[0] for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".png"))}
      labels = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.lower().endswith(".txt")}
      #se utilizaran los mismos nombres de archivos, cada imagen .png o .jpg debe tener su archivo .txt con el mismo nombre
      #se realiza una operación de conjuntos
      missing_labels = images - labels #imagenes que no tiene su archivo txt con etiquetas
      missing_images = labels - images #archivos txt que no tienen su imagen
      if(moverfaltantes): #opcional mover faltantes
        carpetapadr = os.path.basename(os.path.dirname(img_dir))
        pathfaltante = os.path.join(self.repo_path,carpetapadr,"faltantes")
        if not os.path.exists(pathfaltante):
          os.makedirs(pathfaltante) #si no existe la carpeta faltantes la creo
        missing_img_dir = os.path.join(pathfaltante, "falta_labels")
        missing_lbl_dir = os.path.join(pathfaltante, "falta_imagen")
        if not os.path.exists(missing_img_dir):
          os.makedirs(missing_img_dir)
        if not os.path.exists(missing_lbl_dir):
          os.makedirs(missing_lbl_dir)

      if missing_labels:
          #añado la tupla nombre_imagen, "falta el archivo txt"
          self.missing.extend([(img, "falta el archito txt") for img in missing_labels])
          if(moverfaltantes):
            print(f"Moviendo {len(missing_labels)} imágenes sin etiquetas...")
            for img_base in missing_labels:
              source_img = os.path.join(img_dir, f"{img_base}.png") # Asumimos .png, se usará png para facilitar el proceso
              dest_img = os.path.join(missing_img_dir, f"{img_base}.jpg")
              shutil.move(source_img, dest_img)
      if missing_images:
          #añado la tupla archivo_txt, "falta imagen"
          self.missing.extend([(lbl, "missing_image") for lbl in missing_images])
          if(moverfaltantes):
            print(f"Moviendo {len(missing_images)} archivos txt sin imágenes...")
            for lbl_base in missing_images:
              source_lbl = os.path.join(label_dir, f"{lbl_base}.txt")
              dest_lbl = os.path.join(missing_lbl_dir, f"{lbl_base}.txt")
              shutil.move(source_lbl, dest_lbl)

    #2.2 Tratamiento de Outliers y 2.3 estandarizar formatos Revisión
    def _check_outliers(self, label_dir):
      self.logger.info(f"Inicia Verificación de Outliers en: {os.path.dirname(label_dir)}")
      #Detecta anotaciones fuera de rango o mal formateadas
      #proceso cada archivo txt (estos contienen las etiquetas en formato YOLO para cada imagen)
      for txt in glob.glob(os.path.join(label_dir, "*.txt")):
        with open(txt, "r") as f: #Abro el archivo para lectura
          for i,line in enumerate(f,1): #itero en cada línea dentro del archivo
            try:
              parts = line.strip().split() #divido la línea en partes
              if len(parts) != 5: #un fomrato YOLOV8 válido debe tener exactamente 5 partes (clase, x, y, w, h)
                self.outliers.append((txt, "formato inválido (linea no cumple 5 partes)", f"Línea {i}: {line.strip()}"))
                continue #salto a la siguiente linea

              cls, x, y, w, h = map(float, parts) #si esta conversión falla quiere decir que no son valores nunéricos float

              if not (0 <= cls <= self.nclasesmax):# Validar que sea una clase válida
                self.outliers.append((txt, f"Clase inválida (debe ser entre 0 y {self.nclasesmax})", f"Línea {i}: {line.strip()}"))
                continue

              if not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
                self.outliers.append((txt, "fuera de rango (revisar normalizacion)", f"Línea {i}: {line.strip()}"))
            except:
              self.outliers.append((txt, "error (no se puede mapear)", f"Línea {i}: {line.strip()}"))

    def fit(self, X=None, y=None):
        #Escanea la estructura de un dataset YOLOv8 train/val/test en busca de problemas
        for subset in ["train", "val", "test"]:
            self.logger.info(f"Fit sen Subcarpet {subset}/")
            img_dir = os.path.join(self.repo_path, subset, "images")
            label_dir = os.path.join(self.repo_path, subset, "labels")

            if os.path.exists(img_dir) and os.path.exists(label_dir):
                self._check_missing(img_dir, label_dir, self.moverarchivosincompletos)
                self._check_outliers(label_dir)
        self.logger.info("Fit DataCleaner completado")
        return self

    # Aplicar Opcional Limpieza
    def transform(self,X=None, y=None):
        #Acción sobre los problemas encontrados.
        if self.removerLabelsinvalidos: #borra el archivo de labels(habría que volverlo a generar pero bien)
            for file, issue, line in self.outliers:
                #print(f"remover label inválido: {file} | {issue} | {line}")
                self.logger.info(f"remover label inválido: {file} | {issue} | {line}")
                os.remove(file)
        self.logger.info("Transform DataCleaner completado")
        return X

