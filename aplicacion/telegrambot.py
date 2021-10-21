import json # Paquete que permite manipular archivos .dat y .json
import requests # Paquete para hacer requests
class telegrambot:
    def cargarLlaves(name):

        # Leer el .dat

        retorno =["",""]
        try:
            with open(name + ".dat", "r") as f:
                loaded_keys = json.loads(f.read())
            token_telegram=loaded_keys["token_telegram"] # Acceso al bot
            id_Rodrigo=loaded_keys["id_Rodrigo"] # Rodrigo
            retorno = [token_telegram,id_Rodrigo]
        except Exception as e:
            print(e)
        return retorno

    def NotificarRodrigo(token_telegram,id_Rodrigo,mensaje):

        texto=f"https://api.telegram.org/bot{token_telegram}/sendMessage?chat_id={id_Rodrigo}&parse_mode=MarkdownV2&text={mensaje}"

        response=requests.get(texto)

        return response.json()