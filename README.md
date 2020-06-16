# 8x8-text-display
Python code to display text on an Adafruit 8x8 dot matrix display. Again.

The two most important files here are:
 * displayServer.py - Runs as a service, accepting socket-based messages to display.
 * font.py - Code that implements a simple, bold, font.

## TODO:
 * Clear display when done
 * Accept a "delay" parameter; how?
 * Somebody is eating the input whitespace - who?
