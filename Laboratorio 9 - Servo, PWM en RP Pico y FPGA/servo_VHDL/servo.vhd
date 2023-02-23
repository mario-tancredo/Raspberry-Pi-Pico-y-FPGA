library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity servo is
	port(servo_in: in std_logic;
		  servo_out: out std_logic);
end servo;

architecture solucion of servo is
begin
	servo_out <= not servo_in;
end solucion;