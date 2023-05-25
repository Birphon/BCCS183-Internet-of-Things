from time import sleep
from gpio import *
from realhttp import *

SERVER_PORT = 8765
PASSWORD = '12345'
PIN_ALARM = 0
PIN_DOOR = 1
PIN_LCD = 2

alarm_msg = ''
alarm_enabled = False
password = ''
door_msg = ''
is_open = False
alarm_trigger = False
pass_check = False

def startup():
    global is_open
    global alarm_msg
    global password
    global alarm_trigger
    current_is_open = customRead(PIN_DOOR)
    is_open = bool(int(current_is_open))
    password = ''
    alarm_msg = ''
    alarm_trigger = True
    digitalWrite(PIN_ALARM, LOW)   

def writeLCD(msg):
    customWrite(PIN_LCD, msg)

def alarm_checker():
    global alarm_msg
    if alarm_enabled == True: 
        alarm_msg = 'Alarm enabled'
    if alarm_enabled == False: 
        alarm_msg = 'Alarm disable'

# To turn the alarm (light) on or off
def alarm_toggle():
    
    global alarm_trigger
    if alarm_enabled == True:
        if is_open == True:
            alarm_msg = "Alarm!"
            digitalWrite(PIN_ALARM, HIGH)            
            writeLCD("{}\{}".format(door_msg, alarm_msg))
            
            if is_open == False:
                writeLCD("{}\{}".format(door_msg, alarm_msg))
                
            alarm_trigger = True

    if alarm_trigger == True:
        if pass_check == True:
            alarm_trigger = False
            digitalWrite(PIN_ALARM, LOW)
            alarm_checker()
            writeLCD("{}\{}".format(door_msg, alarm_msg))
            

def password_checker():
    global pass_check
    if password == PASSWORD:
        pass_check = True

def door():
    global is_open
    global door_msg
    
    if PIN_DOOR:
        is_open = not is_open
    writeLCD("{}\n{}".format(door_msg, alarm_msg))
    
    if is_open == True:
        door_msg = "Door Closed"
    else:
        door_msg = "Door Open"

# To turn the alarm (system) on or off
def alarm_setter():
    global door_msg
    global alarm_msg
    global alarm_enabled
    if is_open == True:
        door_msg = "Door is open - Can not enable alarm"
        alarm_msg = ''
        alarm_enabled = True
    else:
        alarm_enabled = False

def login_page(context, request, reply):
    global password
    msg_body = request.body()
    req_method = request.method()
    
    print('request.method(): {}\n'.format(req_method))
    print(type(msg_body))
    password = msg_body.replace('password=', '')
    print('Message body is: ' + password)
    
    reply.sendFile('index.html')
    reply.setStatus(200)
    reply.end()

def show_home(context, request, reply):
    
    html_reply = """
    <!DOCTYPE html>
    <html lang = 'en'>
       <head>
          <title>Home Page</title>
       </head>
       <body>
          <p>{}</p>
          <p>{}</p>
       </body>
    </html>
    """.format(door_msg,alarm_msg)
    reply.setContent(html_reply)
    reply.setStatus(200)
    reply.end()

def main():
    startup()
    global password
    server = RealHTTPServer()
    server_start = server.start(SERVER_PORT)
    print('Server started: {}'.format(server_start))
    server.route("/login", ["GET", "POST"], login_page)
    server.route("/",["GET"], show_home)
    while True:
        alarm_checker()
        alarm_toggle()
        sleep(1)

if __name__ == "__main__":
    add_event_detect(PIN_DOOR, door)
    main()