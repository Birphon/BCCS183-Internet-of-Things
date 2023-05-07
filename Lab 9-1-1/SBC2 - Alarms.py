from time import *

from gpio import *
from tcp import *
from udp import *

port = 5000
server = TCPServer()

ALARM_ON = 1
ALARM_OFF = 2

PIN_ALARM1 = 0
PIN_ALARM2 = 1
PIN_ALARM3 = 2
PIN_ALARM4 = 3
PIN_ALARM5 = 4

ALARM_START = 0
ALARM_END = 4
START_ALARM = "StartAlarm"
STOP_ALARM = "StopAlarm"

alarm_instruction = ""


def onTCPNewClient(client):
    """ToDo"""

    def onTCPConnectionChange(type):
        print("connection to " + client.remoteIP() + " changed to state " + str(type))

    def onTCPReceive(data):
        global alarm_instruction
        print("received from " + client.remoteIP() + " with data: " + data)
        alarm_instruction = data

    client.onConnectionChange(onTCPConnectionChange)
    client.onReceive(onTCPReceive)


def alarm_control():
    """ToDo"""
    if alarm_instruction == START_ALARM:
        for alarm in range(ALARM_START, ALARM_END + 1):
            digitalWrite(alarm, HIGH)
        delay(50)
        for alarm in range(ALARM_START, ALARM_END + 1):
            digitalWrite(alarm, LOW)

    if alarm_instruction == STOP_ALARM:
        for alarm in range(ALARM_START, ALARM_END + 1):
            digitalWrite(alarm, LOW)


def main():
    """ToDo"""
    server.onNewClient(onTCPNewClient)
    print(server.listen(port))

    # don't let it finish
    while True:
        alarm_control()
        sleep(1)


if __name__ == "__main__":
    main()
