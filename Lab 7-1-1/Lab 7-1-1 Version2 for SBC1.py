from time import *

from gpio import *
from udp import *

GROUP1_LED_START = 2
GROUP1_LED_STOP = 5
GROUP3_LED_START = 5
GROUP3_LED_STOP = 8
START_STOP_BUTTON = 8

flashing_leds = False
flashing_lower_leds = False
flashing_top_leds = True

IP_ADDRESS = '192.168.1.4'
DESTINATION_IP_ADDRESS = '192.168.1.5'
DESTINATION_UDP_PORT = 5000
PORT = 5000
MESSAGE = ''
DESTINATION_MESSAGE = 'Send'


def onUDPReceive(ip, port, data):
    """ Recieves the info from the outside"""
    global flashing_lower_leds
    print('Received: {} from IP:{} Port:{}'.format(data, ip, port))
    if data == 'Send':
    	flashing_lower_leds = True
    return None
        
        
def start_stop_button_event_handler():
    """ handles once the button is pressed """
    global flashing_leds
    if digitalRead(START_STOP_BUTTON, HIGH):
        flashing_leds = not flashing_leds
        DESTINATION_MESSAGE = 'Send'
        

def flash_led(start, stop):
    """ Flashes the Leds in sequence """
    
    for led in range (start, stop):
        digitalWrite(led, HIGH);
        delay(50)
        digitalWrite(led, LOW);
        delay(50)

def main():
    """ Start the Event """
    global flashing_top_leds
    global flashing_lower_leds
    # Create an socket
    socket = UDPSocket()
    # Add an event handler so that onUDPReceive is called when a UDP datagram is received
    socket.onReceive(onUDPReceive)
    # Start listening
    return_value = socket.begin(PORT)
    while True:
        if flashing_leds:
            if flashing_top_leds:
                flash_led(GROUP1_LED_START, GROUP1_LED_STOP)
                flashing_top_leds = False
                # Send a datagram to the loopback address on port 5000
                socket.send(DESTINATION_IP_ADDRESS, DESTINATION_UDP_PORT, DESTINATION_MESSAGE)
                
        if flashing_lower_leds:
            flash_led(GROUP3_LED_START, GROUP3_LED_STOP)
            flashing_lower_leds = False
            flashing_top_leds = True

        delay(50)


if __name__ == "__main__":
    add_event_detect(START_STOP_BUTTON, start_stop_button_event_handler) 
    
    main()