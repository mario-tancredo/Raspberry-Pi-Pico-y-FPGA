from machine import Pin, I2C #Importamos las librerias Pin e I2C
import utime #Importamos la libreria utime para implementar delays
import ustruct #Importamos la libreria ustruct para la conversion de datos
import sys #Importamos la libreria finalizar el codigo en caso haya algun error

#Dirección del I2C del acelerometro
MMA8452Q_ADDR = 0X1C

#Registros
REG_DEVID = 0X0D #Registro en el que se encuentra el ID
REG_POWER_CTL = 0X2A #Registro de control
REG_DATAX0 = 0X00 # Registro del Eje X

#Otras constantes
DEV_ID = 0x2A #ID del dispositivo
SENSITIVITY_2G = 1.0/1024 #(g/LSB)
EARTH_GRAVITY = 9.81 #gravedad en [m/s^2]

#Inicializar I2C
i2c = machine.I2C(1, scl = Pin(15), sda = Pin(14), freq = 200000)

def reg_write(i2c, addr, reg, data):
    #escribe bytes al registro especificado
    
    #Construir mensaje
    msg = bytearray()
    msg.append(data)
    
    #escribe el mensaje al registro
    i2c.writeto_mem(addr, reg, msg)

def reg_read(i2c, addr, reg, nbytes = 1):
    #Lee bytes del registro especificado,
    #si es mayor a 1 lee de registros consecutivos
    
    #Se asegura que se está solicitando 1 o más bytes
    if nbytes < 1:
        return bytearray()
    
    #Solicita data de los registros especificados
    data = i2c.readfrom_mem(addr, reg, nbytes)
    
    return data

#Main program

#Lee el ID del dispositivo para asegurarse de que es posible comunicarse con MMA8452Q
data = reg_read(i2c, MMA8452Q_ADDR, REG_DEVID)
if (data != bytearray((DEV_ID,))):
    print("ERROR: No se pudo comunicar con MMA8452Q")
    sys.exit()
    
#Lee el registro de Control
data = reg_read(i2c, MMA8452Q_ADDR, REG_POWER_CTL)
print(data)

#Pide al MMA8452Q empezar a tomar medidas estableciendo el bit de medicion a HIGH
data = int.from_bytes(data, "big") | 1
reg_write(i2c, MMA8452Q_ADDR, REG_POWER_CTL, data)

#Test: lee el registro de Power Control otra vez para asegurarse que el bit de medicion fue establecido
data = reg_read(i2c, MMA8452Q_ADDR, REG_POWER_CTL)
print(data)

#Espera antes de tomar medidas
utime.sleep(2.0)

#Ejecutar en bucle
while 1:
    #Lee los valores de X, Y y Z de los registros
    data = reg_read(i2c, MMA8452Q_ADDR, REG_DATAX0, 6)
    
    #Convertimos los bytes en un entero
    acc_x = ustruct.unpack_from("<h", data, 0)[0] / 16
    acc_y = ustruct.unpack_from("<h", data, 2)[0] / 16
    acc_z = ustruct.unpack_from("<h", data, 4)[0] / 16
    
    #Convertimos medidas a m/s^2
    acc_x = acc_x * SENSITIVITY_2G * EARTH_GRAVITY
    acc_y = acc_y * SENSITIVITY_2G * EARTH_GRAVITY
    acc_z = acc_z * SENSITIVITY_2G * EARTH_GRAVITY
    
    #Imprimir resultados
    print("X:", "{:.2f}".format(acc_x), \
          "| Y:", "{:.2f}".format(acc_y), \
          "| Z:", "{:.2f}".format(acc_z))
    utime.sleep(0.1)










