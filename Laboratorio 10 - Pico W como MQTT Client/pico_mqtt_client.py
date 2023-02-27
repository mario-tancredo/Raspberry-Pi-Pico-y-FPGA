import network
import time
from umqtt.simple import MQTTClient

ssid = "Nombre de la red"
password = "contraseña de la red"

mqtt_server = "test.mosquitto.org"
topic_test = b"picowboard/test"

def wlan_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('esperando conexion...')
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('fallo de conexion')
    else:
        print('conectado')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

def callback(topic, msg):
    print("Mensaje recibido")
    print(msg.decode('utf-8'))

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
print('Esperando mensaje...')
client.wait_msg()