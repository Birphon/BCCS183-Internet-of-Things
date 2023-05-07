
from realhttp import *
from time import *
from json import *
 
POLLING_TIME = 5  
# Your room_Id is in the JSON you extracted from the previous step in this lab.
ROOM_ID = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMTZmMGJmYzAtZDI3MC0xMWVkLTllN2QtZDk3NGMyMzhhZjJh' 
# You will need to create a new access token as they are only valid for 12 hours from when you log into Webex
PERSONAL_ACCESS_TOKEN = 'MjA4NGM5NTUtM2YxNy00OWQzLWIyYmMtZGVmOTdiMDJmMTgwZDYxNjBhZmEtZjkx_P0A1_cb0fa6b7-6c1c-45f5-aae5-b00413680b83'
API_AUTHORORISATION_KEY = 'Bearer {}'.format(PERSONAL_ACCESS_TOKEN)
MAX_MESSAGES = 1
API_URL = 'https://api.ciscospark.com/v1/messages?roomId={}&max={}'.format(ROOM_ID, MAX_MESSAGES)
HEADER = {'Authorization':API_AUTHORORISATION_KEY}
 
def onHTTPDone(status, data):
    print('status: {}'.format(status))
    print('data: {}'.format(data))
    j_data = loads(data)
    print(j_data)
    print(type(j_data))
 
def main():
    http = RealHTTPClient()
    http.onDone(onHTTPDone)
 
    while True:
        print('Polling')
        http.getWithHeader(API_URL, HEADER)
        sleep(POLLING_TIME)
 
if __name__ == "__main__":
    main() 
