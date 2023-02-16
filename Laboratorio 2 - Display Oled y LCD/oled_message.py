from ssd1306 import SSD1306_I2C
from machine import Pin, I2C

ancho = 128
largo = 32

#inicializamos el controlador I2C del Raspberry
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq = 200000)

#inicializamos el display
oled = SSD1306_I2C(ancho, largo, i2c)

#limpiar la pantalla en caso tenga pixeles encendidos
oled.fill(0)

#añadir texto
oled.text("What is my", 5, 8)
oled.text("purpose master?", 5, 18)

#mostrar
oled.show()