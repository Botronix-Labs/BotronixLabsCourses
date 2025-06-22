from machine import Pin
from lcd_display import LCDDisplay
from ble_tank_client import BLETankClient
import time

# Initialize LCD
lcd = LCDDisplay()

# Define Buttons
button_b = Pin(17, Pin.IN, Pin.PULL_UP)  # Connect
button_x = Pin(19, Pin.IN, Pin.PULL_UP)  # Disconnect

# Joystick pins
up = Pin(2, Pin.IN, Pin.PULL_UP)
down = Pin(18, Pin.IN, Pin.PULL_UP)
left = Pin(16, Pin.IN, Pin.PULL_UP)
right = Pin(20, Pin.IN, Pin.PULL_UP)
ctrl = Pin(3, Pin.IN, Pin.PULL_UP)  # Center = Stop

obstacle_status = "Unknown"

def on_rx(msg):
    global obstacle_status
    print("📩 Received from tank:", msg)
    if msg in ["Obstacle Detected", "Path Clear"]:
        obstacle_status = msg
        draw_gui(selected=last_command)# update the screen
        
  
# Setup BLE
ble = BLETankClient()
ble.on_rx = on_rx
last_command = ""
connection_status = "Disconnected"
tank_name = "PicoTank"

def draw_gui(selected=""):
    lcd.fill(lcd.white)
    lcd.text("Pico BLE Controller", 20, 10, lcd.red)
    lcd.text("Tank: " + tank_name, 20, 30, lcd.green)
    lcd.text("B: Connect  X: Disconnect", 20, 50, lcd.blue)
    lcd.text("Status: " + connection_status, 20, 70, lcd.red)

    # Arrow layout
    # Arrow color logic
    # ASCII arrow alternatives
    def color(key): return lcd.red if key == selected else lcd.black

    lcd.text("^", 115, 100, color("F"))
    lcd.text("v", 115, 140, color("B"))
    lcd.text("<", 95, 120, color("L"))
    lcd.text(">", 135, 120, color("R"))
    lcd.text("X", 115, 120, color("S"))  # Stop
    # Outline buttons (like a D-pad)
    lcd.rect(114, 99, 10, 10, color("F"))  # Up
    lcd.rect(114, 139, 10, 10, color("B"))  # Down
    lcd.rect(94, 119, 10, 10, color("L"))   # Left
    lcd.rect(134, 119, 10, 10, color("R"))  # Right
    lcd.rect(114, 119, 10, 10, color("S"))  # Stop

        # Obstacle status label
    lcd.text("Obstacle:", 20, 180, lcd.black)
    lcd.text(obstacle_status, 100, 180, lcd.red if obstacle_status == "Obstacle!" else lcd.green)
    lcd.show()

draw_gui()

while True:
    try:
        # Handle Connect
        if not button_b.value():
            if not ble.connected:
                print("🔗 Button B pressed: Connecting...")
                connection_status = "Connecting..."
                draw_gui()
                ble.connect()
                time.sleep(0.5)

        # Handle Disconnect
        if not button_x.value():
            if ble.connected:
                print("❌ Button X pressed: Disconnecting...")
                ble.ble.gap_disconnect(ble.conn_handle)
                connection_status = "Disconnected"
                draw_gui()
                time.sleep(0.5)

        # Refresh status if changed externally
        if ble.connected and connection_status != "Connected":
            connection_status = "Connected"
            print("✅ BLE connected")
            draw_gui()
        elif not ble.connected and connection_status != "Disconnected":
            connection_status = "Disconnected"
            print("🔌 BLE disconnected")
            draw_gui()

        # Handle joystick movement
        command = ""
        if not up.value():
            command = "F"
        elif not down.value():
            command = "B"
        elif not left.value():
            command = "L"
        elif not right.value():
            command = "R"
        elif not ctrl.value():
            command = "S"

        if command and command != last_command:
            ble.send_command(command)
            print(f"➡️ Sent command: {command}")
            draw_gui(selected=command)
            last_command = command

        elif not command and last_command:
            draw_gui(selected=None)
            last_command = ""

        time.sleep(0.1)

    except KeyboardInterrupt:
        print("🛑 Script interrupted")
        if ble.connected:
            ble.send_command("S")
            ble.ble.gap_disconnect(ble.conn_handle)
        break
