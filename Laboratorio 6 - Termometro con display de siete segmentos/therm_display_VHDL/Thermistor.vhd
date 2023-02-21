library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity Thermistor is
	port(	clk: in std_logic;
			temperatura: in std_logic_vector(11 downto 0);
			display: out std_logic_vector(7 downto 0);
			segmentos: out std_logic_vector(7 downto 0));
end Thermistor;

architecture solucion of Thermistor is
	signal EM0,EM1,EM2,EM3,EM4,EM5,EM6,EM7,SM: std_logic_vector(4 downto 0);
	signal SEL: std_logic_vector(2 downto 0);
	signal conta_16: std_logic_vector(15 downto 0);
begin
	
	EM0 <= "11111";
	EM1 <= '0' & temperatura(11 downto 8);
	EM2 <= '1' & temperatura(7 downto 4);
	EM3 <= '0' & temperatura(3 downto 0);
	EM4 <= "11111";
	EM5 <= "01100"; --Letra C
	EM6 <= "11111";
	EM7 <= "11111";
	
	--Contador--------------------------------------
	process(clk)
	begin
		if rising_edge(clk) then
			conta_16 <= conta_16+1;
			if conta_16 = 50000 then
				conta_16 <= (others=>'0');
				sel <= sel+1;
			end if;
		end if;
	end process;	
	--------------------------------------------------
	--Multiplexador-----------------------------------
	with sel select display <= "11111110" when "000",
								      "11111101" when "001",
								      "11111011" when "010",
								      "11110111" when "011",
								      "11101111" when "100",
								      "11011111" when "101",
								      "10111111" when "110",
								      "01111111" when others;
	--------------------------------------------------
	--Selector de numero/simbolo----------------------
	with sel select SM <= EM0 when "000",
								 EM1 when "001",
								 EM2 when "010",
								 EM3 when "011",
								 EM4 when "100",
								 EM5 when "101",
								 EM6 when "110",
								 EM7 when others;
	--------------------------------------------------
 
	--Lista de numeros/simbolos-----------------------------------
	with SM       select segmentos <="11000000" when "00000", --0
												"11111001" when "00001", --1
												"10100100" when "00010", --2
												"10110000" when "00011", --3
												"10011001" when "00100", --4
												"10010010" when "00101", --5
												"10000010" when "00110", --6
												"11111000" when "00111", --7
												"10000000" when "01000", --8
												"10011000" when "01001", --9
												"10001000" when "01010", --A
												"10000011" when "01011", --B
												"11000110" when "01100", --C
												"10100001" when "01101", --D
												"10000110" when "01110", --E
												"11111111" when "01111", --F
												"01000000" when "10000", --0.
												"01111001" when "10001", --1.
												"00100100" when "10010", --2.
												"00110000" when "10011", --3.
												"00011001" when "10100", --4.
												"00010010" when "10101", --5.
												"00000010" when "10110", --6.
												"01111000" when "10111", --7.
												"00000000" when "11000", --8.
												"00011000" when "11001", --9.
												"11111111" when others;  --
	-------------------------------------------------------------
		
end solucion;