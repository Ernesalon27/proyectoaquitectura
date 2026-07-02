"""
ubidots.py
==========
Envía las variables del proyecto (humedad, estado de la bomba) a Ubidots
mediante HTTP POST usando la librería urequests.

IMPORTANTE: urequests no viene incluido por defecto en MicroPython.
Instalarlo una vez desde el REPL del Pico W (ya conectado a WiFi):

    import mip
    mip.install("urequests")

O copiarlo manualmente con Thonny (Tools > Manage Packages).
"""

import urequests
from config import UBIDOTS_URL, UBIDOTS_TOKEN


def enviar_datos(humedad, bomba_activa):
    """
    Envía el porcentaje de humedad y el estado de la bomba (0/1) a Ubidots.
    No detiene el programa si falla: solo imprime el error, para que el
    bucle principal siga funcionando aunque se caiga el WiFi un momento.
    """
    payload = {
        "humedad": humedad,
        "bomba": 1 if bomba_activa else 0
    }
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        respuesta = urequests.post(UBIDOTS_URL, json=payload, headers=headers)
        print(">> Datos enviados a Ubidots:", payload, "- status:", respuesta.status_code)
        respuesta.close()
    except Exception as error:
        print(">> ERROR enviando a Ubidots:", error)
