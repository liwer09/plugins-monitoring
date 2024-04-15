import paramiko
import re
import time
import sys
from cryptography.fernet import Fernet

#Funcion para ejecutar los comandos en la cabina y parsear el output
def ssh_execution(command, ip, password):
    string = ""
    #Creamos la conexión SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username = "", password = password)
        shell = ssh.invoke_shell()
    except:
        print("SSH can't connect")
        sys.exit(2)
    #Enviamos el comando a ejecutar y recogemos el output
    shell.send(f"{command} \n")
    time.sleep(0.5)
    if shell.recv_ready():
        string = string + str(shell.recv(9999))
    if "command not found" in string:
        print("Command not found")
        sys.exit(2)
    string = string.split("\\r\\n")
    #Eliminamos las 2 primeras lineas que es la del comando y el encabezado de la tabla que nos devuelve el comando.
    string = string[3:-1]
    return string

#Funcion para recorrer el output y detectar el status del servicio
def get_result(command, output):
    error = 0
    name = ""
    disk_space_used = ""
    metrics = ""
    for line in output:
        line = re.sub(" +", " ", line)
        line = line.split(" ")
        #Si detectamos en una linea que no hay un resultado online, guardamos en name el item afectado segun el comando.
        if not "online" in str(line) and not "active" in str(line):
            error = error + 1
            if command == "lsarray":
                name = f"{name} {line[1]},"
            elif command == "lsdrive":
                name = f"{name} {line[7]} {line[6]},"
            elif command == "lsenclosure":
                name = f"{name} {line[5]},"
            elif command == "lsenclosurebattery" or command == "lsenclosurecanister" or command == "lsenclosurepsu" or command == "lsenclosureslot":
                name = f"{name} {line[0]} {line[1]},"
            elif command == "lsvdisk":
                name = f"{name} {line[1]},"
            elif command == "lsmdiskgrp":
                name = f"{name} {line[1]},"
        #Para el comando lsmdiskgrp queremos obtener de los discos el espacio ocupado.
        elif command == "lsmdiskgrp" and "online" in str(line):
            #Hacemos el calculo del porcentaje usado e indicamos por cada pool su status para que se pueda ver en el output correctamente
            used = re.sub("TB","",line[9])
            total = re.sub("TB","",line[5])
            percent_used = (float(used)/float(total))*100
            if float(percent_used) >= 90.00:
                disk_space_used = f"{disk_space_used} {line[1]} : {percent_used:.2f}CRIT!!,"
                metrics = f"{metrics} {line[1]} = {percent_used:.2f},"
            elif float(percent_used) >= 80.00:
                disk_space_used = f"{disk_space_used} {line[1]} : {percent_used:.2f}WARN!!,"
                metrics = f"{metrics} {line[1]} = {percent_used:.2f},"
            else:
                disk_space_used = f"{disk_space_used} {line[1]} : {percent_used:.2f},"
                metrics = f"{metrics} {line[1]} = {percent_used:.2f},"

    if len(output) == error and error >= 1:
        print("CRIT - All is not online")
        sys.exit(2)
    if error >=1:
        #Si hay un not online, devolvemos el diskspace used del resto.
        if command == "lsmdiskgrp":
            if "CRIT" in disk_space_used:
                print(f"This not online: {name} diskpace used: {disk_space_used} | {metrics}")
                sys.exit(2)
            elif "WARN" in disk_space_used:
                print(f"This not online: {name} diskpace used: {disk_space_used} | {metrics}")
                sys.exit(1)
            else:
                print(f"This not online: {name} diskpace used: {disk_space_used} | {metrics}")
                sys.exit(1)
        else:
            print(f"WARN - This not online: {name}")
            sys.exit(1)
    else:
        #Como todos estan online, devolvemos el diskspace used de todos.
        if command == "lsmdiskgrp":
            if "CRIT" in disk_space_used:
                print(f"All is online, diskpace used: {disk_space_used} | {metrics}")
                sys.exit(2)
            elif "WARN" in disk_space_used:
                print(f"All is online, diskpace used: {disk_space_used} | {metrics}")
                sys.exit(1)
            else:
                print(f"All is online, diskpace used: {disk_space_used}| {metrics}")
                sys.exit(0)
        else:
            print("OK - All is online")

#Funcion para hacer decrypt de la password de SSH
def decrypt_password(name):
    with open("/opt/scripts/ibm/key.fernet", "rb") as f:
        key = f.read()
        f.close()
    fernet = Fernet(key)
    with open(f"/opt/scripts/ibm/{name}.fernet", 'rb') as file:
        password = file.read()
    decrypted_password = fernet.decrypt(password)
    return decrypted_password.decode()

if __name__ == '__main__':
    password = decrypt_password("ibm_storage")
    #Argumento 1: comando, 2: ip
    execution = ssh_execution(sys.argv[1], sys.argv[2], password)
    get_result(sys.argv[1], execution)
