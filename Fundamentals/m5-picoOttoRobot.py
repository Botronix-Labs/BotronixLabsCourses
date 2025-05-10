from machine import Pin, PWM
import time

# Power Indicator LED
power_led = Pin(5, Pin.OUT)
power_led.high()  # LED on when powered

# Ultrasonic Sensor Pins
trig = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)

# Buzzer
buzzer = Pin(4, Pin.OUT)

# Servo Motors (Continuous Rotation)
left_servo = PWM(Pin(14))
right_servo = PWM(Pin(13))

left_servo.freq(50)
right_servo.freq(50)


# 7-Segment Display connected to GP16–GP22
segment_pins = [
    Pin(16, Pin.OUT),  # A
    Pin(17, Pin.OUT),  # B
    Pin(18, Pin.OUT),  # C
    Pin(19, Pin.OUT),  # D
    Pin(20, Pin.OUT),  # E
    Pin(21, Pin.OUT),  # F
    Pin(22, Pin.OUT)   # G
]

# Segment bit patterns for common characters
segment_map = {
    'F': [1, 1, 0, 0, 0, 1, 1],
    'S': [1, 0, 1, 1, 0, 1, 1],
    'B': [0, 0, 1, 1, 1, 1, 1],
    'U':[1,1,1,1,0,0,0],
    'W':[1,1,1,1,0,0,1],
    'O':[1,1,1,1,1,1,0]
}

# Function to measure distance
def measure_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()

    while echo.value() == 0:
        pulse_start = time.ticks_us()

    while echo.value() == 1:
        pulse_end = time.ticks_us()

    duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (duration * 0.0343) / 2  # in cm
    return distance

# Servo control functions
def stop():
    left_servo.duty_u16(5000)
    right_servo.duty_u16(5000)

def forward():
    left_servo.duty_u16(8000)
    right_servo.duty_u16(3000)

def backward():
    left_servo.duty_u16(3000)
    right_servo.duty_u16(8000)

def turn_left():
    left_servo.duty_u16(3000)
    right_servo.duty_u16(3000)

def turn_right():
    left_servo.duty_u16(8000)
    right_servo.duty_u16(8000)

def display_char(char):
    pattern = segment_map.get(char.upper(), [0] * 7)
    for pin, val in zip(segment_pins, pattern):
        pin.value(val)
# Main loop
try:
    while True:
        
        distance = measure_distance()
        print("Distance:", distance, "cm")

        if distance < 10:
            stop()
            buzzer.high()
            display_char('O')
            time.sleep(0.5)

            # Backup and turn logic
            backward()
            time.sleep(1)
            turn_right()
            time.sleep(1)
            stop()

        elif distance < 20:
            display_char('W')
            buzzer.high()
            forward()
            time.sleep(0.2)
            buzzer.low()

        else:
            buzzer.low()
            forward()
            display_char('U')
            time.sleep(0.1)

except KeyboardInterrupt:
    stop()
    buzzer.low()
    power_led.low()
    print("Program stopped.")

