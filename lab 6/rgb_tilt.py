from gpiozero import RGBLED, MCP3008
from time import sleep

rgb_led = RGBLED(21,20,16)
tilt1 = MCP3008(0)
tilt2 = MCP3008(1)

while True:
        tilt_1, tilt_2 = round(tilt1.value), round(tilt2.value)
        print(tilt_1, tilt_2)

        if tilt_1 == 0 and tilt_2 == 0:
                rgb_led.color = (1,0,0)
        elif tilt_1 == 1 and tilt_2 == 0:
                rgb_led.color = (0,1,0)
        elif tilt_1 == 1 and tilt_2 == 1:
                rgb_led.color = (0,0,1)
        else:
                pass

        sleep(0.25)
