# #normal python
# 
import serial
# import RPi.GPIO as GPIO
# import time
# 
# led_pin = 13
ser = serial.Serial(port='COM9',baudrate=115200, timeout=1)
# 
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(led_pin, GPIO.OUT)
# GPIO.output(led_pin, GPIO.LOW)
# 
# pwm = GPIO.pwm(led_pin, 1000)
# pwm.start(0)
# 
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
# 
while True:
    if ser.readline():
        pot_value = int(ser.readline().decode('ascii'))
        print(pot_value, map(pot_value, 0, 1023, 0, 100))
#         pwm.ChangeDutyCycle(map(pot_value, 0, 1023, 0, 100))