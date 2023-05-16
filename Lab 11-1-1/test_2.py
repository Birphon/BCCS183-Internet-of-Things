from realhttp import *
from time import *
from gpio import *
LOCAL_PORT = 8765
################
# Physical Device Setup
PIN_LCD = 0
PIN_ALARM = 1
PIN_DOOR = 2
DOOR_CLOSED = "0"
DOOR_OPEN = "1"
################
door = 'A'
alarm = 'B'

def startup():
    customWrite(PIN_DOOR, DOOR_CLOSED)
    print("Startup")

def door_system(context, request, reply):
    """Docstring needed here """
    #status()
    html_reply = """
    <!DOCTYPE html>
    <html lang = 'en'>
       <head>
          <title>Door System</title>
       </head>
       <body>
          <p>Door: {}</p>
          <p>Alarm: {}</p>
          <p>Refresh the page for the next report.</p>
       </body>
    </html>
    """.format(door, alarm)
    reply.setContent(html_reply)
    reply.setStatus(200)
    reply.end()

def main():
    """Docstring needed here """
    startup()
    server = RealHTTPServer()
    print('Server started: {}'.format(server.start(LOCAL_PORT)))
    server.route('*', ['GET'], door_system)
    while True:
        # Handle events
        sleep(1)
 
if __name__ == '__main__':
    main()