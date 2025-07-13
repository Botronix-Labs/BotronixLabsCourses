
"""
ble_led.py

Provides a BleLED class for controlling an onboard LED via MicroPython on a microcontroller (e.g., Raspberry Pi Pico W).
Includes methods to turn the LED on/off, toggle its state, and blink with a specified delay.
"""

from machine import Pin
import time


class BleLED:
    """
    Class to control an onboard LED using MicroPython's Pin API.

    Args:
        pin_num (int): GPIO pin number for the LED (default: 16).
    """
    def __init__(self, pin_num=16):
        self.led = Pin(pin_num, Pin.OUT)
        self.blink_state = False  # Track blink state if needed for future expansion

    def on(self):
        """Turn the LED on (set pin high)."""
        self.led.value(1)

    def off(self):
        """Turn the LED off (set pin low)."""
        self.led.value(0)

    def toggle(self):
        """Toggle the LED state (on/off)."""
        self.led.toggle()

    def blink(self, delay=0.3):
        """
        Blink the LED by toggling its state, then waiting for the specified delay.

        Args:
            delay (float): Time in seconds to wait after toggling (default: 0.3).
        """
        self.toggle()
        time.sleep(delay)
