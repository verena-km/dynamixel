from v_dynamixel import DynamixelSystem
from time import sleep

ds = DynamixelSystem()

motor1 = ds.get_motor(1)
motor2 = ds.get_motor(2)

print("model_number:", motor1.model_number)
print("model_information:", motor1.model_information)
print("firmware_version:", motor1.firmware_version)
print("drive_mode:", '{0:07b}'.format(motor1.drive_mode))
print("operating_mode:", motor1.operating_mode)
print("homing_offset:", motor1.homing_offset)
print("moving_threshold", motor1.moving_threshold)
print("velocity_limit:", motor1.velocity_limit)
print("max_position_limit:", motor1.max_position_limit)
print("min_position_limit:", motor1.min_position_limit)

print("torque:", motor1.torque)
print("led:", motor1.led)
print("goal_velocity:", motor1.goal_velocity)
print("goal_position:", motor1.goal_position)
print("present_position:", motor1.present_position)
