# Joystick-Based Base Rotation Control for Robotic Arm
# Hardware: Raspberry Pi Pico + HW-504 Joystick + Servo Motor (on GP2)
# Author: Botronix Labs
# Description:
#   This script demonstrates how to control a servo motor (base rotation)
#   using the X-axis of an analog joystick module with real-time response,
#   a dead zone filter, and a button press detector.

from machine import ADC, Pin, PWM
from time import sleep

# --- Hardware Setup ---
x_axis = ADC(26)                          # X-axis of joystick connected to ADC pin GP26
button = Pin(15, Pin.IN, Pin.PULL_UP)     # Joystick push-button on GP15 with pull-up
base_servo = PWM(Pin(2))                  # Servo connected to GP2 (PWM pin)
base_servo.freq(50)                       # Standard servo PWM frequency (50Hz)

# --- Helper Functions ---

def angle_to_duty(angle):
    """
    Converts a servo angle (0–180 degrees) to a PWM duty cycle.
    """
    min_us = 500       # Minimum pulse width in microseconds
    max_us = 2500      # Maximum pulse width in microseconds
    us = min_us + (max_us - min_us) * angle // 180
    return int(us * 65535 / 20000)  # Convert microseconds to 16-bit duty cycle

def move_base(angle):
    """
    Moves the base servo to the specified angle.
    """
    base_servo.duty_u16(angle_to_duty(angle))

def sweep_to_angle(current, target):
    """
    Smoothly sweeps the servo from current angle to target angle in 1° steps.
    """
    step = 1 if current < target else -1
    for a in range(current, target + step, step):
        move_base(a)
        sleep(0.02)  # Delay for smooth movement
    return target

# --- Initialization ---

center = 32767            # Joystick center value for 16-bit ADC range
dead_zone = 2000          # Ignore small movements around the center
current_base_angle = 0    # Start from 0° angle
move_base(current_base_angle)  # Initialize servo to starting position

# --- Main Loop ---

while True:
    # Read analog value from X-axis of joystick
    x_val = x_axis.read_u16()
    print(f"X: {x_val}")

    # Dead zone filter: Only react to meaningful movement
    if abs(x_val - center) > dead_zone:
        angle = int(x_val * 180 / 65535)  # Map joystick value to angle (0–180°)

        # Sweep base servo to new angle smoothly
        current_base_angle = sweep_to_angle(current_base_angle, angle)
        print(f"Base Angle: {current_base_angle}")

    # Detect joystick button press
    if button.value() == 0:
        print("Joystick button pressed!")

    sleep(0.05)  # Short delay for stability
