# displayText.py
# (c)2020 robcranfill@gmail.com
# A service to display scrolling messages on an Adafruit 8x8 LED matrix.
#

from Adafruit_LED_Backpack import Matrix8x8
import font  # This is my data for a simple 8x8 font, found in this directory.

import socketserver
import sys
import threading
import time

# globals. sorry.
thread_ = threading.Thread()
threadRun_ = False
displayDelay_ = 0.1


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
        print(f" Recieved new command from {self.client_address[0]}: {self.data}")

        commandAndMessage = self.data.decode("UTF-8")
        command, message = commandAndMessage.split(" ", 1)
        print(f"command, message: '{command}', '{message}'")

        if command == "STOP":
            print("STOP not implemented yet")
            self.request.sendall(b"OK\n")
        elif command == "DELAY":
            displayDelay_ = float(message)
            self.request.sendall(b"OK\n")
        elif command == "DISPLAY":
            if thread_.isAlive():
                threadRun_ = False
                while thread_.isAlive():
                    # print(" Sleeping to wait for old thread to die....")
                    time.sleep(0.1)
            vrasters = makeVRasters(message)
            thread_ = threading.Thread(target=displayVRasters, args=(vrasters,))
            # print(" Starting new displayVRasters thread....")
            threadRun_ = True
            thread_.start()
            self.request.sendall(b"OK\n")
        else:
            print(f"UNKNOWN COMMAND '{command}'")
            self.request.sendall(b"UNKNOWN COMMAND '{}'\n".format(command))


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

    display = Matrix8x8.Matrix8x8()
    display.begin()

    while threadRun_:
        # get the 8x8 list bits to display
        for i in range(len(vrs)-8):
            dispBits = []
            for j in range(8):
                dispBits.append(vrs[i+j])
            displayRaster(display, dispBits)
            time.sleep(displayDelay_)
            if not threadRun_:
                break

# display the 8 raster lines
# This is funky because I have my 8x8 matrix mounted sideways!
#
def displayRaster(display, r):
    display.clear()
    for i in range(8):
        ri = r[i]
        for j in range(8):
            rtest = 1 if (ri & (1 << j)) else 0
            display.set_pixel(j, i, rtest)
    display.write_display()


# Return a list of the bytes for the given character.
# TODO: catch missing chars?
#
def byteListForChar(char):
    bits = font.FontData[char]
    return bits


# TODO: hold on to the display object so we can clear it
def clearDisplay():
        return


if __name__ == "__main__":

#    global displayDelay_

    if len(sys.argv) > 1:
        displayDelay_ = float(sys.argv[1])

    # instantiate the server, and bind to host and port
    server = socketserver.TCPServer(("localhost", 3141), aTCPSocketHandler)
    try:
        # activate the server; this will keep running until Ctrl-C
        print(f"Message server listening on port 3141; defauly delay {displayDelay_}")
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        clearDisplay()
        raise
    except:
        # report error and proceed
        raise
