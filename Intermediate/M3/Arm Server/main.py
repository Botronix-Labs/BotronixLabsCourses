
"""
main.py

Main script for the BLE-controlled robot arm server.
Initializes servos, BLE server, and handles incoming BLE commands to control the arm.
Provides functions for smooth servo movement and angle conversion.
"""

from machine import Pin, PWM
import bluetooth
import time

from ble_led import BleLED
from ble_arm_server import BLEArmServer

# Servo motor pins
base = PWM(Pin(2))
shoulder = PWM(Pin(3))
elbow = PWM(Pin(4))
gripper = PWM(Pin(5))

for servo in [base, shoulder, elbow, gripper]:
    servo.freq(50)

# LED indicator (yellow)
led = BleLED(13)

def angle_to_duty(angle):
    """
    Convert an angle in degrees to PWM duty cycle for servo control.
    Args:
        angle (int): Angle in degrees (0-180)
    Returns:
        int: PWM duty cycle value
    """
    us = 500 + (angle * 2000) // 180
    return int(us * 65535 / 20000)

def move_servo(servo, angle):
    """
    Move a servo to the specified angle.
    Args:
        servo (PWM): Servo PWM object
        angle (int): Target angle in degrees
    """
    servo.duty_u16(angle_to_duty(angle))

def sweep_servo(servo, start_angle, end_angle, step=1, delay=0.01):
    """
    Sweep a servo smoothly from start_angle to end_angle.
    Args:
        servo (PWM): Servo PWM object
        start_angle (int): Starting angle
        end_angle (int): Ending angle
        step (int): Step size in degrees
        delay (float): Delay between steps in seconds
    """
    if start_angle == end_angle:
        return
    direction = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle, direction * step):
        move_servo(servo, angle)
        time.sleep(delay)
    move_servo(servo, end_angle)  # Ensure final position

def initialize_servos():
    """
    Initialize all servos to their default positions.
    """
    move_servo(base, 90)
    move_servo(shoulder, 0)
    move_servo(elbow, 0)
    move_servo(gripper, 180)
    print("✅ Servos initialized to default positions.")

angles = {
    "base": 90,
    "shoulder": 0,
    "elbow": 0,
    "gripper": 180
}

def on_rx(command):
    """
    BLE receive callback to handle incoming commands for servo movement.
    Args:
        command (str): Command string, e.g. 'B90' for base to 90 degrees
    """
    print("📥 Received command:", command)
    led.on()
    try:
        if command.startswith("B"):  # Base
            angle = int(command[1:])
            sweep_servo(base, angles["base"], angle)
            angles["base"] = angle
        elif command.startswith("S"):  # Shoulder
            angle = int(command[1:])
            sweep_servo(shoulder, angles["shoulder"], angle)
            angles["shoulder"] = angle
        elif command.startswith("E"):  # Elbow
            angle = int(command[1:])
            sweep_servo(elbow, angles["elbow"], angle)
            angles["elbow"] = angle
        elif command.startswith("G"):  # Gripper
            angle = int(command[1:])
            sweep_servo(gripper, angles["gripper"], angle)
            angles["gripper"] = angle
        elif command == "T":  # Toggle gripper open/close
            # Toggle between open (180) and closed (0)
            if angles["gripper"] == 180:
                move_servo(gripper, 0)
                angles["gripper"] = 0
                print("🔒 Gripper closed")
            else:
                move_servo(gripper, 180)
                angles["gripper"] = 180
                print("🔓 Gripper opened")
    except Exception as e:
        print("❌ Command error:", e)

# BLE setup
ble = bluetooth.BLE()
arm_server = BLEArmServer(ble, on_rx)

initialize_servos()

print("🦾 BLE Robot Arm is waiting for connection...")

# Status loop
try:
    while True:
        if arm_server._connections:
            led.on()
        else:
            led.blink()
        time.sleep(0.3)

except KeyboardInterrupt:
    print("🛑 Server stopped")
    led.off()
