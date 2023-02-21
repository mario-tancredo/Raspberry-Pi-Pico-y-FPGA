from machine import Pin #Importamos la librería para el control de los pines
import utime #Importamos la librería utime para implementar delays
import math #Importamos la librería math para realizar operaciones de logaritmos


#Constantes para la conversion de la temperatura
sensibilidad = 1.0/65536 #(1/LSB)
volt_max = 3.3 #voltaje fuente del divisor

T0 = 298.15 #Temperatura ambiente en kelvin
R0 = 100000 #Resitencia del therm a temperatura ambiente
B = 4250 #Constante B

#Inicializar el pin del ADC
thermistor = machine.ADC(27)

#Pines de salida al FPGA
x0 = Pin(0, Pin.OUT)
x1 = Pin(1, Pin.OUT)
x2 = Pin(2, Pin.OUT)
x3 = Pin(3, Pin.OUT)
x4 = Pin(4, Pin.OUT)
x5 = Pin(5, Pin.OUT)
x6 = Pin(6, Pin.OUT)
x7 = Pin(7, Pin.OUT)
x8 = Pin(8, Pin.OUT)
x9 = Pin(9, Pin.OUT)
x10 = Pin(10, Pin.OUT)
x11 = Pin(11, Pin.OUT)

while 1:
    #leer el voltaje del pin 27 como un numero de 16 bits
    therm = thermistor.read_u16()
    
    #Convertir el numero leido en el valor del voltaje
    voltaje = volt_max * therm * sensibilidad
    
    #Calcular la resistencia del Thermisor a partir del voltaje
    resistencia = (voltaje * 470000)/(3.3 - voltaje)
    
    #Hallar la inversa de la temperatura en kelvin
    T_inv = (1/T0) + (1/B) * math.log(resistencia/R0)
    
    #Invierte el valor y convierte la temperatura de K a C
    T = round((1/ T_inv) - 273.15,1)
    
    #Imprime el valor de la temperatura en Celsius en pantalla
    print(T)
    utime.sleep(0.1)
    
    #Conversion a BCD
    Disp = int(T * 10) #Eliminar el punto decimal
    decimal = str(Disp % 10)
    unidades = str((Disp//10) % 10)
    decenas = str((Disp//100) % 10)
    
    BCD_disp = "{0:04b}".format(int(decenas, 16)) + \
               "{0:04b}".format(int(unidades, 16)) + \
               "{0:04b}".format(int(decimal, 16))
    
    #Imprime el valor de la temperatura en BCD
    print(BCD_disp)
    
    #Envía los valores binarios del string en BCD
    x0.value(int(BCD_disp[11]))
    x1.value(int(BCD_disp[10]))
    x2.value(int(BCD_disp[9]))
    x3.value(int(BCD_disp[8]))
    
    x4.value(int(BCD_disp[7]))
    x5.value(int(BCD_disp[6]))
    x6.value(int(BCD_disp[5]))
    x7.value(int(BCD_disp[4]))
    
    x8.value(int(BCD_disp[3]))
    x9.value(int(BCD_disp[2]))
    x10.value(int(BCD_disp[1]))
    x11.value(int(BCD_disp[0]))
    
    utime.sleep(0.1)