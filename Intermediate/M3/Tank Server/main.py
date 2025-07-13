
"""
main.py

Entry point for the Pico Robot Tank BLE server.
Initializes BLE, LED, and tank motor control, and processes BLE commands to control the robot.
Designed for MicroPython on Raspberry Pi Pico W or similar boards.
"""

from machine import Pin
import bluetooth
import time

from robot_tank import RobotTank
from ble_tank_server import BLETankServer
from ble_led import BleLED

# --- Setup Components ---
led = BleLED()                            # BLE indicator LED (e.g., GPIO 16)
tank = RobotTank(2, 3, 4, 5)              # Motor driver pins: IN1, IN2, IN3, IN4

def on_rx(command):
    """
    BLE receive callback. Handles incoming commands and controls the tank robot.

    Args:
        command (str): Single-character command from BLE client.
            'F' = Forward, 'B' = Backward, 'L' = Left, 'R' = Right, 'S' = Stop
    """
    print("📥 Command received:", command)
    led.toggle()  # Indicate command received

    try:
        if command == "F":
            tank.forward()
        elif command == "B":
            tank.backward()
        elif command == "L":
            tank.turn_left()
        elif command == "R":
            tank.turn_right()
        elif command == "S":
            tank.stop()
        else:
            print("⚠️ Unknown command")
    except Exception as e:
        print("❌ Error executing command:", e)

# --- Setup BLE server ---
ble = bluetooth.BLE()
ble_server = BLETankServer(ble, on_rx)

print("🛠️ Pico Robot Tank is waiting for BLE connection...")
connected = False

try:
    while True:
        # Check BLE connection status
        is_connected = bool(ble_server._connections)

        if is_connected != connected:
            connected = is_connected
            if connected:
                print("✅ BLE Connected.")
                led.on()
            else:
                print("🔄 Waiting for BLE connection...")
                led.off()

        if not connected:
            led.blink()  # Blink LED while waiting for connection

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Script stopped by user")
    tank.stop()
    led.off()
