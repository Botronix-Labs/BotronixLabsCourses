
"""
main.py (mpu_plot_sender.py)

Reads data from the MPU9255 IMU sensor and prints pitch, roll, and gyro data for real-time plotting.
Uses the MPU9255Sensor class and its static method for pitch/roll calculation.
"""

from machine import Pin, I2C
from mpu9255_sensor import MPU9255Sensor
import time

# Setup LED pins (for status indication)
eye_l = Pin(17, Pin.OUT)
eye_r = Pin(16, Pin.OUT)

# Initialize I2C and sensor
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Adjust pins if needed
imu = MPU9255Sensor(i2c)
print(i2c.scan())  # Expect [104] or [105]

eye_l.value(1)
eye_r.value(1)

while True:
    # Read raw accelerometer and gyroscope data
    ax, ay, az, gx, gy, gz = imu.get_accel_gyro()
    # Calculate pitch and roll using the instance method
    pitch, roll = imu.get_pitch_roll()

    # Print data in CSV format: pitch,roll,gx,gy,gz
    print(f"{pitch:.2f},{roll:.2f},{gx},{gy},{gz}")
    time.sleep(0.1)
