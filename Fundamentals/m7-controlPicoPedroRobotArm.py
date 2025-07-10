"""
m7-controlPicoPedroRobotArm.py

Demonstrates control of a 4-DOF robot arm (base, shoulder, elbow, gripper) using PWM on a Raspberry Pi Pico.
Includes both direct angle moves and smooth sweeping motion for each servo.
"""

from machine import Pin, PWM
from time import sleep

# Setup PWM for each servo (base, shoulder, elbow, gripper)
base = PWM(Pin(2))
shoulder = PWM(Pin(3))
elbow = PWM(Pin(4))
gripper = PWM(Pin(5))

# Set PWM frequency to 50 Hz (standard for servo motors)
for servo in [base, shoulder, elbow, gripper]:
    servo.freq(50)

def move_servo(servo, angle):
    """
    Move a servo to a specified angle (0-180 degrees).
    Args:
        servo (PWM): The PWM object for the servo
        angle (int): Target angle in degrees
    """
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * angle // 180
    duty = int(us * 65535 / 20000)
    servo.duty_u16(duty)

################# Example: Move each servo #################
# Uncomment the following block to test direct moves:
# move_servo(base, 0)
# sleep(1)
# move_servo(shoulder, 0)
# move_servo(elbow, 0)
# move_servo(gripper, 0)
# sleep(3)
# print("All servo move 90 degree")
# move_servo(base, 90)
# sleep(1)
# move_servo(shoulder, 90)
# move_servo(elbow, 90)
# move_servo(gripper, 90)
# sleep(5)
# print("Move shoulder to 30 degree")
# move_servo(shoulder, 30)
# sleep(5)
# print("Open and close gripper")
# move_servo(gripper, 0)   # open
# sleep(1)
# move_servo(gripper, 180)  # close
# sleep(3)
# move_servo(base, 0)
# sleep(1)
# move_servo(shoulder, 0)
# move_servo(elbow, 0)
# move_servo(gripper, 0)
# sleep(3)

#################### Smooth Sweeping Motion ###########################
def angle_to_duty(angle):
    """
    Convert an angle (0-180 degrees) to a 16-bit PWM duty cycle.
    Args:
        angle (int): Target angle in degrees
    Returns:
        int: Duty cycle value for PWM
    """
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * angle // 180
    return int(us * 65535 / 20000)

def sweep_to_angle(servo, current_angle, target_angle, step=2, delay=0.02):
    """
    Smoothly sweep a servo from current_angle to target_angle.
    Args:
        servo (PWM): The PWM object for the servo
        current_angle (int): Starting angle
        target_angle (int): Target angle
        step (int): Step size in degrees
        delay (float): Delay between steps in seconds
    Returns:
        int: The final angle reached (target_angle)
    """
    if current_angle < target_angle:
        for angle in range(current_angle, target_angle + 1, step):
            servo.duty_u16(angle_to_duty(angle))
            sleep(delay)
    else:
        for angle in range(current_angle, target_angle - 1, -step):
            servo.duty_u16(angle_to_duty(angle))
            sleep(delay)
    return target_angle  # Update current angle

# Initial angles for each joint
base_angle = 0
shoulder_angle = 0
elbow_angle = 0
gripper_angle = 0
sleep(1)

# Move to pick-up pose smoothly
base_angle = sweep_to_angle(base, base_angle, 90)
sleep(1)
shoulder_angle = sweep_to_angle(shoulder, shoulder_angle, 90)
elbow_angle = sweep_to_angle(elbow, elbow_angle, 0)
gripper_angle = sweep_to_angle(gripper, gripper_angle, 100)
sleep(1)

# Lift pose
shoulder_angle = sweep_to_angle(shoulder, shoulder_angle, 60)
elbow_angle = sweep_to_angle(elbow, elbow_angle, 10)
sleep(1)

# Drop pose
base_angle = sweep_to_angle(base, base_angle, 0)
sleep(1)
gripper_angle = sweep_to_angle(gripper, gripper_angle, 0)
sleep(1)

# Reset to rest
base_angle = sweep_to_angle(base, base_angle, 0)
sleep(1)
shoulder_angle = sweep_to_angle(shoulder, shoulder_angle, 0)
elbow_angle = sweep_to_angle(elbow, elbow_angle, 0)
gripper_angle = sweep_to_angle(gripper, gripper_angle, 0)
