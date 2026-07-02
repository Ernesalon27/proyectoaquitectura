"""
boton.py
========
Maneja la lectura del botón físico con anti-rebote (debounce).
El botón usa pull-up interno, por lo tanto value() == 0 significa presionado.
"""

import machine
import utime
from config import PIN_BOTON, ANTIRREBOTE_BOTON, PAUSA_POST_BOTON

boton = machine.Pin(PIN_BOTON, machine.Pin.IN, machine.Pin.PULL_UP)


def boton_presionado():
    """
    Verifica si el botón fue presionado, aplicando anti-rebote.
    Devuelve True solo si la pulsación fue confirmada.
    """
    if boton.value() == 0:
        utime.sleep_ms(ANTIRREBOTE_BOTON)
        if boton.value() == 0:
            utime.sleep_ms(PAUSA_POST_BOTON)
            return True
    return False
