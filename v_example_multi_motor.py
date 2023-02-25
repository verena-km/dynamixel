from v_dynamixel import DynamixelSystem
from time import sleep

ds = DynamixelSystem()

motor1 = ds.get_motor(1)
motor2 = ds.get_motor(2)


# ## zwei Motoren gleichzeitig 
m1_goal_pos = 2000
m1_velocity = 20
m2_goal_pos = 6000
m2_velocity = 60

motor1.operating_mode = 4
motor1.profile_velocity = m1_velocity
motor1.torque = 1
motor1.goal_position = m1_goal_pos

motor2.operating_mode = 4
motor2.profile_velocity = m2_velocity
motor2.torque = 1
motor2.goal_position = m2_goal_pos


while True:
    motor1_actual_position = motor1.present_position
    motor2_actual_position = motor2.present_position

    print("Motor1: ", motor1_actual_position)
    print("Motor2: ", motor2_actual_position)

    if abs(motor1_actual_position-m1_goal_pos) < 20 and (motor2_actual_position-m2_goal_pos) < 20:
        break
motor1.torque = 0
motor2.torque = 0

print("Back to start position")
motor1.extended_goto_position(0)
motor2.extended_goto_position(0)