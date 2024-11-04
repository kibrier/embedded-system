from signal import signal, SIGTERM, SIGHUP, pause
from threading import Thread
from gpiozero import MCP3008
from rpi_lcd import LCD
from time import sleep

x_axis, y_axis = 0,0

x = MCP3008(0)
y = MCP3008(1)
lcd = LCD()
reading = True

def safe_exit(signnum, frame):
    exit(1)

def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def read_axes():
    global x_axis, y_axis
    while reading:
        x_axis, y_axis = map(x.value,0,1,0,255), map(y.value,0,1,0,255)
        print(f'x: {x_axis}, y: {y_axis}')
        sleep(0.1)
        
def display_axes():
    global x_axis, y_axis
    while reading:
        sleep(0.25)
        lcd.text(f'X Axis: {x_axis}', 1)
        lcd.text(f'Y Axis: {y_axis}', 2)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    reader = Thread(target=read_axes, daemon=True)
    display = Thread(target=display_axes, daemon=True)
    
    reader.start()
    display.start()
    
    pause()

except KeyboardInterrupt:
    pass

finally:
    reading = False
    sleep(0.5)
    lcd.clear()
