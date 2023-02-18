library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity ball is
	port(	BALL_X, BALL_Y: in std_logic_vector(2 downto 0);
			filas,columnas: out std_logic_vector(7 downto 0);
			IO_SDA_PI,IO_SDA_SLAVE: in std_logic;
			IO_SCL_PI,IO_SCL_SLAVE: in std_logic);
end ball;

architecture solucion of ball is
begin
	
	with BALL_X select filas	<=	"00111111" when "000",
											"10011111" when "001",
											"11001111" when "010",
											"11100111" when "011",
											"11110011" when "100",
											"11111001" when "101",
											"11111100" when "110",
											"11111111" when "111",
											"11111111" when others;
									
	with BALL_Y select columnas	<=	"11111100" when "000",
												"11111001" when "001",
												"11110011" when "010",
												"11100111" when "011",
												"11001111" when "100",
												"10011111" when "101",
												"00111111" when "110",
												"11111111" when "111",
												"11111111" when others;
end solucion;