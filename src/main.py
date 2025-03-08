# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Autumn Pan                                                      #
# 	Created:      3/8/2025, 2:42:07 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
# Initialize controller
controller = Controller()


# Control functions

# The claw itself is moved in in the xy plane by two axes, and can be moved vertically.
# Each axis needs its own motor, which will be referred to by its corresponding axis.

x_motor = Motor(Ports.PORT1)
y_motor = Motor(Ports.PORT2)
z_motor = Motor(Ports.PORT3)

min_joystick_pos = 10
# Each tick, check the joystick.
def check_x():
    if controller.axis4.position() > min_joystick_pos:
        x_motor.spin(FORWARD)
    elif controller.axis4.position() > min_joystick_pos:
        x_motor.spin(REVERSE)
    else:
        x_motor.stop()


def check_y():
    if controller.axis3.position() > min_joystick_pos:
        y_motor.spin(FORWARD)
    elif controller.axis3.position() > min_joystick_pos:
        y_motor.spin(REVERSE)
    else:
        y_motor.stop()
        
# How long the initiation countain lasts
max_countdown = 5
# Give countdown before starting
def initiate():
    for i in range(countdown, 0):
        brain.screen.clear_screen()
        brain.screen.print("Starting in " + i + "...")
        wait(1)
    brain.clear_screen()
    control()
# Run checks every 20ms
def control():
    while True:
        check_x()
        check_y()
        wait(20, MSEC)
    
    
initiate()
        
