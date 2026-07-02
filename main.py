"""
main.py
=======
Punto de entrada del sistema de riego automatizado.
Orquesta los módulos de sensores, bomba y botón dentro del bucle principal.

Flujo:
    1. Cada INTERVALO_LECTURA ms, imprime el % de humedad en el shell.
    2. Si se presiona el botón y la bomba está apagada, la enciende.
    3. En cada ciclo, revisa si la bomba debe apagarse automáticamente.
"""

import utime
from config import INTERVALO_LECTURA, PAUSA_CICLO
from sensores import obtener_porcentaje_humedad
from bomba import encender_bomba, actualizar_bomba, bomba_esta_activa
from boton import boton_presionado

# Espera de estabilidad inicial al encender la placa
utime.sleep_ms(500)
print("--- Sistema Iniciado Correctamente ---")

# Restamos INTERVALO_LECTURA para que la primera lectura se imprima de inmediato
ultimo_envio_shell = utime.ticks_ms() - INTERVALO_LECTURA

while True:
    tiempo_actual = utime.ticks_ms()

    # 1. Mostrar humedad en el shell
    if utime.ticks_diff(tiempo_actual, ultimo_envio_shell) >= INTERVALO_LECTURA:
        humedad_actual = obtener_porcentaje_humedad()
        print("El porcentaje de humedad en la tierra es: {}%".format(humedad_actual))
        ultimo_envio_shell = tiempo_actual

    # 2. Lógica del botón (encender bomba)
    if boton_presionado() and not bomba_esta_activa():
        encender_bomba(tiempo_actual)

    # 3. Control de tiempo de la bomba (apagado automático)
    actualizar_bomba(tiempo_actual)

    # Pausa mínima de control
    utime.sleep_ms(PAUSA_CICLO)
