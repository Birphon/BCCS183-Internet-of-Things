from realhttp import *
from time import *
from gpio import *
from file import *


PORT = 8765
PIN_ALARM = 0
PIN_DOOR = 1
PIN_LCD = 2
CORRECT_PASSWORD = '12345'
HTTP_GET_METHOD = 'GET'
HTTP_POST_METHOD = 'POST'
RESTRICT_MSG = 'Please close the garage door first.'
REPLY_TEMP =  """<!DOCTYPE html>
                <html lang = 'en'>
                <head>
                    <title>Garage Status</title>
                </head>
                <body>
                    <p> {} </p>
                    <p> {} </p>
                </body>
                </html>"""
BAD_PASS = 'Bad password'
FILENAME = 'login.html'
READ_MODE = 'r'

alarm_status = True
door_open = False
door_msg = ''
lcd_message = ''
door_state = None
entered_password = ''
html_message = ''

def startup():
    global door_state
    global alarm_status
    current_door_state = customRead(PIN_DOOR)
    door_state = bool(int(current_door_state))
    alarm_status = True
    digitalWrite(PIN_ALARM, LOW)

def show_home(context, request, reply):
    alarm_msg = alarm_message()
    reply_msg = REPLY_TEMP.format(door_msg, alarm_msg)
    
    reply.setContent(reply_msg)
    reply.setStatus(200)
    reply.end()

def show_login(context, request, reply):
    global entered_password
    global alarm_status
    global door_state
    request_method = request.method()
    msg_body = request.body()
    headers = request.headers()
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
            reply_msg = html_template.format('Enable','Enable')
        else:
            reply_msg = html_template.format('Disable','Disable')
            
    elif request_method == HTTP_POST_METHOD:
        entered_password = msg_body.replace('password=','')
        print(entered_password)
        if door_state == True and alarm_status == False:
                reply_msg = REPLY_TEMP.format(RESTRICT_MSG)
        elif entered_password == CORRECT_PASSWORD:
            alarm_status = not alarm_status
            alarm_msg = alarm_message()
            reply_msg = REPLY_TEMP.format(alarm_msg)
        else:
            reply_msg = REPLY_TEMP.format(BAD_PASS)
            
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
    if door_state == True and alarm_status == True:
        alarm_msg = 'Alarm!'
    elif alarm_status == True:
        alarm_msg = 'Alarm enabled.'
    else:
        alarm_msg = 'Alarm disabled.'
    return alarm_msg
        

def manual_door_control():
    """ Sets the door state as a boolean from reading a door event"""
    global door_state
    print("Door Event")
    door_state = not door_state
    

def alarm_on():
    """ Turns the alarm on if the conditions are met and disables it """
    if door_state == True and alarm_status == True:
        digitalWrite(PIN_ALARM, HIGH)
    elif alarm_status == False:
        digitalWrite(PIN_ALARM, LOW)

def main():
    """  """
    global lcd_message
    startup()
    server = RealHTTPServer()
    print('Server started: '.format(server.start(PORT)))
    server.route("/login", ["GET","POST"], show_login) 
    server.route("/", ["GET"], show_home)
    
    while True:
        alarm_msg = alarm_message()
        door_message()
        alarm_on()
        lcd_message = '{} \n{}'.format(door_msg, alarm_msg)
        customWrite(PIN_LCD, lcd_message)
        sleep(1)
 
if __name__ == "__main__":
    add_event_detect(PIN_DOOR, manual_door_control)
    main()