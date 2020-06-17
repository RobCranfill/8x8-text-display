#!/usr/bin/python3

from Adafruit_LED_Backpack import Matrix8x8

display = Matrix8x8.Matrix8x8()
display.begin()
display.clear()
display.write_display()
