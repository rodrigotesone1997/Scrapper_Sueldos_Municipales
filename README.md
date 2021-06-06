<h1 align="center">Bienvenido 👋</h1>
<p>
  <a href="ss" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/rodrigotesone97?s=08" target="_blank">
    <img alt="Twitter: Rodrigo Tesone" src="https://img.shields.io/twitter/follow/rodrigotesone97.svg?style=social" />
  </a>
</p>

> El repositorio consta de un script que scrapea la pagina web de la [Municipalidad de Rosario](https://www.rosario.gob.ar/web/gobierno/personal/sueldos), descarga los pdf que contienen los sueldos dentro de ella, verifica si son iguales a la última actualización disponible en la carpeta pdf de este [archivo](Gasto_Publico_Argentino_files.zip).<br/>
> En caso de que se actualizen se incorporan en una nueva carpeta con el siguiente formato: "Año_Mes_Sueldos".<br/>
> Finalmente abre el archivo "Seguimiento.txt" para ver que transcurrio en el proceso (Si hubo o no hubo cambio de archivos)

### 🏠 Clonar Reposotorio

> `git clone https://github.com/rodrigotesone1997/Scrapper_Sueldos_Municipales.git`

## Install
Ademas de los requerimientos que estan [aquí](requirements.txt) es posible que surga el siguiente error al momento de uso:
```
TesseractNotFound Error: tesseract is not installed or it's not in your path
```
En ese caso se recomienda seguir el siguiente [video](https://www.youtube.com/watch?v=DG5D8A3zi4o&ab_channel=MotechApp).
Para usuarios Windows el paquete `pdf2image` necesita la descarga del ejecutable ubicado [aquí](https://github.com/oschwartz10612/poppler-windows/releases/).
Para mas información al respecto mirar https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/
## Usage

1. (Opcional) Crear un entorno virtual `virtualenv` y activarlo.
2. Instalar las depedencias `pip install -r requirements.txt`
3. Descomprimir el [.zip](Gasto_Publico_Argentino_files.zip)
4. Reemplazar el path de "Gasto_Publico_Argentino_files" dentro de la variable `path_local` del programa
5. Revisar el código en caso de necesitar comentar algunas lineas (mas información comentada en el código)
6. Por último, ejecutarlo

## 

Cualquier sugerencia de arquitectura de código,pregunta o problema enviar mail a rodrigotesone1997@outlook.com.ar

## Author

👤 **Rodrigo Tesone**

<!---* Website: xadec
-->
* Twitter: [@rodrigotesone97](https://twitter.com/rodrigotesone97?s=08)
* Github: [rodrigotesone1997](https://github.com/rodrigotesone1997)
<!---* LinkedIn: [@ff](https://linkedin.com/in/ff)
-->
## 🤝 Contributing

Agrdezco a [Bautista](https://github.com/coltking) por la motivación e ideas al proyecto , a [Alejandro](https://github.com/alexdraven) la revisión de código y a la Municipalidad de Rosario por publicar tan pauperrimamente sus datos y obligarme a hacer esto.


## 📝 License

Copyright © 2021 [Rodrigo](https://github.com/rodrigotesone1997).<br />
This project is [MIT](LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
