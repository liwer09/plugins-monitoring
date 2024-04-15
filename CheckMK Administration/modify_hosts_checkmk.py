import requests
import json
import re
import time
import pandas as pd
from tqdm import tqdm #Requiere instalacion
import os
#Definimos variables generales
headers = {"Authorization": "","Accept": "application/json","Content-Type": "application/json"}
etag = ""

#Obtenemos el etag del host para poder modificarlo posteriormente, si no existe el etag significa que el host al que se esta atacando no existe, devolvemos un "failed" para realizar el filtrado de los que SI tienen etag.
def getetag(hostname):
    #Declaramos las variables de la peticion.
    global etag
    global headers
    url = "http://HOST/master/check_mk/api/1.0/objects/host_config/" + hostname
    #Mandamos la peticion.
    request = requests.get(url, headers=headers,verify=False, timeout=10)
    if request.status_code != 200:
        etag = ""
        return("failed")
    else:
        #Recogemos el valor de la peticion.
        return(request.headers.get("ETag"))

#Modificamos los hosts que tienen etag a traves de una request a la API
def modify_host_checkmk(etag, hostname):
    #Declaramos las variables de la peticion.
    url = "http://HOST/master/check_mk/api/1.0/objects/host_config/" + hostname
    headers = {"Authorization": "", "If-Match": etag ,"Accept": "application/json","Content-Type": "application/json", }
    data=json.dumps({
        'update_attributes': {
            "tag_criticality": "prod"
        }
    })
    #Mandamos la peticion.
    request = requests.put(url, headers=headers, data=data, verify=False, timeout=10)
    if request.status_code == 200:
        hola = "hola"
    else:
        print(request.content)
    #Aplicamos los cambios.
    url = "http://HOST/master/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke"
    requests.post(url, headers=headers)
    
#Aplica los cambios realizados en CheckMK   
def apply_changes():
    global headers
    requests.post("http://HOST/master/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke", headers=headers, verify=False, timeout=60)


if __name__ == '__main__':
    #Solicitamos en un input los hosts a los que se les va a realizar la modificacion
    hosts = input("Listado de hosts que van a ser modificados: \n")
    #Spliteamos el resultado para obtener una lista con todos los hosts como valores
    hosts = hosts.split(",")
    os.system('cls')
    for i in tqdm(hosts, desc="Getting information from host"):
        i = re.sub(" ","", i)
        try:
            etag = getetag(i)
            modify_host_checkmk(str(etag), i)
        except:
            time.sleep(5)
            etag = getetag(i)
            modify_host_checkmk(str(etag), i)            
    #Una vez todos los hosts se han modificado se llama a la funcion "apply_changes" para aplicar los cambios
    apply_changes()
            