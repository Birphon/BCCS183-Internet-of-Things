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
START_ALARM = 'StartAlarm'
STOP_ALARM = 'StopAlarm'

alarm_instruction = ''

def onTCPNewClient(client):
    """
    Handles a new TCP client connection by setting up event handlers for the client.
    
    Args:
        client: A TCPClient object representing the new client connection.
        
    Returns:
        None
    """
    def onTCPConnectionChange(type):
        print("connection to " + client.remoteIP() + " changed to state " + str(type))
        
    def onTCPReceive(data):
        global alarm_instruction
        print("received from " + client.remoteIP() + " with data: " + data)
        alarm_instruction = data

    client.onConnectionChange(onTCPConnectionChange)
    client.onReceive(onTCPReceive)

def alarm_control():
    """
    Control the alarm system based on received instructions.

    Args:
        None

    Returns:
        None
    """
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
    """
    This is the main function that runs the program. 
    It sets up the TCP Server and listens for incoming client connections then calls the alarm_control function.
    
    Args:
        None

    Returns:
        None
    """
    server.onNewClient(onTCPNewClient)
    print(server.listen(port))
    while True:
        alarm_control()
        sleep(1)

if __name__ == "__main__":
    main()