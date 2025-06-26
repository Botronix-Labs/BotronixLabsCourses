from machine import Pin, PWM
from time import sleep

class Servo:
    def __init__(self, pin_num):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(50)
        self.angle = 90
        self.move_to(90)

    def angle_to_duty(self, angle):
        us = 500 + (angle * 2000 // 180)
        return int(us * 65535 / 20000)

    def move_to(self, angle):
        angle = max(0, min(180, angle))  # Clamp
        self.pwm.duty_u16(self.angle_to_duty(angle))
        self.angle = angle

class RobotArm:
    def __init__(self):
        self.base = Servo(2)
        self.shoulder = Servo(3)
        self.elbow = Servo(4)
        self.gripper = Servo(5)

    def handle_command(self, cmd):
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
