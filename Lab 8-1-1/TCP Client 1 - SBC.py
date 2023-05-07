from tcp import *
from gpio import *
from time import *
 
SERVER_IP = '192.168.1.11'
SERVER_PORT = 5000

FALSE_TOGGLE = 0
TRUE_TOGGLE = 1

PIN_BTN = 0

def send_instruction(instruction):
    """Create TCP client, send instruction to server and close the client"""
    client = TCPClient()
    client.connect(SERVER_IP, SERVER_PORT)
    delay(1)
    client.send(instruction)
    client.close()

def btn_handler():
    global toggle
    if digitalRead(PIN_BTN, HIGH):
        toggle = TRUE_TOGGLE
 
def main():
    global toggle
    add_event_detect(PIN_BTN, btn_handler)
    while True:
        if toggle == TRUE_TOGGLE:
            data = 'data'
            send_instruction(data)
            toggle = FALSE_TOGGLE
        delay(250)
 
if __name__ == "__main__":
    toggle = FALSE_TOGGLE
    main()