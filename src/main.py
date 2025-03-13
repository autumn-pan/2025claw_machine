
#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
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

# Motor speed
x_speed = 0
y_speed = 0

variable_speed = True

# Reset claw position
x_reset = False
y_reset = False



x_force_halt = False
y_force_halt = False

# Control functions

# The claw itself is moved in in the xy plane by two axes, and can be moved vertically.
# Each axis needs its own motor, which will be referred to by its corresponding axis.

x_motor = Motor(Ports.PORT1)
y_motor = Motor(Ports.PORT2)
z_motor = Motor(Ports.PORT3)
claw_motor = Motor(Ports.PORT4)

claw_motor.set_velocity(127, RPM)


phase_shift = 0

def check_z():
    if controller.axis3.position() > 10:
        z_motor.spin(REVERSE, controller.axis3.position())
    elif controller.axis3.position() < -10:
        z_motor.spin(REVERSE, controller.axis3.position())
    else:
        z_motor.stop()

min_joystick_pos = 10



def get_joystick_r_abs():
    return (controller.axis1.position()**2 + controller.axis2.position()**2)**0.5

    
def calibrate_phase_shift():
    global phase_shift
    if controller.buttonLeft.pressing():
        phase_shift -= 0.1
    if controller.buttonRight.pressing():
        phase_shift += 0.1

# Each tick, check the joystick.
def check_x():
    global x_force_halt
    global y_force_halt
    
    if controller.axis4.position() > min_joystick_pos and not (x_force_halt or y_force_halt):
        x_motor.spin(FORWARD, x_speed)
    elif controller.axis4.position() < -min_joystick_pos and not (x_force_halt or y_force_halt):
        x_motor.spin(REVERSE, x_speed)
    elif x_reset and not (x_force_halt or y_force_halt):
        x_motor.spin(FORWARD)
    else:
        x_motor.stop()
    if x_force_halt and controller.axis4.position() == 0:
        x_force_halt = False

def check_y():
    global x_force_halt
    global y_force_halt

    if controller.axis4.position() > min_joystick_pos and not (x_force_halt or y_force_halt):
        y_motor.spin(REVERSE,y_speed)
    elif controller.axis4.position() < -min_joystick_pos and not (x_force_halt or y_force_halt):
        y_motor.spin(FORWARD,y_speed)
    elif y_reset and not (x_force_halt or y_force_halt):
        y_motor.spin(REVERSE)
    else:
        y_motor.stop()
    if (y_force_halt) and controller.axis4.position() == 0:
        y_force_halt = False

def set_speed():
    global x_speed
    global y_speed

    x_speed = abs(controller.axis4.position())
    y_speed = abs(controller.axis4.position())


def x_is_at_edge():
    if x_motor.torque() > 0.5:
        return True
    else:
        return False

def y_is_at_edge():
    if y_motor.torque() > 0.95:
        return True
    else:
        return False



def reset():
    global x_reset
    global y_reset

    x_reset = True
    y_reset = True


# controller.buttonA.pressed(reset)


previous_angle = 0
current_rotation = 0

def set_claw_angle():
    global previous_angle, current_rotation

    x_pos = controller.axis3.position()
    y_pos = controller.axis4.position()

    current_angle_rad = math.atan2(y_pos, x_pos)
    current_angle_deg = math.degrees(current_angle_rad)

    angle_diff = current_angle_deg - previous_angle

    if angle_diff > 180:
        angle_diff -= 360
    elif angle_diff < -180:
        angle_diff += 360
    current_rotation += angle_diff
    claw_motor.spin_to_position(current_rotation)

    previous_angle = current_angle_deg


time = 3000
def timer():
    global time

    seconds = time / 100 

    time -= 1
    brain.screen.clear_screen()
    if seconds > 0:
        brain.screen.print(seconds)
        if seconds < 6:
            controller.rumble('.')

    else:
        brain.screen.print("Time's up!")
        controller.rumble('...')

# Run checks every 10ms
def control():
    while True:
        check_x()
        check_y()
        check_z()
        set_claw_angle()
        calibrate_phase_shift()

        if variable_speed:
            set_speed()

        wait(6.9, MSEC)

        
    
    
control()
