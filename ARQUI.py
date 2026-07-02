import machine
import utime

# ==========================================
# CONFIGURACIÓN DE HARDWARE
# ==========================================

# Sensores analógicos
sensor1 = machine.ADC(27)
sensor2 = machine.ADC(26)

# Configuración del Relé (Inicia en HIGH/1 para que comience APAGADO)
rele = machine.Pin(16, machine.Pin.OUT, value=1) 

# Configuración del Botón con Pull-Up interno
boton = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# Espera de estabilidad inicial al encender la placa
utime.sleep_ms(500)
print("--- Sistema Iniciado Correctamente ---")

# ==========================================
# VARIABLES DE CONTROL Y CALIBRACIÓN
# ==========================================
# Restamos 10000 para que la primera lectura de humedad se imprima inmediatamente al iniciar
ultimo_envio_shell = utime.ticks_ms() - 10000  
bomba_activa = False
tiempo_encendido_bomba = 0

# Calibración de los sensores (Ajustar si es necesario)
VALOR_SECO = 65535 
VALOR_HUMEDO = 20000 

def obtener_porcentaje_humedad():
    lectura1 = sensor1.read_u16()
    lectura2 = sensor2.read_u16()
    promedio_crudo = (lectura1 + lectura2) / 2
    
    # Cálculo del porcentaje
    porcentaje = ((VALOR_SECO - promedio_crudo) / (VALOR_SECO - VALOR_HUMEDO)) * 100
    
    # Limitar el rango entre 0% y 100%
    if porcentaje > 100: porcentaje = 100
    if porcentaje < 0: porcentaje = 0
    return int(porcentaje)

# ==========================================
# BUCLE PRINCIPAL
# ==========================================
while True:
    tiempo_actual = utime.ticks_ms()
    
    # 1. MOSTRAR HUMEDAD EN EL SHELL (Cada 10 segundos exactos)
    if utime.ticks_diff(tiempo_actual, ultimo_envio_shell) >= 10000:
        humedad_actual = obtener_porcentaje_humedad()
        print("El porcentaje de humedad en la tierra es: {}%".format(humedad_actual))
        ultimo_envio_shell = tiempo_actual

    # 2. LÓGICA DEL BOTÓN (Encender bomba)
    if boton.value() == 0 and not bomba_activa:
        utime.sleep_ms(50) # Anti-rebote para confirmar que se presionó el botón
        if boton.value() == 0:
            rele.value(0) # 0 ENCIENDE la bomba (Lógica inversa)
            bomba_activa = True
            tiempo_encendido_bomba = tiempo_actual
            print(">> BOMBA ENCENDIDA por botón (Duración: 5s)")
            
            # Pausa para evitar lecturas repetidas si dejas el dedo puesto
            utime.sleep_ms(300) 

    # 3. CONTROL DE TIEMPO DE LA BOMBA (Apagar tras 5 segundos)
    if bomba_activa:
        if utime.ticks_diff(tiempo_actual, tiempo_encendido_bomba) >= 5000:
            rele.value(1) # 1 APAGA la bomba
            bomba_activa = False
            print(">> BOMBA APAGADA automáticamente")
            utime.sleep_ms(200) # Breve descanso eléctrico

    # Pausa mínima de control para que el procesador no trabaje al 100% en vacío
    utime.sleep_ms(20)