from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(15))  # use GP15
servo.freq(50)        # 50 Hz for standard servo

def move_servo_us(us):
    duty = int(us * 65535 / 20000)  # convert microsecond to 16-bit PWM
    servo.duty_u16(duty)

def move_servo_angle(angle):
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * angle // 180
    move_servo_us(us)
    

# Example 1 usage: 
#Move to 0 degrees (~500us)
move_servo_us(500)
sleep(1)

# Move to 90 degrees (~1500us)
move_servo_us(1500)
sleep(1)

# Move to 180 degrees (~2500us)
move_servo_us(2500)
sleep(1)

#Example 2 usage:
for angle in [0, 90, 180, 90, 0]:
    move_servo_angle(angle)
    sleep(1)
    
    
