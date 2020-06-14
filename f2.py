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

# For the string, create the big list of bit values (columns), left to right.
def makeBits(string):
    bits = []
    for char in string:
        bl = byteListForChar(char)
        for b in range(8):
            bits.append(bl[b])

    # add the first char to the end so we can rotate thru this easily.
    bl = byteListForChar(string[0])
    for b in range(8):
        bits.append(bl[b])

    return bits

# Rotate the bitstring thru the display, forever.
# The input string has the first char duplicated at the end, for ease of rotation.
def displayBits(bitstring, delay):

    # display = Matrix8x8.Matrix8x8()
    # display.begin()

    # get the bits to display
    for i in range(len(bitstring)-8):
        dispBits = []
        for j in range(8):
            dispBits.append(bitstring[i+j])
        print("Display: {}".format(dispBits))
        time.sleep(delay)

bitstring = makeBits("-T")
print(bitstring)
displayBits(bitstring, 0.1)
