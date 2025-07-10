"""
stepper_motor.py

Provides a StepperMotor class for controlling a stepper motor using GPIO pins.
Supports multiple microstepping modes and direction control.
"""

from machine import Pin
from time import sleep_us
import stepping_mode

class StepperMotor:
    """
    Controls a stepper motor using step, direction, and microstepping pins.
    - step_pin: GPIO pin for step pulses
    - dir_pin: GPIO pin for direction
    - ms1_pin, ms2_pin, ms3_pin: GPIO pins for microstepping mode selection
    """
    def __init__(self, step_pin, dir_pin, ms1_pin, ms2_pin, ms3_pin):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.ms1 = Pin(ms1_pin, Pin.OUT)
        self.ms2 = Pin(ms2_pin, Pin.OUT)
        self.ms3 = Pin(ms3_pin, Pin.OUT)

    def set_stepping_mode(self, mode):
        """Set the microstepping mode using a tuple from stepping_mode.py."""
        self.ms1.value(mode[0])
        self.ms2.value(mode[1])
        self.ms3.value(mode[2])

    def set_direction(self, clockwise=True):
        """Set the rotation direction. True for clockwise, False for counterclockwise."""
        self.dir_pin.value(1 if clockwise else 0)

    def rotate_steps(self, steps, delay_us=1000):
        """Rotate the motor a given number of steps with a specified delay (in microseconds) between steps."""
        for _ in range(steps):
            self.step_pin.high()
            sleep_us(delay_us)
            self.step_pin.low()
            sleep_us(delay_us)

    def rotate_degrees(self, degrees, steps_per_rev=200):
        """Rotate the motor by a specified number of degrees."""
        microsteps = self.calculate_microsteps(steps_per_rev)
        steps_needed = int((degrees / 360.0) * microsteps)
        self.rotate_steps(steps_needed)

    def calculate_microsteps(self, base_steps=200):
        """Calculate the effective number of microsteps per revolution based on the current stepping mode."""
        mode_state = (self.ms1.value(), self.ms2.value(), self.ms3.value())
        microstep_table = {
            (0, 0, 0): 1,    # Full step
            (1, 0, 0): 2,    # Half step
            (0, 1, 0): 4,    # Quarter step
            (1, 1, 0): 8,    # Eighth step
            (1, 1, 1): 16    # Sixteenth step
        }
        return base_steps * microstep_table.get(mode_state, 1)
