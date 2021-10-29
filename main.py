servo = PWM(Pin(15))
servo.freq(50)
servo.init()

def sub_cb(topic, msg):
  Mensaje = msg
  Topico = topic
  print((topic, msg))
  if Mensaje == b'calor' and Topico == b'Alerta1':
      print('Ventilador encendido')
      ventilador.value(1)
  elif Mensaje == b'frio' and Topico == b'Alerta1':
      print('Ventilador apagado')
      ventilador.value(0)
      
  elif Mensaje == b'movimiento' and Topico == b'Pir':
      print('Luminaria exterior encendida')
      luminaria.value(1)
      
  elif Mensaje == b'vacio' and Topico == b'Pir':
      print('Luminaria exterior apagada')
      luminaria.value(0)
      
  elif Mensaje == b'cerca' and Topico == b'Ultrasonico':
      print('Alarma encendida')
      bocina.value(1)
  elif Mensaje == b'lejos' and Topico == b'Ultrasonico':
      print('Alarma apagada')
      bocina.value(0)
      
  elif Mensaje == b'ON' and Topico == b'Led1':
      print('Luz sala encendida')
      led1.value(1)
  elif Mensaje == b'OFF' and Topico == b'Led1':
      print('Luz sala apagada')
      led1.value(0)
      
  elif Mensaje == b'Abierta' and Topico == b'Servo':
      d = 90 
      servo.duty(d)
      tSleep = (d/1023)*20
      time.sleep(tSleep)
      print('Talanquera abierta')
      #luminaria.value(0)
  elif Mensaje == b'Cerrada' and Topico == b'Servo':
      c = 45
      servo.duty(c)
      tSleep = (c/1023)*20
      time.sleep(tSleep)
      print('Talanquera cerrada')
      #bocina.value(1)

  else:
      print('Sin cambios')
      
   
def sub_cb1(topic, msg):
  venti = msg
  print((topic, msg))
  print(len(venti))

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  client.subscribe(topic_sub1)
  client.subscribe(topic_sub2)
  client.subscribe(topic_sub3)
  client.subscribe(topic_sub4)
  client.subscribe(topic_sub5)
  print('Conectado a %s MQTT broker, suscrito a los topicos' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Error al conectarse a MQTT broker. Reconectando...')
  time.sleep(10)
  machine.reset()



def midePromedio():
    suma=0
    for i in range (0,16):
        distancia = medidor.distance_cm ()
        sleep (0.1)
        if (distancia > 0):
            suma+=distancia
    return suma/16

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

############################################################################

while True:
  try:
    client.check_msg()
  except OSError as e:
    restart_and_reconnect()



##   
  sleep (1)
  sensordht11.measure ()
  temp = sensordht11.temperature ()
  hum = sensordht11.humidity()
  temp = str(temp)
  hum = str(hum)
  client.publish(topic_pub, temp)
  client.publish(topic_pub7, hum)
  #print(hum) 

##
  if (PIR.value()==1):
      if aux2 == 1:
          mov = 'Uno'
          client.publish(topic_pub2, mov)
          aux1 = 1
          aux2 = aux2 + 1
          aux5 = aux5 + 1
          aux6 = str(aux5)
          client.publish(topic_pub8, aux6)
      
  elif (PIR.value()==0):
      if aux1 == 1:
          mov = 'Cero'
          client.publish(topic_pub2, mov)
          aux1 = aux1 + 1
          aux2 = 1

##
  prox=midePromedio()
  prox1 = str(prox)
  client.publish(topic_pub6, prox1)
  #print ("Distancia = ", prox)
  if prox <= 2.20:
      if aux3 == 1:
          distancia = 'Cuidado'
          client.publish(topic_pub3, distancia)
          aux4 = 1
          aux3 = aux2 + 1
          
          
          
  elif prox > 2.20:
      if aux4 == 1:
          distancia = 'Ok'
          client.publish(topic_pub3, distancia)
          aux4 = aux4 +1
          aux3 = 1
##
