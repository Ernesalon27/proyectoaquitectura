"""
bomba.py
========
Controla el módulo relé que enciende y apaga la bomba de agua.

Lógica inversa del relé:
    rele.value(0) -> ENCIENDE la bomba
    rele.value(1) -> APAGA la bomba (estado inicial)
"""

import machine
import utime
from config import PIN_RELE, DURACION_BOMBA, DESCANSO_RELE

rele = machine.Pin(PIN_RELE, machine.Pin.OUT, value=1)  # Inicia apagado

_bomba_activa = False
_tiempo_encendido = 0


def encender_bomba(tiempo_actual):
    """Enciende la bomba y registra el instante de encendido."""
    global _bomba_activa, _tiempo_encendido
    rele.value(0)
    _bomba_activa = True
    _tiempo_encendido = tiempo_actual
    print(">> BOMBA ENCENDIDA por botón (Duración: {}s)".format(DURACION_BOMBA // 1000))


def actualizar_bomba(tiempo_actual):
    """
    Debe llamarse en cada ciclo del bucle principal.
    Apaga automáticamente la bomba si ya se cumplió DURACION_BOMBA.
    """
    global _bomba_activa
    if _bomba_activa:
        if utime.ticks_diff(tiempo_actual, _tiempo_encendido) >= DURACION_BOMBA:
            rele.value(1)
            _bomba_activa = False
            print(">> BOMBA APAGADA automáticamente")
            utime.sleep_ms(DESCANSO_RELE)


def bomba_esta_activa():
    """Devuelve True si la bomba está actualmente encendida."""
    return _bomba_activa
