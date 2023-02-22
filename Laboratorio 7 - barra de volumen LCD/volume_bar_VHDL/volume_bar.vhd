library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity volume_bar is
	port(clk: in std_logic;
		  boton_up, boton_down: in std_logic; -- botones de la placa
		  botones: out std_logic_vector(1 downto 0); --bus hacia el Raspberry
		  GP_IO: in std_logic_vector(5 downto 0); --bus desde el Raspberry
		  LCD: out std_logic_vector(5 downto 0); -- bus hacia el LCD
		  IO_SDA_PI,IO_SDA_SLAVE: in std_logic;
		  IO_SCL_PI,IO_SCL_SLAVE: in std_logic);
end volume_bar;

architecture solucion of volume_bar is
begin
	LCD <= GP_IO;
	botones <= not boton_up & not boton_down ;
end solucion;