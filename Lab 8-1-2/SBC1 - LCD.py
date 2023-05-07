from json import *
from time import *

from gpio import *
from realhttp import *
from tcp import *
from udp import *

# Vars and Globals
should_alert = False
message = ''
alarm_status = ''
data_carbon = 0
data_aqi = 0
TIMER = 50
PIN_LCD = 0
THRESH = 1670 # THRESH is the Threshold, New Zealand has the Ambiant set to 10 milligrams per cubic
TENMIN = 600

# Networking
IPV4_DEST_IP = '192.168.0.3'
IPV6_DEST_IP = '2001:DB8:ACAD:0:0:0:0001:0003'
PORT = 5000

# API URL Stuff
lat = -43.5379285
lon = 172.6416436
appid = 'b6f2ab6d117dde167c890593abb7ef56'
API_URL = "http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}".format(lat,lon,appid)

# CODE

def startup():
    """
        Initializes the alarm_status variable

        Args:
            None
        
        Returns:
            None
    """
    global alarm_status
    alarm_status = ''

def writeLCD(msg):
    customWrite(PIN_LCD, msg)

def onHTTPDone(status, data):
    """
        Callback function that is triggered when an HTTP Request is completed, parsing relevant data into global variables

        Args:
            status (int): HTTP Status code
            data (str): The response from the request
        
        Returns:
            None
    """
    global data_carbon
    global data_aqi
    global should_alert
    global alarm_status
    j_data = loads(data)
    # print(data)
    aqi = j_data['list'][0]['main']['aqi']
    c_data = j_data['list'][0]['components']['co']
    data_carbon = c_data
    data_aqi = aqi
    # aqi = 1
    # c_data = 200
    if c_data >= THRESH:
        should_alert = True
        alarm_status = 'ALARM'
    else:
        should_alert = False
        alarm_status = 'Normal'

def send_instruction(instruction):
    """
    Sends an instruction message to a TCP client at a specified IPv6 address and port.

    Args:
        instruction (str): The instruction message to be sent.

    Returns:
        None
    """
    client = TCPClient()
    client.connect(IPV6_DEST_IP, PORT)
    delay(TIMER)
    client.send(instruction)
    delay(TIMER)
    client.close()
    
def main():
    """
    The main function that runs the program. 
    It retrieves data from the API, checks the carbon monoxide level, and sends a message to a TCP client.

    Args:
        None

    Returns:
        None
    """
    global message
    global alarm_status
    startup()
    http = RealHTTPClient()
    http.onDone(onHTTPDone)
    while True:
        http.get(API_URL)
        print(data_aqi, data_carbon)
        if should_alert == True:
            writeLCD("AQI: " + str(data_aqi) + '\n' + "Status: " + alarm_status)
            message = 'StartAlarm'
            send_instruction(message)
        else:
            writeLCD("AQI: " + str(data_aqi) + '\n' + "Status: " + alarm_status)
            message = 'StopAlarm'
            send_instruction(message)
        sleep(TENMIN)
        # sleep(5) # This is for testing

if __name__ == '__main__':
    main()