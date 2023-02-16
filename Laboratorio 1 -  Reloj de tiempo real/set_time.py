from machine import Pin, I2C #Importamos las librerias Pin e I2C
import utime #Importamos la libreria utime para implementar delays

#Direccion I2C del reloj
RX8010SJ_ADDR = 0X32
#Direccion del registro que indica el tiempo
REG_TIME = 0X10

#Inicializar I2C
i2c = machine.I2C(1, scl = machine.Pin(15), sda = machine.Pin(14), freq = 200000)

#Main program
set_time = bytearray.fromhex('002111') #Convierte el string ('ssmmhh') a un bytearray
i2c.writeto_mem(RX8010SJ_ADDR, REG_TIME, set_time) #Escribe el bytearray en los registros

#Lee e imprime los valores de H, M y S de los registros
time = i2c.readfrom_mem(RX8010SJ_ADDR, REG_TIME, 3)
time_s = time.hex()[0:2]
time_m = time.hex()[2:4]
time_h = time.hex()[4:6]
print(time_h, ":", time_m, ":", time_s)