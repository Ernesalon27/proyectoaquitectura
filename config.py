"""
config.py
=========
Configuración centralizada del proyecto: pines de hardware,
calibración de sensores y tiempos usados por el resto de módulos.

Modificar aquí si cambian los pines físicos o si se necesita
recalibrar los sensores de humedad.
"""

# ==========================================
# PINES DE HARDWARE
# ==========================================
PIN_SENSOR1 = 27   # ADC0 - Sensor de humedad 1
PIN_SENSOR2 = 26   # ADC1 - Sensor de humedad 2
PIN_RELE = 16      # GPIO16 - Módulo relé que controla la bomba
PIN_BOTON = 15     # GPIO15 - Botón con pull-up interno

# ==========================================
# CALIBRACIÓN DE SENSORES DE HUMEDAD
# ==========================================
# VALOR_SECO: lectura ADC con el sensor al aire / tierra seca
# VALOR_HUMEDO: lectura ADC con el sensor en agua / tierra húmeda
# Ajustar estos valores según las pruebas físicas de cada sensor.
VALOR_SECO = 65535
VALOR_HUMEDO = 20000

# ==========================================
# TIEMPOS DE CONTROL (en milisegundos)
# ==========================================
INTERVALO_LECTURA = 10000     # Cada cuánto se imprime la humedad en el shell
DURACION_BOMBA = 5000         # Cuánto tiempo permanece encendida la bomba
ANTIRREBOTE_BOTON = 50        # Anti-rebote al detectar el botón presionado
PAUSA_POST_BOTON = 300        # Pausa tras activar el botón (evita múltiples disparos)
DESCANSO_RELE = 200           # Pausa eléctrica tras apagar el relé
PAUSA_CICLO = 20              # Pausa mínima del bucle principal
INTERVALO_UBIDOTS = 10000     # Cada cuánto se envían datos a Ubidots

# ==========================================
# WIFI
# ==========================================
WIFI_SSID = "NOMBRE_DE_TU_RED"
WIFI_PASSWORD = "CONTRASEÑA_DE_TU_RED"

# ==========================================
# UBIDOTS
# ==========================================
# Token de tu cuenta Ubidots (Perfil -> API Credentials)
UBIDOTS_TOKEN = "BBUS-Cf2TbDrAyH0DF7wkCg6hJcyOBtsus6"
# Label del device creado en Ubidots (ej: "pico-riego")
UBIDOTS_DEVICE_LABEL = "pico-riego"
UBIDOTS_URL = "https://stem.ubidots.com/api/v1.6/devices/{}".format(UBIDOTS_DEVICE_LABEL)
