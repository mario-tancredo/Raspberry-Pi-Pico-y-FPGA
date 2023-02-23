library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity PWM is
	generic(
		sys_clk   : integer := 50_000_000;             --frecuencia del reloj del sistema en Hz
		pwm_freq  : integer := 50);                    --Frecuencia PWM en Hz
	port(
		clk       : in  std_logic;                     --reloj del sistema
		duty      : in  std_logic_vector(7 downto 0);  --ciclo de trabajo
		leds      : out std_logic_vector(7 downto 0);  --leds indicadores del ciclo de trabajo
		pwm_out   : out std_logic;                     --salida PWM
		pwm_n_out : out std_logic);                    --salida PWM inversa
end PWM;

architecture logic of PWM is
	constant  periodo        : integer := sys_clk/pwm_freq;        --numero de ciclos de reloj en un periodo PWM
	signal	 contador       : integer range 0 to periodo - 1;     --contador de periodo
	signal	 half_duty      : integer range 0 to periodo/2;       --numero de ciclos de reloj en medio ciclo de trabajo
begin
	leds <= duty;
	process(clk)
	begin
		if rising_edge(clk) then
		
			half_duty <= conv_integer(duty)*periodo/(2**8)/2;   --numero de ciclos de reloj en medio ciclo de trabajo
			
			if(contador = periodo - 1) then              --final del periodo alcanzado
				contador <= 0;                            --poner contador a cero
			else                                         --final del periodo no alcanzado
				contador <= contador + 1;                 --aumentar contador
			end if;
			
			if(contador = half_duty) then                --flanco de bajada de la fase alcanzado
				pwm_out <= '0';                           --establecer la salida pwm a 0
				pwm_n_out <= '1';                         --establecer la salida inversa a 1
			elsif(contador = periodo - half_duty) then   --flanco de subida de la fase alcanzado
				pwm_out <= '1';                           --establecer la salida pwm a 1
				pwm_n_out <= '0';                         --establecer la salida inversa a 0
			end if;
			
		end if;
	end process;
end logic;
