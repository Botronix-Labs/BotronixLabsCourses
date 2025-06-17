from robot_tank import RobotTank
from time import sleep

# Initialize the robot tank with your motor driver pins
tank = RobotTank(2, 3, 4, 5)

try:
    # Main loop or movement code
    print("Tank is moving forward...")
    tank.forward()
    sleep(2)
    tank.stop()
    sleep(2)
    
    print("Tank is moving backward...")
    tank.backward()
    sleep(2)
    tank.stop()
    sleep(2)
    
    print("Tank is moving left...")
    tank.turn_left()
    sleep(2)
    tank.stop()
    sleep(2)
    
    print("Tank is moving right...")
    tank.turn_right()
    sleep(2)
    tank.stop()
    sleep(2)

except KeyboardInterrupt:
    # This catches Ctrl+C or IDE stop button
    print("KeyboardInterrupt detected. Stopping the robot...")

except Exception as e:
    # Catch all other exceptions
    print(f"An error occurred: {e}")

finally:
    # Ensure the motors stop
    print("Stopping motors safely.")
    tank.stop()

