
"""
robot_tank.py

Implements RobotTank class for controlling a tank robot with two motors using GPIO pins.
"""

from machine import Pin

class RobotTank:
    """
    Controls a tank robot with two motors using GPIO pins for direction control.
    """
    def __init__(self, in1_pin, in2_pin, in3_pin, in4_pin):
        """
        Initialize motor driver pins.
        Args:
            in1_pin, in2_pin, in3_pin, in4_pin (int): GPIO pins for motor driver
        """
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.in3 = Pin(in3_pin, Pin.OUT)
        self.in4 = Pin(in4_pin, Pin.OUT)

    def forward(self):
        """
        Move the tank forward by setting both motors forward.
        """
        self.in1.low()
        self.in2.high()
        self.in3.low()
        self.in4.high()

    def backward(self):
        """
        Move the tank backward by setting both motors backward.
        """
        self.in1.high()
        self.in2.low()
        self.in3.high()
        self.in4.low()

    def turn_right(self):
        """
        Turn the tank right by running left motor backward and right motor forward.
        """
        self.in1.high()
        self.in2.low()
        self.in3.low()
        self.in4.high()

    def turn_left(self):
        """
        Turn the tank left by running left motor forward and right motor backward.
        """
        self.in1.low()
        self.in2.high()
        self.in3.high()
        self.in4.low()

    def stop(self):
        """
        Stop both motors.
        """
        self.in1.low()
        self.in2.low()
        self.in3.low()
        self.in4.low()
