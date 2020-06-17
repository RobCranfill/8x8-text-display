# 8x8-text-display
Python code to display text on an Adafruit 8x8 dot matrix display. Again.

The two most important files here are:
 * displayServer.py - Runs as a service, accepting socket-based messages to display.
 * font.py - Code that implements a simple, bold, font.

## References
 * https://learn.adafruit.com/adafruit-led-backpack/1-2-8x8-matrix
 * https://github.com/adafruit/Adafruit_Python_LED_Backpack

## To Do:
 * Something is eating leading and trailing input whitespace - who? (I think it's the sending program, not the server.)
 * Re-write my code to be more object-y? Remove globals where possible?
 * <strike>Clear display when done</strike>
 * <strike>Implement commands</strike>
