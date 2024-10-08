from gpiozero import LEDBoard, LED
from time import sleep
# from signal import pause

# leds = LEDBoard('BOARD8', 'BOARD10', 'BOARD12', 'BOARD16', 'BOARD32', 'BOARD36', 'BOARD38', 'BOARD40')
led0 = LED('BOARD8')
led1 = LED('BOARD10')
led2 = LED('BOARD12')
led3 = LED('BOARD16')
led4 = LED('BOARD32')
led5 = LED('BOARD36')
led6 = LED('BOARD38')
led7 = LED('BOARD40')

leds = [led0, led1, led2, led3, led4, led5, led6, led7]

def reset():
    for led in leds:
        led.off()

def pattern1():
    for led in leds:
        led.on()
        sleep(0.5)
        reset()
    for led in reversed(leds):
        led.on()
        sleep(0.5)
        reset()
    return 'pattern 1 done'

def pattern2():
    count = 0
    while count <= 6:
        leds[count].on()
        count+=2
    sleep(0.5)
    reset()
    count = 1
    while count <= 7:
        leds[count].on()
        count+=2
    sleep(0.5)
    reset()
    return 'pattern 2 done'

def pattern3():
    first = [0, 7]
    index = [0, 7]
    count = 0
    while count <= 3:
        if count == 3:
            for y in first:
                leds[y].on()
            sleep(0.5)
            reset()

        for x in index:
            leds[x].on()
        sleep(0.5)
        reset()
        index[0] += 1
        index[1] -= 1
        count+=1
    return 'pattern 3 done'

while True:
    print(pattern1())
    sleep(0.5)
    print(pattern2())
    sleep(0.5)
    print(pattern2())
    sleep(0.5)
    print(pattern3())
    sleep(0.5)
        

