from machine import Pin
import bluetooth
import time

from robot_tank import RobotTank
from ble_tank_server import BLETankServer
from ble_led import BleLED

# 🚗 Setup Components
led = BleLED()                            # BLE indicator LED (e.g., GPIO 16)
tank = RobotTank(2, 3, 4, 5)              # Motor driver pins: IN1, IN2, IN3, IN4

# 🔄 BLE receive callback
def on_rx(command):
    print("📥 Command received:", command)
    led.toggle()

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

# 📡 Setup BLE server
ble = bluetooth.BLE()
ble_server = BLETankServer(ble, on_rx)

print("🛠️ Pico Robot Tank is waiting for BLE connection...")
connected = False

try:
    while True:
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
            led.blink()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Script stopped by user")
    tank.stop()
    led.off()
