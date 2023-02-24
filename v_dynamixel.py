from dynamixel_sdk import PortHandler, PacketHandler
from dynamixel_sdk import COMM_SUCCESS
from dynamixel_sdk import GroupSyncRead
from time import sleep
from v_control_table import *

LEN_PRESENT_POSITION        = 4

# TODO - put in class
DXL_MOVING_STATUS_THRESHOLD = 20 

class DynamixelSystem(object):
    def __init__(self, device='/dev/ttyUSB0', baudrate = 57600):
        self.device = device
        self.baudrate = baudrate
        self.portHandler = PortHandler(device)
        self.packetHandler = PacketHandler(2.0)

        if self.portHandler.openPort():
            # print("Succeeded to open the port")
            pass
        else:
            print("Failed to open the port")
            quit()
        if self.portHandler.setBaudRate(self.baudrate):
            # print("Succeeded to change the baudrate")
            pass
        else:
            print("Failed to change the baudrate")
            quit()
        self.motors = {}
        self.create_motors()

    def handle_error(self,result, error):
        if result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(result))
        elif error != 0:
            print("%s" % self.packetHandler.getRxPacketError(error))

    def create_motors(self):
        data_list = self.broadcast_ping()
        for key in data_list.keys():
            self.motors[key] = DynamixelMotor(self, key)

    def get_motors(self):
        return self.motors

    def get_motor(self,id):
        return self.motors[id]

    def factory_reset(self,id,option):
        result, error = self.packetHandler.factoryReset(self.portHandler, id, option)
        self.handle_error(result,error)

    def broadcast_ping(self):
        data_list, result = self.packetHandler.broadcastPing(self.portHandler)
        self.handle_error(result, 0)
        return data_list 

    def ping(self,id):
        model_number, result, error = self.packetHandler.ping(self.portHandler, id)
        self.handle_error(result,error)
        return model_number

    def reboot(self,id):
        result, error = self.packetHandler.reboot(self.portHandler, id)
        self.handle_error(result,error)

    def read(self, id, entry):
        if entry.size == 1:
            data, result, error = self.packetHandler.read1ByteTxRx(self.portHandler, id, entry.address)
        if entry.size == 2:            
            data, result, error = self.packetHandler.read2ByteTxRx(self.portHandler, id, entry.address)
        if entry.size == 4:            
            data, result, error = self.packetHandler.read4ByteTxRx(self.portHandler, id, entry.address)
        self.handle_error(result,error)
        return data

    def write(self, id, entry, value):
        if entry.size == 1:
            result, error = self.packetHandler.write1ByteTxRx(self.portHandler, id, entry.address,value)
        if entry.size == 2:
            result, error = self.packetHandler.write2ByteTxRx(self.portHandler, id, entry.address,value)
        if entry.size == 4:
            result, error = self.packetHandler.write4ByteTxRx(self.portHandler, id, entry.address,value)
        self.handle_error(result,error)

    def sync_readTxRx(self, ids, address, length):
        groupSyncRead = GroupSyncRead(self.ds.portHandler, self.ds.packetHandler, address, length)
        result = {}
        for id in ids:
            groupSyncRead.addParam(id)
            dxl_comm_result = groupSyncRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.ds.packetHandler.getTxRxResult(dxl_comm_result))
        for id in self.ids:
            dxl_getdata_result = groupSyncRead.isAvailable(id, address, length)
            if dxl_getdata_result != True:
                print("[ID:%03d] groupSyncRead getdata failed" % id)
                quit()            
            value = groupSyncRead.getData(id, address, length)
            result[id] = value
        return result

