from time import *

from gpio import *

""" STATES """
IDLE_STATE = 0
INPUT_STATE = 1
TIMER_STATE = 2
TIMER_START_STATE = 3
CANCEL_STATE = 4
ENTER_STATE = 5
DOOR_OPEN = 6
DOOR_CLOSE = 7

""" PINS """
PIN_DOOR = 0
PIN_LCD = 1
PIN_A = 2
PIN_B = 3
PIN_C = 4
PIN_D = 5
PIN_E = 6
PIN_F = 7
PIN_ENTER = 8
PIN_CANCEL = 9

""" CONST AND VARS """
PASS = "AB"
DOOR_CLOSE_TIME = 5
TIME_OUT = 5
EXPIRE_TIME = 10
cur_uptime = 0
time_state = 0
btn_press = 0
usr_input = ""
door_can_open = False

""" Debugger / Validator - could also add a limited for user inputting as well """
def to_many_hexas():
    if len(PASS) > 4:
        print("\nPasscode too long\nMax 4 Hexadecimals!\n")
        quit()

""" CODE """

""" Outputs the uptime() into "Human" time and counts down the 10 seconds """
def expire_time():
    global state
    global cur_uptime
    global time_state
    if state == TIMER_START_STATE:
        time_state = uptime()
    current_time = (((time_state - uptime())*-1)-10)*-1
    msg = 'Entering Code\n{:.0f} seconds left'.format(current_time)
    write_lcd(msg)
    if current_time <= 0:
        write_lcd('Timed Out!')
        sleep(TIME_OUT)
        return setup()
    return TIMER_STATE

""" Initial / Idle state """
def waiting_for_user():
    if usr_input != '':
        return TIMER_START_STATE
    customWrite(PIN_LCD, 'Enter Code to \nOpen the Door')
    return IDLE_STATE

""" Simple Enter Button Code"""
def enter():
    global state
    if digitalRead(PIN_ENTER, HIGH):
        state = ENTER_STATE

""" Simple Cancel Button Code """
def cancel():
    global state    
    if digitalRead(PIN_CANCEL, HIGH):
        cancel_btn()

""" Defaulter - when run sets all the defaults """
def setup():
    global usr_input
    global state
    global cur_uptime
    cur_uptime = 0
    usr_input = "" 
    state = IDLE_STATE
    return state

""" Simple Button Code """
def a_btn_press():
    global usr_input
    global state
    CHAR = "A"
    if digitalRead(PIN_A):
        usr_input = usr_input+CHAR
        return usr_input

def b_btn_press():
    global usr_input
    global state
    CHAR = "B"
    if digitalRead(PIN_B):
        usr_input = usr_input+CHAR
        return usr_input
        
def c_btn_press():
    global usr_input
    global state
    CHAR = "C"
    if digitalRead(PIN_C):
        usr_input = usr_input+CHAR
        return usr_input
        
def d_btn_press():
    global usr_input
    global state
    CHAR = "D"
    if digitalRead(PIN_D):
        usr_input = usr_input+CHAR
        return usr_input
        
def e_btn_press():
    global usr_input
    global state
    CHAR = "E"
    if digitalRead(PIN_E):
        usr_input = usr_input+CHAR
        return usr_input
        
def f_btn_press():
    global usr_input
    global state
    CHAR = "F"
    if digitalRead(PIN_F):
        usr_input = usr_input+CHAR
        return usr_input
    
def write_lcd(message):
    customWrite(PIN_LCD, message)

""" Opens the door if the Validator is True, closes after 5 seconds """
def open_door():
    global state
    pass_validator()
    customWrite(PIN_DOOR, 'Open')
    write_lcd("Doors open")
    sleep(DOOR_CLOSE_TIME)
    state = DOOR_CLOSE    
    return state

def cancel_btn():
    global state
    write_lcd("No code\nentered")
    sleep(TIME_OUT)
    state = CANCEL_STATE

""" Door Close Code - Seperated if it needs to be called elsewhere"""    
def close_door():
    customWrite(PIN_DOOR, 'Close')
    write_lcd("Doors closed")
    return setup()

""" Validator for the password - compares between PASS (Admin set) and usr_input (User Input)"""
def pass_validator():
    global state
    if state == INPUT_STATE:
        if PASS == usr_input:
            state = DOOR_OPEN
        else:
            cancel_btn()
    return state

def main():
    global state
    to_many_hexas()
    setup()
    while True:
        if state == IDLE_STATE:
            state = waiting_for_user()
        if state == ENTER_STATE:
            state = open_door()
        if state == CANCEL_STATE:
            state = setup()
        if state == DOOR_CLOSE:
            state = close_door()
        if state == TIMER_START_STATE:
            state = expire_time()
        if state == TIMER_STATE:
            state = expire_time()
        sleep(1)

if __name__ == "__main__":
    add_event_detect(PIN_A, a_btn_press)
    add_event_detect(PIN_B, b_btn_press)
    add_event_detect(PIN_C, c_btn_press)
    add_event_detect(PIN_D, d_btn_press)
    add_event_detect(PIN_E, e_btn_press)
    add_event_detect(PIN_F, f_btn_press)
    add_event_detect(PIN_ENTER, enter)
    add_event_detect(PIN_CANCEL, cancel)
    main()