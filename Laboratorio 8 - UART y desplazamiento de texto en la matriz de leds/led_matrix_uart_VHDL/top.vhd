library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity top is
  port (clk       : in  std_logic;                    --reloj del sistema
		  filas     : out std_logic_vector(7 downto 0); --filas de la matriz de leds
		  columnas  : out std_logic_vector(7 downto 0); --columnas de la matriz de leds
        rx        : in  STD_LOGIC);                   --pin de recepción
end top;

architecture str of top is
  signal rx_data     :  STD_LOGIC_VECTOR(7 DOWNTO 0);
  signal rx_d        :  STD_LOGIC_VECTOR(7 DOWNTO 0);
begin
	
	UART : entity work.UART(logic)
	port map(clk => clk,          --conectar el pin de reloj de uart.vhd con el pin de reloj de top.vhd
				rx => rx,            --conectar el pin de recepcion de uart.vhd con el pin de recepción de top.vhd
				rx_data => rx_data); --conectar la salida de datos "rx_data" con la señal "rx_data"
	
	LEDS : entity work.LEDS(logic)
	port map(clk => clk,          --conectar el pin de reloj de leds.vhd con el pin de reloj de top.vhd
				filas => filas,      --conectar la salida a las filas con los pines de salida a las filas de top.vhd
				columnas => columnas,--conectar la salida a las columnas con los pines de salida a las columnas de top.vhd
				rx_d => rx_d);       --conectar la señal "rx_data" con la entrada de datos "rx_data"
	
	rx_d <= rx_data; --conectar la señal rx_data a la señal rx_d
	
end architecture;