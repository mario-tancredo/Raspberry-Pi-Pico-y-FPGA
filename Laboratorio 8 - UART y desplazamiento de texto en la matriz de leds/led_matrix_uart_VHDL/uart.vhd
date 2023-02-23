LIBRARY ieee;
USE ieee.std_logic_1164.all;

ENTITY uart IS
  GENERIC(
    clk_freq  :  INTEGER    := 50_000_000;  --frecuencia del reloj del sistema en Hz
    baud_rate :  INTEGER    := 9_600;       --tasa de baudios en bits/seg
    os_rate   :  INTEGER    := 16;          --tasa de sobremuestreo para encontrar el centro de los bits de recepción (en muestras por período de baudios)
    d_width   :  INTEGER    := 8;           --ancho del bus de datos
    parity    :  INTEGER    := 0;           --0 sin paridad, 1 con paridad
    parity_eo :  STD_LOGIC  := '0');        --'0' para paridad par, '1' para paridad impar
  PORT(
    clk      :  IN   STD_LOGIC;                             --reloj del sistema
    rx       :  IN   STD_LOGIC;                             --pin de recepción
    rx_data  :  OUT  STD_LOGIC_VECTOR(d_width-1 DOWNTO 0)); --datos recibidos
END uart;
    
ARCHITECTURE logic OF uart IS
  TYPE   rx_machine IS(idle, receive);                        --tipo de datos de la máquina de estado recibir
  SIGNAL rx_state     :  rx_machine;                          --máquina de estado recibir
  SIGNAL baud_pulse   :  STD_LOGIC := '0';                    --pulso periódico que se produce a la tasa de baudios
  SIGNAL os_pulse     :  STD_LOGIC := '0';                    --pulso periódico que se produce a la tasa de sobremuestreo
  SIGNAL parity_error :  STD_LOGIC;                           --indicador de error de paridad recibir
  SIGNAL rx_parity    :  STD_LOGIC_VECTOR(d_width DOWNTO 0);  --calculo de la paridad de recepcion
  SIGNAL rx_buffer    :  STD_LOGIC_VECTOR(parity+d_width DOWNTO 0) := (OTHERS => '0');   --valores recibidos
BEGIN

  --generar pulsos de habilitación de reloj a la velocidad en baudios y la velocidad de sobremuestreo
  PROCESS(clk)
    VARIABLE count_baud :  INTEGER RANGE 0 TO clk_freq/baud_rate-1 := 0;         --contador para determinar el período de velocidad en baudios
    VARIABLE count_os   :  INTEGER RANGE 0 TO clk_freq/baud_rate/os_rate-1 := 0; --contador para determinar el período de sobremuestreo
  BEGIN
    IF rising_edge(clk) THEN
      --crear pulso de habilitacion de baudios
      IF(count_baud < clk_freq/baud_rate-1) THEN        --período de baudios no alcanzado
        count_baud := count_baud + 1;                     --incrementa el contador de periodos de baudios
        baud_pulse <= '0';                                --establece a cero el pulso de la tasa de baudios
      ELSE                                              --periodo de baudios alcazado
        count_baud := 0;                                  --reiniciar el contador de períodos de baudios
        baud_pulse <= '1';                                --establece a uno el pulso de la tasa de baudios
        count_os := 0;                                    --reiniciar el contador del período de sobremuestreo para evitar errores acumulativos
      END IF;
      --crear pulso de habilitacion del sobremuestreo
      IF(count_os < clk_freq/baud_rate/os_rate-1) THEN  --periodo de sobremuestreo no alcanzado
        count_os := count_os + 1;                         --incrementa el contador de periodo del sobremuestreo
        os_pulse <= '0';                                  --establece a cero el pulso de la tasa de sobremuestreo
      ELSE                                              --periodo de sobremuestreo alcanzado
        count_os := 0;                                    --reiniciar el contador del periodo del sobremuestreo
        os_pulse <= '1';                                  --establecer a uno el pulso del sobremuestreo
      END IF;
    END IF;
  END PROCESS;

  --receive state machine
  PROCESS(clk)
    VARIABLE rx_count :  INTEGER RANGE 0 TO parity+d_width+2 := 0; --contar los bits recibidos
    VARIABLE os_count :  INTEGER RANGE 0 TO os_rate-1 := 0;        --contar los pulsos de tasa de sobremuestreo
  BEGIN
    IF(rising_edge(clk) AND os_pulse = '1') THEN --habilitar el reloj a la tasa de muestreo
      CASE rx_state IS
        WHEN idle =>                                           --en reposo
          IF(rx = '0') THEN                                      --comprobar si hay un bit de inicio
            IF(os_count < os_rate/2) THEN                          --el contador de pulso de sobremuetreo no esta al centro del bit de inicio
              os_count := os_count + 1;                              --incrementar el contador de sobremuestreo
              rx_state <= idle;                                      --mantenerse en estado de reposo
            ELSE                                                   --el contador del pulso de sobremuestreo está al centro del bit de inicio
              os_count := 0;                                         --resetear el contador de pulso de sobremuestreo
              rx_count := 0;                                         --resetear el contador de bits recibidos
              rx_buffer <= rx & rx_buffer(parity+d_width DOWNTO 1);  --desplazar el bit de inicio al buffer de recibido						
              rx_state <= receive;                                   --cambiar a estado recibir
            END IF;
          ELSE                                                   --no hay bit de inicio
            os_count := 0;                                         --resetear el contador de pulso de sobremuestreo
            rx_state <= idle;                                      --mantenerse en estado de reposo
			 END IF;
        WHEN receive =>                                        --estado de recibir
          IF(os_count < os_rate-1) THEN                          --no es el centro del bit
            os_count := os_count + 1;                              --incrementar el contador del pulso de sobremuestreo
            rx_state <= receive;                                   --mantenerse en estado de recibir
          ELSIF(rx_count < parity+d_width) THEN                  --centro del bit y no de todos los bits recibidos
            os_count := 0;                                         --resetear el contador de pulso de sobremuestreo 
            rx_count := rx_count + 1;                              --incrementar el contador de bits recibidos
            rx_buffer <= rx & rx_buffer(parity+d_width DOWNTO 1);  --desplazar el bit de inicio al buffer de recibido	
            rx_state <= receive;                                   --mantenerse en estado de recibir
          ELSE                                                   --es el centro del bit de stop
            rx_data <= rx_buffer(d_width DOWNTO 1);                --asignar los bits recibidos al bus de salida
            rx_state <= idle;                                      --volver a estado de reposo
          END IF;
      END CASE;
    END IF;
  END PROCESS;
    
  --logica de calculo de paridad
  rx_parity(0) <= parity_eo;
  rx_parity_logic: FOR i IN 0 to d_width-1 GENERATE
    rx_parity(i+1) <= rx_parity(i) XOR rx_buffer(i+1);
  END GENERATE;
  WITH parity SELECT  --comparar el bit de paridad calculado con el bit de paridad recibido para determinar el error
    parity_error <= rx_parity(d_width) XOR rx_buffer(parity+d_width) WHEN 1,  --usando pariad
                    '0' WHEN OTHERS;                                          --sin usar paridad
END logic;
