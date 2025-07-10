
"""
ble_led.py

Controls an onboard LED to indicate BLE connection status.
"""

from machine import Pin
import time

class BleLED:
    """
    Controls the onboard LED to indicate BLE connection status.
    """
    def __init__(self, pin_num=16):
        """
        Initialize the onboard LED pin (default GPIO 16).
        """
        self.led = Pin(pin_num, Pin.OUT)
        self.blink_state = False

    def on(self):
        """
        Turn the LED on (BLE connected).
        """
        self.led.value(1)

    def off(self):
        """
        Turn the LED off (BLE disconnected).
        """
        self.led.value(0)

    def toggle(self):
        """
        Toggle the LED state.
        """
        self.led.toggle()

    def blink(self, delay=0.3):
        """
        Blink the LED with a specified delay.
        Args:
            delay (float): Time in seconds to wait between toggles
        """
        self.toggle()
        time.sleep(delay)
