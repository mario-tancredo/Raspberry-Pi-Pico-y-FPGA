from machine import Pin, I2C
import utime
import ustruct
import sys

#I2C address
MMA8452Q_ADDR = 0X1C

#Registros
REG_DEVID = 0X0D
REG_POWER_CTL = 0X2A
REG_DATAX0 = 0X00

#Otras constantes
DEV_ID = 0x2A
SENSITIVITY_2G = 1.0/1024
EARTH_GRAVITY = 9.81

#Inicializar I2C with pins
i2c = machine.I2C(1, scl = machine.Pin(15), sda = machine.Pin(14), freq = 400000)

x0 = Pin(0, Pin.OUT)
x1 = Pin(1, Pin.OUT)
x2 = Pin(2, Pin.OUT)

y0 = Pin(3, Pin.OUT)
y1 = Pin(4, Pin.OUT)
y2 = Pin(5, Pin.OUT)

def reg_write(i2c, addr, reg, data):
    #escribe bytes al registro especificado
    
    #Construir mensaje
    msg = bytearray()
    msg.append(data)
    
    #escribe el mensaje al registro
    i2c.writeto_mem(addr, reg, msg)

def reg_read(i2c, addr, reg, nbytes = 1):
    
    #Lee bytes del registro especificado, si es mayor a 1 lee de registros consecutivos
    
    #Se asegura que se está solicitando 1 o más bytes
    if nbytes < 1:
        return bytearray()
    
    #Solicita data de los registros especificados en I2C
    data = i2c.readfrom_mem(addr, reg, nbytes)
    
    return data

#Main program

#Lee el ID del dispositivo para asegurarse de que es posible comunicarse con MMA8452Q
data = reg_read(i2c, MMA8452Q_ADDR, REG_DEVID)
if (data != bytearray((DEV_ID,))):
    print("ERROR: No se pudo comunicar con MMA8452Q")
    sys.exit()
    
#Lee el registro de Power Control
data = reg_read(i2c, MMA8452Q_ADDR, REG_POWER_CTL)
print(data)

#Pide al MMA8452Q empezar a tomar medidas estableciendo el bit de medicion a HIGH
data = int.from_bytes(data, "big") | (1<<0)
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
    
    ball_x = int(acc_x)
    ball_y = int(acc_y)
    ball_z = int(acc_z)
    
    if ball_x < -2:
        x2.value(0); x1.value(0); x0.value(0)
    elif ball_x == -2:
        x2.value(0); x1.value(0); x0.value(1)
    elif ball_x == -1:
        x2.value(0); x1.value(1); x0.value(0)
    elif ball_x == -0:
        x2.value(0); x1.value(1); x0.value(1)
    elif ball_x == 1:
        x2.value(1); x1.value(0); x0.value(0)
    elif ball_x == 2:
        x2.value(1); x1.value(0); x0.value(1)
    else:
        x2.value(1); x1.value(1); x0.value(0)
    
    if ball_y < -2:
        y2.value(0); y1.value(0); y0.value(0)
    elif ball_y == -2:
        y2.value(0); y1.value(0); y0.value(1)
    elif ball_y == -1:
        y2.value(0); y1.value(1); y0.value(0)
    elif ball_y == -0:
        y2.value(0); y1.value(1); y0.value(1)
    elif ball_y == 1:
        y2.value(1); y1.value(0); y0.value(0)
    elif ball_y == 2:
        y2.value(1); y1.value(0); y0.value(1)
    else:
        y2.value(1); y1.value(1); y0.value(0)
        
    #Imprimir resultados
    print("X:", "{:.2f}".format(ball_x), \
          "| Y:", "{:.2f}".format(ball_y), \
          "| Z:", "{:.2f}".format(ball_z))
    
    utime.sleep(0.1)





