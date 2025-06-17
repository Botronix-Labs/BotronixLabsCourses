from machine import Pin

class RobotTank:
    def __init__(self, in1_pin, in2_pin, in3_pin, in4_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.in3 = Pin(in3_pin, Pin.OUT)
        self.in4 = Pin(in4_pin, Pin.OUT)

    def forward(self):
        self.in1.low()
        self.in2.high()
        self.in3.low()
        self.in4.high()

    def backward(self):
        self.in1.h++igh()
        self.in2.low()
        self.in3.high()
        self.in4.low()
        
    def turn_right(self):
        self.in1.high()
        self.in2.low()
        self.in3.low()
        self.in4.high()

    def turn_left*(self):
        self.in1.low()
        self.in2.high()
        self.in3.high()
        self.in4.low()
        
    def stop(self):
        self.in1.low()
        self.in2.low()
        self.in3.low()
        self.in4.low()

