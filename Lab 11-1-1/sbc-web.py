from realhttp import *
from time import *
from gpio import *
SERVER_PORT = 8765
PASSWORD = '12345'
PIN_ALARM = 0
PIN_DOOR = 1
PIN_LCD = 2
password = ''

door_open = False
alarm_disabled = True
alarm_on = False

def writeLCD(msg):
    customWrite(PIN_LCD, msg)

def show_home(context, request, reply):
    """Docstring needed here """
    global password
    msg_body = request.body()
    
    print('request.method(): {}\n'.format(request.method))
    print(type(msg_body))
    password = msg_body.replace('password=','')
    print('Message body is: \n' + password)
    
    reply.sendFile('index.html')
    reply.setStatus(200)
    reply.end()

def alarm_flash():
    digitalWrite(PIN_ALARM, HIGH)
    delay(50)
    digitalWrite(PIN_ALARM, LOW)

def door():
    global door_open
    if PIN_DOOR:
        door_open = not door_open

def security():
    writeLCD("Door closed\nAlarm Disabled")
    if door_open == False and alarm_disabled == True:
        print("Can manually open door")

def main():
    """Docstring needed here """
    global password
    server = RealHTTPServer()
    print('Server started: '.format(server.start(SERVER_PORT)))
    server.route("*", ["GET","POST"], show_home)
    while True:
        # Handle events
        sleep(1)
 
if __name__ == "__main__":
    add_event_handle(PIN_DOOR)
    main()