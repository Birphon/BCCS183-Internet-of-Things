import random
from time import sleep

from gpio import *
from realhttp import *

PIN_ALARM = 0
PIN_DOOR = 1
PIN_LCD = 2
DOOR_CLOSED = "0"
DOOR_OPEN = "1"
LOCAL_PORT = 8765
PASSWORD = "12345"
door_status = "closed"
alarm_status = False


def start():
    global door_status
    global alarm_status
    customWrite(PIN_DOOR, DOOR_OPEN)
    door_status = "closed"
    alarm_status = False
    print("start -- door_status: " + door_status)
    print("start -- alarm_status: " + str(alarm_status))


def write_lcd(msg):
    customWrite(PIN_LCD, msg)


def alarm_flash():
    if alarm_flash == True:
        digitalWrite(PIN_ALARM, HIGH)
        delay(50)
        digitalWrite(PIN_ALARM, LOW)


def open_door():
    global door_status
    global alarm_status
    door_status = "open"
    alarm_status = False
    customWrite(PIN_DOOR, DOOR_OPEN)
    print("open_door -- door_status: " + door_status)
    print("open_door -- alarm_status: " + str(alarm_status))


def close_door():
    global door_status
    global alarm_status
    door_status = "closed"
    alarm_status = True
    customWrite(PIN_DOOR, DOOR_CLOSED)
    print("close_door -- door_status: " + door_status)
    print("close_door -- alarm_status: " + str(alarm_status))


def garage_control(context, request, reply):
    global door_status
    global alarm_status

    if request.method == "POST":
        if "password" in request.form:
            password = request.form["password"]
            if password == PASSWORD:
                open_door()
            else:
                close_door()

    html_reply = """
    <!DOCTYPE html>
    <html lang='en'>
       <head>
          <title>Garage Door Control</title>
       </head>
       <body>
          <p>Door: {}</p>
          <p>Alarm: {}</p>
          <form method='post'>
              <label for='password'>Enter Password:</label>
              <input type='password' id='password' name='password'>
              <button type='submit'>Submit</button>
          </form>
       </body>
    </html>
    """.format(
        door_status.capitalize(), "Disabled" if not alarm_status else "Activated"
    )
    write_lcd(
        "Door: {}\nAlarm: {}".format(
            door_status.capitalize(), "Disabled" if not alarm_status else "Activated"
        )
    )
    reply.setContent(html_reply)
    reply.setStatus(200)
    reply.end()


def main():
    start()
    server = RealHTTPServer()
    print("Server started: {}".format(server.start(LOCAL_PORT)))
    server.route("*", ["GET", "POST"], garage_control)
    server.route("/login", ["GET"], garage_control)
    server.route("/login", ["POST"], garage_control)

    while True:
        # Handle events
        sleep(1)


if __name__ == "__main__":
    main()
