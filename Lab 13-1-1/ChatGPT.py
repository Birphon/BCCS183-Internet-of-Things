from realhttp import *
from time import *
from gpio import *
from file import *


# Constants
PORT = 8765
PIN_ALARM = 0
PIN_DOOR_STATUS = 1
PIN_DOOR_RECEIV = 2
PIN_LCD = 3
CORRECT_PASSWORD = '12345'
HTTP_GET_METHOD = 'GET'
HTTP_POST_METHOD = 'POST'
RESTRICT_MSG = 'Please close the garage door first.'
REPLY_TEMP = """<!DOCTYPE html>
                <html lang='en'>
                <head>
                    <title>Garage Status</title>
                    <meta http-equiv="refresh" content="3;URL='{}'" />
                </head>
                <body>
                    <p>{}</p>
                    <p>{}</p>
                    <br>
                    <p>{}</p>
                    <br>
                    <p>{}</p>
                </body>
                </html>"""
BAD_PASS = 'Bad password'
FILENAME = 'index.html'
READ_MODE = 'r'

# Variables
alarm_status = True
door_open = False
door_msg = ''
lcd_message = ''
door_state = None
entered_password = ''
html_template = ''
redirect = 'Redirecting you to http://127.0.0.1:8765/status'
endis = 'Click <a href="http://127.0.0.1:8765/login">here</a> to enable/disable the alarm'
close = 'Click <a href="http://127.0.0.1:8765/close_door">here</a> to close the door'

def startup():
    global door_state, alarm_status
    current_door_state = customRead(PIN_DOOR_STATUS)
    print(current_door_state)
    door_state = bool(int(current_door_state))
    print(door_state)
    alarm_status = True
    digitalWrite(PIN_ALARM, LOW)

def show_home(context, request, reply):
    reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/status', redirect, '', '', '')
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()

def show_status(context, request, reply):
    alarm_msg = alarm_message()
    reply_msg = REPLY_TEMP.format('', door_msg, alarm_msg, endis, close)
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()

def close_door(context, request, reply):
    door_state = False
    reply_msg = REPLY_TEMP.format('', 'Closing the door...', '', '', '')
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()

def show_login(context, request, reply):
    global entered_password, alarm_status, door_state
    request_method = request.method()
    msg_body = request.body()
    print('request.method(): {}\n'.format(request_method))
    
    if request_method == HTTP_GET_METHOD:
        file_handle = open(FILENAME, READ_MODE) 
        html_template = ''
        val = ' '
        print(val)
        while val != '':
            val = file_handle.readline()
            if val != '':
                html_template = html_template + str(val)
        file_handle.close()
        if alarm_status == False:
            reply_msg = html_template.format('Enable', 'Enable')
        else:
            reply_msg = html_template.format('Disable', 'Disable')
            
    elif request_method == HTTP_POST_METHOD:
        entered_password = msg_body.replace('password=', '')
        print(entered_password)
        if door_state == True and alarm_status == False:
            reply_msg = REPLY_TEMP.format('', RESTRICT_MSG, '', '', '')
        elif entered_password == CORRECT_PASSWORD:
            alarm_status = not alarm_status
            reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/status', '', '', '', '')
        else:
            reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/status', BAD_PASS, '', '', '')
    
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()
    

def door_message():
    global door_msg
    if door_state == True:
        door_msg = 'Door open.'
    else:
        door_msg = 'Door closed.'

def alarm_message():
    if door_state == True and alarm_status == True:
        alarm_msg = 'Alarm!'
    elif alarm_status == True:
        alarm_msg = 'Alarm enabled.'
    else:
        alarm_msg = 'Alarm disabled.'
    return alarm_msg
        

def manual_door_control():
    global door_state
    door_state = not door_state
    

def alarm_on():
    if door_state == True and alarm_status == True:
        digitalWrite(PIN_ALARM, HIGH)
    elif alarm_status == False:
        digitalWrite(PIN_ALARM, LOW)

def redirect_to_status(reply):
    reply.setHeader("Refresh", "3;URL='/show_status'")
    reply.setStatus(301)
    reply.end()

def redirect_to_login(reply):
    reply.setHeader("Refresh", "3;URL='/login'")
    reply.setStatus(301)
    reply.end()

def main():
    global lcd_message
    startup()
    door_message()
    server = RealHTTPServer()
    print('Server started: '.format(server.start(PORT)))
    server.route("/login", ["GET", "POST"], show_login)
    server.route("/status", ["GET"], show_status)
    server.route("/close_door", ["GET"], close_door)
    server.route("/", ["GET"], show_home)
    server.route("/.*", ["GET"], redirect_to_status)  # Redirect all other URLs to status page
    
    while True:
        alarm_msg = alarm_message()
        door_message()
        alarm_on()
        lcd_message = '{} \n{}'.format(door_msg, alarm_msg)
        customWrite(PIN_LCD, lcd_message)
        sleep(1)

if __name__ == "__main__":
    add_event_detect(PIN_DOOR_STATUS, manual_door_control)
    main()
