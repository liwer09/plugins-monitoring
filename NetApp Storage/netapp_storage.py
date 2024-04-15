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
    if command == "df -g":
        string = re.sub(r"\\r\\n/vol","\\r\\n\\r\\n/vol", str(string))
        string = string.split('\r\n\r\n')
    elif command == "aggr status":
        string = re.sub(r"\\r\\naggr","\\r\\n\\r\\naggr", str(string))
        string = string.split('\r\n\r\n')
    else:
        string = string.spli('\r\n')
    #Eliminamos las 2 primeras lineas que es la del comando y el encabezado de la tabla que nos devuelve el comando.
    string = string[1:-1]
    return string

#Funcion para recorrer el output y detectar el status del servicio
def get_result(command, output):
    error = 0
    name = ""
    disk_space_used = ""
    metrics = ""
    for line in output:
        line = re.sub(r"\\r\\n",'',line)
        line = re.sub(" +", " ", line)
        line = line.split(" ")
        #Si el comando ejecutado es df -g, buscamos los volumenes para evitar lineas erroneas y si supera el 90% de uso lo marcamos como critical y si es mas del 80% un warning.
        if command == "df -g":
            if "/vol" in str(line):
                used = re.sub("%","",line[4])
                if int(used) >= 90:
                    name = f"{name} {line[0]} space used: {line[2]}({line[4]} CRIT!!!),"
                    metrics = f"{metrics} {line[0]}_space_used={line[2]}, {line[0]}_percentage_used={line[4]}"
                elif int(used) >=80:
                    name = f"{name} {line[0]} space used: {line[2]}({line[4]} WARN!!!),"
                    metrics = f"{metrics} {line[0]}_space_used={line[2]}, {line[0]}_percentage_used={line[4]}"
                else:
                    metrics = f"{metrics} {line[0]}_space_used={line[2]}, {line[0]}_percentage_used={line[4]}"
        elif command == "aggr status" and "online" in str(line):
                used = re.sub("%","",line[3])
                used_total = float(re.sub(r"(TB|GB)","",line[1]))- float(re.sub(r"(TB|GB)","",line[2]))
                if int(used) >=90:
                    name = f"{name} {line[0]} space used: {used_total}({line[3]} CRIT!!!),"
                    metrics = f"{metrics} {line[0]}_space_used={used_total}, {line[0]}_percentage_used={line[3]}"
                elif int(used) >=80:
                    name = f"{name} {line[0]} space used: {used_total}({line[3]} WARN!!!),"
                    metrics = f"{metrics} {line[0]}_space_used={used_total}, {line[0]}_percentage_used={line[3]}"
                else:
                    metrics = f"{metrics} {line[0]}_space_used={used_total}, {line[0]}_percentage_used={line[3]}"
        elif command == "aggr status" and not "online" in str(line):
            error = error + 1
            name = f"{name} {line[0]} not online!!!, "
    #Si detectamos que el output del comando df -g parseado contiene warning o critical, devolvemos el correspondiente estado al servicio, sino, marcamos un OK y devolvemos el espacio usado.
    if len(output) == error:
        print("all is offline")
        sys.exit(2)
    elif command == "df -g" or command == "aggr status":
        if "CRIT" in name:
            print(f"have storage criticals: {name} | {metrics}")
            sys.exit(2)
        elif "WARN" in name:
            print(f"Have storage in warning: {name} | {metrics}")
            sys.exit(1)
        else:
            print(f"All storage OK | {metrics}")
            sys.exit(0)


#Funcion para hacer decrypt de la password de SSH
def decrypt_password(name):
    with open("key.fernet", "rb") as f:
        key = f.read()
        f.close()
    fernet = Fernet(key)
    with open(f"{name}.fernet", 'rb') as file:
        password = file.read()
    decrypted_password = fernet.decrypt(password)
    return decrypted_password.decode()

if __name__ == '__main__':
    password = decrypt_password("")
    #Argumento 1: comando, 2: ip
    execution = ssh_execution(sys.argv[1], sys.argv[2], password)
    get_result(sys.argv[1], execution)
