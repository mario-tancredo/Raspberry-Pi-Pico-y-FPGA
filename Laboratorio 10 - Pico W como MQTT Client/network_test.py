import network
import time

ssid = "Nombre de la red"
password = "contraseña de la red"

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
