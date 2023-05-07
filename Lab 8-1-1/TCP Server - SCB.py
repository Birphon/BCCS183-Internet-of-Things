from time import *

from gpio import *
from tcp import *

port = 5000
server = TCPServer()

LED_ON = 1
LED_OFF = 2

PIN_LED = 0

def onTCPNewClient(client):
	def onTCPConnectionChange(type):
		print("connection to " + client.remoteIP() + " changed to state " + str(type))
		
	def onTCPReceive(data):
		print("received from " + client.remoteIP() + " with data: " + data)
		led_control(data)

	client.onConnectionChange(onTCPConnectionChange)
	client.onReceive(onTCPReceive)

def led_control(data):
	global lights
	if data != '':
		if lights == LED_OFF:
			digitalWrite(PIN_LED, HIGH)
			lights = LED_ON
		elif lights == LED_ON:
			digitalWrite(PIN_LED, LOW)
			lights = LED_OFF
	return

def main():
	server.onNewClient(onTCPNewClient)
	print(server.listen(port))

	# don't let it finish
	while True:
		sleep(3600)

if __name__ == "__main__":
	lights = LED_OFF
	main()