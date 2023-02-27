cmake_minimum_required(VERSION 3.12) #Version de CMake

include(pico_sdk_import.cmake) #Importar pico_sdk_import.cmake

project(accel_data_collection) #Nombre del proyecto

pico_sdk_init() #Inicializar el SDK

add_executable(accel_data #Definir los nombre de la build
    accel_data.cpp        #y de los scripts
)

target_link_libraries(accel_data #Definir las librerías que se importarán
    pico_stdlib  #Librería Estandar del RP Pico
    hardware_i2c #Librería para la comuniación I2C
)

pico_enable_stdio_usb(accel_data 1) #Habilitar la comunicación por el puerto USB Serial
pico_enable_stdio_uart(accel_data 0) #Deshabilitar la comunicación por UART

pico_add_extra_outputs(accel_data) #Funcion del SDK que genera algunos archivos adicionales para el ejecutable