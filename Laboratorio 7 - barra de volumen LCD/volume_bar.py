from machine import Pin #Imprtamos la librería para el control de los pines
from gpio_lcd import GpioLcd #Importamos la librería del display LCD
import utime #IMportamos la librerí utime para implementar delays

#Declaramos las entradas
boton_down = Pin(0, Pin.IN)
boton_up = Pin(1, Pin.IN)

#Variables del display
bar_size = 0 #Tamaño de la barra
volume = 0.0 #Porcentaje de volumen

#Inicializamos el display LCD
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)


#Main porgram

#Escribe el porcentaje
lcd.move_to(0, 1) 
lcd.putstr(str("{:.2f}".format(volume)) + "%  ")
lcd.move_to(0, 0)

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
            utime.sleep(0.3)