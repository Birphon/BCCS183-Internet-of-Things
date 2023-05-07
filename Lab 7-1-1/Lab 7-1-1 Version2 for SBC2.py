from udp import *
from gpio import *
from time import *

GROUP2_LED_START = 4
GROUP2_LED_STOP = 10

IP_ADDRESS = '192.168.1.5'
DESTINATION_IP_ADDRESS = '192.168.1.4'
DESTINATION_UDP_PORT = 5000
PORT = 5000
MESSAGE = ''
#DB added
message = ''
DESTINATION_MESSAGE = 'Send'
flashing_leds = False

def onUDPReceive(ip, port, data):
    """ Recieves the info from the outside"""
    global message
    print('Received: {} from IP:{} Port:{}'.format(data, ip, port))
    message = data
    return None


def flash_led(start, stop):
    """ Flashes the Leds in sequence """

    for led in range (start, stop):
        digitalWrite(led, HIGH);
        delay(50)
        digitalWrite(led, LOW);
        delay(50)


def main():
    """ Start the Event """
    # This is no longer used
    # global flashing_leds
    global message
    
    # Create an socket
    socket = UDPSocket()
    # Add an event handler so that onUDPReceive is called when a UDP datagram is received
    socket.onReceive(onUDPReceive)
    # Start listening
    return_value = socket.begin(PORT)
    while True:
        if message == 'Send':
            flash_led(GROUP2_LED_START, GROUP2_LED_STOP)
            message = ''
       
            socket.send(DESTINATION_IP_ADDRESS, DESTINATION_UDP_PORT, DESTINATION_MESSAGE)
        delay(50)

if __name__ == "__main__":
    main()