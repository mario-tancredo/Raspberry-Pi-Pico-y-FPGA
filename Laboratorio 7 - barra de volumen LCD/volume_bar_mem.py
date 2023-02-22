from machine import Pin
from gpio_lcd import GpioLcd
import utime

#Declaramos las entradas
boton_down = Pin(0, Pin.IN)
boton_up = Pin(1, Pin.IN)

#Variables del display
bar_size = 0 #Tamaño de la barra
volume = 0.00 #Porcentaje de volumen

#Dirección y registro de la memoria
EEPROM_ADDR = 0X50 #Direccion I2C de la memoria
REG_DATA = 0X00 #Direccion del registro dentro de la memoria

#Inicializamos la comunicacion con los perifericos
i2c = machine.I2C(1, scl = Pin(15), sda = Pin(14), freq = 200000)

#Inicializamos el display LCD
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)

#Funciones de lectura y escritura por I2C
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
    
    #Solicita data de los registros especificados en I2C
    data = i2c.readfrom_mem(addr, reg, nbytes)
    
    return data

#Main porgram
mem = reg_read(i2c, EEPROM_ADDR, REG_DATA) #Lee el tamaño de la barra guardado en la memoria
bar_size = int.from_bytes(mem, "big") #Asigna a la barra el valor guardado en memoria
volume = bar_size * 6.25              #Asigna el porcentaje de volumen de acuerdo al tamaño de la barra

#Escribe el porcentaje
lcd.move_to(0, 1) #Mueve el cursor a (0, 1)
lcd.putstr(str("{:.2f}".format(volume)) + "%  ") #Imprime el porcentaje de volumen
lcd.move_to(0, 0) #Regresa el cursor a (0, 0)

#Dibuja la barra al tamaño correspondiente
for i in range(0, bar_size):
    lcd.putchar(chr(219)) #Imprime un cuadrado


while True:
    if (boton_up.value() == 1 and boton_down.value() == 0):
        if (bar_size < 16):
            #Aumenta la barra en una unidad
            lcd.putchar(chr(219))   #Imprime un cuadrado
            bar_size = bar_size + 1 #Aumenta en 1 la cuenta del tamaño de la barra
            volume = volume + 6.25  #Aumenta 6.25% a la cuenta del volumen
            #Actualiza el porcentaje
            lcd.move_to(0, 1)       #Mueve el cursor a (0, 1)
            lcd.putstr(str("{:.2f}".format(volume)) + "%  ") #Imprime el volumen guardado en la variable
            lcd.move_to(bar_size, 0) #utiliza el tamaño de la barra para devolver el cursor a su posición original
            
            #Guarda la ubicacion del cursor en la memoria
            reg_write(i2c, EEPROM_ADDR, REG_DATA, bar_size)
            utime.sleep(0.3)
            
    elif (boton_down.value() == 1 and boton_up.value() == 0):
        if (bar_size > 0):
            #Disminuye una barrita
            lcd.move_to(bar_size - 1, 0) #Mueve el cursor una casilla a la izquierda
            lcd.putchar(' ')             #Imprime un espacio para borrar la barra
            bar_size = bar_size - 1      #Disminuye en 1 la cuenta del tamaño de la barra
            volume = volume - 6.25       #Disminuye 6.25% a la cuenta del volumen
            #Actualiza el porcentaje
            lcd.move_to(0, 1)            #Mueve el cursor a (0, 1)
            lcd.putstr(str("{:.2f}".format(volume)) + "%  ") #Imprime el volumen guardado en la variable
            lcd.move_to(bar_size, 0)     #utiliza el tamaño de la barra para devolver el cursor a su posición original
            
            #Guarda la ubiacion del cursor en la memoria
            reg_write(i2c, EEPROM_ADDR, REG_DATA, bar_size)
            utime.sleep(0.3)