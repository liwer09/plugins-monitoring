#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#move the plugin to the folder /opt/omd/sites/nameofsite/local/lib/check_mk/base/plugins/agent_based
#chown in the script for the user site (name of site)
#execute in OMD "cmk --debug -I --detect-plugins=nameofplugin -v"
#Executi in OMD "cmk -O" for apply changes
from .agent_based_api.v1 import *
import re
import pprint




def discover_certificate_signing(section):
    yield Service(item="Caducidad ADFS Signing certificado")

def check_certificate_signing(item, section):
    valor = ""
    for i in section:
        for a in i:
            valor = str(valor) + str(a) + " " 
    if "Caducidad ADFS Signing certificado" in str(item):
        if "Crit" in str(valor):
            yield Result(state = State.CRIT, summary = f"{str(valor)}")
            return
        elif "Warn" in str(valor):
            yield Result(state = State.WARN, summary = f"{str(valor)}")
            return
        else:
            yield Result(state = State.OK, summary = f"{str(valor)}")
            return

register.agent_section(
    name = "ADFS_Signing",
)

register.check_plugin(
    name="ADFS_Signing",
    service_name="%s",
    discovery_function = discover_certificate_signing,
    check_function=check_certificate_signing,
)
