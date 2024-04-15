import requests
import pandas as pd
import warnings
import json

#variables globales
headers = {"Authorization": "","Accept": "application/json","Content-Type": "application/json"}

#Funcion discovery servicios
def service_discovery(line):
    global headers
    body = {"host_name": line[0], "mode": "new"}
    requests.post("https://HOST/master/check_mk/api/v0/domain-types/service_discovery_run/actions/start/invoke", headers=headers, data=body, verify=False)

#Funcion aplicar cambios
def apply_changes():
    global headers
    requests.post("https://HOST/master/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke", headers=headers, verify=False)

#Funcion crear host en checkmk
def crearhost(line):
    #Definimos variables
    global session
    i = 0
    agente = "no-agent"
    snmp = "no-snmp"
    #Verificamos si se va a usar snmp o cmk-agent o ninguno y sacamos el output correspondiente.
    if "cmk-agent" in str(line[4]):
        agente = "cmk-agent"
    elif "snmp" in str(line[4]):
        snmp = "snmp-v2"
    for a in line:
        i = i + 1
        if "nan" in str(a):
            line[i-1] = "NA"
    #Formateamos el json del body
    data = json.dumps({"folder": line[3], "host_name": line[0], "attributes":
    { "ipaddress": line[2], 
    "alias": line[1], 
    "tag_agent": agente, 
    "tag_snmp_ds": snmp
    }})
    #enviamos la request
    peticion = requests.post('https://HOST/master/check_mk/api/1.0/domain-types/host_config/collections/all', verify=False, headers=headers, data=data)
    if peticion.status_code != 200:
        print(peticion.json())


#Funcion obtener datos de excel
def readexcel():
    #Importamos el excel
    data_frame = pd.read_excel('importar_hosts.xlsx')
    #Recorremos el excel 
    for index, row in data_frame.iterrows():
        crearhost(row.values)
        service_discovery(row.values)
    apply_changes()




if __name__ == '__main__':
    #filtramos los errores de warning que nos devuelve por el ssl verify.
    warnings.filterwarnings('ignore')
    #Llamamos a la funcion "readexcel"
    readexcel()
    