# fuggit - do it myself
#
# TODO: make a version of font.py that has *vertical* raster data?
#
import font  # This is my "font" code, found in this directory.
import time
from Adafruit_LED_Backpack import Matrix8x8


# return a list of the bytes for the given character
def byteListForChar(char):
    bits = font.FontData[char]
    return bits

def printBitsForChar(char):
    byteList = byteListForChar(char)
    print(f'Bytes for "{char}": {byteList}')
    for ib in range(8):
        b = byteList[ib]
        print(f"byte {ib} = {b:08b}")
    print()

def printByteList(bytelist):
    for i in range(8):
        print(f'{bytelist[i]:08b}')

# For the string, create the big list of bit values (columns), left to right.
def makeVRasters(string):
    bits = []
    print(f"making vraster for string '{string}'")
    for char in string:
        # bl is the list of *horizontal* rasters for the char
        bl = byteListForChar(char)
        print(f"\nhorizontal raster for char '{char}'':")
        printByteList(bl)
        for bitIndex in range(7,-1,-1):
            thisVR = 0
            for hRasterIndex in range(7,-1,-1):
                bitVal = ((1 << bitIndex) & bl[hRasterIndex])
                if bitVal > 0:
                    thisVR += (1 << (7-hRasterIndex))
                    # print(f'bit {bitIndex} of raster {7-hRasterIndex} set; adding 2^{7-hRasterIndex} -> {thisVR}')
            print(f" -> thisVR({bitIndex}): {thisVR:08b}")
            bits.append(thisVR)
    return bits


# Rotate the list of vertical rasters thru the display, forever.
# The input data already has the first char duplicated at the end, for ease of rotation.
#
def displayVRasters(vrs, delay):

    display = Matrix8x8.Matrix8x8()
    display.begin()

    testing = True
    while True:
        # get the bits to display
        for i in range(len(vrs)):
            dispBits = []
            for j in range(8):
                dispBits.append(vrs[i+j])
                print(f"XXXX Display {(i+j)}: {dispBits}")
            displayRaster(display, dispBits)
            time.sleep(delay)
        if testing:
            print("Stopping for test")
            break

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


vrasters = makeVRasters(" >")
print(f"vraster: {vrasters}")

displayVRasters(vrasters, 0.05)
