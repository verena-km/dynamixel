from v_dynamixel import DynamixelSystem
from time import sleep

ds = DynamixelSystem()

motor1 = ds.get_motor(1)
motor2 = ds.get_motor(2)

motor1.goto_position(position = 1000, velocity = 20)
sleep(1)
motor1.goto_position(position = 0, velocity = 100)

sleep(1)

motor1.goto_degree(degree = 90, velocity = 20)
sleep(1)
motor1.goto_degree(degree = 180, velocity = 10)
sleep(1)
motor1.goto_degree(degree = 0, velocity = 50)
sleep(1)
motor1.goto_position(position = 0)


motor1.goto_position(position = 2000, velocity = 50, acceleration = 5)
sleep(1)
motor1.goto_position(position = 0, velocity = 50, acceleration = 5 )
sleep(1)



motor2.goto_position_time_based(position = 2000, total_time = 3000, acceleration_time = 1000)
sleep(1)
motor2.goto_position_time_based(position = 0, total_time = 5000, acceleration_time = 2000)