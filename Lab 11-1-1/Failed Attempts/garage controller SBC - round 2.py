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


def get_login(context, request, reply):
    print("Get_Login: " + request.url() + " @ " + request.ip())
    reply.sendFile("index.html")
    reply.setStatus(200)
    reply.end()


def post_login(context, request, reply):
    global door_status
    global alarm_status

    print("Post_Login: " + request.url() + " @ " + request.ip())
    if "password" in request.form:
        password = request.form["password"]
        if password == PASSWORD:
            open_door()
        else:
            close_door()

    reply.setContent("posted data ...")
    print(request.body)
    reply.setStatus(200)
    reply.end()


def main():
    start()
    server = RealHTTPServer()
    print("Server started: {}".format(server.start(LOCAL_PORT)))
    server.route("/", ["GET"], get_login)
    server.route("/login", ["GET"], get_login)
    server.route("/login", ["POST"], post_login)

    while True:
        # Handle events
        sleep(1)


if __name__ == "__main__":
    main()
