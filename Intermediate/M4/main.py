"""
main.py

Demonstration script for testing all microstepping modes of a stepper motor.
Cycles through each mode in both clockwise and counterclockwise directions.
"""

from stepper_motor import StepperMotor
import stepping_mode
import time

# Initialize the stepper motor with GPIO pin assignments
motor = StepperMotor(step_pin=15, dir_pin=14, ms1_pin=10, ms2_pin=11, ms3_pin=12)

while True:
    # Test each stepping mode in clockwise direction for 360 degrees
    for mode_name, mode in [
        ("Full Step", stepping_mode.FULL_STEP),
        ("Half Step", stepping_mode.HALF_STEP),
        ("Quarter Step", stepping_mode.QUARTER_STEP),
        ("Eighth Step", stepping_mode.EIGHTH_STEP),
        ("Sixteenth Step", stepping_mode.SIXTEENTH_STEP)
    ]:
        print(f"Testing {mode_name} in clockwise with 360 degrees!")
        motor.set_stepping_mode(mode)
        motor.set_direction(clockwise=True)
        motor.rotate_degrees(360)
        time.sleep(3)

    # Test each stepping mode in counterclockwise direction for 180 degrees, then restore
    for mode_name, mode in [
        ("Full Step", stepping_mode.FULL_STEP),
        ("Half Step", stepping_mode.HALF_STEP),
        ("Quarter Step", stepping_mode.QUARTER_STEP),
        ("Eighth Step", stepping_mode.EIGHTH_STEP),
        ("Sixteenth Step", stepping_mode.SIXTEENTH_STEP)
    ]:
        print(f"Testing {mode_name} in counterclockwise with 180 degrees then restore positions!")
        motor.set_stepping_mode(mode)
        motor.set_direction(clockwise=False)
        motor.rotate_degrees(180)
        time.sleep(1)
        motor.set_direction(clockwise=True)
        motor.rotate_degrees(180)
        time.sleep(3)