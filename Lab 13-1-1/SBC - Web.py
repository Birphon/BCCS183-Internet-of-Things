from time import *
from file import *
from gpio import *
from realhttp import *

# Constants
PORT = 8765
PIN_ALARM = 0
PIN_DOOR_STATUS = 1
PIN_DOOR_RECEIV = 2
PIN_LCD = 3
PASSWORD = '12345'
HTTP_GET_METHOD = 'GET'
HTTP_POST_METHOD = 'POST'
REPLY_TEMP = """<!DOCTYPE html>
                <html lang='en'>
                <head>
                    <title>Garage Status</title>
                    <meta http-equiv="refresh" content="3;URL='{}'" />
                </head>
                <body>
                    <p>{} <br> {}</p>
                    <p>{} <br> {}</p>
                </body>
                </html>"""
BAD_PASS = 'Bad password'
FILENAME = 'index.html'
READ_MODE = 'r'

# Variables
alarm_armed = False
alarm_flash = False
door_closed = False
door_msg = ''
lcd_message = ''
door_state = None
alarm_login_pass = ''
close_door_pass = ''
html_template = ''
door_close = False
alert_on = False

# Could be constants - wanted to make the URL dynamic
redirect = 'Redicrecting you to http://127.0.0.1:8765/show_status'
endis = 'Click <a href="http://127.0.0.1:8765/login">here</a> to enable/disable the alarm'
close = 'Click <a href="http://127.0.0.1:8765/close_door">here</a> to close the door'

def startup():
    global door_state, alarm_armed
    current_door_state = customRead(PIN_DOOR_STATUS)
    print(current_door_state)
    door_state = bool(int(current_door_state))
    print(door_state)
    alarm_armed = True
    digitalWrite(PIN_ALARM, LOW)

def show_home(context, request, reply):
    reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/show_status',redirect, '','','')
    print(59)
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()

def show_status(context, request, reply):
    alarm_msg = alarm_message()
    reply_msg = REPLY_TEMP.format('', door_msg, alarm_msg, endis, close)
    print(67)
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()

def show_door_close(context, request, reply):
    global close_door_pass, door_close, door_state
    request_method = request.method()
    msg_body = request.body()
    print('request.method(): {}\n'.format(request_method))
    
    if door_state == True and alarm_armed == True:
        reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/show_status','Please disable the alarm first.','','','')
        print(80)
    elif request_method == HTTP_GET_METHOD:
        file_handle = open(FILENAME, READ_MODE) 
        html_template = ''
        val = ' '
        print(val)
        while val != '':
            val = file_handle.readline()
            if val != '':
                html_template = html_template + str(val)
        file_handle.close()
        if door_state == True:
            reply_msg = html_template.format('Close Door','Close Door')
        else:
            reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/show_status','Door is already closed...','','','')
            
    elif request_method == HTTP_POST_METHOD:
        close_door_pass = msg_body.replace('password=','')
        print(close_door_pass)
        if door_state == False:
            if close_door_pass == PASSWORD:
                door_close = True # True means door is open
                door_control()
                door_close = False # False means door is closed
                reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/show_status','Closing door...','','','')
            else:
                reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/show_status',BAD_PASS,'','','')
            
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()
    

def show_login(context, request, reply):
    global alarm_login_pass, alarm_armed, door_state, alert_on
    request_method = request.method()
    msg_body = request.body()
    print('request.method(): {}\n'.format(request_method))
    
    if door_state == True and alarm_armed == False:
        reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/show_status','Please close the garage door first.','','','')
    elif request_method == HTTP_GET_METHOD:
        file_handle = open(FILENAME, READ_MODE) 
        html_template = ''
        val = ' '
        print(val)
        while val != '':
            val = file_handle.readline()
            if val != '':
                html_template = html_template + str(val)
        file_handle.close()
        if alarm_armed == False:
            reply_msg = html_template.format('Enable alarm','Enable alarm')
        else:
            reply_msg = html_template.format('Disable alarm','Disable alarm')
            
    elif request_method == HTTP_POST_METHOD:
        alarm_login_pass = msg_body.replace('password=','')
        print(alarm_login_pass)
        if door_state == True and alarm_armed == False:
                reply_msg = REPLY_TEMP.format('','Please close the garage door first.','','','')
        elif alarm_login_pass == PASSWORD:
            alarm_armed = not alarm_armed
            if alert_on == True:
                alert_on = False
            reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/show_status','','','','')
        else:
            reply_msg = REPLY_TEMP.format('http://127.0.0.1:8765/login',BAD_PASS,'','','')
            
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
    """ """
    global alert_on
    if alert_on == True:
        alarm_msg = 'Alarm!'
    elif door_state == True and alarm_armed == True:
        alarm_msg = 'Alarm!'
        alert_on = True
    elif alarm_armed == True:
        alarm_msg = 'Alarm enabled.'
    elif alarm_armed == False:
        alarm_msg = 'Alarm disabled.'
    elif alarm_triggered == True and door_state == True and alarm_armed == True:
        alarm_msg = 'Alarm!'
    return alarm_msg
        

def manual_door_control():
    """ Sets the door state as a boolean from reading a door event"""
    global door_state
    door_state = not door_state

def door_control():
    customWrite(PIN_DOOR_RECEIV, "CLOSE")
    delay(20)
    customWrite(PIN_DOOR_RECEIV, "")
    delay(20)    

def alarm_toggle():
    global alarm_triggered
    """ Turns the alarm on if the conditions are met and disables it """
    if door_state == True and alarm_armed == True:
        digitalWrite(PIN_ALARM, HIGH)
        alarm_triggered = True
    elif alarm_armed == False:
        digitalWrite(PIN_ALARM, LOW)

def main():
    """  """
    global door_close
    startup()
    door_message()
    server = RealHTTPServer()
    print('Server started: '.format(server.start(PORT)))
    server.route("/login", ["GET","POST"], show_login) 
    server.route("/show_status", ["GET"], show_status) 
    server.route("/close_door", ["GET","POST"], show_door_close) 
    server.route("/", ["GET"], show_home)
    
    while True:
        alarm_msg = alarm_message()
        door_message()
        alarm_toggle()
        lcd_message = '{} \n{}'.format(door_msg, alarm_msg)
        customWrite(PIN_LCD, lcd_message)
        sleep(1)
 
if __name__ == "__main__":
    add_event_detect(PIN_DOOR_STATUS, manual_door_control)
    main()