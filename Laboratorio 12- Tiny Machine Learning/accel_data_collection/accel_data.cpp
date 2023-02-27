#include "pico/stdlib.h" //Librería estandar del RP Pico
#include "hardware/i2c.h"//Librería para la comunicación I2C
#include <stdio.h>       // Librería para la comunicación serial

#define I2C_PORT i2c1 //Definimos cual de los controladores I2C del pico usaremos

static int addr = 0x1C; //Dierección I2C del sensor

// Inicializar el acelerometro
void accel_init(void){
    // Verificar que está correctamente conectado
    sleep_ms(1000);
    uint8_t REG_DEV_ID = 0x0D; // Registro del acelerometro en el que está la ID del sensor
    uint8_t ACCEL_ID[1];  // Variable en la que guardaremos la información leída
    i2c_write_blocking(I2C_PORT, addr, &REG_DEV_ID, 1, true); //Escribimos la dirección del registro que queremos leer
    i2c_read_blocking(I2C_PORT, addr, ACCEL_ID, 1, false);//Esperamos el mensaje y lo guardamos en la variable chipID

    if(ACCEL_ID[0] != 0x2A){ //Comparamos el ID leído en el registro con el ID que se conoce deL Datasheet
        while(1){
            printf("ID incorrecto - Verificar Conexión!"); //Imprimir en caso el ID no coincida
            sleep_ms(5000);
        }
    }

    // Configurar el Modo
    uint8_t DATA[2];// Variable con la dirección y el mensaje
    DATA[0] = 0x2A; // Dierección del registro de control
    DATA[1] = 0x01; // Mensaje a escribir en el registro de control
    i2c_write_blocking(I2C_PORT, addr, DATA, 2, true); // Escribimos "00000001" en el registro de control
    sleep_ms(50);
}

int main(void){
    stdio_init_all(); // Inicializamos STD I/O para imprimir a través del puerto serial

    // Configuramos la comunicación I2C
    i2c_init(I2C_PORT, 200 * 1000); // Inicializamos la comunicación a travez de I2C a 200KHz
    gpio_set_function(14, GPIO_FUNC_I2C); // Definimos el pin GP14 como pin I2C
    gpio_set_function(15, GPIO_FUNC_I2C); // Definimos el pin GP15 como pin I2C
    gpio_pull_up(14); // Definimos el pin GP14 como PULL UP
    gpio_pull_up(15); // Definimos el pin GP15 como PULL UP

    // LLamamos a nuestra función para inicializar el acelerometro
    accel_init();

    uint8_t accel[6]; // Variable para guardar los valores de los 6 registros que tienen los valores de los ejes
    int16_t accelX, accelY, accelZ; // Variables para guardar el valor de cada eje
    float f_accelX, f_accelY, f_accelZ; // Variables para guardar el valor de cada eje en [m/s^2]
    float avg_accelX, avg_accelY, avg_accelZ; // Variables para guardar el promedio de las ultimos valores de cada eje
    uint8_t val = 0x00; // Registro de inicio

    int avg = 10; // Numero de ultimas muestras a promediar
    float buffer[avg*3] = { 0 }; // buffer en el que se guardan las "avg" ultimas muestras 
    int i = 0; // indice del buffer en el que se guardará el ultimo valor leído
    int j = 0; // inice del iterador que suma todos los elementos del buffer y los promedia

    // Bucle infinito
    while(1){
        i2c_write_blocking(I2C_PORT, addr, &val, 1, true); // Escribimos la dirección del registro por el que empezaremos a leer
        i2c_read_blocking(I2C_PORT, addr, accel, 6, false);// Esperamos el mensaje de 6 registros

        accelX = ((accel[1]<<8) | accel[0]); // Unimos los valores de los registros que conforman el valor del eje X
        accelY = ((accel[3]<<8) | accel[2]); // Unimos los valores de los registros que conforman el valor del eje Y
        accelZ = ((accel[5]<<8) | accel[4]); // Unimos los valores de los registros que conforman el valor del eje Z

        f_accelX = ((accelX * 9.81) / 1024) / 16; // Convertimos el valor del eje X a [m/s^2]
        f_accelY = ((accelY * 9.81) / 1024) / 16; // Convertimos el valor del eje Y a [m/s^2]
        f_accelZ = ((accelZ * 9.81) / 1024) / 16; // Convertimos el valor del eje Z a [m/s^2]

        buffer[i + 0] = f_accelX; // Asignamos el ultimo valor leído de X en el buffer
        buffer[i + 1] = f_accelY; // Asignamos el ultimo valor leído de Y en el buffer
        buffer[i + 2] = f_accelZ; // Asignamos el ultimo valor leído de Z en el buffer

        if (i < (avg*3 - 3)){ // Incrementamos el indice en el que se guardará el siguiente valor leido
            i += 3;
        }
        else{
            i = 0;            // Reseteamos el indice en caso este haya alcanzado su valor máximo
        }

        avg_accelX = 0; // Variable en la que se guardará el promedio de los ultimos "avg" valores de X
        avg_accelY = 0; // Variable en la que se guardará el promedio de los ultimos "avg" valores de Y
        avg_accelZ = 0; // Variable en la que se guardará el promedio de los ultimos "avg" valores de Z

        // Promediamos los valores guardados en el buffer separandolos por ejes
        for (j = 0; j <= (avg*3 - 3); j += 3)
        {
            avg_accelX += buffer[j + 0];
            avg_accelY += buffer[j + 1];
            avg_accelZ += buffer[j + 2];
        }
        
        avg_accelX /= avg;
        avg_accelY /= avg;
        avg_accelZ /= avg;

        // Imprimimos en el monitor serial
        printf("%6.2f\t", avg_accelX);
        printf("%6.2f\t", avg_accelY);
        printf("%6.2f\n", avg_accelZ);
        sleep_ms(10);
    }
}