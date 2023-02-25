from v_dynamixel import DynamixelSystem
from time import sleep

ds = DynamixelSystem()
motor1 = ds.get_motor(1)
motor2 = ds.get_motor(2)

motor1.start_rotation(velocity = 20)
sleep(2)
motor1.stop_rotation()

motor1.start_rotation(velocity = 200, acceleration_time = 3000)
sleep(8)
motor1.stop_rotation()

# reverse
motor1.start_rotation(velocity = -100)
sleep(2)
motor1.stop_rotation()