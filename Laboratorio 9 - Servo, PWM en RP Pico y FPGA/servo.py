from machine import Pin, PWM
import utime

MIN = 640000
MID = 1570000
MAX = 2500000

servo1 = PWM(Pin(1))
servo1.freq(50)

def servo_angulo(servo,angulo):
    duty = (angulo/180)*(MAX - MIN) + MIN
    servo.duty_ns(round(duty))
    
while True:
    servo_angulo(servo1,0)
    utime.sleep(2)
    servo_angulo(servo1,180)
    utime.sleep(2)