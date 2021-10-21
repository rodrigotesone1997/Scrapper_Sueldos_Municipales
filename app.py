from aplicacion.funciones import URL, obtencion_url_pdfs, descarga_pdfs,obtencion_lista_mes,creacion_imagenes,buscador_mes_nuevo,estado_cambio,final
from datetime import datetime,timedelta # Funciones para habilitar Fecha,hora,etc
from shutil import rmtree
from aplicacion.variables import folder_imagenes_provisorias

Inicio_programa=datetime.now()

url="https://www.rosario.gob.ar/web/gobierno/personal/sueldos"
soup=URL(url)

lista_enlaces=obtencion_url_pdfs(html=soup)

descarga_pdfs(enlaces=lista_enlaces)

creacion_imagenes()

meses_pdf=obtencion_lista_mes()

rmtree(folder_imagenes_provisorias)
mes_nuevo,anio_nuevo, archivos_mezclados=buscador_mes_nuevo(lista_mes=meses_pdf)

cambio=estado_cambio(mes_nuevo,anio_nuevo,archivos_mezclados)

Finalizacion_programa=datetime.now()

tiempo=Finalizacion_programa-Inicio_programa

tiempo_medido=str(timedelta(seconds=tiempo.seconds))[2:]
print(tiempo_medido)
final(cambio,mes_nuevo,anio_nuevo,tiempo_medido)