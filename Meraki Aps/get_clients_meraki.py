import requests
import json
import sys
import re
import warnings

headers = {
    "X-Cisco-Meraki-API-Key": ""
}

def get_clients(serial):
    global headers
    metricas = ""
    diccionario = {}
    counter = 0
    request = requests.get((f"https://api.meraki.com/api/v1/devices/{serial}/clients"), headers=headers, verify=False)
    clients = request.json()
    for client in clients:
        client = str(client).split(",")
        client = client[7].split(":")
        vlan = re.sub(" ","",client[1])
        if not vlan in diccionario:
            diccionario[vlan] = 1
        else:
            diccionario[vlan] = diccionario[vlan] + 1
    for clave, valor in diccionario.items():
        counter = counter + int(valor)
        metricas = metricas + str(clave) + "=" + str(valor) + " "
    print("OK - Hay un total de %s conexiones | %s total_conexiones=%i" % (str(counter), str(metricas), int(counter)))


#Funcion para 
def get_serial(mac):
    global headers
    try:
        request = requests.get("https://api.meraki.com/api/v1/organizations/508943/devices", headers=headers, verify=False)
    except:
        error = ""
    for devices in request.json():
        devices = str(devices).split(",")
        if mac in str(devices[2]):
            serial = str(devices[1]).split(":")
            serial = re.sub("'","",serial[1])
            serial = re.sub(" ","",serial)
            get_clients(serial)

if __name__ == "__main__" :
    #Ignoramos los warnings que aparecen del SSL a pesar del verify False y llamamos a la funcion get_serial.
    warnings.filterwarnings('ignore')
    get_serial(sys.argv[1])
