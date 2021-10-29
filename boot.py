import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
import dht 
from machine import Pin, PWM
from time import sleep
import utime
from hcsr04 import HCSR04

### Variables auxs
aux1 = 1
aux2 = 1
aux3 = 1
aux4 = 1
aux5 = 0
#######################Sensores##############################
PIR = Pin (4, Pin.IN)                 #Entrada del sensor PIR
sensordht11 = dht.DHT11(Pin(5))       #Entrada del sensor DHT11
medidor = HCSR04 (trigger_pin = 2 ,echo_pin = 0, echo_timeout_us = 10000)
#######################Actuadores##############################
ventilador = Pin(12,Pin.OUT)            #Salida del LED de DHT11
luminaria = Pin(13, Pin.OUT, value = 0)      #Salida del LED de PIR
bocina = Pin(14, Pin.OUT, value = 0)
led1 = Pin(16, Pin.OUT, value = 0)
#led2 = Pin(16, Pin.OUT, value = 0)

###################################################################3
ssid = 'TIGO-Tv'
password = '2NB144200821'
mqtt_server = '192.168.0.10'
client_id = 'EspLuis'
#########################  Suscripcione #################################
topic_sub = 'msg'   
topic_sub1 = 'Alerta1'
topic_sub2 = 'Pir'
topic_sub3 = 'Ultrasonico'
topic_sub4 = 'Led1'
topic_sub5 = 'Servo'
#########################  Publicaciones ################################
topic_pub = 'temp' 
topic_pub1 = 'alerta1'
topic_pub2 = 'pir'
topic_pub3 = 'ultrasonico'
topic_pub4 = 'led1'
topic_pub5 = 'servo'
topic_pub6 = 'ultra'
topic_pub7 = 'hum'
topic_pub8 = 'pir1'

last_message = 0
message_interval = 5
counter = 0
 
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
  pass
print('Conexion exitosa')
print(station.ifconfig())
