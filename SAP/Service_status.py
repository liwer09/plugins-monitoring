import subprocess
#Creamos variables necesarias.
final_status = 0
final_output = ""

#Ejecutamos el comando para ver el estado de la instancia
def get_data(instance):
    cmd = subprocess.Popen([f"su - USUARIO_SAP -c 'sapcontrol -nr {instance} -function GetProcessList'"], stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    string = stdout.decode().splitlines()
    output, status = process_output(string, instance)
    print(output)
    return(output, status)

#Procesamos el output del comando anterior y buscamos que no haya nada que no este en GREEN, ya que si no esta en estos estados debe de saltar un criticla.  
def process_output(string, instance):
    diccionario = {}
    status = 0
    #Buscamos el estado de los servicios.
    for i in string:
        #Si esta en GREEN, añadimos al diccionario el nombre del servicio de SAP y el status.
        if "GREEN" in str(i):
            i = i.split(", ")
            diccionario[i[0]] = i[2]
        #Si esta en GREY o STOP se marca el status 2 para hacer saltar un critical y añadimos al diccionario el nombre del servicio de SAP y el status.
        elif "GREY" in str(i) or "STOP" in str(i):
            i = i.split(", ")
            diccionario[i[0]] = i[2]
            status = 2
    output = f"Instancia {instance}: "
    for clave, valor in diccionario.items():
        output = f"{output}{clave} : {valor}, "
    if not "GREEN" in str(output) and not "GREY" in str(output):
        return("", status)
    else:
        return(output, status)
    
if __name__ == "__main__":
    for i in "00", "01", "02":
        output, status = get_data(i)
        final_output = final_output + output
        if status == 1:
            final_status = status
    print(f'{final_status} "SAP service status" - {final_output}')
        