
"""
obstacle_sensor.py

Implements ObstacleSensor class for detecting obstacles using a digital sensor.
"""

from machine import Pin

class ObstacleSensor:
    """
    Detects obstacles using a digital sensor connected to a GPIO pin.
    """
    def __init__(self, pin_num=17):
        """
        Initialize the obstacle sensor pin (default GPIO 17).
        """
        self.sensor = Pin(pin_num, Pin.IN)
        self.last_state = self.read()

    def read(self):
        """
        Read the current value from the obstacle sensor pin.
        Returns:
            int: 0 if obstacle detected, 1 if clear
        """
        return self.sensor.value()

    def is_obstacle(self):
        """
        Check if an obstacle is detected (active low).
        Returns:
            bool: True if obstacle detected, False otherwise
        """
        return self.read() == 0

    def has_changed(self):
        """
        Check if the obstacle sensor state has changed since last check.
        Returns:
            tuple: (changed (bool), current state (int))
        """
        current = self.read()
        changed = current != self.last_state
        self.last_state = current
        return changed, current
