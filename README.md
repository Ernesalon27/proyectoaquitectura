Sistema de Riego Automatizado con Raspberry Pi Pico W

Proyecto de agricultura de precisión de bajo costo. Monitorea la humedad de la
tierra con dos sensores analógicos y permite activar una bomba de agua de
forma manual (botón físico) durante un tiempo controlado, además de reportar
el porcentaje de humedad periódicamente por consola.

Estructura del proyecto

```
proyecto_riego/
├── main.py          Punto de entrada, orquesta el bucle principal
├── config.py         Pines, calibración y tiempos
├── sensores.py        Lectura y cálculo del % de humedad
├── bomba.py           Control del relé / bomba de agua
├── boton.py            Lectura del botón con anti-rebote
└── diagram.json         Diagrama de simulación para Wokwi
```

Descripción de cada módulo
`config.py`
Centraliza toda la configuración del proyecto: número de pines usados,
valores de calibración de los sensores (`VALOR_SECO` y `VALOR_HUMEDO`) y los
tiempos del sistema (intervalo de lectura, duración de la bomba, anti-rebote,
etc.). Es el único archivo que normalmente hay que tocar si cambia el
hardware o se necesita recalibrar.

`sensores.py`
Inicializa los dos ADC (`sensor1`, `sensor2`) y expone
`obtener_porcentaje_humedad()`, que promedia ambas lecturas crudas y las
convierte a un porcentaje de 0 a 100 usando los valores de calibración de
`config.py`.

`bomba.py`
Controla el relé que enciende/apaga la bomba. Nótese la **lógica inversa**:
`rele.value(0)` enciende y `rele.value(1)` apaga (así viene el relé al
iniciar). Expone tres funciones:
- `encender_bomba(tiempo_actual)`: enciende y guarda el instante de encendido.
- `actualizar_bomba(tiempo_actual)`: debe llamarse en cada ciclo; apaga la
  bomba automáticamente al cumplirse `DURACION_BOMBA`.
- `bomba_esta_activa()`: consulta el estado actual.

`boton.py`
Lee el botón (con pull-up interno, así que presionado = `0`) aplicando
anti-rebote por software. `boton_presionado()` devuelve `True` solo si la
pulsación fue confirmada tras el retardo de anti-rebote.

`main.py`
Importa los demás módulos y ejecuta el bucle principal:
1. Cada `INTERVALO_LECTURA` ms imprime el porcentaje de humedad.
2. Si se presiona el botón y la bomba está apagada, la enciende.
3. En cada vuelta del bucle revisa si la bomba debe apagarse sola.

`diagram.json`
Diagrama de conexiones para simular el circuito en [Wokwi](https://wokwi.com):
Raspberry Pi Pico W + dos potenciómetros (simulan los sensores de humedad),
un módulo relé y un pulsador.

Instrucciones de armado (hardware físico)

Materiales
- 1x Raspberry Pi Pico W
- 2x Sensores de humedad de suelo (salida analógica)
- 1x Módulo relé de 1 canal (5V)
- 1x Mini bomba de agua sumergible (5V)
- 1x Pulsador (push-button)
- Cables jumper (macho-macho y macho-hembra)
- Protoboard
- Fuente de alimentación externa para la bomba (según su consumo)

 Conexiones

| Componente          | Pin del sensor/módulo | Pin en el Pico W |
|----------------------|------------------------|-------------------|
| Sensor de humedad 1  | VCC                     | 3V3                |
|                       | GND                     | GND                |
|                       | AOUT (señal)            | GP27 (ADC1)        |
| Sensor de humedad 2  | VCC                     | 3V3                |
|                       | GND                     | GND                |
|                       | AOUT (señal)            | GP26 (ADC0)        |
| Módulo relé          | VCC                     | VBUS (5V)          |
|                       | GND                     | GND                |
|                       | IN                      | GP16               |
| Bomba de agua        | Terminal +/−            | Salida del relé (NO + COM), alimentada por fuente externa |
| Pulsador             | Pata 1                  | GP15               |
|                       | Pata 2                  | GND                |

- Importante: la bomba no se alimenta directamente desde el Pico W.
- Se conecta a través del relé, usando una fuente externa adecuada a su
- voltaje/corriente, para no dañar la placa.

Pasos para armar y ejecutar

1. Instalar MicroPython en la Raspberry Pi Pico W (firmware `.uf2` desde
   [micropython.org](https://micropython.org/download/RPI_PICO_W/)).
2. Conectar todos los componentes según la tabla de conexiones anterior.
3. Copiar los 5 archivos `.py` del proyecto a la Pico W usando Thonny (o
   `mpremote`/`rshell`), manteniendo `main.py` en la raíz del sistema de
   archivos (así se ejecuta automáticamente al encender la placa).
4. Conectar la Pico W por USB a la computadora y abrir el monitor
   serie/shell de Thonny para ver los mensajes de humedad.
5. Presionar el botón físico para activar la bomba durante 5 segundos; se
   apagará sola automáticamente.
6. (Opcional) Ajustar `VALOR_SECO` y `VALOR_HUMEDO` en `config.py` según las
   lecturas reales obtenidas con el sensor al aire y en agua.

Simulación sin hardware físico

Si solo se quiere probar la lógica sin armar el circuito, se puede cargar
`diagram.json` junto con los archivos `.py` en un proyecto de
[Wokwi](https://wokwi.com/projects/new/micropython-pi-pico-w), reemplazando
los sensores reales por los potenciómetros del diagrama para simular
distintos niveles de humedad.