# class MotorGroup(object):
#     def __init__(self, dynamixel_system, motor_list):
#         self.ds = dynamixel_system
#         self.motor_list = motor_list


    # def get_present_positions(self):
        
    #     ds.sync_readTxRx()

        # groupSyncRead = GroupSyncRead(self.ds.portHandler, self.ds.packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        # for motor in self.motor_list:
        #     groupSyncRead.addParam(motor.id)
        # dxl_comm_result = groupSyncRead.txRxPacket()
        # if dxl_comm_result != COMM_SUCCESS:
        #     print("%s" % self.ds.packetHandler.getTxRxResult(dxl_comm_result))
        # for motor in self.motor_list:
        #     dxl_getdata_result = groupSyncRead.isAvailable(motor.id, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        #     if dxl_getdata_result != True:
        #         print("[ID:%03d] groupSyncRead getdata failed" % motor.id)
        #         quit()            
        #     dxl1_present_position = groupSyncRead.getData(motor.id, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        #     print(dxl1_present_position)

class DynamixelMotor(object):
    def __init__(self, dynamixel_system, id):
        self.ds = dynamixel_system
        self.id = id

    @property
    def model_number(self):
        """Returns model number of the motor"""        
        return self.ds.read(self.id, MODEL_NUMBER)

    @property
    def model_information(self):
        """Returns model information of the motor"""          
        return self.ds.read(self.id, MODEL_INFORMATION)    

    @property
    def firmware_version(self):
        """Returns firmware information of the motor"""      
        return self.ds.read(self.id, FIRMWARE_VERSION)

    # @property
    # def id(self):
    #     """Returns id of the motor"""    
    #     #return self.ds.read(id, ID)
    #     return self.id

    # @id.setter
    # def id(self, newid):
    #     """Set new motor id"""        
    #     self.ds.write(self.id, ID, newid)

    # Return Delay time
    # Drive mode

    @property
    def operating_mode(self):
        """Returns the active operation mode""" 
        return self.ds.read(self.id, OPERATING_MODE)

    @operating_mode.setter
    def operating_mode(self, mode):
        "Set the operation mode"
        self.ds.write(self.id, OPERATING_MODE, mode)

    @property
    def drive_mode(self):
        """Returns the active dive mode""" 
        return self.ds.read(self.id, DRIVE_MODE)

    @drive_mode.setter
    def drive_mode(self, mode):
        "Set the drive mode"
        self.ds.write(self.id, DRIVE_MODE, mode)

    # TODO gives an data value out of range error
    # NOTE: Torque On by Goal Update is available from firmware V45.
    # we have 44
    # @property
    # def torque_on_by_goal_update(self):
    #     """Returns torque on by goal update""" 
    #     drive_mode = self.drive_mode
    #     # check if Bit 3 is set
    #     return 0b1000 & drive_mode

    # @torque_on_by_goal_update.setter
    # def torque_on_by_goal_update(self,enable):
    #     """Sets torque on by goal update""" 
    #     drive_mode = drive_mode = self.drive_mode
    #     if enable:
    #         newdrive_mode = drive_mode | 0b00001000
    #     else:
    #         newdrive_mode = drive_mode & 0b11110111
    #     self.drive_mode = newdrive_mode

    @property
    def profile_configuration(self):
        """Returns profile configuration""" 
        drive_mode = self.drive_mode
        # check if Bit 2 is set
        return 0b100 & drive_mode

    @profile_configuration.setter
    def profile_configuration(self,value):
        """Sets profile configuration""" 
        drive_mode = drive_mode = self.drive_mode
        if value: # time based
            newdrive_mode = drive_mode | 0b00000100
        else: # velocity based
            newdrive_mode = drive_mode & 0b11111011
        self.drive_mode = newdrive_mode

    @property
    def reverse_mode(self):
        """Returns if reverse_mode is on""" 
        drive_mode = self.drive_mode
        # check if Bit 0 is set
        return 0b1 & drive_mode

    @reverse_mode.setter
    def reverse_mode(self,on):
        """Sets profile configuration""" 
        drive_mode = drive_mode = self.drive_mode
        if on: # reverse mode on 
            newdrive_mode = drive_mode | 0b00000001
        else: # reverse mode off
            newdrive_mode = drive_mode & 0b11111110
        print(newdrive_mode)
        self.drive_mode = newdrive_mode

    @property
    def homing_offset(self):
        """Returns the homing offset"""                
        return self.ds.read(self.id, HOMING_OFFSET)

    @homing_offset.setter
    def homing_offset(self, homing_offset):
        """Sets max velocity for velocity (wheel) mode"""    
        self.ds.write(self.id, HOMING_OFFSET, homing_offset)

    @property
    def moving_threshold(self):
        """Returns the homing offset"""                
        return self.ds.read(self.id, MOVING_THRESHOLD)

    @moving_threshold.setter
    def moving_threshold(self, moving_threshold):
        """Sets max velocity for velocity (wheel) mode"""    
        self.ds.write(self.id, MOVING_THRESHOLD, moving_threshold)

    @property
    def velocity_limit(self):
        """Returns max velocity in velocity (wheel) mode"""                
        # TODO Umrechung in UMIN
        return self.ds.read(self.id, VELOCITY_LIMIT)

    @velocity_limit.setter
    def velocity_limit(self, velocity_limit):
        """Sets max velocity for velocity (wheel) mode"""    
        # TODO Umrechung in UMIN
        self.ds.write(self.id, VELOCITY_LIMIT, velocity_limit)

    @property
    def max_position_limit(self):
        """Returns max target position in position mode"""                
        return self.ds.read(self.id, MAX_POSITION_LIMIT)

    @max_position_limit.setter
    def max_position_limit(self, max_position_limit):
        """Sets max target position in position mode"""    
        self.ds.write(self.id, MAX_POSITION_LIMIT, max_position_limit)

    @property
    def min_position_limit(self):
        """Returns min target position in position mode"""                
        return self.ds.read(self.id, MIN_POSITION_LIMIT)

    @min_position_limit.setter
    def min_position_limit(self, min_position_limit):
        """Sets max target position in position mode"""    
        self.ds.write(self.id, MIN_POSITION_LIMIT, min_position_limit)        

    ### RAM Area operations

    @property
    def torque(self):
        return self.ds.read(self.id, TORQUE_ENABLE)

    @torque.setter
    def torque(self, enable):
        self.ds.write(self.id, TORQUE_ENABLE, enable)

    @property
    def led(self):
        return self.ds.read(self.id, LED)

    @led.setter
    def led(self, on):
        self.ds.write(self.id, LED, on)

    @property
    def goal_velocity(self):
        return self.ds.read(self.id, GOAL_VELOCITY)

    @goal_velocity.setter
    def goal_velocity(self, position):
        self.ds.write(self.id, GOAL_VELOCITY, position)


    @property
    def profile_acceleration(self):
        return self.ds.read(self.id, PROFILE_ACCELERATION)

    @profile_acceleration.setter
    def profile_acceleration(self, acceleration):
        self.ds.write(self.id, PROFILE_ACCELERATION, acceleration)

    @property
    def profile_velocity(self):
        return self.ds.read(self.id, PROFILE_VELOCITY)

    @profile_velocity.setter
    def profile_velocity(self,velocity):
        self.ds.write(self.id, PROFILE_VELOCITY, velocity)

    @property
    def goal_position(self):
        return self.ds.read(self.id, GOAL_POSITION)

    @goal_position.setter
    def goal_position(self, position):
        self.ds.write(self.id, GOAL_POSITION, position)

    @property
    def realtime_tick(self):
        return self.ds.read(self.id, REALTIME_TICK)

    @property
    def moving(self):
        return self.ds.read(self.id, MOVING)

    @property
    def moving_status(self):
        return self.ds.read(self.id, MOVING_STATUS)

    @property
    def arrived(self):
        return self.ds.read(self.id, MOVING_STATUS) & 0b00000001

    @property
    def profile_in_progress(self):
        return self.ds.read(self.id, MOVING_STATUS) & 0b00000010
    
    @property
    def velocity_profile(self):
        value = (self.ds.read(self.id, MOVING_STATUS) & 0b00110000) >> 4
        if value == 1:
            print("Rectangular Profile")
        if value == 3:
            print("Trapezoidal Profile")
        return value

    @property
    def present_velocity(self):
        return self.ds.read(self.id, PRESENT_VELOCITY)

    @property
    def present_position(self):
        return self.ds.read(self.id, PRESENT_POSITION)

    @property
    def present_temperature(self):
        return self.ds.read(self.id, PRESENT_TEMPERATURE)


    def ping(self):
        model_number = self.ds.ping(self, id)
        return model_number

    def factory_reset(self, option=0x02):
        self.ds.factory_reset(self.id, option)

    def goto_position(self,position, velocity = 50, acceleration = 0 ):
        #print(self.max_position_limit)
        #print(self.min_position_limit)
   
        if position <= self.max_position_limit and position >= self.min_position_limit:
            # set operation mode "Position Control Mode (3)"
            self.operating_mode = 3

            # set acceleration
            self.profile_acceleration = acceleration

            # set velocity
            self.profile_velocity = velocity

            # Enable Torque
            self.torque = 1
            # Write goal position
            self.goal_position = position

            while 1:
                # Read present position
                present_position = self.present_position
                #print("[ID:%04d] GoalPos:%04d  PresPos:%03d" % (self.id, position, dxl_present_position))
                # break if position was reached
                if not abs(position - present_position) > DXL_MOVING_STATUS_THRESHOLD:
                    break
            # Disable Torque
            self.torque = 0
        # else:
        #     print("Position limit exceeded")

    def goto_position_time_based(self, position, total_time = 5, acceleration_time = 0):
        if position <= self.max_position_limit and position >= self.min_position_limit:
            # set operation mode "Position Control Mode (3)"
            self.operating_mode = 3

            # set time based profile            
            self.profile_configuration = 1

            # set acceleration
            self.profile_acceleration = acceleration_time

            # set velocity
            self.profile_velocity = total_time

            # Enable Torque
            self.torque = 1
            # Write goal position
            self.goal_position = position

            while 1:
                # Read present position
                present_position = self.present_position
                #print("[ID:%04d] GoalPos:%04d  PresPos:%03d" % (self.id, position, dxl_present_position))
                # break if position was reached
                if not abs(position - present_position) > DXL_MOVING_STATUS_THRESHOLD:
                    break
            # Disable Torque
            self.torque = 0
            # reset Profile
            self.profile_configuration = 0
        # else:
        #     print("Position limit exceeded")


    def goto_degree(self, degree, velocity = 50, acceleration = 0 ):

        units = int(degree * 4096/360 + 2048)
        self.goto_position(units, velocity, acceleration)

        # 0.087891 Grad entspricht einer Unit


    def goto_degree_time_based(self, degree, total_time = 5, acceleration_time = 0):

        units = int(degree * 4096/360 + 2048)
        self.goto_position_time_based(units, total_time, acceleration_time)


    def extended_goto_position(self, position, velocity = 50, acceleration = 0):
        # set operation mode "Extended Position Control Mode (4)"
        self.operating_mode = 4
        # set velocity
        self.profile_velocity = velocity
        # set acceleration
        self.profile_acceleration = acceleration
        # Enable Torque
        self.torque = 1
        # Write goal position
        self.goal_position = position

        while 1:
            # Read present position
            present_position = self.present_position
            #print("[ID:%04d] GoalPos:%04d  PresPos:%03d" % (self.id, position, dxl_present_position))
            # break if positon was reached
            if not abs(position - present_position) > DXL_MOVING_STATUS_THRESHOLD:
                break
        # Disable Torque
        self.torque = 0
        


    def extended_goto_position_time_based(self, position, total_time = 5, acceleration_time = 0):
        # set operation mode "Extended Position Control Mode (4)"
        self.operating_mode = 4
        # set time based profile            
        self.profile_configuration = 1

        # set velocity
        self.profile_velocity = total_time
        # set acceleration
        self.profile_acceleration = acceleration_time
        # Enable Torque
        self.torque = 1
        # Write goal position
        self.goal_position = position

        while 1:
            # Read present position
            present_position = self.present_position
            #print("[ID:%04d] GoalPos:%04d  PresPos:%03d" % (self.id, position, dxl_present_position))
            # break if positon was reached
            if not abs(position - present_position) > DXL_MOVING_STATUS_THRESHOLD:
                break
        # Disable Torque
        self.torque = 0
        # reset Profile
        self.profile_configuration = 0        


    def start_rotation(self, velocity=50, acceleration_time = 0):
        if abs(velocity) <= self.velocity_limit:
            # set operation mode "Velocity Control Mode (1)"
            self.operating_mode = 1

            if acceleration_time > 0:
                # set time based profile            
                self.profile_configuration = 1
                # set acceleration value
                self.profile_acceleration = acceleration_time

            else:
                self.profile_configuration = 0

            # IMPORTANT: First set torque and then velocity!!
            # Enable Torque
            self.torque = 1
            # set velocity
            self.goal_velocity = velocity
        else:
            print("error")

    def stop_rotation(self):
        self.goal_velocity = 0
        while 1:
            #print(self.present_velocity)
            if self.present_velocity == 0:
                break
        # Disable Torque
        self.torque = 0


