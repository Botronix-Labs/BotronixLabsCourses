
"""
main.py

Main script for the BLE controller client.
Handles LCD display, button/joystick input, BLE connection, and command sending for PicoTank and PicoArm.
"""

from machine import Pin
from lcd_display import LCDDisplay
from ble_controller_client import BLEControllerClient
import time

# --- Init LCD ---
lcd = LCDDisplay()

# --- Buttons ---
button_a = Pin(15, Pin.IN, Pin.PULL_UP)  # Toggle Target
button_b = Pin(17, Pin.IN, Pin.PULL_UP)  # Connect
button_x = Pin(19, Pin.IN, Pin.PULL_UP)  # Disconnect
button_y = Pin(21, Pin.IN, Pin.PULL_UP)  # Reset/Servo Control

# --- Joystick ---
up = Pin(2, Pin.IN, Pin.PULL_UP)
down = Pin(18, Pin.IN, Pin.PULL_UP)
left = Pin(16, Pin.IN, Pin.PULL_UP)
right = Pin(20, Pin.IN, Pin.PULL_UP)
ctrl = Pin(3, Pin.IN, Pin.PULL_UP)  # Center button

# --- BLE Setup ---
ble = BLEControllerClient()
last_command = ""
connection_status = "Disconnected"

# --- Track mode ---
targets = ["PicoTank", "PicoArm"]
target_index = 0
last_toggle_time = 0
servo_angles = {"B": 90, "S": 90, "E": 90, "G": 90}  # base, shoulder, elbow, gripper
servo_directions = {"B": 1, "S": 1, "E": 1, "G": 1}

def draw_gui(selected=None, status_msg=""):
    """
    Draw the LCD GUI with current status and selected command.
    Args:
        selected (str): The currently selected command (F, B, L, R, S)
        status_msg (str): Additional status message to display
    """
    lcd.fill(lcd.white)
    lcd.text("Pico BLE Controller", 20, 10, lcd.red)
    lcd.text("Target: " + ble.target_name, 20, 30, lcd.green)
    lcd.text("B: Connect", 20, 50, lcd.blue)
    lcd.text("X: Disconnect", 20, 70, lcd.blue)
    lcd.text("A: Toggle Target", 20, 90, lcd.blue)
    lcd.text("Y+Joy: Control Arm", 20, 110, lcd.blue)
    lcd.text("Status: " + connection_status, 20, 130, lcd.red)
    lcd.text("Info: " + status_msg, 20, 150, lcd.black)

    # Draw D-pad
    def c(k): return lcd.red if k == selected else lcd.black
    lcd.text("^", 115, 170, c("F"))
    lcd.text("v", 115, 210, c("B"))
    lcd.text("<", 95, 190, c("L"))
    lcd.text(">", 135, 190, c("R"))
    lcd.text("X", 115, 190, c("S"))
    lcd.rect(114, 169, 10, 10, c("F"))  # Up
    lcd.rect(114, 209, 10, 10, c("B"))  # Down
    lcd.rect(94, 189, 10, 10, c("L"))   # Left
    lcd.rect(134, 189, 10, 10, c("R"))  # Right
    lcd.rect(114, 189, 10, 10, c("S"))  # Center
    lcd.show()

draw_gui()

def send_servo_command(joint):
    angle = servo_angles[joint]
    direction = servo_directions[joint]
    angle += 20 * direction
    if angle >= 180:
        angle = 180
        servo_directions[joint] = -1
    elif angle <= 0:
        angle = 0
        servo_directions[joint] = 1
    servo_angles[joint] = angle
    ble.send_command(f"{joint}{angle}")
    draw_gui(status_msg=f"{joint} angle â {angle}Â°")

def reset_servos():
    for joint in ["B", "S", "E", "G"]:
        servo_directions[joint] = 1
        if joint == "B":
            ble.send_command(f"{joint}90")
            servo_angles[joint] = 90
        elif joint == "S":
            ble.send_command(f"{joint}0")
            servo_angles[joint] = 0
        elif joint == "E":
            ble.send_command(f"{joint}0")
            servo_angles[joint] = 0
        elif joint == "G":
            ble.send_command(f"{joint}180")
            servo_angles[joint] = 180
        time.sleep(0.3)  # Add a short delay after each command
    draw_gui(status_msg="Reset all servos")

# Main loop
while True:
    try:
        now = time.ticks_ms()

        # --- Toggle BLE Target ---
        if not button_a.value() and time.ticks_diff(now, last_toggle_time) > 1000:
            target_index = (target_index + 1) % len(targets)
            ble.switch_target(targets[target_index])
            draw_gui(status_msg="Switched target")
            last_toggle_time = now

        # --- Connect ---
        if not button_b.value():
            if not ble.connected:
                connection_status = "Connecting..."
                draw_gui()
                ble.connect()
                time.sleep(0.5)

        # --- Disconnect ---
        if not button_x.value():
            if ble.connected:
                ble.disconnect()
                connection_status = "Disconnected"
                draw_gui()
                time.sleep(0.5)

        # --- BLE State UI ---
        if ble.connected and connection_status != "Connected":
            connection_status = "Connected"
            draw_gui()
        elif not ble.connected and connection_status != "Disconnected":
            connection_status = "Disconnected"
            draw_gui()

        command = ""
        # --- Tank joystick controls ---
        if ble.target_name == "PicoTank":
            if not up.value(): command = "F"
            elif not down.value(): command = "B"
            elif not left.value(): command = "L"
            elif not right.value(): command = "R"
            elif not ctrl.value(): command = "S"

            if command and command != last_command:
                ble.send_command(command)
                draw_gui(selected=command)
                last_command = command
            elif not command and last_command:
                draw_gui(selected=None)
                last_command = ""

        # --- Arm joystick + button_y control ---
        if ble.target_name == "PicoArm":
            if not button_y.value():
                if not up.value(): send_servo_command("S")   # shoulder
                elif not down.value(): send_servo_command("E")  # elbow
                elif not left.value(): send_servo_command("B")  # base
                elif not right.value(): send_servo_command("G")  # gripper angle
                else: reset_servos()
                time.sleep(0.2)
            if not ctrl.value():
                ble.send_command("T")  # Toggle gripper open/close
                draw_gui(status_msg="Gripper toggled")
                time.sleep(0.2)

        time.sleep(0.05)

    except Exception as e:
        print("❌ Error:", e)
        draw_gui(status_msg=str(e))
        time.sleep(1)
