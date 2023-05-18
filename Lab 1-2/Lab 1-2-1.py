from gpio import *
from time import *

""" Setting constants for the ports """
LEDPORT = 0
LCDPORT = 1
TOGGLEBUTTON = 2

# Function to change the message
def writeLCD(msg):
	customWrite(LCDPORT, msg)
	
# Loop to make the LED Blink
def LEDBlinker():
	print("Blinking")
	digitalWrite(LEDPORT, HIGH);
	writeLCD("Blinking")
	sleep(1)
	writeLCD("")
	digitalWrite(LEDPORT, LOW);
	sleep(0.5)

def main():
	pinMode(LEDPORT, OUT)
	# The while True is needed to run the code "forever"
	while True:
		# While the button is pressed it will run the loop
		while digitalRead(TOGGLEBUTTON, LOW):
			LEDBlinker()

if __name__ == "__main__":
	main()