ds = DynamixelSystem()
#print(ds.get_motors())
motor1 = ds.get_motor(1)
motor2 = ds.get_motor(2)

# motor1.factory_reset()
# motor2.factory_reset()

# print("model_number:", motor1.model_number)
# print("model_information:", motor1.model_information)
# print("firmware_version:", motor1.firmware_version)
# print("drive_mode:", '{0:07b}'.format(motor1.drive_mode))
# print("operating_mode:", motor1.operating_mode)
# print("homing_offset:", motor1.homing_offset)
# print("moving_threshold", motor1.moving_threshold)
# print("velocity_limit:", motor1.velocity_limit)
# print("max_position_limit:", motor1.max_position_limit)
# print("min_position_limit:", motor1.min_position_limit)

# print("torque:", motor1.torque)
# print("led:", motor1.led)
# print("goal_velocity:", motor1.goal_velocity)
# print("goal_position:", motor1.goal_position)
# print("present_position:", motor1.present_position)
# print("present_position:", motor2.present_position)

#motor1.goto_position(0)
#motor1.extended_goto_position(0)

# motor1.velocity_limit = 700
# motor1.start_rotation(velocity = 700, acceleration_time = 1000)
#motor2.start_rotation(velocity = 200, acceleration_time = 0)

#motor1.extended_goto_position(6000)
# for i in range(5):
#     sleep(1)
#     print(motor1.present_velocity)
#     print(motor1.present_temperature)

