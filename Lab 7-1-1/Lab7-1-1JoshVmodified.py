from json import *
from time import *

from gpio import *
from realhttp import *
from udp import *

DEST_IP = '192.168.1.2'
PORT = 5000

# States
SEND_STATE = 1
IDLE_STATE = 2
LED_FIRST_STATE = 3
LED_SECOND_STATE = 4

# Pins
LED_1 = 2
LED_2 = 3
LED_3 = 4
LED_10 = 5
LED_11 = 6
LED_12 = 7
PIN_BTN = 0

# Globales
TOP_START = 2
TOP_END = 4

BOT_START = 5
BOT_END = 7

top_flash = True
bot_flash = False
should_flash = False
previous_message_id = ''
message = ''
http_message = ''

TIMER = 250
POLLING_TIME = 1000
# Your room_Id is in the JSON you extracted from the previous step in this lab.
ROOM_ID = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMTZmMGJmYzAtZDI3MC0xMWVkLTllN2QtZDk3NGMyMzhhZjJh' 
# You will need to create a new access token as they are only valid for 12 hours from when you log into Webex
PERSONAL_ACCESS_TOKEN = 'MGUwMTgyMTItZTZlNS00OTUyLTk5NDMtYmJhOWNmZWE5YWY2N2E4OGQyY2EtZWVk_P0A1_cb0fa6b7-6c1c-45f5-aae5-b00413680b83'
API_AUTHORORISATION_KEY = 'Bearer {}'.format(PERSONAL_ACCESS_TOKEN)
MAX_MESSAGES = 1
API_URL = 'https://api.ciscospark.com/v1/messages?roomId={}&max={}'.format(ROOM_ID, MAX_MESSAGES)
HEADER = {'Authorization':API_AUTHORORISATION_KEY}
def onHTTPDone(status, data):
    global should_flash
    global previous_message_id
    j_data = loads(data)
    http_message = j_data['items'][0]['text']
    message_id = j_data['items'][0]['created']
    if message_id != previous_message_id:
        previous_message_id = message_id
        if http_message == '/start':
            should_flash = True
        elif http_message == '/stop':
            should_flash = False
            
    ##print('The http_message currently is: {}'.format(http_message))
    ##http_control(http_message, message_id)

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

def button_handler():
    global should_flash
    global message
    if digitalRead(PIN_BTN, HIGH):
        should_flash = not should_flash
        message = 'Send'

def main():
    global state
    global top_flash
    global bot_flash
    global should_flash
    http = RealHTTPClient()
    http.onDone(onHTTPDone)
    socket.onReceive(onUDPReceive)
    return_value = socket.begin(PORT)
    add_event_detect(PIN_BTN, button_handler)
    while True:
        http.getWithHeader(API_URL, HEADER)
        if should_flash:
            if top_flash:
                flash_led(TOP_START, TOP_END)
                message = 'Send'
                top_flash = False
                socket.send(DEST_IP, PORT, message)
                message = ''
                
            if bot_flash:
                flash_led(BOT_START, BOT_END)
                bot_flash = False
                top_flash = True
        sleep(POLLING_TIME)
 
if __name__ == "__main__":
    # add_event_detect(PIN_BTN, button_handler)
    state = LED_FIRST_STATE
    socket = UDPSocket()
    main()
