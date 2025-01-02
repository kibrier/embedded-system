import RPi.GPIO as GPIO
from time import sleep, time
from random import randint
from RPLCD.i2c import CharLCD

# Pin configurations
button_pin = None
victory_led_pin = None
standby_led_pin = None
death_led_pin = None
in_out_pins = []

# Functions
def setup_gpio(pins):
    global button_pin, victory_led_pin, standby_led_pin, death_led_pin
    button_pin = pins[0]
    victory_led_pin = pins[1]
    standby_led_pin = pins[2]
    death_led_pin = pins[3]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with pull-up
    GPIO.setup(victory_led_pin, GPIO.OUT)
    GPIO.setup(standby_led_pin, GPIO.OUT)
    GPIO.setup(death_led_pin, GPIO.OUT)

    # Turn off all LEDs initially
    GPIO.output(victory_led_pin, GPIO.LOW)
    GPIO.output(standby_led_pin, GPIO.LOW)
    GPIO.output(death_led_pin, GPIO.LOW)

def cleanup_gpio():
    GPIO.cleanup()

def lobby():
    lcd.clear()
    lcd.cursor_pos = (0, 1)
    lcd.write_string("Press to play")
    lcd.cursor_pos = (1, 1)
    lcd.write_string(f"Highscore: {highscore}")

    while GPIO.input(button_pin):
        GPIO.output(standby_led_pin, GPIO.HIGH)

    GPIO.output(standby_led_pin, GPIO.LOW)
    lcd.clear()

def move_player_pos(player_pos_y):
    return 1 if player_pos_y == 0 else 0

def choose_obstacle_pos_y():
    return randint(0, 1)

def move_obstacle(score, player_pos_x, obstacle_pos_x, obstacle_pos_y):
    if obstacle_pos_x <= player_pos_x:
        obstacle_pos_y = choose_obstacle_pos_y()
        score += 1
        return 15, obstacle_pos_y, score  # Reset to the right side and increase score
    else:
        obstacle_pos_x -= 1
        return obstacle_pos_x, obstacle_pos_y, score

def check_highscore(score, highscore):
    with open('highscore.txt', 'w') as file:
        file.write(str(max(score, highscore)))
    return max(score, highscore)

def check_death(player_pos_x, player_pos_y, obstacle_pos_x, obstacle_pos_y, sw):
    if player_pos_x == obstacle_pos_x and player_pos_y == obstacle_pos_y:
        lcd.clear()
        lcd.cursor_pos = (0, 3)
        lcd.write_string("Game Over!")
        lcd.cursor_pos = (1, 3)
        lcd.write_string(f"Score: {score}")
        for _ in range(3):
            GPIO.output(death_led_pin, GPIO.HIGH)
            sleep(1)
            GPIO.output(death_led_pin, GPIO.LOW)
            sleep(0.5)
        game(sw) if sw.value else stop()

def check_victory(score, highscore, sw):
    if score >= 100:
        sleep(1)
        lcd.clear()
        lcd.cursor_pos = (0, 4)
        lcd.write_string("You Won!")
        lcd.cursor_pos = (1, 3)
        lcd.write_string(f"Score: {score}")
        for _ in range(3):
            GPIO.output(victory_led_pin, GPIO.HIGH)
            sleep(1)
            GPIO.output(victory_led_pin, GPIO.LOW)
            sleep(0.5)
        game(sw) if sw.value else stop()

# Variables
try:
    with open('highscore.txt', 'r') as file:
        highscore = int(file.read())
except FileNotFoundError:
    highscore = 0

score = 0
player_pos_x = 7
player_pos_y = 0
obstacle_pos_x = 15
obstacle_pos_y = choose_obstacle_pos_y()
start_time = time()
interval_limit = 0.5  # Interval for moving the obstacle (seconds)

def stop():
    lcd.backlight_enabled = False
    lcd.clear()
    lcd.close()
    cleanup_gpio()

def start(pins, sw):
    global lcd
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, charmap='A00')
    lcd.clear()

    setup_gpio(pins)
    game(sw) if sw.value else stop()

# Main Game Function
def game(sw):
    try:
        global score, highscore, player_pos_x, player_pos_y, obstacle_pos_x, obstacle_pos_y, start_time, interval_limit
        obstacle = "o"
        player = "+"
        score_label = "CS:"
        highscore_label = "HS:"
        interval_limit = 0.3
        score = 0
        player_pos_x = 7
        player_pos_y = 0
        obstacle_pos_x = 15
        obstacle_pos_y = choose_obstacle_pos_y()
        lobby()

        while sw.value:
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"{score_label}{score}")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"{highscore_label}{highscore}")

            lcd.cursor_pos = (0, 6)
            lcd.write_string("|")
            lcd.cursor_pos = (1, 6)
            lcd.write_string("|")

            lcd.cursor_pos = (player_pos_y, player_pos_x)
            lcd.write_string(player)

            lcd.cursor_pos = (obstacle_pos_y, obstacle_pos_x)
            lcd.write_string(obstacle)

            # Move the player when the button is pressed
            if not GPIO.input(button_pin):  # Button is pressed
                player_pos_y = move_player_pos(player_pos_y)
                sleep(0.15)  # Small delay to debounce

            # Move the obstacle after the interval
            if time() - start_time >= interval_limit:
                start_time = time()
                interval_limit = max(interval_limit - 0.01, 0.1)  # Increase speed, limit to 0.1s
                obstacle_pos_x, obstacle_pos_y, score = move_obstacle(score, player_pos_x, obstacle_pos_x, obstacle_pos_y)

            check_death(player_pos_x, player_pos_y, obstacle_pos_x, obstacle_pos_y, sw)
            highscore = check_highscore(score, highscore)
            check_victory(score, highscore, sw)

    except KeyboardInterrupt:
        print("Lab 4 Interrupted, program exiting...")

    except Exception as e:
        print(f"Some other error occurred: {e}")

    finally:
        stop()