# motor1.stop_rotation()
#motor2.stop_rotation()

# print("present_position:", motor1.present_position)
# print("present_position:", motor2.present_position)




# ## zwei Motoren gleichzeitig 
# m1_goal_pos = 1000
# m2_goal_pos = 4000

# motor1.set_operating_mode(3)
# motor1.set_torque(1)
# motor1.set_goal_position(m1_goal_pos)
# motor2.set_operating_mode(3)
# motor2.set_torque(1)
# motor2.set_goal_position(m2_goal_pos)

# while True:
#     motor1_actual_position = motor1.get_present_position()
#     motor2_actual_position = motor2.get_present_position()

#     print(motor1_actual_position)
#     print(motor2_actual_position)

#     if abs(motor1_actual_position-m1_goal_pos) < 20 and (motor2_actual_position-m2_goal_pos) < 20:
#         break
# motor1.set_torque(0)
# motor2.set_torque(0)


#motor2.set_id(2)

#print(motor1.get_model_number())
#print(motor2.get_model_information())

# motor1.factory_reset()
# motor2.factory_reset()

# motor1.start_rotation(-30)
# sleep(5)
# motor1.stop_rotation()


#motor2.goto_position(3000)

# motor2.start_rotation(-50)
# sleep(5)
# motor2.start_rotation(50)
# sleep(5)
# motor2.stop_rotation()
#print(motor1.get_velocity_limit())
# motor2.start_rotation()
# sleep(2)
# motor1.stop_rotation()
# sleep(2)
# motor2.stop_rotation()
# for i in range(1,10):
#     motor2.goto_position(1000)
#     motor2.goto_position(4000,4000)


# motor1.goto_degree(90)
# motor2.goto_degree(90)