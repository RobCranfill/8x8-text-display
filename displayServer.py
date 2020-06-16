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
        print(f" Recieved new message from {self.client_address[0]}: {self.data}")

        # just send back the same data, but upper-cased
        # no; self.request.sendall(self.data.upper())
        self.request.sendall(b"OK\n")

        if thread_.isAlive():
            threadRun_ = False
            while thread_.isAlive():
                # print(" Sleeping to wait for old thread to die....")
                time.sleep(1)

        message = self.data.decode("UTF-8")
        vrasters = makeVRasters(message)

        thread_ = threading.Thread(target=displayVRasters, args=(vrasters,displayDelay_,))
        # print(" Starting new displayVRasters thread....")
        threadRun_ = True
        thread_.start()


# return a list of the bytes for the given character
def byteListForChar(char):
    bits = font.FontData[char]
    return bits


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
#
def displayVRasters(vrs, delay):
    global threadRun_

    display = Matrix8x8.Matrix8x8()
    display.begin()

    while threadRun_:
        # get the 8x8 list bits to display
        for i in range(len(vrs)-8):
            dispBits = []
            for j in range(8):
                dispBits.append(vrs[i+j])
            displayRaster(display, dispBits)
            time.sleep(delay)
            if not threadRun_:
                break

# display the 8 raster lines
def displayRaster(display, r):
    display.clear()
    for i in range(8):
        ri = r[i]
        for j in range(8):
            rtest = 1 if (ri & (1 << j)) else 0
            display.set_pixel(j, i, rtest)
    display.write_display()

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
        print(f"Message server listening on port 3141; delay {displayDelay_}")
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        clearDisplay()
        raise
    except:
        # report error and proceed
        raise
