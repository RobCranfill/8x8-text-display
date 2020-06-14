# fuggit - do it myself

import font
import time
from Adafruit_LED_Backpack import Matrix8x8

# return a list of the bytes for the character
def byteListForChar(char):
    bits = font.FontData[char]
    return bits

def printBitsForChar(char):
    byteList = byteListForChar(char)
    print('Bytes for "{}": {}'.format(char, byteList))
    for ib in range(8):
        b = byteList[ib]
        print("byte {} = {:08b}".format(ib, b))
    print()

# Display the character
def displayChar(display, char):

    print("Display bits for '{}':".format(char))

    display.clear()

    byteList = byteListForChar(char)
    for ib in range(8):
        b = byteList[ib]
        bStr = "{:08b}".format(b)
        for i in range(8):
            onOrOff = 1 if bStr[i] == '1' else 0
            # print("Set {},{} to {}".format(ib, i, onOrOff))
            display.set_pixel(7-ib, i, onOrOff)

    display.write_display()


display = Matrix8x8.Matrix8x8()
display.begin()

while True:
    for c in "This is a test! Z Z Z ":
        displayChar(display, c)
        time.sleep(0.2)
