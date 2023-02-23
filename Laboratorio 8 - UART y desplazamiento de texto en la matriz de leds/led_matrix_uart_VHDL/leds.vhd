library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity leds is
	port(clk      : in  std_logic; --reloj del sistema
		  filas    : out std_logic_vector(7 downto 0); --filas de la matriz de leds
		  columnas : out std_logic_vector(7 downto 0); --columnas de la matriz de leds
		  rx_d     : in  std_logic_vector(7 downto 0)); --datos recibidos por el modulo UART
end leds;

architecture logic of leds is
	signal cuenta   : integer range 0 to 6250000;	--contador para el desplazador
   signal cuenta_2 : integer range 0 to 5;			--contador para instertar las letras nuevas
	signal cuenta_3 : integer range 0 to 50000;		--contador para multiplexar las filas de la matriz
	signal sel      : std_logic_vector(2 downto 0);	--selector de filas de la matriz
	
	signal letra_1  : std_logic_vector(4 downto 0):="11111"; --columnas encendidas de la fila 1 de la letra recibida
	signal letra_2  : std_logic_vector(4 downto 0):="11111"; --columnas encendidas de la fila 2 de la letra recibida
	signal letra_3  : std_logic_vector(4 downto 0):="11111"; --columnas encendidas de la fila 3 de la letra recibida
	signal letra_4  : std_logic_vector(4 downto 0):="11111"; --columnas encendidas de la fila 4 de la letra recibida
	signal letra_5  : std_logic_vector(4 downto 0):="00000"; --columnas encendidas de la fila 5 de la letra recibida
	
	signal columnas_0 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 0 del buffer sobre el que se irán desplazando las columnas
	signal columnas_1 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 1 del buffer sobre el que se irán desplazando las columnas
	signal columnas_2 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 2 del buffer sobre el que se irán desplazando las columnas
	signal columnas_3 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 3 del buffer sobre el que se irán desplazando las columnas
	signal columnas_4 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 4 del buffer sobre el que se irán desplazando las columnas
	signal columnas_5 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 5 del buffer sobre el que se irán desplazando las columnas
	signal columnas_6 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 6 del buffer sobre el que se irán desplazando las columnas
	signal columnas_7 : std_logic_vector(17 downto 0):= "111111111111111111"; --fila 7 del buffer sobre el que se irán desplazando las columnas
begin
		
	--Desplazador---------------------------------------------------------
	process(clk)
	begin
		if (rising_edge(clk)) then
			cuenta <= cuenta+1;
			
			if rx_d(7 downto 5) = "001" then --letra_1
				letra_1 <= rx_d(4 downto 0);
			elsif rx_d(7 downto 5) = "010" then --letra_2
            letra_2 <= rx_d(4 downto 0);
			elsif rx_d(7 downto 5) = "011" then --letra_3
            letra_3 <= rx_d(4 downto 0);
			elsif rx_d(7 downto 5) = "100" then --letra_4
            letra_4 <= rx_d(4 downto 0);
			elsif rx_d(7 downto 5) = "101" then --letra_5
            letra_5 <= rx_d(4 downto 0);
			end if;
			
			if cuenta = 6250000 then
				cuenta <= 0;
				
			--	columnas_0 <= columnas_0(16 downto 0) & columnas_0(17);
				columnas_1 <= columnas_1(16 downto 0) & columnas_1(17);
				columnas_2 <= columnas_2(16 downto 0) & columnas_2(17);
				columnas_3 <= columnas_3(16 downto 0) & columnas_3(17);
				columnas_4 <= columnas_4(16 downto 0) & columnas_4(17);
				columnas_5 <= columnas_5(16 downto 0) & columnas_5(17);
			--	columnas_6 <= columnas_6(16 downto 0) & columnas_6(17);
			--	columnas_7 <= columnas_7(16 downto 0) & columnas_7(17);
				
				cuenta_2 <= cuenta_2 + 1;
				
				if cuenta_2 = 5 then
					cuenta_2 <= 0;
					
				   columnas_1 <= letra_1 & columnas_1(11 downto 0) & '1';
				   columnas_2 <= letra_2 & columnas_2(11 downto 0) & '1';
				   columnas_3 <= letra_3 & columnas_3(11 downto 0) & '1';
				   columnas_4 <= letra_4 & columnas_4(11 downto 0) & '1';
				   columnas_5 <= letra_5 & columnas_5(11 downto 0) & '1';
				end if;
			end if;
		end if;
	end process;
   ----------------------------------------------------------------------
	
	
	--Multiplexador-------------------------------------------------------
	process(clk)
   begin
		if rising_edge(clk) then
			cuenta_3 <= cuenta_3 + 1;
			if cuenta_3 = 50000 then
				cuenta_3 <= 0;
				sel <= sel+1;
			end if;
		end if;
	end process;
	
	with SEL select filas <=	"01111111" when "000",
										"10111111" when "001",
										"11011111" when "010",
										"11101111" when "011",
										"11110111" when "100",
										"11111011" when "101",
										"11111101" when "110",
										"11111110" when "111",
										"11111111" when others;
	
	with SEL select columnas  <=  columnas_0(7 downto 0) when "000",
											columnas_1(7 downto 0) when "001",
											columnas_2(7 downto 0) when "010",
											columnas_3(7 downto 0) when "011",
											columnas_4(7 downto 0) when "100",
											columnas_5(7 downto 0) when "101",
											columnas_6(7 downto 0) when "110",
											columnas_7(7 downto 0) when "111",
											"11111111" 				when others;
	------------------------------------------------------------------------
	
end logic;