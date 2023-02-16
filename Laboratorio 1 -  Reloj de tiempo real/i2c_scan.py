from machine import Pin, I2C #Importamos las librerías Pin e I2C

#inicializa el controlador I2C, en este caso el I2C1
#a traves de los pines 15 y 14 a una frecuencia de 200Kb/s
i2c = machine.I2C(1, scl = Pin(15), sda = Pin(14), freq = 200000)

#Devuelve una lista de las direcciones de los dispositivos encontrados
devices = i2c.scan()

#Comprueba que exista almenos un dispositivo e imprime su direccion
if len(devices) == 0:
    print('ningun dispositivo i2c encontrado')
else:
    print('dispositivos i2c encontrados: ', len(devices))
    for d in devices:
        print('Direccion en hexadecimal:', hex(d))