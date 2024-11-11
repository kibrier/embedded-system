#!/usr/bin/python
# modified from https://github.com/brettmclean/pad4pi/blob/develop/rpi_gpio_demo2.py

from pad4pi import rpi_gpio
from rpi_lcd import LCD
import time
import sys

entered_password = ""
correct_password = "1234ABC"
entered_chars = ""
lcd = LCD(width=16,rows=2)

def cleanup():
    global keypad, lcd
    keypad.cleanup()
    lcd.clear()

def characters_entered(key):
    global entered_chars
    
    if len(entered_chars) >= 16:
        entered_chars += str(key)
        lcd.text(entered_chars[16:], 2)
        print(entered_chars)
    else:
        entered_chars += str(key)
        lcd.text(entered_chars[0:16], 1)
        print(entered_chars)

def keys_pressed(key):
    global entered_chars, lcd
    
    if key == "*" and len(entered_chars) > 0:
        if len(entered_chars) > 16:
            entered_chars = entered_chars[:-1]
            lcd.text(entered_chars[16:], 2)
            print(entered_chars)
        else:
            entered_chars = entered_chars[:-1]
            lcd.text(entered_chars[0:16], 1)
            print(entered_chars)
    else:    
        characters_entered(key)

def correct_passcode_entered():
    print("Passcode accepted. Access granted.")
    global keypad, lcd
    try:
        keypad.unregisterKeyPressHandler(key_pressed)
        keypad.registerKeyPressHandler(keys_pressed)
        
    except KeyboardInterrupt:
        cleanup()
        sys.exit()

def incorrect_passcode_entered():
    print("Incorrect passcode. Access denied.")
    cleanup()
    sys.exit()

def password_entered(key):
    global entered_password, correct_password
    
    entered_password += str(key)
    print(entered_password)

    if len(entered_password) == len(correct_password):
        if entered_password == correct_password:
            correct_passcode_entered()
        else:
            incorrect_passcode_entered()

def key_pressed(key):
    global entered_password
    
    if key == "*" and len(entered_password) > 0:
        entered_password = entered_password[:-1]
        print(entered_password)
    else:    
        password_entered(key)
        
try:
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_4_by_4_keypad()

    keypad.registerKeyPressHandler(key_pressed)

    print(f"Enter password (hint: {correct_password}).")
    print("Press * to clear previous character.")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Goodbye")

finally:
    cleanup()
