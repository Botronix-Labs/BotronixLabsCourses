"""
m4-powerUpControl360DegreeServo.py

Demonstrates control of a 360-degree continuous rotation servo motor using PWM on a Raspberry Pi Pico.
Includes functions for clockwise, counterclockwise, and stop, with LED feedback.
"""

from machine import Pin, PWM
import time

# Initialize PWM on GPIO 1 for the servo and GPIO 25 for onboard LED
servo = PWM(Pin(1))
servo.freq(50)
led = Pin(25, Pin.OUT)

def clockwise():
    """Rotate the servo clockwise (forward). Adjust duty as needed for your servo."""
    servo.duty_u16(8000)

def counterclockwise():
    """Rotate the servo counterclockwise (reverse). Adjust duty as needed for your servo."""
    servo.duty_u16(3000)

def stop():
    """Stop the servo by sending a neutral pulse width."""
    servo.duty_u16(5000)

# Main loop: demonstrate servo motion and LED feedback
while True:
    led.value(1)  # Turn on LED to indicate activity
    print("Spinning Clockwise")
    clockwise()
    time.sleep(2)
    print("Stopping")
    stop()
    time.sleep(1)
    print("Spinning Counter-Clockwise")
    counterclockwise()
    time.sleep(2)
    print("Stopping")
    stop()
    time.sleep(1)


