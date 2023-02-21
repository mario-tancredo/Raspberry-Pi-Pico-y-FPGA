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