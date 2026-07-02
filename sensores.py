"""
sensores.py
===========
Encapsula la lectura de los sensores de humedad de tierra y el
cálculo del porcentaje de humedad a partir de las lecturas crudas del ADC.
"""

import machine
from config import PIN_SENSOR1, PIN_SENSOR2, VALOR_SECO, VALOR_HUMEDO

sensor1 = machine.ADC(PIN_SENSOR1)
sensor2 = machine.ADC(PIN_SENSOR2)


def obtener_porcentaje_humedad():
    """
    Lee ambos sensores, promedia sus valores crudos y devuelve
    el porcentaje de humedad de la tierra, acotado entre 0 y 100.
    """
    lectura1 = sensor1.read_u16()
    lectura2 = sensor2.read_u16()
    promedio_crudo = (lectura1 + lectura2) / 2

    porcentaje = ((VALOR_SECO - promedio_crudo) / (VALOR_SECO - VALOR_HUMEDO)) * 100

    if porcentaje > 100:
        porcentaje = 100
    if porcentaje < 0:
        porcentaje = 0

    return int(porcentaje)
