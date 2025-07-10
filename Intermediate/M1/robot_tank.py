"""
robot_tank.py

Defines the RobotTank class for controlling a simple 2-motor tank robot using GPIO pins.
Provides methods for forward, backward, left, right, and stop movements.
"""

from machine import Pin

class RobotTank:
    def __init__(self, in1_pin, in2_pin, in3_pin, in4_pin):
        """
        Initialize the RobotTank with four motor driver pins.
        Args:
            in1_pin, in2_pin, in3_pin, in4_pin (int): GPIO pin numbers for motor control
        """
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.in3 = Pin(in3_pin, Pin.OUT)
        self.in4 = Pin(in4_pin, Pin.OUT)

    def forward(self):
        """Move the tank forward."""
        self.in1.low()
        self.in2.high()
        self.in3.low()
        self.in4.high()

    def backward(self):
        """Move the tank backward."""
        self.in1.high()
        self.in2.low()
        self.in3.high()
        self.in4.low()
        
    def turn_right(self):
        """Turn the tank right in place."""
        self.in1.high()
        self.in2.low()
        self.in3.low()
        self.in4.high()

    def turn_left(self):
        """Turn the tank left in place."""
        self.in1.low()
        self.in2.high()
        self.in3.high()
        self.in4.low()
        
    def stop(self):
        """Stop all motors."""
        self.in1.low()
        self.in2.low()
        self.in3.low()
        self.in4.low()

