from machine import Pin
import time

class BleLED:
    def __init__(self, pin_num=16):
        self.led = Pin(pin_num, Pin.OUT)
        self.blink_state = False

    def on(self):
        self.led.value(1)

    def off(self):
        self.led.value(0)

    def toggle(self):
        self.led.toggle()

    def blink(self, delay=0.3):
        self.toggle()
        time.sleep(delay)
