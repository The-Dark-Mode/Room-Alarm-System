import tinytuya
import curses

# Define functions for turning on and off
def turn_on():
    print("Device turned on")
    d.turn_on()

def turn_off():
    print("Device turned off")
    d.turn_off()

# Connect to Device
d = tinytuya.OutletDevice(
    dev_id='id',
    address='private_ipv4',
    local_key='keyl', 
    version=3.3)

# Get Status
data = d.status() 
print('set_status() result %r' % data)

# Initialize curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)

# Define listener function
def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Press 'e' to turn on and 'r' to turn off\n") # for testing - used with a physical wired keyboard
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('e'):
            turn_on()
        elif key == ord('r'):
            turn_off()
        elif key == ord('q'):
            break

# Run the listener
curses.wrapper(main)