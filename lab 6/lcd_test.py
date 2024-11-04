from rpi_lcd import LCD
from time import sleep

lcd = LCD(width=16,rows=2)

while True:
    lcd.text('Hello wworld!', 1)
    lcd.text('Buset', 2)

    sleep(5)

    lcd.clear()