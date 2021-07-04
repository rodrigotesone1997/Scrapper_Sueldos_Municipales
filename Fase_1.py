#!/usr/bin/env python
# coding: utf-8

# # Fase 1

# In[ ]:


from datetime import datetime
Inicio_programa=datetime.now()


# ### Importo los paquetes

# In[ ]:


import os # Funciones para interactuar con el sistema operativo
import re # Funciones de expresiones regulares
import wget # Función que descarga pdf's
import random # Funcionalidades para la aleatoridad
import requests #
from bs4 import BeautifulSoup # Obtiene html de una pagina en cuestión
from datetime import date,datetime # Funciones para habilitar Fecha,hora,etc
from pdf2image import convert_from_path # Convierte pdf's a imagenes
import pytesseract # Habilita funciones para extraer texto de imagenes
from PIL import Image # Función para manejo de imagenes
import shutil # Funciones para interctuar con el sistema operativo que no tiene os
import datetime
import numpy as np # Funcionalidad para listas y matrices de una manera mas eficiente
from natsort import natsorted # Funcionalidad para ordenar folder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib # Funciones para mandar mail
import json


# ### Obtengo los url para la descarga

# In[ ]:


# La función URL recibe un url de tipo string y develve una variable soup.Entre sus atributos se
# encuentra el html de la pagina como un string

def URL(url):
    global soup 
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

URL("https://www.rosario.gob.ar/web/gobierno/personal/sueldos")

'''
Luego de revisar el html de la pagina utilizo metodos de soup para tener acceso a los enlaces de
descarga de los pdf.
Primero obtengo la lista de "ul" de la pagina
Segundo voy a la "ul" en el que especificamente estan los url buscados
Tercero busco todos los enlaces del "ul" seleccionado
Cuarto, uso expresiones regulares para extraer los url necesarios para la descarga y los pongo en una
lista
'''

# print(soup.prettify())
# Si te interesa ver como queda el el html extraido podes decomentar la linea de arriba código

pagina_sueldos="https://www.rosario.gob.ar"
lista_enlaces=[]

tag_class=soup.find_all("ul")

tag_class=tag_class[-5].find_all("a")
for i in range(0,len(tag_class)):
    try:
        tag_cadena=str(tag_class[i])
        inicio=re.search("href=\"",tag_cadena).span()[1]
        final=re.search("\"",tag_cadena[inicio:-1]).span()[0]
        lista_enlaces.append(pagina_sueldos+tag_cadena[inicio:final+inicio])
    except :
        pass


# ### Pongo el path donde esta ubicado la carpeta "Gasto_Publico_Argentino_files"

# In[ ]:


# Se tiene que reemplazar por el path en tu maquina local

path_local="path/Gasto_Publico_Argentino_files"


# ### Descarga de pdf's

# In[ ]:


'''
Creo una carpeta y guardo todos los pdf ahi
'''

path_pdf=path_local+"/Salarios_Rosario/pdf/carpeta_prueba_Sueldos"
os.mkdir(path_pdf)
for url in lista_enlaces:
    wget.download(url,path_pdf)


# # Una vez descargado los nuevos pdf's hay 3 posibilidades
# - Que sean los mismos pdf que la ultima vez que se descargo
# - Que sean distinto (nuevos) pdf's que la ultima vez
# - Que algunos hayan cambiado y otros no
# 
# En lineas generales lo que voy a hacer en los siguientes bloques es determinar en cual de los siguientes casos estamos

# ### Veo cuantas carpetas de pdf tengo actualmente

# In[ ]:


url_folder_pdf=path_local+"/Salarios_Rosario/pdf"
list_folder=natsorted(os.listdir(url_folder_pdf))


# In[ ]:


'''
Una vez tengo la lista de las carpetas de pdf's reviso que no todas carpetas terminen
en "_Sueldos" que es el patron de carpetas en la carpeta pdf.
'''

for i in list_folder:
    if str(re.search("_Sueldos",i)) == "None":
        list_folder.remove(i)


# In[ ]:


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


# In[ ]:


