from machine import Pin
import bluetooth
import time

from robot_tank import RobotTank
from ble_tank_server import BLETankServer
from ble_led import BleLED
from obstacle_sensor import ObstacleSensor

# ð· Setup Components
led = BleLED()
tank = RobotTank(2, 3, 4, 5)
obstacle = ObstacleSensor()

# Store last command to restore after obstacle clears
last_command = "S"

def on_rx(command):
    global last_command
     
    print("ð¥ Command received:", command)
    led.toggle()  

    try:
        if command in ["F", "B", "L", "R"]:
            last_command = command

        if obstacle.is_obstacle():
            print("â Obstacle detected â stopping")
            tank.stop()
        else:
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
                last_command = "S"
            else:
                print("â ï¸ Unknown command")
    except Exception as e:
        print("â Error executing command:", e)

# Setup BLE
ble = bluetooth.BLE()
ble_server = BLETankServer(ble, on_rx)

print("ð ï¸ Pico Robot Tank is waiting for BLE connection...")
connected = False

try:
    while True:
        is_connected = bool(ble_server._connections)
        if is_connected != connected:
            connected = is_connected
            if connected:
                print("â BLE Connected.")
                led.on()
            else:
                print("ð Waiting for BLE connection...")
                led.off()

        if not connected:
            led.blink()
        else:
            changed, state = obstacle.has_changed()
            if changed:
                if state == 0:
                    print("â Obstacle Detected")
                    tank.stop()
                    ble_server.send("Obstacle Detected")
                    print("ð¤ Message sent to client.")
                else:
                    print("â Path Clear")
                    ble_server.send("Path Clear")
                    print("ð¤ Message sent to client.")
                    if last_command != "S":
                        on_rx(last_command)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("ð Script stopped by user")
    tank.stop()
    led.off()
