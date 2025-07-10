"""
m6-interface180servoMotor.py

Demonstrates how to control a standard 180-degree servo motor using PWM on a Raspberry Pi Pico.
Includes functions for moving the servo by microseconds and by angle.
"""

from machine import Pin, PWM
from time import sleep

# Initialize PWM on GPIO 15 for the servo
servo = PWM(Pin(15))  # use GP15
servo.freq(50)        # 50 Hz for standard servo

def move_servo_us(us):
    """
    Move the servo to a position specified by pulse width in microseconds.
    Args:
        us (int): Pulse width in microseconds (typically 500-2500 for 0-180 degrees)
    """
    duty = int(us * 65535 / 20000)  # convert microsecond to 16-bit PWM
    servo.duty_u16(duty)

def move_servo_angle(angle):
    """
    Move the servo to a specified angle (0-180 degrees).
    Args:
        angle (int): Target angle in degrees
    """
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * angle // 180
    move_servo_us(us)
    

# Example 1 usage: Move to specific pulse widths
move_servo_us(500)    # Move to 0 degrees (~500us)
sleep(1)
move_servo_us(1500)   # Move to 90 degrees (~1500us)
sleep(1)
move_servo_us(2500)   # Move to 180 degrees (~2500us)
sleep(1)

# Example 2 usage: Move to angles in sequence
for angle in [0, 90, 180, 90, 0]:
    move_servo_angle(angle)
    sleep(1)


