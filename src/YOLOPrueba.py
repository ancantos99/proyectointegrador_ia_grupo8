from ultralytics import YOLO
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from base.YOLOResultsDB import YOLOResultsDB
from base.YOLOPredictor import YOLOPredictor
from base.YOLOCompararPaginas import YOLOComparadorResultados


db_config = {
    'server': 'localhost', 'database': 'BD_TEST',
    'user': 'sa', 'password': 'Runever19'
}
ruta_modelopt3 = "C:/MIA/best_exp2.pt"
ruta_imagenweb = "C:/MIA/senescytcambio2.png"
ruta_prediccion = "C:/MIA/prediccion.png"

accion = "comparar"


predictor = YOLOPredictor(model_path=ruta_modelopt3, conf=0.25, iou=0.45,agnostic_nms=True, max_det=1000,db_config=db_config)
#si identificador_web es None , no se guarda en la base de datos los resultados
pred_resultados = predictor.predict(image_path=ruta_imagenweb, identificador_web=None, show_image=False, output_path=ruta_prediccion )
print("**************INFO PREDECIDO POR EL MODELO*****************")
for r in pred_resultados:
    print(r)
#Cerrar BD al final
predictor.close_db()


predictor = YOLOPredictor(model_path=ruta_modelopt3, conf=0.25, iou=0.45,agnostic_nms=True, max_det=1000,db_config=db_config)
pred_resultados = predictor.predict(image_path=ruta_imagenweb, identificador_web=None, show_image=False, output_path=ruta_prediccion )
for r in pred_resultados:
    print(r)
predictor.close_db()

# Comparar
if(accion == "comparar"):
    conexiondb = YOLOResultsDB(server=db_config['server'], database=db_config['database'], user=db_config['user'],
                               password=db_config['password'])
    registrosbd = conexiondb.get_results_por_web("websenescyt")
    conexiondb.close()
    print("**************INFO CONSULTADA BASE DATOS*****************")
    for r in registrosbd:
        print(r)

    comparador = YOLOComparadorResultados()
    resultadoc = comparador.comparar_paginas(registrosbd, pred_resultados, conf_thresh=predictor.datamodel_conf)

    if resultadoc['pagina_cambio']:
        print("La página cambió:")
        for c in resultadoc['cambios']:
            print(c)
    else:
        print("La página está igual.")

