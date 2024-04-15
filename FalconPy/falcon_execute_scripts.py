#!/usr/bin/env python
# Librerias a importar
import logging # Requiere instalacion
from falconpy import APIHarness, Hosts, RealTimeResponseAdmin # Requiere instalacion
from getpass import getpass
import re
#Variables globales
client = ""
secret = ""

#Declaramos el script a ejecutar
script = """
"""

# Funcion para ejecutar el script en la consola abierta anteriormente.
def sendcommands(consoleid):
    #Importamos las variables globales necesarias
    global client
    global secret
    global script
    command_string = f"runscript -Raw=```{script}```"
    #Realizamos la ejecucion
    falcon = RealTimeResponseAdmin(client_id=client, client_secret=secret)
    falcon.execute_admin_command(session_id=consoleid,base_command="runscript",command_string=command_string)
    logging.info("Se ha ejecutado el comando.")


# Funcion para crear el ID de la consola para poder ejecutar los comandos.
def createconsole(hostid, host):
    global client
    global secret
    print("\n Obteniendo el consoleID del host %s." % (host))
    #Realizamos la peticion
    falcon = APIHarness(creds={'client_id': client, 'client_secret': secret})
    body = {'device_id': hostid[0]}
    response = falcon.command(action='RTR-InitSession', body=body)
    #Si nos devuelve un 201 buscaremos el resultado dentro del json
    if "201" in str(response["status_code"]):
        sessionid = response["body"]["resources"][0]["session_id"]
        if len(sessionid) != 0:
            print("\nEl ID se ha obtenido de forma exitosa.")
            logging.info("La session id del host %s es: %s" % (host, sessionid))
            return sessionid
        else:
            print("\nNo se ha podido obtener el ID.")
            logging.error("No se ha podido obtener el ID de la sesion del host %s" % (host))
            return "failed"
    #Si el resultado es diferente a 201, devolveremos un failed.
    else:
        print("\nNo se pudo realizar la peticion a la API.")
        logging.error("la peticion ha fallado")
        return "failed"

# Funcion para obtener los IDs de los hosts a partir del hostname.
def gethost(hostname):
    global client
    global secret
    print("\n Obteniendo el ID del host %s." % (hostname))
    #Realizamos la peticion
    falcon = Hosts(client_id=client, client_secret=secret)
    response = falcon.query_devices_by_filter(filter=f"hostname:*'*{hostname}*'")
    #Si nos devuelve un 200 OK buscaremos el resultado dentro del json
    if "200" in str(response["status_code"]):
        hostid = response["body"]["resources"]
        if len(hostid) != 0:
            print("\nEl ID se ha obtenido de forma exitosa.")
            logging.info("El host %s tiene el ID: %s" % (hostname, str(hostid[0])))
            return hostid
        else:
            print("\nNo se ha podido obtener el ID.")
            logging.warning("El host %s no tiene el cliente de CrowdStrike operativo." % (hostname))
            return "failed"
    #Si el resultado es diferente a 200 OK, devolveremos un failed.
    else:
        print("\nNo se pudo realizar la peticion a la API.")
        logging.error("No se ha podido contactar con la API")
        return "failed"

#Funcion principal para deployar la app, diferencia de que opcion viene y llama a las diferentes funciones para poder deployar la app correctamente.
def deployapp(host, flag_array):
    # Verificamos si se ha activado la opcion 1 del menu.
    if "1" in str(flag_array):
        # Transformamos el string en array para recorrerlo y por cada host hacer el despliegue
        host = host.split(",")
        for i in host:
            # Eliminamos los espacios para poder obtener los IDs sin problemas.
            i = re.sub(' ', '', i)
            #Obtenemos el host ID
            hostid = gethost(i)
            #Si no falla la peticion obtendremos el consoleID
            if not "failed" in hostid:
                consoleid = createconsole(hostid, i)
                #Si no falla la obtencion del consoleID ejecutaremos el script
                if not "failed" in consoleid:
                    sendcommands(consoleid)

    else:
        #Obtenemos el host ID
        hostid = gethost(host)
        #Si no falla la peticion obtendremos el consoleID
        if not "failed" in hostid:
                consoleid = createconsole(hostid, host)
                #Si no falla la obtencion del consoleID ejecutaremos el script
                if not "failed" in consoleid:
                    sendcommands(consoleid)

def menu():
# Funcion menú
    a = 0
    while a < 1:
        accion = input("\n\nSeleccionar una opcion: \n 1. Desplegar aplicacion en varios hosts. \n 2. Desplegar aplicación en un unico host. \n 3. Cerrar aplicación. \n\nIntroduce la opción a escoger: ") 
        if accion == "1":
            logging.info("Seleccionada la opción de despliegue de varios hosts.")
            hosts = []
            hosts = input("\nIndica el listado de hosts en los que quieres desplegar (deben de ir separados por una coma): ")
            deployapp(hosts, 1)

        elif accion == "2":
            logging.info("Seleccionada la opción de despliegue de un solo host.")
            host = input("\nIndica el hostname: ")
            deployapp(host, 0)
            
        elif accion == "3":
            logging.info("Cerrando el programa.")
            print("Se cerrara el aplicativo.")
            a = 1
        else:
            print("No se ha escogido una opcion correcta.")

# Función para obtener los datos de conexion a la API
def getclient():
    global client
    global secret
    client = input("\nIndica el client ID: ")
    secret = getpass(prompt='\nIndica el client secret: ')


# Inicializacion de la aplicacion
if __name__ == "__main__":
    #Definimos el log.
    logging.basicConfig(filename='log_info.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
    logging.info("Iniciando el programa.")
    getclient()
    menu()