import hpilo
import json
import re
import sys
#Script used for request the status and events of ILO.
def getiloinfo(host, user, password):
    #Define vars.
    statusexit = 0
    #Define connection vs Ilo and get status of components.
    ilo = hpilo.Ilo(host, user, password)
    chassis = str(ilo.get_embedded_health())
    #Split the result of the command execution.
    chassis = chassis.split(",")
    #Travel the result and if the line have the status, save status in var, if the var is not OK we change the exit for get critical in Check MK.
    for line in chassis:
        if "bios_hardware" in line:
            line = re.sub("}","", line)
            bios_hardware = line.split(':')[3]
            if("OK" not in bios_hardware):
                statusexit = 2
        if "'fans': {'status'" in line:
            line = re.sub("}","", line)
            fans = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
        if "'temperature': {'status'" in line:
            line = re.sub("}","", line)
            temperature = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
        if "'power_supplies': {'status" in line:
            line = re.sub("}","", line)
            power_supplies = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
        if "'battery': {'status" in line:
            line = re.sub("}","", line)
            battery = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
        if "'processor': {'status" in line:
            line = re.sub("}","", line)
            processor = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
        if "'memory': {'status" in line:
            line = re.sub("}","", line)
            memory = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
        if "'network': {'status" in line:
            line = re.sub("}","", line)
            network = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
        if "'storage': {'status" in line:
            line = re.sub("}","", line)
            storage = line.split(':')[2]
            if("OK" not in fans):
                statusexit = 2
    #Print all info for see in the description of Check MK service and we close the script whit the status exit (0 for OK, 2 for critical)
    print("bios_hardware:" + bios_hardware + ", fans:"+ fans + ", temperature:" + temperature + ", power_supplies:" + power_supplies + ", battery:" + battery + ", processor:" + processor + ", memory:" + memory + ", network:" + network + ", storage:" + storage)
    sys.exit(statusexit)

if __name__ == "__main__":
    #We start the script and get the 3 variables from Check MK rule.
    getiloinfo(sys.argv[1], sys.argv[2], sys.argv[3])