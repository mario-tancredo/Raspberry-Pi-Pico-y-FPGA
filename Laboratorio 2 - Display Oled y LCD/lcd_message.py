from machine import Pin
from gpio_lcd import GpioLcd
 
# Crear un objeto de clase LCD
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)
 
lcd.putstr('Salutations')
lcd.move_to(0,1)
lcd.putstr('Humans')


battery = bytearray([0x0E,0x1F,0x11,0x11,0x1F,0x1F,0x1F,0x1F])
lcd.custom_char(0, battery)
lcd.move_to(15,1)
lcd.putchar(chr(0))