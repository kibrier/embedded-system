import RPi.GPIO as GPIO
import time

class make_8x8_dot_matrix:
    def __init__(self, row_pins, col_pins):
        """
        Initializes the 8x8 dot matrix.
        
        Args:
            row_pins (list): A list of GPIO pins connected to the rows.
            col_pins (list): A list of GPIO pins connected to the columns.
        """
        if len(row_pins) != 8 or len(col_pins) != 8:
            raise ValueError("row_pins and col_pins must each have exactly 8 pins.")
        
        self.row_pins = row_pins
        self.col_pins = col_pins
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in row_pins + col_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def pixel(self, row, col, state):
        """
        Turns on or off a specific pixel in the matrix.

        Args:
            row (int): The row number (0-7).
            col (int): The column number (0-7).
            state (bool): True to turn the pixel on, False to turn it off.
        """
        if not (0 <= row <= 7 and 0 <= col <= 7):
            raise ValueError("Row and column numbers must be between 0 and 7.")

        # Activate the row
        GPIO.output(self.row_pins[row], GPIO.HIGH if state else GPIO.LOW)

        # Activate the column
        GPIO.output(self.col_pins[col], GPIO.LOW)

    def clear(self):
        """
        Turns off all LEDs in the matrix.
        """
        for row in self.row_pins:
            GPIO.output(row, GPIO.LOW)
        for col in self.col_pins:
            GPIO.output(col, GPIO.HIGH)

    def cleanup(self):
        """
        Cleans up the GPIO settings.
        """
        GPIO.cleanup()
