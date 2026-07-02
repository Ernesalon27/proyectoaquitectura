"""
wifi.py
=======
Conecta la Raspberry Pi Pico W a la red WiFi configurada en config.py.
Necesario antes de poder enviar datos a Ubidots.
"""

import network
import utime
from config import WIFI_SSID, WIFI_PASSWORD


def conectar_wifi(timeout_ms=15000):
    """
    Conecta el Pico W a la red WiFi.
    Devuelve True si logró conectar antes de timeout_ms, False si no.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print(">> WiFi ya conectado:", wlan.ifconfig()[0])
        return True

    print(">> Conectando a WiFi: {}...".format(WIFI_SSID))
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    inicio = utime.ticks_ms()
    while not wlan.isconnected():
        if utime.ticks_diff(utime.ticks_ms(), inicio) >= timeout_ms:
            print(">> ERROR: No se pudo conectar al WiFi (timeout)")
            return False
        utime.sleep_ms(200)

    print(">> WiFi conectado. IP:", wlan.ifconfig()[0])
    return True
