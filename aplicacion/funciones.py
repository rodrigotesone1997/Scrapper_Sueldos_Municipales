import os # Funciones para interactuar con el sistema operativo
import re # Funciones de expresiones regulares
import wget # Función que descarga pdf's
import random # Funcionalidades para la aleatoridad
import requests # Peticiones http a la pagina
from bs4 import BeautifulSoup # Obtiene html de una pagina en cuestión
from pdf2image import convert_from_path # Convierte pdf's a imagenes
import pytesseract # Habilita funciones para extraer texto de imagenes
from PIL import Image # Función para manejo de imagenes
import shutil # Funciones para interctuar con el sistema operativo que no tiene os
import numpy as np # Funcionalidad para listas y matrices de una manera mas eficiente
from natsort import natsorted # Funcionalidad para ordenar folder
from aplicacion.variables import Meses,ultimo_anio,ultimo_mes,folder_pdf,folder_imagenes_provisorias,folder_imagenes_finales,path_repositorio
from aplicacion.telegrambot import *

def URL(url):

    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def obtencion_url_pdfs(html):

    pagina_sueldos="https://www.rosario.gob.ar"
    lista_enlaces=[]

    tag_class=html.find_all("ul")

    tag_class=tag_class[-4].find_all("a")
    for i in range(0,len(tag_class)):
        try:
            tag_cadena=str(tag_class[i])
            inicio=re.search("href=\"",tag_cadena).span()[1]
            final=re.search("\"",tag_cadena[inicio:]).span()[0]
            lista_enlaces.append(pagina_sueldos+tag_cadena[inicio:final+inicio])
        except :
            pass
    return lista_enlaces

def descarga_pdfs(enlaces):
    os.mkdir(folder_pdf)
    for url in enlaces:
        wget.download(url,folder_pdf)

def creacion_imagenes():
# Aca va cambio en el path
    try:
        os.mkdir(folder_imagenes_provisorias)
        os.mkdir(folder_imagenes_finales)
    except:
        pass

    path_carpeta_prueba=os.listdir(folder_pdf)

    for nombre_archivo in path_carpeta_prueba:
        path_pdf_a_convertir=os.path.join(folder_pdf,nombre_archivo)

        # Para usuarios Linux

        primera_hoja=convert_from_path(path_pdf_a_convertir, first_page=0, last_page=0)

        # Para usuarios windows

        # primera_hoja=convert_from_path(path_pdf_a_convertir, first_page=0, last_page=0, poppler_path = poppler_path_local)
        nombre_archivo=nombre_archivo.replace(".pdf","")
        path_auxiliar=f"{folder_imagenes_provisorias}/{nombre_archivo}.jpg"
        primera_hoja[0].save(path_auxiliar, 'JPEG')
    
    for nombre_archivo in os.listdir(folder_imagenes_provisorias):

        path_auxiliar=f"{folder_imagenes_provisorias}/{nombre_archivo}"
        im = Image.open(path_auxiliar)
        width, height = im.size

        left = 1300
        top = 300
        right = 1600
        bottom = 440

        im1 = im.crop((left, top, right, bottom))

        path_final=f"{folder_imagenes_finales}/{nombre_archivo}"
        im1.save(path_final)


def obtencion_lista_mes():
    '''
    Dentro de la carpeta imagenes voy agregando imagenes de la primera hoja de cada uno de los pdf recien
    descargados.Luego extraigo el texto de cada imagen y obtengo que mes tienen en cada imagen
    (se encuentra) en la esquina superior derecha.
    Una vez localizado se agrega a "lista_mes"
    '''

    lista_mes=[]

    '''
    En caso de haber descargado el ejecutable descomentar las siguientes 2
    líneas de código.
    En caso de tenerlo instalado cambiar path_tesseract_exe por la ubicacion del ejecutable
    de tu maquina.
    '''

    # path_tesseract_exe="path/tesseract.exe"
    # pytesseract.pytesseract.tesseract_cmd=path_tesseract_exe

    '''
    Si se descargo el ejecutable asociado a pdf2image descomentar la siguiente linea.
    '''

    # poppler_path_local= "C:/Program Files (x86)/poppler-21.03.0/Library/bin"


    # Tambien descomentar la linea que corresponda a su sistema operativo para la variable primera_hoja.

    path_carpeta_prueba=os.listdir(folder_imagenes_finales)

    for nombre_archivo in path_carpeta_prueba:

        # Para usuarios windows

        # primera_hoja=convert_from_path(path_pdf_a_convertir, first_page=0, last_page=0, poppler_path = poppler_path_local)

        _path_auxiliar=f"{folder_imagenes_finales}/{nombre_archivo}"
        imagen=Image.open(_path_auxiliar)
        text=pytesseract.image_to_string(imagen)
        for i in Meses:
            try:
                buscador_de_mes=re.search(i,text).span()[1]
                lista_mes.append(i)
                break
            except:
                pass

    return lista_mes

