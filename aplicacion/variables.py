import json

file="ultimos_datos.dat"

with open(file) as f:
    data = json.load(f)
    ultimo_anio=data["ultimo_anio"]
    ultimo_mes=data["ultimo_mes"]

folder_pdf="carpeta_prueba_sueldos"
folder_imagenes_provisorias="imagenes_provisorias"
folder_imagenes_finales="imagenes_finales"
path_repositorio="YOUR_PATH/Scrapper_Sueldos_Municipales/"
Meses=["ENERO",
      "FEBRERO",
      "MARZO",
      "ABRIL",
      "MAYO",
      "JUNIO",
      "JULIO",
      "AGOSTO",
      "SEPTIEMBRE",
      "OCTUBRE",
      "NOVIEMBRE",
      "DICIEMBRE"]
