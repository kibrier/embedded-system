from dot_matrix import make_8x8_dot_matrix
from time import sleep

# Define GPIO pins
row_pins = [4,2,26,3,5,19,6,13]
col_pins = [18,16,20,14,21,15,23,24]

# Create matrix instance
matrix = make_8x8_dot_matrix(row_pins, col_pins)

def render_pattern(pattern):
    for n in range(100):
     matrix.clear()
     for i in range(8):
      for j in range(8):
       matrix.pixel(i,j,int(pattern[i][j]))
       sleep(0.000001)
       matrix.clear()

def I():
    I = [
    "00000000",
    "00111100",
    "00011000",
    "00011000",
    "00011000",
    "00011000",
    "00111100",
    "00000000"]
    render_pattern(I)

def heart():
    heart = [
    "00000000",
    "01100110",
    "11111111",
    "11111111",
    "01111110",
    "00111100",
    "00011000",
    "00000000"]
    render_pattern(heart)

def cock():
    cock = [
    '00111100',
    '00100100',
    '00111100',
    '00100100',
    '00100100',
    '11000011',
    '10011001',
    '11100111']
    render_pattern(cock)

def smiley():
    smiley = [
    "11111111",
    "11111111",
    "10011001",
    "10011001",
    "11111111",
    "11011011",
    "11100111",
    "11111111"]
    render_pattern(smiley)

try:
    while True:
     I()
     heart()
     cock()
     smiley()

except KeyboardInterrupt:
    matrix.clear()
    matrix.cleanup()

finally:
    # Clean up GPIO
    matrix.cleanup()
