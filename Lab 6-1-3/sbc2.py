from time import *

from gpio import *
from udp import *

LED_4 = 2
LED_5 = 3
LED_6 = 4
LED_7 = 5
LED_8 = 6
LED_9 = 7

flashing = False
TIMER = 250

GROUP_ONE_START = 2
GROUP_ONE_END = 7

DEST_IP = '192.168.1.1'
PORT = 5000
DEST_MSG = 'Send'
message = ''
should_flash = False

def startup():
    """
    Initializes a group of LEDs by setting them to the LOW state.

    Args:
        None

    Returns:
        None
    """
    for led in range(GROUP_ONE_START, GROUP_ONE_END + 1):
        digitalWrite(led, LOW)

def onUDPReceive(ip, port, data):
    """
    Receives and processes UDP messages.

    Args:
        ip (str): The IP address of the sender.
        port (int): The port number used by the sender.
        data (str): The content of the message.

    Returns:
        None
    """
    global message
    print('Received: {} from IP:{} Port:{}'.format(data, ip, port))
    message = data
    return None

def flash_led(start, stop):
    """
    Iterates through a range of LED pins, turning them on and off.

    Args:
        start (int): The first LED pin to be activated.
        stop (int): The last LED pin to be activated.
        timer (int): The delay time between turning LEDs on and off.

    Returns:
        None
    """
    for led in range (start, stop +1):
        digitalWrite(led, HIGH);
        delay(TIMER)
        digitalWrite(led, LOW);
        delay(TIMER)


def main():
    """
    The main function of the program. Initializes global variables, sets up a UDP socket, and listens for incoming messages.

    Args:
        None

    Returns:
        None
    """
    global message
    global should_flash
    socket = UDPSocket()
    socket.onReceive(onUDPReceive)
    return_value = socket.begin(PORT)
    while True:
        if message == 'Send':
            flash_led(GROUP_ONE_START, GROUP_ONE_END)       
            socket.send(DEST_IP, PORT, DEST_MSG)
            message = ''
            should_flash = False
        delay(50)

if __name__ == "__main__":
    main()