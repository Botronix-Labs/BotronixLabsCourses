# main.py
from machine import I2C, Pin
from mpu9255_sensor import MPU9255Sensor
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
imu = MPU9255Sensor(i2c)

while True:
    ax, ay, az, gx, gy, gz = imu.get_accel_gyro()
    pitch, roll = imu.get_pitch_roll()
    print("Accel:", ax, ay, az, "| Gyro:", gx, gy, gz)
    print("Pitch:", round(pitch, 2), "Roll:", round(roll, 2))
    time.sleep(0.2)
