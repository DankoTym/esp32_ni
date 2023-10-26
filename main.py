# Tymcziszyn Danko M.
# Curso IOT 2023

from machine import Pin, Timer, unique_id
import dht
import time
import json
import ubinascii
from collections import OrderedDict
from settings import SERVIDOR_MQTT
from umqtt.robust import MQTTClient

CLIENT_ID = ubinascii.hexlify(unique_id()).decode('utf-8')


mqtt = MQTTClient(CLIENT_ID, SERVIDOR_MQTT,
                  port=8883, keepalive=10, ssl=True)

led = Pin(2, Pin.OUT)
d = dht.DHT22(Pin(25))
contador = 0
registro_temp = 0
bandera=0

def heartbeat(nada):
    global contador
    if contador > 5:
        contador = 0
        return
    led.value(not led.value())
    contador += 1
  
def transmitir(pin):
    print("publicando")
    mqtt.connect()
    mqtt.publish(f"iot/{CLIENT_ID}",datos)
    mqtt.disconnect()


while True:
    try:
        d.measure()
        temperatura = d.temperature()
        registro_temp = temperatura
        humedad = d.humidity()
        datos = json.dumps(OrderedDict([
            ('Temperatura',temperatura),
            ('humedad',humedad)
        ]))

        if temperatura >= 25.0 and bandera == 0:        # Establecí 25°C como temperatura superior a partir de la cual notifica.
            bandera = 1
            transmitir(datos)

        if temperatura<22.0:                            # Reinicia la bandera al bajar de 22°C.
            bandera = 0

        print(datos)
    except OSError as e:
        print("sin sensor")
    time.sleep(5)
