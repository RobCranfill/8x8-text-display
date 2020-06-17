# displayText.py
# (c)2020 robcranfill@gmail.com
# A service to display scrolling messages on an Adafruit 8x8 LED matrix.
# Optional arguments: [port number]
#
from Adafruit_LED_Backpack import Matrix8x8
import font  # This is my data for a simple 8x8 font, found in this directory.

import socketserver
import sys
import syslog
import threading
import time

# globals. sorry.
thread_ = threading.Thread()
threadRun_ = False
displayDelay_ = 0.025 # this is a nice default for my Pi3B
display_ = None

# if true, log to sysloc, otherwise print to console.
printToLog_ = True

def printOrLog(str):
    if printToLog_:
        syslog.syslog(str)
    else:
        print(str)


class aTCPSocketHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global thread_
        global threadRun_
        global displayDelay_

        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        printOrLog(f"Recieved new command from {self.client_address[0]}: {self.data}")

        commandAndMessage = self.data.decode("UTF-8")
        message = ""
        if commandAndMessage.find(" ") == -1:
            command = commandAndMessage
        else:
            command, message = commandAndMessage.split(None, 1)
        # print(f"command, message: '{command}', '{message}'")

        if command == "STOP":
            threadRun_ = False
            while thread_.isAlive():
                # print("Sleeping to wait for old thread to die....")
                time.sleep(0.1)
            clearDisplay()
            self.request.sendall(b"OK\n")
        elif command == "DELAY":
            displayDelay_ = float(message)
            self.request.sendall(b"OK\n")
        elif command == "DISPLAY":
            threadRun_ = False
            while thread_.isAlive():
                # print("Sleeping to wait for old thread to die....")
                time.sleep(0.1)
            vrasters = makeVRasters(message)
            thread_ = threading.Thread(target=displayVRasters, args=(vrasters,))
            # print("Starting new displayVRasters thread....")
            threadRun_ = True
            thread_.start()
            self.request.sendall(b"OK\n")
        else:
            printOrLog(syslog.LOG_ERR, f"UNKNOWN COMMAND '{command}'")
            self.request.sendall("UNKNOWN COMMAND '{}'\n".format(command).encode())


# For the string, create the big list of bit values (columns), left to right.
#
def makeVRasters(string):
    bits = []
    if len(string) == 0: # is there a better way to handle this null-input case?
        string = " "
    else:
        string += string[0] # duplicate the first char onto the end of the data for easier scrolling. TODO: needed?
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

    # print(f"vraster (len {len(bits)}): {bits}")
    return bits


# Rotate the list of vertical rasters thru the display, forever.
# The input data already has the first char duplicated at the end, for ease of rotation.
# Uses global displayDelay_ so we can change that after creating the thread.
#
def displayVRasters(vrs):
    global threadRun_
    global displayDelay_
    global display_

    while threadRun_:
        # get the proper 8x8 bits to display
        for i in range(len(vrs)-8):
            displayRaster(display_, vrs[i:i+8])
            time.sleep(displayDelay_)
            if not threadRun_:
                break


# Display the 8 raster lines
# This is slightly funky because I have my 8x8 matrix mounted sideways - YMMV!
#
def displayRaster(display, rasters):
    display.clear()
    for i in range(8):
        for j in range(8):
            # rtest = 1 if (rasters[i] & (1 << j)) else 0 # fixme
            # display.set_pixel(j, i, rtest)
            display.set_pixel(j, i, rasters[i] & (1<<j))
    display.write_display()


# Return a list of the bytes for the given character.
# TODO: catch missing chars?
#
def byteListForChar(char):
    bits = font.FontData[char]
    return bits


def clearDisplay():
    global display_
    if display_:
        display_.clear()
        display_.write_display()
    return


# Main
# Optional args: [port number]
#
if __name__ == "__main__":

    portNumber = 3141 # get it?
    if len(sys.argv) > 1:
        portNumber = int(sys.argv[1])

    display_ = Matrix8x8.Matrix8x8()
    display_.begin()

    # Instantiate the server, and bind to host and port.
    server = socketserver.TCPServer(("localhost", portNumber), aTCPSocketHandler)
    try:
        # Activate the server; this will keep running until ctrl-C (or SIGINT?)
        printOrLog(f"Message server listening on port {portNumber}; default delay {displayDelay_}")
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        clearDisplay()
        raise
    except:
        # report error and proceed
        raise
