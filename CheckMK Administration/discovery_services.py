import requests
import warnings
import re
import time
import json
import os
from tqdm import tqdm #Requiere instalacion
#variables globales
headers = {"Authorization": "","Accept": "application/json","Content-Type": "application/json"}

#Funcion discovery servicios
def service_discovery(host):
    global headers
    
    body = ({"host_name": host, "mode": 'new'})
    r = requests.post("https://HOST/master/check_mk/api/v0/domain-types/service_discovery_run/actions/start/invoke", headers=headers, data=json.dumps(body), verify=False)
    if r.status_code == 200:
        return("ok")
    else:
        print(r.json())
        return("nok")

#Funcion aplicar cambios
def apply_changes():
    global headers
    requests.post("https://HOST/master/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke", headers=headers, verify=False)

if __name__ == '__main__':
    #filtramos los errores de warning que nos devuelve por el ssl verify.
    warnings.filterwarnings('ignore')
    #Hacemos una llamada al usuario con input para que ponga el listado de hosts y lo spliteamos
    hosts = input("Indica el listado de hosts (recuerda que deben de estar separados por una coma): \n")
    hosts = hosts.split(",")
    #Limpiamos la shell de Windows, si se requiere para Linux modificar con "clear"
    os.system('cls')
    #Recorremos el listado de hosts y añadimos una barra de carga por la cantidad de elementos que existen.
    for i in tqdm(hosts, desc="Discovering services"):
        #Eliminamos espacios y llamamos a la funcion que hace el discovery de servicios.
        i = re.sub(" ","", i)
        service_discovery(i)
    # #Una vez recorridos todos los hosts, aplicamos los cambios.
    apply_changes()