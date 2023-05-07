from udp import *
from gpio import *
from time import *

LED_1 = 2
LED_2 = 3
LED_3 = 4
LED_10 = 5
LED_11 = 6
LED_12 = 7

PIN_BTN = 9

TOP_START = 2
TOP_END = 4

BOT_START = 5
BOT_END = 7

top_flash = True
bot_flash = False
should_flash = False
message = ''
TIMER = 250

DEST_IP = '192.168.1.2'
PORT = 5000

def startup():
    """
    Initializes two groups of LEDs by setting them to the LOW state.

    Args:
        None

    Returns:
        None
    """
    for led in range(TOP_START, TOP_END + 1):
        digitalWrite(led, LOW)
    for led in range(BOT_START, BOT_END + 1):
        digitalWrite(led, LOW)

def onUDPReceive(ip, port, data):
    """
    Receives and processes UDP messages, setting a global variable to trigger an action.

    Args:
        ip (str): The IP address of the sender.
        port (int): The port number used by the sender.
        data (str): The content of the message.

    Returns:
        None
    """
    global bot_flash
    print('Received: {} from IP:{} Port:{}'.format(data, ip, port))
    if data == 'Send':
        bot_flash = True
    return None
        
        
def start_stop_button_event_handler():
    """
    Handles events related to a start/stop button. Changes a global variable to trigger an action.

    Args:
        None

    Returns:
        None
    """
    global should_flash
    global message
    if digitalRead(PIN_BTN, HIGH):
        should_flash = not should_flash
        message = 'Send'
        

def flash_led(start, stop): 
    """
    Flashes a sequence of LEDs in a given range by turning them on and off with a delay.

    Args:
        start (int): The first LED pin to be activated.
        stop (int): The last LED pin to be activated.

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
    The main function that runs the program, handling LED flashing and UDP communication.

    Args:
        None

    Returns:
        None
    """
    global top_flash
    global bot_flash
    socket = UDPSocket()
    socket.onReceive(onUDPReceive)
    return_value = socket.begin(PORT)
    while True:
        if should_flash:
            if top_flash:
                flash_led(TOP_START, TOP_END)
                top_flash = False
                socket.send(DEST_IP, PORT, message)
                
        if bot_flash:
            flash_led(BOT_START, BOT_END)
            bot_flash = False
            top_flash = True

        delay(TIMER)


if __name__ == "__main__":
    add_event_detect(PIN_BTN, start_stop_button_event_handler)     
    main()