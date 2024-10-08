from gpiozero import PWMLED, MCP3008
from time import sleep

#create an object called pot that refers to MCP3008 channel 0
pot = MCP3008(0) #reads values from 0-1

#create a PWMLED object called led that refers to GPIO 13
led = PWMLED('BOARD33') #can only take values from 0-1, closer to 0 means less brightness, 1 being the max brightness

def map(x, in_min, in_max, out_min, out_max):
    return float((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    if(pot.value < 0.001):
        led.value = 0
    else:
        led.value = pot.value
    voltage = round( map(pot.value, 0, 1, 0, 3.3), 2 )
    print(f'Voltage = {voltage}')
    sleep(0.1)
