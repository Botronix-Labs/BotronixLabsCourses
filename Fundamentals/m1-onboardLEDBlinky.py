"""
m1-onboardLEDBlinky.py

Simple script to blink the onboard LED on a Raspberry Pi Pico or Pico W.
Demonstrates basic GPIO output and timing control.
"""

from machine import Pin
import time

# Initialize the onboard LED (GPIO 25 on Pico, or use Pin("LED") for Pico W)
led = Pin(25, Pin.OUT)

while True:
    led.toggle()  # Toggle the LED state (on/off)
    time.sleep(0.5)  # Wait for 0.5 seconds
