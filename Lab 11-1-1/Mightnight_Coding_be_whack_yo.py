from time import *

from gpio import *
from realhttp import *

# PINS
PIN_ALARM = 0
PIN_DOOR = 1
PIN_LCD = 2

# CONSTS
DOOR_CLOSED = "0"
DOOR_OPEN = "1"
LOCAL_PORT = 8765
PASSWORD = "12345"

# STATES
CLOSE_DOOR = 0
OPEN_DOOR = 1
ALARM_ACTIVE = 2
ALARM_DEACTIVE = 3

# VARS
door_state = False  # False = Door Closed
alarm_state = False  # False = Alarm Off
can_close = False  # False = Door can't be closed
alarm_close = False  # False = Alarm can't be deactivated
password = ""


def write_lcd(msg):
    customWrite(PIN_LCD, msg)


def show_home(context, request, reply):
    """Docstring needed here"""
    global password

    request_method = request.method()
    msg_body = request.body()
    headers = request.headers()

    password = msg_body.replace("password=", "")
    print("Message body is: " + password)

    reply.sendFile(file)
    reply.setStatus(200)
    reply.end()


def open_door():
    global door_state
    door_state = True


def close_door():
    global door_state
    door_state = False


def activate_alarm():
    global alarm_state
    alarm_state = True
    if alarm_state == True:
        digitalWrite(PIN_ALARM, HIGH)
        delay(50)
        digitalWrite(PIN_ALARM, LOW)


def deactivate_alarm():
    global alarm_state
    alarm_state = False
    if alarm_state == False:
        digitalWrite(PIN_ALARM, LOW)


def check_door_state():
    if door_state == OPEN_DOOR:
        if alarm_state and password == PASSWORD:
            deactivate_alarm()
    elif door_state == CLOSE_DOOR:
        if alarm_state and password == PASSWORD:
            activate_alarm()


def check_alarm_state():
    if alarm_state == ALARM_ACTIVE:
        if door_state == OPEN_DOOR:
            print("Alarm goes off!")
        elif door_state == CLOSE_DOOR:
            if password != PASSWORD:
                print("Incorrect password. Alarm stays active.")


def main():
    global door_state
    global alarm_state
    # Default state: Door is closed and Alarm is Deactivated
    door_state = CLOSE_DOOR
    alarm_state = ALARM_DEACTIVE
    server = RealHTTPServer()
    print("Server started: ".format(server.start(8765)))
    server.route("*", ["GET", "POST"], show_home)
    while True:
        # Handle events
        sleep(1)


if __name__ == "__main__":
    main()
