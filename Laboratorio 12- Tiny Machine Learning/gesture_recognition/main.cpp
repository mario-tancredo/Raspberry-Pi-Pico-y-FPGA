#include "pico/stdlib.h"       // Librería estandar del RP Pico
#include "pico/multicore.h"    // Libreria para el uso de los dos nucleos del RP Pico
#include "ei_run_classifier.h" // El modelo entrenado
#include "hardware/i2c.h"      // Librería para la comunicacion I2C
#include <stdio.h>             // Libreria para la comunicacion serial

#define I2C_PORT i2c1 // Definimos el controlador I2C del RP Pico que usaremos

// Asignar un buffer del tamaño del input del modelo para guardar los valores que leeremos del acelerometro
float buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE] = { 0 };

static int addr = 0x1C; // Establecer la dirección I2C del acelerometro
const uint PIN_0 = 0;   // Establecer el Pin 0
const uint PIN_1 = 1;   // Establecer el Pin 1

void core1_entry(){
    gpio_init(PIN_0); // Inicializar el Pin GP0
    gpio_init(PIN_1); // Inicializar el Pin GP1
    gpio_set_dir(PIN_0, GPIO_OUT); // Establecer el Pin GP0 como output
    gpio_set_dir(PIN_1, GPIO_OUT); // Establecer el Pin GP1 como output

    while(true){

        uint64_t tick = (EI_CLASSIFIER_INTERVAL_MS); // Determinar el tiempo del siguiente instante

        float clasif[EI_CLASSIFIER_LABEL_COUNT] = {0}; // Array flotante del tamaño del número de
                                                       // clasificaciones que hace nuestro modelo

        // Convertir el buffer en una señal que el modelo pueda clasificar
        signal_t signal;
        int err = numpy::signal_from_buffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
        if (err != 0) {
            ei_printf("Error al crear la señal a partir del buffer (%d)\n", err);
        }
        
        // Ejecutar el clasificador
        ei_impulse_result_t result = { 0 };
        err = run_classifier(&signal, &result, false);
        if (err != EI_IMPULSE_OK) {
            ei_printf("ERROR: Fallo al ejecutar el clasificador (%d)\n", err);
        }
        
        //Imprimir los resultados de la clasificación
        ei_printf("\n");
        for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
            ei_printf("%s: %.2f\t", result.classification[ix].label, result.classification[ix].value);
            clasif[ix] = result.classification[ix].value;
        }
        
        //Enviar el resultado fuera del RP Pico
        if(clasif[0] > clasif[1] && clasif[0] > clasif[2] && clasif[0] > clasif[3]){ // for_back
            gpio_put(PIN_0, 0);
            gpio_put(PIN_1, 0);
        }
        if (clasif[1] > clasif[0] && clasif[1] > clasif[2] && clasif[1] > clasif[3]) // left_right
        {
            gpio_put(PIN_0, 1);
            gpio_put(PIN_1, 0);
        }
        if (clasif[2] > clasif[0] && clasif[2] > clasif[1] && clasif[2] > clasif[3]) // resting
        {
            gpio_put(PIN_0, 0);
            gpio_put(PIN_1, 1);
        }
        if (clasif[3] > clasif[0] && clasif[3] > clasif[1] && clasif[3] > clasif[2]) // up_down
        {
            gpio_put(PIN_0, 1);
            gpio_put(PIN_1, 1);
        }

        sleep_ms(tick);
    }
}

// Inicializar el aceleormetro
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

    // Configure the I2C Communication
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
    uint8_t val = 0x00; // Direccion del registro por el que se empezará a leer

    int avg = 10; // Numero de ultimas muestras a promediar
    float buffer_avg[avg*3] = { 0 }; // buffer en el que se guardan las "avg" ultimas muestras 
    int i = 0; // indice del buffer en el que se guardará el ultimo valor leído
    int j = 0; // inice del iterador que suma todos los elementos del buffer y los promedia
    
    multicore_launch_core1(core1_entry); // Ejecutar la función core1_entry en el segundo nucleo del RP Pico

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

        buffer_avg[i + 0] = f_accelX; // Asignamos el ultimo valor leído de X en el buffer_avg
        buffer_avg[i + 1] = f_accelY; // Asignamos el ultimo valor leído de Y en el buffer_avg
        buffer_avg[i + 2] = f_accelZ; // Asignamos el ultimo valor leído de Z en el buffer_avg

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
            avg_accelX += buffer_avg[j + 0];
            avg_accelY += buffer_avg[j + 1];
            avg_accelZ += buffer_avg[j + 2];
        }
        
        avg_accelX /= avg;
        avg_accelY /= avg;
        avg_accelZ /= avg;

        // Determinar el tiempo del siguiente instante
        uint64_t tick = (EI_CLASSIFIER_INTERVAL_MS);
        
        //Desplazar los valores guardados en el buffer para insertar los valores nuevos de cada eje
        for (size_t ix = 0; (ix < (EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3)); ix += 3) {
            buffer[ix + 0] = buffer[ix + 3];
            buffer[ix + 1] = buffer[ix + 4];
            buffer[ix + 2] = buffer[ix + 5];
        }
        
        //Insertar los valores nuevos de cada eje al buffer
        buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 3] = avg_accelX;
        buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 2] = avg_accelY;
        buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE - 1] = avg_accelZ;   

        sleep_ms(tick);
    }

    return 0;
}