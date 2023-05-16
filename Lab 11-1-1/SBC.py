from realhttp import *
from gpio import *
from time import *

PIN_LCD = 0
PIN_ALARM = 1
PIN_GARAGE = 2
PASS = 12345

def show_home(context, request, reply):
    reply.sendFile('index.html')
    reply.setStatus(200)
    reply.end()

def writeLCD(msg):
    customWrite(PIN_LCD, msg)

def main():
    server = RealHTTPServer()
    print('Server started: '.format(server.start(8765)))
    server.route("*", ["GET"], show_home)
    while True:
        # Handle events
        sleep(1)
 
if __name__ == "__main__":
    main()