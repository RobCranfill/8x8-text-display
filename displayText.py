# displayText.py
# (c)2020 robcranfill@gmail.com
# Code to display a scrolling message on an Adafruit 8x8 LED matrix.
#
import font  # This is my data for a simple 8x8 font, found in this directory.
import time
from Adafruit_LED_Backpack import Matrix8x8


# return a list of the bytes for the given character
def byteListForChar(char):
    bits = font.FontData[char]
    return bits

# def printBitsForChar(char):
#     byteList = byteListForChar(char)
#     print(f'Bytes for "{char}": {byteList}')
#     for ib in range(8):
#         b = byteList[ib]
#         print(f"byte {ib} = {b:08b}")
#     print()
#
# def printByteList(bytelist):
#     for i in range(8):
#         print(f'{bytelist[i]:08b}')

# For the string, create the big list of bit values (columns), left to right.
def makeVRasters(string):
    bits = []
    string += string[0]
    for char in string:
        # bl is the list of *horizontal* rasters for the char
        bl = byteListForChar(char)
        for bitIndex in range(7,-1,-1):
            thisVR = 0
            for hRasterIndex in range(7,-1,-1):
                bitVal = ((1 << bitIndex) & bl[hRasterIndex])
                if bitVal > 0:
                    thisVR += (1 << (7-hRasterIndex))
            bits.append(thisVR)
    return bits


# Rotate the list of vertical rasters thru the display, forever.
# The input data already has the first char duplicated at the end, for ease of rotation.
#
def displayVRasters(vrs, delay):

    display = Matrix8x8.Matrix8x8()
    display.begin()

    while True:
        # get the bits to display
        for i in range(len(vrs)-8):
            dispBits = []
            for j in range(8):
                dispBits.append(vrs[i+j])
            displayRaster(display, dispBits)
            time.sleep(delay)

# display the 8 raster lines
def displayRaster(display, r):
    display.clear()
    for i in range(8):
        ri = r[i]
        for j in range(8):
            rtest = 1 if (ri & (1 << j)) else 0
            display.set_pixel(j, i, rtest)
            # print(rtest, end="")
        # print("")
    display.write_display()


vrasters = makeVRasters(" This is a test.")
# print(f"vraster: {vrasters} (len {len(vrasters)})")
displayVRasters(vrasters, 0.03)
