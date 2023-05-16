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
PIN_LCD = 0
THRESH = 1670 # THRESH is the Threshold, New Zealand has the Ambiant set to 10 milligrams per cubic
TENMIN = 600

# Networking
IPV4_DEST_IP = '192.168.0.18'
PORT = 5000

# API URL Stuff
lat = -43.5379285
lon = 172.6416436
appid = 'b6f2ab6d117dde167c890593abb7ef56'
API_URL = "http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}".format(lat,lon,appid)

# CODE

def startup():
    global alarm_status
    alarm_status = ''

def writeLCD(msg):
    customWrite(PIN_LCD, msg)

def onHTTPDone(status, data):
    global data_carbon
    global data_aqi
    global should_alert
    global alarm_status
    """
        Currently getting invalid Key - using temp nums instead
    """
    j_data = loads(data)
    # print(data)
    # aqi = j_data['list'][0]['main']['aqi']
    # c_data = j_data['list'][0]['components']['co']
    c_data = 2000
    aqi = 1
    data_carbon = c_data
    data_aqi = aqi
    if c_data >= THRESH:
        should_alert = True
        alarm_status = 'ALARM'
    else:
        should_alert = False
        alarm_status = 'Normal'

def send_instruction(instruction):
    client = TCPClient()
    client.connect(IPV4_DEST_IP, PORT)
    delay(50)
    client.send(instruction)
    delay(50)
    client.close()
    
def main():
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
        # sleep(TENMIN)
        sleep(5) # This is for testing

if __name__ == '__main__':
    main()