'''
Dentro de la carpeta imagenes voy agregando imagenes de la primera hoja de cada uno de los pdf recien
descargados.Luego extraigo el texto de cada imagen y obtengo que mes tienen en cada imagen
(se encuentra) en la esquina superior derecha.
Una vez localizado se agrega a "lista_mes"
'''

try:
    os.mkdir(path_local+"/Salarios_Rosario/imagenes")
except:
    pass

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

for i in os.listdir(path_local+"/Salarios_Rosario/pdf/carpeta_prueba_Sueldos"):
    path_pdf_a_convertir=os.path.join(path_local+"/Salarios_Rosario/pdf/carpeta_prueba_Sueldos",i)
    
    # Para usuarios Linux
    
    # primera_hoja=convert_from_path(path_pdf_a_convertir, first_page=0, last_page=0)
    
    # Para usuarios windows
    
    # primera_hoja=convert_from_path(path_pdf_a_convertir, first_page=0, last_page=0, poppler_path = poppler_path_local)
    
    i=re.sub(".pdf","",i)
    path_auxiliar=path_local+"/Salarios_Rosario/imagenes/"+i+".jpg"
    primera_hoja[0].save(path_auxiliar, 'JPEG')
    imagen=Image.open(path_auxiliar)
    text=pytesseract.image_to_string(imagen)
    for i in Meses:
        try:
            buscador_de_mes=re.search(i,text).span()[1]
            lista_mes.append(i)
            break
        except:
            pass


# In[ ]:


'''
Aca se separa en 2 casos:
Si "lista_mes" tiene el mismo mes en todas sus componentes procedo a extraer el mes de un pdf elegido
de manera aleatoria de "carpeta_prueba" con el mismo pdf en la penultima carpeta
(que son los datos mas actuales de momento).
Tambien descomentar la linea que corresponda a su sistema operativo.
'''

if len(np.unique(np.array(lista_mes)))==1:
    numero_random=random.choice(range(17))
    pdf_viejo=list_folder[-2]
    path_pdf_viejo=url_folder_pdf+"/"+pdf_viejo+"/"+natsorted(os.listdir(url_folder_pdf+"/"+pdf_viejo))[numero_random]
    pdf_nuevo=list_folder[-1]
    path_pdf_nuevo=url_folder_pdf+"/"+pdf_nuevo+"/"+natsorted(os.listdir(url_folder_pdf+"/"+pdf_nuevo))[numero_random]
    
    # Para usuarios Linux
    
    # imagen_vieja=convert_from_path(path_pdf_viejo)
    
    # Para usuarios Windows 
    
    # imagen_vieja=convert_from_path(path_pdf_viejo, poppler_path = poppler_path_local)
    
    imagen_vieja[0].save(path_local+'/Salarios_Rosario/imagen_vieja.jpg', 'JPEG')

    imagen_vieja=Image.open(path_local+'/Salarios_Rosario/imagen_vieja.jpg')
    imagen_nueva=Image.open(path_local+'/Salarios_Rosario/imagenes/'+natsorted(os.listdir(path_local+"/Salarios_Rosario/imagenes"))[numero_random])

    text_viejo=pytesseract.image_to_string(imagen_vieja)
    text_nuevo=pytesseract.image_to_string(imagen_nueva)
    for i in Meses:
        try:
            final=re.search(i,text_viejo).span()[1]
            ano_viejo=text_viejo[final+4:final+8]
            mes_viejo=i
            break
        except:
            pass

    for i in Meses:
        try:
            final=re.search(i,text_nuevo).span()[1]
            ano_nuevo=text_nuevo[final+4:final+8]
            mes_nuevo=i
            break
        except:
            pass
else:
    pass

'''
Esto es una idea para hacer un poco mas preciso el código pero no lo pense de momento
Faltaria resolver esta parte que basicamente seria obtener cuales archivos son nuevos y cuales viejos
Recordemos que si llego a este bloque de código es porque hay mix de archivos viejos y archivos nuevos
Quiza deba dejar por defecto una carpeta con las imagenes de la portada de la anterior carpeta de pdf (2021_03_Sueldos en este caso)
'''


