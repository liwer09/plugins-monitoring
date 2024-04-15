import requests
import json
import sys
import re
import warnings

headers = {
    "stationviewData": "MAC:46b4.a969.1110&IP:10.36.32.139&TYPE:unknown"
}

def get_clients():
    global headers
    metricas = ""
    diccionario = {}
    counter = 0
    request = requests.get(("http://comms:comms2@10.36.32.100/ap_stationview-client.shtml"), headers=headers, verify=False)
    print(request)
    for line in request:
        if "Signal Strength   :" in str(line):
            print(str(line))
            line = re.sub("  +","  ", str(line))
            line = line.split("  ")
            line = line[1].split( )
            print(line[0])


if __name__ == "__main__" :
    warnings.filterwarnings('ignore')
    get_clients()
