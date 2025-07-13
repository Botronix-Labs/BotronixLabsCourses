
"""
robot_arm.py

Defines Servo and RobotArm classes for controlling a multi-servo robot arm.
Provides methods for moving servos to specified angles and handling BLE commands.
"""

from machine import Pin, PWM
from time import sleep

class Servo:
    """
    Represents a single servo motor controlled via PWM.
    """
    def __init__(self, pin_num):
        """
        Initialize the servo on the given pin and set to default angle (90).
        Args:
            pin_num (int): GPIO pin number
        """
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(50)
        self.angle = 90
        self.move_to(90)

    def angle_to_duty(self, angle):
        """
        Convert an angle in degrees to PWM duty cycle.
        Args:
            angle (int): Angle in degrees (0-180)
        Returns:
            int: PWM duty cycle value
        """
        us = 500 + (angle * 2000 // 180)
        return int(us * 65535 / 20000)

    def move_to(self, angle):
        """
        Move the servo to the specified angle, clamped to [0, 180].
        Args:
            angle (int): Target angle in degrees
        """
        angle = max(0, min(180, angle))  # Clamp
        self.pwm.duty_u16(self.angle_to_duty(angle))
        self.angle = angle

class RobotArm:
    """
    Controls a multi-servo robot arm and handles BLE commands for movement.
    """
    def __init__(self):
        """
        Initialize all servos for the robot arm.
        """
        self.base = Servo(2)
        self.shoulder = Servo(3)
        self.elbow = Servo(4)
        self.gripper = Servo(5)

    def handle_command(self, cmd):
        """
        Handle a BLE command to move a servo to a specified angle.
        Args:
            cmd (str): Command string, e.g. 'B90' for base to 90 degrees
        """
        if len(cmd) < 2:
            print("⚠️ Invalid command")
            return

        servo_map = {
            'B': self.base,
            'S': self.shoulder,
            'E': self.elbow,
            'G': self.gripper
        }

        try:
            servo_id = cmd[0]
            angle = int(cmd[1:])
            if servo_id in servo_map:
                servo_map[servo_id].move_to(angle)
                print(f"✅ Moved {servo_id} to {angle}°")
            else:
                print("⚠️ Unknown servo ID")
        except ValueError:
            print("❌ Invalid angle format")
