from time import *
from gpio import *
from realhttp import *
SERVER_PORT = 8765
PASSWORD = '12345'
PIN_ALARM = 0
PIN_DOOR = 1
PIN_LCD = 2
PASSWORD = 12345

password = ''
is_active = False
is_open = False
alarm_status = True
lock_open = True

def startup():
    global is_open
    global alarm_status
    global password
    global is_active
    global lock_open
    current_is_open = customRead(PIN_DOOR)
    is_open = bool(int(current_is_open))
    print(is_open)
    alarm_status = True
    password = ''
    is_active = False
    lock_open = False

def writeLCD(msg):
    customWrite(PIN_LCD, msg)

def door():
    global is_open
    if PIN_DOOR:
        is_open = not is_open

def alarm_control():
    global alarm_status
    if alarm_status == True:
        digitalWrite(PIN_ALARM, HIGH)
        delay(50)
        digitalWrite(PIN_ALARM, LOW)
    if alarm_status == False:
        digitalWrite(PIN_ALARM, LOW)

def pass_check():
    global is_active
    if password == PASSWORD:
        is_active = True

def lock():
    global is_open
    if lock_open == True:
        print('cant close door')
        is_open = True
        sleep(1)

def security():
    global is_open
    global is_active
    global lock_open
    global password
    # Alarm Disabled
    if is_active == False:
        if is_open == True:
            writeLCD("Door open\nAlarm Disabled")
        if is_open == False:
            writeLCD("Door closed\nAlarm Disabled")

    # Alarm Enabled
    if is_active == True:
        if is_open == True:
            writeLCD("Door open\nAlarm Disabled")
            lock_open = True
        if is_open == False:
            writeLCD("Door closed\nAlarm Active")
    

def show_home(context, request, reply):
    """Docstring needed here """
    global password
    msg_body = request.body()
    
    print('request.method(): {}\n'.format(request.method))
    print(type(msg_body))
    password = msg_body.replace('password=','')
    print('Message body is: ' + password)
    
    reply.sendFile('index.html')
    reply.setStatus(200)
    reply.end()

def main():
    startup()
    global password
    server = RealHTTPServer()
    print('Server started: '.format(server.start(SERVER_PORT)))
    server.route("/login", ["GET","POST"], show_home)
    while True:
        pass_check()
        security()
        sleep(1)

if __name__ == "__main__":
    add_event_detect(PIN_DOOR, door)
    main()