def buscador_mes_nuevo(lista_mes):

    '''
    Aca se separa en 2 casos:
    Si "lista_mes" tiene el mismo mes en todas sus componentes procedo a extraer el mes de un pdf elegido
    de manera aleatoria de "carpeta_prueba" con el mismo pdf en la penultima carpeta
    (que son los datos mas actuales de momento).
    Tambien descomentar la linea que corresponda a su sistema operativo.
    '''

    cantidad_meses_distintos=len(np.unique(np.array(lista_mes)))
    if cantidad_meses_distintos==1:
        archivos_mezclados=True
        numero_random=random.choice(range(17))
        file_imagen=str(natsorted(os.listdir(folder_imagenes_finales))[numero_random])
        path_imagen_nueva=f"{folder_imagenes_finales}/{file_imagen}"
        imagen_nueva=Image.open(path_imagen_nueva)

        text_nuevo=pytesseract.image_to_string(imagen_nueva)

        for mes in Meses:
            try:
                final=re.search(mes,text_nuevo).span()[1]
                anio_nuevo=text_nuevo[final+4:final+8]
                mes_nuevo=mes
                break
            except:
                pass
    else:
        anio_nuevo=None
        mes_nuevo=None
        archivos_mezclados=False

    '''
    Esto es una idea para hacer un poco mas preciso el código pero no lo pense de momento
    Faltaria resolver esta parte que basicamente seria obtener cuales archivos son nuevos y cuales viejos
    Recordemos que si llego a este bloque de código es porque hay mix de archivos viejos y archivos nuevos
    Quiza deba dejar por defecto una carpeta con las imagenes de la portada de la anterior carpeta de pdf (2021_03_Sueldos en este caso)
    '''
    return mes_nuevo,anio_nuevo, archivos_mezclados

def estado_cambio(mes_nuevo,anio_nuevo,archivos_mezclados):
    '''
    Habiendo obtenido el mes y el año del pdf nuevo y el pdf viejo los comparo.
    Si son iguales entonces los pdf son iguales por tanto no se detectan cambios y si son distintos
    entonces si se detecta un cambio.
    Si en el bloque de código anterior paso directamente al else entonces no se definio ninguna de las
    variables mes o año.
    En ese paso va a pasar directamente al except.
    '''
    if archivos_mezclados:
        if ultimo_mes != mes_nuevo or ultimo_anio != anio_nuevo:
            cambio=True
        else:
            cambio=False
    else:
        cambio=None
    return cambio

def final(cambio,mes_nuevo,anio_nuevo,tiempo_medido):

    if cambio == True:
        os.remove("{path_repositorio}ultimos_datos.dat")

        string='''{
"ultimo_anio":"%s",
"ultimo_mes":"%s"
}'''%(anio_nuevo,mes_nuevo)

        with open("{path_repositorio}ultimos_datos.dat","w") as f:
            f.write(string)

        tg=telegrambot

        token_telegram,id_Rodrigo=tg.cargarLlaves("{path_repositorio}keys")

        mensaje_bot=f"Se publicaron los salarios del mes de {mes_nuevo.capitalize()} del año {anio_nuevo.capitalize()} de la Municipalidad  de Rosario\nEl proceso tardo aproximadamente {tiempo_medido}.\nRecorda descargarlos"

        tg.NotificarRodrigo(token_telegram,id_Rodrigo,mensaje_bot)

    elif cambio == False:
        pass
    else:
        pass

    try:
        shutil.rmtree(folder_imagenes_finales)
        shutil.rmtree(folder_pdf)
    except:
        pass