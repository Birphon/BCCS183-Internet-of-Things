from json import *
from time import *

from gpio import *
from realhttp import *
from tcp import *
from udp import *

# Global Vars and Consts
room_list = []
total_free_pc = 0
FREE_PC = "" # Testing Value
EMPTY = ''

# Networking
DEST_S265_IPV6 = '2001:DB8:ACAD:1::2'
PORT = 5000

# API
API_URL = 'http://172.17.67.24/api/room_usage/?room={}'

def onHTTPDone(status, data):
    """ 
        Callback function that is triggered when an HTTP Request is completed, parsing relevant data into global variable which is then used in a Check. If the check is meet the value populates a List 
    """
    global total_free_pc
    j_data = loads(data)
    for room in j_data:
        pc_temp = j_data[room]
        if pc_temp == FREE_PC:
            room_list.append(room)
            print(room_list)
            total_free_pc = len(room_list)

def send_instruction(instruction):
    """ Sends an instruction message to a TCP client at a specified IPv6 address and port. """
    client = TCPClient()
    client.connect(DEST_S265_IPV6, PORT)
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
        http.get(API_URL.format('s265'))
        if total_free_pc != EMPTY:
            send_instruction(total_free_pc)
            print(total_free_pc)
            del room_list[:]
            print(total_free_pc)
        sleep(5)

if __name__ == '__main__':
    main()