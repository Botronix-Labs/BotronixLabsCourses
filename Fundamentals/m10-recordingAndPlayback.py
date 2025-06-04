from machine import ADC, Pin, PWM
from time import sleep

# === Initialize ADCs for Joysticks ===
x1 = ADC(Pin(26))  # Joystick 1 X-axis (Base)
x2 = ADC(Pin(27))  # Joystick 1 Y-axis (Shoulder)
x3 = ADC(Pin(28))  # Joystick 2 X-axis (Elbow)

# === Initialize Buttons ===
button1 = Pin(15, Pin.IN, Pin.PULL_UP)  # Button on Joystick 1
button2 = Pin(14, Pin.IN, Pin.PULL_UP)  # Button on Joystick 2

# === Initialize Servos ===
base_servo = PWM(Pin(2))
shoulder_servo = PWM(Pin(3))
elbow_servo = PWM(Pin(4))
for s in (base_servo, shoulder_servo, elbow_servo):
    s.freq(50)

# === Helper Functions ===
def angle_to_duty(angle):
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * angle // 180
    return int(us * 65535 / 20000)

def move_servo(servo, angle):
    servo.duty_u16(angle_to_duty(angle))

def smooth_move(current, target, servo):
    step = 1 if target > current else -1
    for angle in range(current, target + step, step):
        move_servo(servo, angle)
        sleep(0.01)
    return target

# === Initial Positions ===
base_angle = 0
shoulder_angle = 0
elbow_angle = 0

# Move to initial
base_angle = smooth_move(0, base_angle, base_servo)
shoulder_angle = smooth_move(0, shoulder_angle, shoulder_servo)
elbow_angle = smooth_move(0, elbow_angle, elbow_servo)

# === Joystick Deadzone and Center ===
center = 32767
dead_zone = 3000

# === Recording List ===
recorded_steps = []

# === Button state tracking ===
button1_prev = 1
button2_prev = 1

print("Ready to record movements...")

while True:
    b1 = button1.value()
    b2 = button2.value()

    x1_val = x1.read_u16()
    x2_val = x2.read_u16()
    x3_val = x3.read_u16()

    # Joystick 1 X for base
    if abs(x1_val - center) > dead_zone:
        angle = int(x1_val * 180 / 65535)
        base_angle = smooth_move(base_angle, angle, base_servo)

    # Joystick 1 Y for shoulder
    if abs(x2_val - center) > dead_zone:
        angle = int(x2_val * 180 / 65535)
        shoulder_angle = smooth_move(shoulder_angle, angle, shoulder_servo)

    # Joystick 2 X for elbow
    if abs(x3_val - center) > dead_zone:
        angle = int(x3_val * 180 / 65535)
        elbow_angle = smooth_move(elbow_angle, angle, elbow_servo)

    # Record if either button is newly pressed
    if (b1 == 0 and button1_prev == 1) or (b2 == 0 and button2_prev == 1):
        recorded_steps.append((base_angle, shoulder_angle, elbow_angle))
        print("Recorded:", base_angle, shoulder_angle, elbow_angle)
        sleep(0.3)  # Debounce

    # Playback when both buttons are held
    if b1 == 0 and b2 == 0 and len(recorded_steps) > 0:
        print("Playing back sequence...")
        for step in recorded_steps:
            base_angle = smooth_move(base_angle, step[0], base_servo)
            shoulder_angle = smooth_move(shoulder_angle, step[1], shoulder_servo)
            elbow_angle = smooth_move(elbow_angle, step[2], elbow_servo)
            print("Playing back:", base_angle, shoulder_angle, elbow_angle)
            sleep(0.5)
        print("Playback finished.")
        sleep(1)

    button1_prev = b1
    button2_prev = b2
    sleep(0.05)

