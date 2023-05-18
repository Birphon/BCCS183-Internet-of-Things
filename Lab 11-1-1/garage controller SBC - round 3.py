from realhttp import *
from time import *
from gpio import *
from time import *

PIN_ALARM = 0
PIN_DOOR = 1
PIN_LCD = 2
DOOR_CLOSED = "0"
DOOR_OPEN = "1"
LOCAL_PORT = 8765
PASSWORD = "12345"
file = 'enable.html'
password = ''
correct_password = False
door_status = False
alarm_status = False

def start():
    global door_status
    global alarm_status
    global file
    customWrite(PIN_DOOR, DOOR_CLOSED)
    door_status = False
    alarm_status = False
    file = 'enable.html'
    print("start -- door_status: " + door_status)
    print("start -- alarm_status: " + str(alarm_status))

def write_lcd(msg):
    customWrite(PIN_LCD, msg)
    
def show_home(context, request, reply):
    """Docstring needed here """ 
    global password
    
    request_method = request.method()
    msg_body = request.body()
    headers = request.headers()
    
    password = msg_body.replace('password=','')
    print('Message body is: ' + password)
    
    reply.sendFile(file)
    reply.setStatus(200)
    reply.end()

def correct_pass():
    if password == PASSWORD:
        correct_password == True
    else:
        correct_password == False

def alarm_flash():
    if alarm_flash == True:
        digitalWrite(PIN_ALARM, HIGH)
        delay(50)
        digitalWrite(PIN_ALARM, LOW)

def open_door():
    global door_status
    global alarm_status
    door_status = True
    alarm_status = False
    customWrite(PIN_DOOR, DOOR_OPEN)
    print("open_door -- door_status: " + door_status)
    print("open_door -- alarm_status: " + str(alarm_status))

def close_door():
    global door_status
    global alarm_status
    door_status = False
    alarm_status = True
    customWrite(PIN_DOOR, DOOR_CLOSED)
    print("close_door -- door_status: " + door_status)
    print("close_door -- alarm_status: " + str(alarm_status))


def state_check():
    global door_status
    global alarm_status
    global correct_password
    global file

    # Door Closed + Alarm Enabled
    # -> Correct Password
    #     -> Door Open + Alarm Disabled
    #     -> "Door: Open\nAlarm Disabled"
    # -> Incorrect Password
    #     -> Door Closed + Alarm Enabled
    #     -> "Door: Closed\nAlarm Enabled"

    # Door Closed + Alarm Disabled
    #     -> Alarm On
    #     -> Correct Password
    #         -> Door Open + Alarm Disabled
    #         -> "Door: Open\nAlarm Disabled"
    #     -> Incorrect Password
    #         -> Door Closed + Alarm Enabled
    #         -> "Door: Closed\nAlarm Enabled"

    # Door Open + Alarm Enabled
    #     -> Alarms On
    #     -> Correct Password
    #         -> Door Open + Alarm Disabled
    #         -> "Door: Open\nAlarm Disabled"
    #     -> Incorrect Password
    #         -> Door Closed + Alarm Enabled
    #         -> "Door: Closed\nAlarm Enabled"

    # Door Open + Alarm Disabled
    #     -> Defaults Alarm Enabled




def main():
    server = RealHTTPServer()
    print('Server started: '.format(server.start(8765)))
    server.route("*", ["GET","POST"], show_home)
    while True:
        # Handle events
        sleep(1)
 
if __name__ == "__main__":
    main()