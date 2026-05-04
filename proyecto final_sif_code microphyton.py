from machine import Pin
import time

# --- CONFIGURACIÓN DE PINES ---
# Segmentos: A(GP9) a G(GP15)
pines_segmentos = [9, 10, 11, 12, 13, 14, 15]
segmentos = [Pin(p, Pin.OUT) for p in pines_segmentos]

# Control de transistores NPN
pin_unidades = Pin(8, Pin.OUT)
pin_decenas = Pin(7, Pin.OUT)

# Botones
btn_suma = Pin(6, Pin.IN, Pin.PULL_UP)
btn_resta = Pin(5, Pin.IN, Pin.PULL_UP)

# LEDs de Advertencia
led_verde = Pin(4, Pin.OUT)
led_amarillo = Pin(3, Pin.OUT)
led_rojo = Pin(2, Pin.OUT)

# --- MATRIZ CÁTODO COMÚN ---
numeros = [
    [1, 1, 1, 1, 1, 1, 0], # 0
    [0, 1, 1, 0, 0, 0, 0], # 1
    [1, 1, 0, 1, 1, 0, 1], # 2
    [1, 1, 1, 1, 0, 0, 1], # 3
    [0, 1, 1, 0, 0, 1, 1], # 4
    [1, 0, 1, 1, 0, 1, 1], # 5
    [1, 0, 1, 1, 1, 1, 1], # 6
    [1, 1, 1, 0, 0, 0, 0], # 7
    [1, 1, 1, 1, 1, 1, 1], # 8
    [1, 1, 1, 0, 0, 1, 1]  # 9
]

contador = 0
ultimo_suma = 1
ultimo_resta = 1
ultimo_debounce = 0

def escribir(n):
    for i in range(7):
        segmentos[i].value(numeros[n][i])

def limpiar():
    for s in segmentos:
        s.value(0)

# Función para controlar los LEDs según el valor
def actualizar_leds(valor):
    if valor < 10:
        led_verde.value(1)
        led_amarillo.value(0)
        led_rojo.value(0)
    elif 10 <= valor < 17:
        led_verde.value(0)
        led_amarillo.value(1)
        led_rojo.value(0)
    else: # De 17 en adelante (hasta 30)
        led_verde.value(0)
        led_amarillo.value(0)
        led_rojo.value(1)

print("Sistema con semáforo de advertencia listo.")

while True:
    tiempo_actual = time.ticks_ms()
    
    # 1. LÓGICA DE BOTONES
    lectura_suma = btn_suma.value()
    lectura_resta = btn_resta.value()
    
    if time.ticks_diff(tiempo_actual, ultimo_debounce) > 150:
        if lectura_suma == 0 and ultimo_suma == 1:
            contador += 1
            if contador > 20: contador = 0
            ultimo_debounce = tiempo_actual
        
        if lectura_resta == 0 and ultimo_resta == 1:
            contador -= 1
            if contador < 0: contador = 20
            ultimo_debounce = tiempo_actual
            
    ultimo_suma = lectura_suma
    ultimo_resta = lectura_resta
    
    # 2. ACTUALIZAR LEDS DE ADVERTENCIA
    actualizar_leds(contador)
    
    # 3. MULTIPLEXACIÓN DEL DISPLAY
    d = contador // 10
    u = contador % 10
    
    # Decenas
    escribir(d)
    pin_decenas.value(1)
    time.sleep_ms(5)
    pin_decenas.value(0)
    limpiar()
    
    # Unidades
    escribir(u)
    pin_unidades.value(1)
    time.sleep_ms(5)
    pin_unidades.value(0)
    limpiar()