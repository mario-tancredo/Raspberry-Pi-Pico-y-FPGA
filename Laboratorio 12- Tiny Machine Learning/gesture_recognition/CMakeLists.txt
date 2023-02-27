cmake_minimum_required(VERSION 3.13.1) # Minima version requerida de CMake

include(pico_sdk_import.cmake) # Importar pico_sdk_import.cmake

project(gesture_recognition C CXX ASM) # Nombre del proyecto y lenguajes de programación
set(CMAKE_C_STANDARD 11)   # Version de C
set(CMAKE_CXX_STANDARD 17) # Version de C++ 

pico_sdk_init() # Inicializar el SDK

add_executable(app # Definir el nombre del target
     main.cpp # y de los scripts
)

include(./edge-impulse-sdk/cmake/utils.cmake) # Importar utils.cmake

pico_enable_stdio_usb(app 1)  #Habilitar la comunicación por el puerto USB Serial
pico_enable_stdio_uart(app 0) #Deshabilitar la comunicación por UART

target_link_libraries(app #Definir las librerias que se importarán
     pico_multicore #Librería para el uso de los dos núcleos del RP Pico
     pico_stdlib    #Librería Estandar del RP Pico
     hardware_i2c   #Librería para la comuniación I2C
)

add_subdirectory(./edge-impulse-sdk/cmake/zephyr) # Añadir subcarpeta en la que se encuentra otro CMakeLists.txt

target_include_directories(app PRIVATE # Especifica las carpetas a incluir al momento de compilar el target
     .
     ./classifier
     ./tflite-model
     ./model-parameters
)

target_include_directories(app PRIVATE # Especifica las carpetas a incluir al momento de compilar el target
     edge-impulse-sdk
     edge-impulse-sdk/third_party/ruy
     edge-impulse-sdk/third_party/gemmlowp
     edge-impulse-sdk/third_party/flatbuffers/include
     edge-impulse-sdk/third_party
     edge-impulse-sdk/tensorflow
     edge-impulse-sdk/dsp
     edge-impulse-sdk/classifier
     edge-impulse-sdk/anomaly
     edge-impulse-sdk/CMSIS/NN/Include
     edge-impulse-sdk/CMSIS/DSP/PrivateInclude
     edge-impulse-sdk/CMSIS/DSP/Include
     edge-impulse-sdk/CMSIS/Core/Include
)

include_directories(${INCLUDES}) # Incluir las carpetas especificadas hasta ahora

RECURSIVE_FIND_FILE(MODEL_FILES "./tflite-model" "*.cpp")
RECURSIVE_FIND_FILE(SOURCE_FILES "edge-impulse-sdk" "*.cpp")
RECURSIVE_FIND_FILE(CC_FILES "edge-impulse-sdk" "*.cc")
RECURSIVE_FIND_FILE(S_FILES "edge-impulse-sdk" "*.s")
RECURSIVE_FIND_FILE(C_FILES "edge-impulse-sdk" "*.c")
list(APPEND SOURCE_FILES ${S_FILES})
list(APPEND SOURCE_FILES ${C_FILES})
list(APPEND SOURCE_FILES ${CC_FILES})
list(APPEND SOURCE_FILES ${MODEL_FILES})

target_sources(app PRIVATE ${SOURCE_FILES}) #Especifica las fuentes usar al compilar el target

pico_add_extra_outputs(app) #Funcion del SDK que genera algunos archivos adicionales para el ejecutable
