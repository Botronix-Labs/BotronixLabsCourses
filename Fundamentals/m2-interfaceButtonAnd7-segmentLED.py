"""
m2-interfaceButtonAnd7-segmentLED.py

Demonstrates interfacing a push button and a 7-segment LED display with a Raspberry Pi Pico.
Each button press increments the displayed digit (0-9).
"""

from machine import Pin
import time

# Map GPIOs to 7-segment display segments (A-G)
segment_pins = {
    'A': Pin(0, Pin.OUT),
    'B': Pin(1, Pin.OUT),
    'C': Pin(2, Pin.OUT),
    'D': Pin(3, Pin.OUT),
    'E': Pin(4, Pin.OUT),
    'F': Pin(5, Pin.OUT),
    'G': Pin(6, Pin.OUT)
}

# Segment patterns for digits 0-9 (list of segments to turn ON)
digit_patterns = {
    0: ['A', 'B', 'C', 'D', 'E', 'F'],
    1: ['B', 'C'],
    2: ['A', 'B', 'G', 'E', 'D'],
    3: ['A', 'B', 'C', 'D', 'G'],
    4: ['F', 'G', 'B', 'C'],
    5: ['A', 'F', 'G', 'C', 'D'],
    6: ['A', 'F', 'G', 'C', 'D', 'E'],
    7: ['A', 'B', 'C'],
    8: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    9: ['A', 'B', 'C', 'D', 'F', 'G']
}

# Push button input (active HIGH with internal pull-down resistor)
button = Pin(7, Pin.IN, Pin.PULL_DOWN)

def show_digit(num):
    """Display a single digit (0-9) on the 7-segment display."""
    # Turn off all segments first
    for seg in segment_pins:
        segment_pins[seg].value(0)
    # Turn on only required segments
    for seg in digit_patterns[num]:
        segment_pins[seg].value(1)

current_digit = 0
last_button_state = 0

while True:
    button_state = button.value()
    if button_state and not last_button_state:
        # Rising edge detected (button press)
        current_digit = (current_digit + 1) % 10
        show_digit(current_digit)
        time.sleep(0.2)  # Debounce delay
    last_button_state = button_state

