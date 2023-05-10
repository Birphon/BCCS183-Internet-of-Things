from time import *

from gpio import *
from tcp import *
from udp import *

port = 5000
server = TCPServer()

PIN_ALARM = 0
PIN_LCD = 1

alarm_instruction = ""

def writeLCD(msg):
    """
        Custom Write made into a singular function for easier calling
    """
    customWrite(PIN_LCD, msg)

def onTCPNewClient(client):
    """ 
        Handles a new TCP client connection by setting up event handlers for the client.
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
    """
    if alarm_instruction != '':
        writeLCD(alarm_instruction)
        digitalWrite(PIN_ALARM, HIGH)
        delay(50)
        digitalWrite(PIN_ALARM, LOW)
    else:
        writeLCD("status normal")
        digitalWrite(PIN_ALARM, LOW)
        

def main():
    """
        This is the main function that runs the program. 
        It sets up the TCP Server and listens for incoming client connections then calls the alarm_control function.
    """
    server.onNewClient(onTCPNewClient)
    print(server.listen(port))
    
    while True:
        alarm_control()
        sleep(1)

if __name__ == "__main__":
    main()
        
