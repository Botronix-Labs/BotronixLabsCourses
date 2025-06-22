from machine import Pin

class ObstacleSensor:
    def __init__(self, pin_num=17):
        self.sensor = Pin(pin_num, Pin.IN)
        self.last_state = self.read()

    def read(self):
        return self.sensor.value()

    def is_obstacle(self):
        return self.read() == 0

    def has_changed(self):
        current = self.read()
        changed = current != self.last_state
        self.last_state = current
        return changed, current
