from machine import Pin, UART
import utime

#Frase opalabra a enviar
frase = "Game Over"

uart = UART(0, 9600)
uart.init(9600, bits = 8, parity = None, stop = 1)

#Bucle infinito
while True:
    #iterar sobre la palabra que queremos enviar
    for i in frase:
        
        if i == 'a' or i == 'A':
            letra_1 = '00000'
            letra_2 = '01110'
            letra_3 = '01110'
            letra_4 = '00000'
            letra_5 = '01110'
        elif i == 'b' or i == 'B':
            letra_1 = '00001'
            letra_2 = '01110'
            letra_3 = '00001'
            letra_4 = '01110'
            letra_5 = '00001'
        elif i == 'c' or i == 'C':
            letra_1 = '00000'
            letra_2 = '01111'
            letra_3 = '01111'
            letra_4 = '01111'
            letra_5 = '00000'
        elif i == 'd' or i == 'D':
            letra_1 = '00001'
            letra_2 = '01110'
            letra_3 = '01110'
            letra_4 = '01110'
            letra_5 = '00001'
        elif i == 'e' or i == 'E':
            letra_1 = '00000'
            letra_2 = '01111'
            letra_3 = '00011'
            letra_4 = '01111'
            letra_5 = '00000'
        elif i == 'f' or i == 'F':
            letra_1 = '00000'
            letra_2 = '01111'
            letra_3 = '00011'
            letra_4 = '01111'
            letra_5 = '01111'
        elif i == 'g' or i == 'G':
            letra_1 = '00000'
            letra_2 = '01111'
            letra_3 = '01100'
            letra_4 = '01110'
            letra_5 = '00000'
        elif i == 'h' or i == 'H':
            letra_1 = '01110'
            letra_2 = '01110'
            letra_3 = '00000'
            letra_4 = '01110'
            letra_5 = '01110'
        elif i == 'i' or i == 'I':
            letra_1 = '00000'
            letra_2 = '11011'
            letra_3 = '11011'
            letra_4 = '11011'
            letra_5 = '00000'
        elif i == 'j' or i == 'J':
            letra_1 = '00000'
            letra_2 = '11011'
            letra_3 = '11011'
            letra_4 = '11011'
            letra_5 = '00011'
        elif i == 'k' or i == 'K':
            letra_1 = '01110'
            letra_2 = '01101'
            letra_3 = '00011'
            letra_4 = '01101'
            letra_5 = '01110'
        elif i == 'l' or i == 'L':
            letra_1 = '01111'
            letra_2 = '01111'
            letra_3 = '01111'
            letra_4 = '01111'
            letra_5 = '00000'
        elif i == 'm' or i == 'M':
            letra_1 = '01110'
            letra_2 = '00100'
            letra_3 = '01010'
            letra_4 = '01110'
            letra_5 = '01110'
        elif i == 'n' or i == 'N':
            letra_1 = '01110'
            letra_2 = '00110'
            letra_3 = '01010'
            letra_4 = '01100'
            letra_5 = '01110'
        elif i == 'ñ' or i == 'Ñ':
            letra_1 = '10001'
            letra_2 = '11111'
            letra_3 = '00110'
            letra_4 = '01010'
            letra_5 = '01100'
        elif i == 'o' or i == 'O':
            letra_1 = '00000'
            letra_2 = '01110'
            letra_3 = '01110'
            letra_4 = '01110'
            letra_5 = '00000'
        elif i == 'p' or i == 'P':
            letra_1 = '00000'
            letra_2 = '01110'
            letra_3 = '00000'
            letra_4 = '01111'
            letra_5 = '01111'
        elif i == 'q' or i == 'Q':
            letra_1 = '00000'
            letra_2 = '01110'
            letra_3 = '01110'
            letra_4 = '01101'
            letra_5 = '00010'
        elif i == 'r' or i == 'R':
            letra_1 = '00000'
            letra_2 = '01110'
            letra_3 = '00000'
            letra_4 = '01011'
            letra_5 = '01101'
        elif i == 's' or i == 'S':
            letra_1 = '00000'
            letra_2 = '01111'
            letra_3 = '00000'
            letra_4 = '11110'
            letra_5 = '00000'
        elif i == 't' or i == 'T':
            letra_1 = '00000'
            letra_2 = '11011'
            letra_3 = '11011'
            letra_4 = '11011'
            letra_5 = '11011'
        elif i == 'u' or i == 'U':
            letra_1 = '01110'
            letra_2 = '01110'
            letra_3 = '01110'
            letra_4 = '01110'
            letra_5 = '00000'
        elif i == 'v' or i == 'V':
            letra_1 = '01110'
            letra_2 = '01110'
            letra_3 = '01110'
            letra_4 = '10101'
            letra_5 = '11011'
        elif i == 'w' or i == 'W':
            letra_1 = '01110'
            letra_2 = '01110'
            letra_3 = '01010'
            letra_4 = '00100'
            letra_5 = '01110'
        elif i == 'x' or i == 'X':
            letra_1 = '01110'
            letra_2 = '10101'
            letra_3 = '11011'
            letra_4 = '10101'
            letra_5 = '01110'
        elif i == 'y' or i == 'Y':
            letra_1 = '01110'
            letra_2 = '10101'
            letra_3 = '11011'
            letra_4 = '11011'
            letra_5 = '11011'
        elif i == 'z' or i == 'Z':
            letra_1 = '00000'
            letra_2 = '11101'
            letra_3 = '11011'
            letra_4 = '10111'
            letra_5 = '00000'
        else:
            letra_1 = '11111'
            letra_2 = '11111'
            letra_3 = '11111'
            letra_4 = '11111'
            letra_5 = '00000'
         
        uart.write(int('001' + letra_1,2).to_bytes(1,'big'))
        uart.write(int('010' + letra_2,2).to_bytes(1,'big'))
        uart.write(int('011' + letra_3,2).to_bytes(1,'big'))
        uart.write(int('100' + letra_4,2).to_bytes(1,'big'))
        uart.write(int('101' + letra_5,2).to_bytes(1,'big'))
        
        print(i)
        print(letra_1)
        print(letra_2)
        print(letra_3)
        print(letra_4)
        print(letra_5)
        #Esperamos de acuerdo a la velocidad a la que se muevan las letras en el display
        utime.sleep(0.75)