import network
import time
from umqtt.simple import MQTTClient
from machine import Pin
from gpio_lcd import GpioLcd

led = Pin("LED", Pin.OUT)

ssid = "Nombre de la red"
password = "contraseña de la red"

mqtt_server = "test.mosquitto.org"
topic_test = b"picowdiego/test"

#Creamos el objeto LCD
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)

def wlan_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Esperando conexion...')
        lcd.move_to(0, 0)
        lcd.putstr('Esperando')
        lcd.move_to(0, 1)
        lcd.putstr('conexion...')
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('Fallo de conexion')
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Fallo de conexion')
    else:
        print('Conectado')
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Conectado')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
        lcd.move_to(0, 1)
        lcd.putstr('ip=' + status[0])

def callback(topic, msg):
    global mensaje
    mensaje = msg.decode('utf-8')
    print("Mensaje recibido")
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Mensaje recibido")
    print(msg.decode('utf-8'))
    lcd.move_to(0, 1)
    lcd.putstr(msg.decode('utf-8'))


def mqtt_connect():
    #Creamos el cliente
    client = MQTTClient(client_id = "picow_board_1", # Escogemos el nombre que queramos para el cliente
                        server = mqtt_server,        # Direción del servidor
                        port = 1883,                 # Puerto
                        user = None,                 # Usuario (en caso el servidor lo requiera)
                        password = None,             # Contraseña (en case el servidor lo requiera)
                        keepalive = 3600,            # Maximo número de segundos entre mensajes
                        ssl = False,                 #Configuración de ssl
                        ssl_params = {})
    client.connect()              #Conectar el cliente al servidor       
    client.set_callback(callback) #Establecemos nuestra función callback como callback del mensaje
    client.subscribe(topic_test)  #suscribimos al Pico W al tópico especificado
    return(client)

wlan_connect()
time.sleep(3)
client = mqtt_connect()

while True:
    print('Esperando mensaje...')
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr('Esperando')
    lcd.move_to(0, 1)
    lcd.putstr('mensaje...')
    client.wait_msg()
    if mensaje == "on":
        led.on()
    elif mensaje == "off":
        led.off()
    time.sleep(1)