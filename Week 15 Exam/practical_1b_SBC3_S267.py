from time import *

from gpio import *
from tcp import *
from udp import *

port = 5000
server = TCPServer()

PIN_ALARM = 0
PIN_LCD = 1

free_pc_count = ""

def start_up():
    writeLCD("Waiting")

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
        global free_pc_count
        print("received from " + client.remoteIP() + " with data: " + data)
        free_pc_count = data

    client.onConnectionChange(onTCPConnectionChange)
    client.onReceive(onTCPReceive)
        
def main():
    """
        This is the main function that runs the program. 
        It sets up the TCP Server and listens for incoming client connections then calls the alarm_control function.
    """
    start_up()
    server.onNewClient(onTCPNewClient)
    print(server.listen(port))
    
    while True:
        if free_pc_count != "":
            writeLCD("S267: {} free".format(free_pc_count))
        sleep(1)

if __name__ == "__main__":
    main()
        
