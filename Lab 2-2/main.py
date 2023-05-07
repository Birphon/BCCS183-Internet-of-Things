from time import *

from gpio import *

""" Consts """
PIN_BUTTON = 0
PIN_LCD = 1
PIN_HEAT = 2
PIN_SENS = 3
TMIN = 5.0
temp = 0.0
heat_value = ""
override = False

""" temp getter - also maths the changes between what Packet Tracer gives us and what the LCD displays """
def get_temp():
	global temp
	# Convert from the old range to the new range.
	temp = ((float(analogRead(PIN_SENS)) / 1024) * 201) - 100
	return temp

def heater_on():
	global heat_value
	digitalWrite(PIN_HEAT, HIGH)
	heat_value = "On"

def heater_off():
	global heat_value
	digitalWrite(PIN_HEAT, LOW)
	heat_value = "OFF"
	
# Heater will always stay on?
""" temp checker - changes the Heater to be on or off based on the temperature """		
def heat_control():
	if override == False:
		if temp <= TMIN:
			heater_on()
		else:
			heater_off()
	else:
		heater_on()

""" Manual override button to turn on the heater"""
def override_button():
	global override
	if digitalRead(PIN_BUTTON) == LOW:
		if override == True:
			override = False
		else:
			override = True

def main():
	while True:
		heat_control()
		message = 'temp: {:.1f} {}C\nHeater: {} '.format(get_temp(), chr(176), heat_value)
		customWrite(PIN_LCD, message)
		delay(1)

if __name__ == "__main__":
	add_event_detect(PIN_BUTTON, override_button)
	main()