# In[ ]:


'''
Habiendo obtenido el mes y el año del pdf nuevo y el pdf viejo los comparo.
Si son iguales entonces los pdf son iguales por tanto no se detectan cambios y si son distintos
entonces si se detecta un cambio.
Si en el bloque de código anterior paso directamente al else entonces no se definio ninguna de las
variables mes o año.
En ese paso va a pasar directamente al except.
'''

try:
    if mes_viejo != mes_nuevo or ano_viejo != ano_nuevo:
        cambio=True
    else:
        cambio=False
except:
    cambio=None


# In[ ]:


'''
Aca paso el mes a número.
Como el caso anterior, en el caso de que no este definida la variable mes_nuevo pasa el except
'''

for i,j in enumerate(Meses):
    if j == mes_nuevo:
        numero_de_mes=i+1
        mes_nuevo=str(numero_de_mes)
if len(mes_nuevo)==1:
    mes_nuevo="0"+mes_nuevo


# In[ ]:


Actualizacion=str(date.today().strftime("%Y-%m-%d"))


# # Funcion para convertir una carpeta a ".zip"

# In[ ]:


def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s'%(name,format), destination)


# In[ ]:


'''
Aca se separa en los 3 distintos casos:

Caso cambio == True:
Si esta aca es porque cambiaron los pdf respecto a los ultmos entonces conservo la carpeta descargada
y le cambio el nombre con el formato "(año_nuevo)_(mes_nuevo)_Sueldo", abro (o creo) un archivo
llamado "Seguimiento.txt" En que se escribe "Fecha del dia:HUBO UN CAMBIO"

Caso cambio == False:
Ya que no hubo cambio solo se borra la carpeta descargada y se escribe el mismo .txt mencionado
anteriormente

Caso cambio == None:
Se borra la carpeta creada y se reporta al .txt que se cambiaron algunos pdf pero no todos

Luego se borran las imagenes creadas.
'''

if cambio == True:
    os.rename(path_local+"/Salarios_Rosario/pdf/carpeta_prueba_Sueldos",os.path.join(path_local+"/Salarios_Rosario/pdf",ano_nuevo+"_"+ mes_nuevo + "_Sueldos"))
    with open(path_local+"/Seguimiento.txt","a") as f:
        f.write(f"\n{Actualizacion}: HUBO UN CAMBIO")
elif cambio == False:
    shutil.rmtree(path_local+"/Salarios_Rosario/pdf/carpeta_prueba_Sueldos")
    with open(path_local+"/Seguimiento.txt","a") as f:
        f.write(f"\n{Actualizacion}: NO HUBO UN CAMBIO")
else:
    shutil.rmtree(path_local+"/Salarios_Rosario/pdf/carpeta_prueba_Sueldos")
    with open(path_local+"/Seguimiento.txt","a") as f:
        f.write(f"\n{Actualizacion}: Hubo un cambio de algunos archivos pero no se han cambiado todos")

make_archive(path_local, path_local+".zip")

try:
    shutil.rmtree(path_local+"/Salarios_Rosario/imagenes")
    os.remove(path_local+'/Salarios_Rosario/imagen_vieja.jpg')
except:
    pass


# In[ ]:


from datetime import datetime
Finalizacion_programa=datetime.now()

from datetime import timedelta

if cambio == True:
    with open("path/keys_fase_1.json","r") as f:
        loaded_keys=json.loads(f.read())
    
    tiempo=Finalizacion_programa-Inicio_programa

    tiempo_medido=str(timedelta(seconds=tiempo.seconds))[2:]
    
    mail_content = '''Se publicaron los salarios del mes de %s de la Municipalidad 
    de Rosario.\nEl proceso tardo aproximadamente %s.
    '''%(Meses[numero_de_mes-1].capitalize(),tiempo_medido)
    #The mail addresses and password
    sender_address = loaded_keys["sender_address"]
    sender_pass = loaded_keys["sender_pass"]
    receiver_address = loaded_keys["receiver_address"]
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Notificaciones de salarios Municipales'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

