import requests
import json
import re
from tqdm import tqdm #Requiere instalacion
import os
import csv
#Definimos variables generales
headers = {"Authorization": "","Accept": "application/json","Content-Type": "application/json"}
etag = ""

#Obtenemos los datos del host , si no existe el etag significa que el host al que se esta atacando no existe, devolvemos un "failed".
def gethostdata(hostname):
    #Declaramos las variables de la peticion.
    global etag
    global headers
    url = "http://HOST/master/check_mk/api/1.0/objects/host_config/"
    #Mandamos la peticion.
    request = requests.get(url, headers=headers,verify=False)
    if request.status_code != 200:
        etag = ""
        return("failed")
    else:
        #Recogemos los datos si la peticion funciona y los devolvemos para que sean tratados.
        try:
            data = request.json()
            lista = []
            lista.append(data["extensions"]["folder"])
            lista.append(data["extensions"]["attributes"]["alias"])
            lista.append(data["extensions"]["attributes"]["ipaddress"])
            return lista
        except:
            return "failed"

if __name__ == '__main__':
    diccionario = {}
    #Solicitamos en un input los hosts a los que se les va a realizar la modificacion
    hosts = input("Listado de hosts que van a ser modificados: \n")
    #Spliteamos el resultado para obtener una lista con todos los hosts como valores
    hosts = hosts.split(",")
    #Limpiamos la shell de Windows, si se requiere para Linux modificar con "clear"
    os.system('cls')
    #Recorremos el listado de hosts y añadimos una barra de carga por la cantidad de elementos que existen.
    for i in tqdm(hosts, desc="Getting information from host"):
        i = re.sub(" ","", i)
        hostdata = gethostdata(i)
        #Si no se obtiene el etag se pasa al siguiente host de la lista
        if "failed" in etag:
            continue
        else:
            diccionario[i] = hostdata[0], hostdata[1], hostdata[2]
    print(diccionario)
    # Abre el archivo CSV para escritura
    with open('data_hosts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for clave, valor in diccionario.items():
            # Escribe el hostname (clave) y el alias, ip y folder (valor)
            writer.writerow([clave, valor[1], valor[2], valor[0]])