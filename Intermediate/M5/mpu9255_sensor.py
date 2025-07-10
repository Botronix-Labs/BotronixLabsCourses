"""
mpu9255_sensor.py

Provides a class for interfacing with the MPU9255 IMU sensor over I2C.
Includes methods for reading raw accelerometer and gyroscope data, and calculating pitch and roll.
"""

from machine import I2C
import time
import math

class MPU9255Sensor:
    def __init__(self, i2c, addr=0x68):
        """
        Initialize the MPU9255 sensor and wake it up from sleep mode.
        Args:
            i2c (I2C): Initialized I2C bus object
            addr (int): I2C address of the sensor (default 0x68)
        """
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')  # Wake up MPU
        time.sleep(0.1)

    def read_raw(self, register, length):
        """
        Read raw sensor data from a register and convert to signed integer.
        Args:
            register (int): Register address to read from
            length (int): Number of bytes to read
        Returns:
            int: Signed integer value from sensor
        """
        try:
            data = self.i2c.readfrom_mem(self.addr, register, length)
            val = int.from_bytes(data, 'big')
            if val & 0x8000:
                val -= 0x10000
            return val
        except OSError as e:
            print(f"I2C read error at reg {hex(register)}: {e}")
            return 0  # or None, or raise, depending on your needs

    def get_accel_gyro(self):
        """
        Read and return accelerometer and gyroscope data.
        Returns:
            tuple: (ax, ay, az, gx, gy, gz)
        """
        ax = self.read_raw(0x3B, 2)
        ay = self.read_raw(0x3D, 2)
        az = self.read_raw(0x3F, 2)
        gx = self.read_raw(0x43, 2)
        gy = self.read_raw(0x45, 2)
        gz = self.read_raw(0x47, 2)
        return ax, ay, az, gx, gy, gz

    def get_pitch_roll(self):
        """
        Calculate pitch and roll angles from accelerometer data.
        Returns:
            tuple: (pitch, roll) in degrees
        """
        ax, ay, az, *_ = self.get_accel_gyro()
        pitch = math.atan2(ay, math.sqrt(ax ** 2 + az ** 2)) * 180 / math.pi
        roll = math.atan2(-ax, az) * 180 / math.pi
        return pitch, roll
