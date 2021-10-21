import json

path_repositorio="YOUR_PATH/Scrapper_Sueldos_Municipales/"
file=f"{path_repositorio}ultimos_datos.dat"
keys=f"{path_repositorio}keys"

with open(file) as f:
    data = json.load(f)
    ultimo_anio=data["ultimo_anio"]
    ultimo_mes=data["ultimo_mes"]

folder_pdf=f"{path_repositorio}carpeta_prueba_sueldos"
folder_imagenes_provisorias=f"{path_repositorio}imagenes_provisorias"
folder_imagenes_finales=f"{path_repositorio}imagenes_finales"

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
