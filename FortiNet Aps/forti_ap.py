from fortigate_api import Fortigate
import json
import re
import sys

def get_ssid_clients(name):
    diccionario = {}
    counter = 0
    counter5 = 0
    counter2 = 0
    metricas = ""
    fgt = Fortigate(host=":8443", username="", password="!")
    sesiones = fgt.get(url="/api/v2/monitor/wifi/client")
    for sesion in sesiones:
        if name in sesion["wtp_name"]:
            ssid = sesion["ssid"]
            banda = sesion["health"]["band"]["value"]
            ssid_banda = str(ssid) + "_" + str(banda)
            if ssid_banda in diccionario:
                diccionario[ssid_banda] = diccionario[ssid_banda] + 1
            else:
                diccionario[ssid_banda] = 1
    for clave, valor in diccionario.items():
        if "5" in str(clave):
            counter = counter + int(valor)
            counter5 = counter5 + int(valor)
        else:
            clave = clave.split("_")
            clave = re.sub(" ","", clave[0])
            clave = str(clave) + "_2.4ghz" 
            counter = counter + int(valor)
            counter2 = counter2 + int(valor)
        metricas = metricas + str(clave) + "=" + str(valor) + " "
    print("OK - Hay un total de %s conexiones en la banda 5Ghz y un total de %s conexiones en la banda 2.4Ghz | %s total_conexiones=%i" % (str(counter5),str(counter2),str(metricas), int(counter)))
    sys.exit(0)
    
if __name__ == "__main__" :
    get_ssid_clients(sys.argv[1]) 