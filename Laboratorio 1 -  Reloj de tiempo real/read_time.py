from machine import Pin, I2C #Importamoslas librerias Pin e I2C
import utime #Importamos la librería utime para implementar delays

#Direccion I2C del reloj
RX8010SJ_ADDR = 0X32
#Direccion del registro que indica el tiempo
REG_TIME = 0X10

#Inicializar I2C
i2c = machine.I2C(1, scl = Pin(15), sda = Pin(14), freq = 200000)

#Main program
while 1:
    #Lee los valores de Seg, Min y Hora de los registros
    time = i2c.readfrom_mem(RX8010SJ_ADDR, REG_TIME, 3)
    
    #Converitmos los bytes en un string hexadecimal
    time_s = time.hex()[0:2] 
    time_m = time.hex()[2:4]
    time_h = time.hex()[4:6]
    
    #Imprimimos los valores en consola para formar la hora
    print(time_h, ":", time_m, ":", time_s)
    utime.sleep(0.5)