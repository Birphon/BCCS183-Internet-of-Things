from time import *

from gpio import *

SBC_OUT = 0
SBC_IN = 1

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

TIMER = 250
top_flash = True
bot_flash = False
should_flash = False

def startup():
    for led in range(TOP_START, TOP_END + 1):
        digitalWrite(led, LOW)
    for led in range(BOT_START, BOT_END + 1):
        digitalWrite(led, LOW)
    

def led_flash(start, stop):
    for led in range(start, stop + 1):
        digitalWrite(led, HIGH)
        delay(TIMER)
        digitalWrite(led, LOW)
        delay(TIMER)

def detect_remote_sbc():
    global bot_flash
    print('Heard from SBC 1')
    if digitalRead(SBC_IN) == HIGH:
        bot_flash = True
        print("Flashing True")
            
def notify_remote_sbc():
    print('Notifying SBC 2')
    digitalWrite(SBC_OUT, HIGH)
    delay(50)
    digitalWrite(SBC_OUT, LOW)


# This function handles the button press - just changes the `should_flash` property	to True or False when pressed
def start_stop_btn():
    global should_flash
    if digitalRead(PIN_BTN) == HIGH:
        should_flash = not should_flash

def main():
    global top_flash
    global bot_flash
    startup() # Sets defaults
    while True:
        if should_flash == True:
            if top_flash == True: # To flash LED1-3
                led_flash(TOP_START,TOP_END)
                top_flash = False
                notify_remote_sbc()
            if bot_flash == True: # To Flash LED10-12
                led_flash(BOT_START, BOT_END)
                bot_flash = False
                top_flash = True

if __name__ == "__main__":
    print("Starting...")
    add_event_detect(SBC_IN, detect_remote_sbc)
    add_event_detect(PIN_BTN, start_stop_btn)
    main()