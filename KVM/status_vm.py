#!/usr/bin/env python
#Importacion modulos necesarios
import requests
import json
from requests.auth import HTTPBasicAuth
import sys

#Variables
Loginurl = 'URL'
name = ""
status = ""
SAL = []

#El objetivo de esta funcion es parsear los datos recibidos dentro de un json y añadirlos al diccionario SAL.
def alterJSON(name=None, status=None):
	#Definimos las variables que vamos a utilizar para generar el json y enviarlo a Zabbix.
	global SAL
	#Creamos el item json y le anadimos los datos
	json_item = {}
	json_item["Name"] = name
	json_item["status"] = status
	#Añadimos los datos al diccionario
	SAL.append(json_item)
	
#El objetivo de esta funcion es realizar una request y obtener todas las vms y su estado.
def Request():
	#Definimos las variables que seran utilizadas para generar el json y para trabajar la request.
	global name
	global status
	headers = {'Accept':'application/json'}
	#Realizamos una peticion a la API.
	r = requests.get(Loginurl,verify=False, auth=HTTPBasicAuth('USER', 'PASSWORD'), headers=headers)
	#Validamos si el resultado de la peticion es correcto, si la peticion falla acabamos la ejecucion.
	if r.status_code != 200:
		print("API Alert failed")
		sys.exit(1)
	#Cogemos los datos de la peticion.
	test = r.json()
	#Recorremos todos los campos "vm" del json
	for fqdn in test.get("vm"):
		name = fqdn.get("name")
		status = fqdn.get("status")
		#Creamos un json por cada VM con los datos de nombre y estado.
		alterJSON(name, status)
if __name__ == "__main__":
	#Llamamos a la funcion Request.
	Request()
	#Hacemos un print del json para enviarlo a través del agente
	print(json.dumps(SAL))
	sys.exit(0)