from json import *
from time import *

from gpio import *
from realhttp import *
from tcp import *
from udp import *

# Global Vars and Consts
room_list = []
MAXTEMP = 25 # Testing Value
EMPTY = 0

# Networking
DEST_IPV6_ADDR = '2001:DB8:ACAD:1::3'
PORT = 5000

# API
API_URL = 'http://172.17.67.24/api/environment'

def onHTTPDone(status, data):
    """ 
        Callback function that is triggered when an HTTP Request is completed, parsing relevant data into global variable which is then used in a Check. If the check is meet the value populates a List 
    """
    j_data = loads(data)
    for room in j_data:
        pc_temp = j_data[room]
        if pc_temp >= MAXTEMP:
            room_list.append(room)

def send_instruction(instruction):
    """ Sends an instruction message to a TCP client at a specified IPv6 address and port. """
    client = TCPClient()
    client.connect(DEST_IPV6_ADDR, PORT)
    delay(50)
    client.send(instruction)
    delay(50)
    client.close()    

def main():
    """
        The main function that runs the program.
        It retrieves data from the API, checks if the list is empty or not, sends a message
    """
    http = RealHTTPClient()
    http.onDone(onHTTPDone)
    while True:
        http.get(API_URL)
        if room_list != EMPTY:
            send_instruction(room_list)
            print(room_list)
            del room_list[:]
            print(room_list)
        sleep(5)

if __name__ == '__main__':
    main()