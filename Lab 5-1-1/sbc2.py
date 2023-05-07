from time import *
from gpio import *

SBC_IN = 0
SBC_OUT = 1
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


def startup():
    for led in range(GROUP_ONE_START, GROUP_ONE_END + 1):
        digitalWrite(led, LOW)

def led_flash(start, stop):
    for led in range(start, stop + 1):
        digitalWrite(led, HIGH)
        delay(TIMER)
        digitalWrite(led, LOW)
        delay(TIMER)

def detect_remote_sbc():
    global flashing
    print('Heard from SBC 1')
    if digitalRead(SBC_IN) == HIGH:
        flashing = True
        print("Flashing True")

def notify_remote_sbc():
    print('Notifying SBC 1')
    digitalWrite(SBC_OUT, HIGH)
    delay(50)
    digitalWrite(SBC_OUT, LOW)
    
def main():
    global flashing
    startup()
    while True:
        if flashing == True:
            led_flash(GROUP_ONE_START, GROUP_ONE_END)
            flashing = False
            notify_remote_sbc()
        delay(50)

if __name__ == "__main__":
    print('...waiting')
    add_event_detect(SBC_IN, detect_remote_sbc)
    main()