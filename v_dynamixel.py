from dynamixel_sdk import PortHandler, PacketHandler
from dynamixel_sdk import COMM_SUCCESS
from dynamixel_sdk import GroupSyncRead
from time import sleep




# EEPROM Area
ADDR_MODEL_NUMBER           = 0 # 2 Byte
ADDR_MODEL_INFORMATION      = 2 # 4 Byte
ADDR_FIRMWARE_VERSION       = 6 # 1 Byte
ADDR_ID                     = 7 # 1 Byte
ADDR_DRIVE_MODE             = 10 # 1 Byte
ADDR_OPERATING_MODE         = 11 # 1 Byte
ADDR_VELOCITY_LIMIT         = 44 # 4 Byte

# RAM Area
ADDR_TORQUE_ENABLE          = 64 # 1 Byte
ADDR_LED_RED                = 65 # 1 Byte
ADDR_GOAL_VELOCITY          = 104 # 4 Byte
ADDR_PROFILE_VELOCITY       = 112 # 4 Byte
ADDR_GOAL_POSITION          = 116 # 4 Byte
ADDR_PRESENT_POSITION       = 132 # 4 Byte

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
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            quit()
        if self.portHandler.setBaudRate(self.baudrate):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()
        self.motors = {}
        self.create_motors()

    def create_motors(self):
        data_list, dxl_comm_result = self.packetHandler.broadcastPing(self.portHandler)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        else:
            for key in data_list.keys():
                self.motors[key] = DynamixelMotor(self, key)

    def get_motors(self):
        return self.motors

    def get_motor(self,id):
        return self.motors[id]

    def factory_reset(self,id,option):
        self.packetHandler.factoryReset(self.portHandler, id, option)

    def write1ByteTxRx(self, id, address, data):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, address, data)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def write4ByteTxRx(self, id, address, data):
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, id, address, data)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))            

    def read1ByteTxRx(self, id, address):
        data_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, id, address)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return data_read

    def read2ByteTxRx(self, id, address):
        data_read, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, id, address)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return data_read

    def read4ByteTxRx(self, id, address):
        data_read, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, id, address)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return data_read

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

class MotorGroup(object):
    def __init__(self, dynamixel_system, motor_list):
        self.ds = dynamixel_system
        self.motor_list = motor_list


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

    def get_model_number(self):
        """Returns model number of the motor"""
        return self.ds.read2ByteTxRx(self.id, ADDR_MODEL_NUMBER)

    def get_model_information(self):
        """Returns model information of the motor"""        
        return self.ds.read4ByteTxRx(self.id, ADDR_MODEL_INFORMATION)

    def get_firmware_version(self):
        """Returns firmware information of the motor""" 
        return self.ds.read1ByteTxRx(self.id, ADDR_FIRMWARE_VERSION)

    def get_id(self):
        """Returns id of the motor""" 
        return self.ds.read1ByteTxRx(self.id, ADDR_ID)

    def set_id(self, newid):
        """Set new motor id"""         
        self.ds.write1ByteTxRx(self.id, ADDR_ID, newid)

    # Return Delay time
    # Drive mode

    def get_operating_mode(self):
        """Returns the active operation mode""" 
        return self.ds.read1ByteTxRx(self.id, ADDR_OPERATING_MODE)

    def set_operating_mode(self, mode):
        "Set the operation mode"
        self.ds.write1ByteTxRx (self.id, ADDR_OPERATING_MODE, mode)

    # Secondary  id Shadown id
    # Homing Offset

    def set_velocity_limit(self, velocity_limit):
        """Sets max velocity for velocity (wheel) mode"""    
        # TODO Umrechung in UMIN
        self.ds.write4ByteTxRx(self.id, ADDR_VELOCITY_LIMIT, velocity_limit)

    def get_velocity_limit(self):
        """Returns max velocity in velocity (wheel) mode"""                
        # TODO Umrechung in UMIN
        return self.ds.read4ByteTxRx(self.id, ADDR_VELOCITY_LIMIT)

    ### RAM Area operations

    def get_torque(self):
        return self.ds.read1ByteTxRx(self.id, ADDR_TORQUE_ENABLE)

    def set_torque(self, enable):
        self.ds.write1ByteTxRx (self.id, ADDR_TORQUE_ENABLE, enable)

    def led_on(self):
        self.ds.write1ByteTxRx (self.id, ADDR_LED_RED, 1)

    def led_off(self):
        self.ds.write1ByteTxRx (self.id, ADDR_LED_RED, 0)

    def get_goal_velocity(self):
        return self.ds.read4ByteTxRx(self.id, ADDR_GOAL_VELOCITY)

    def set_goal_velocity(self, position):
        self.ds.write4ByteTxRx(self.id, ADDR_GOAL_VELOCITY, position)

    def get_goal_position(self):
        return self.ds.read4ByteTxRx(self.id, ADDR_GOAL_POSITION)

    def set_goal_position(self, position):
        self.ds.write4ByteTxRx(self.id, ADDR_GOAL_POSITION, position)

    def get_present_position(self):
        return self.ds.read4ByteTxRx(self.id, ADDR_PRESENT_POSITION)

    def get_profile_velocity(self):
        return self.ds.read4ByteTxRx(self.id, ADDR_PROFILE_VELOCITY)

    def set_profile_velocity(self,velocity):
        self.ds.write4ByteTxRx(self.id, ADDR_PROFILE_VELOCITY, velocity)

    def factory_reset(self, option=0x02):
        self.ds.factory_reset(self.id, option)

    def goto_position(self,position, velocity = 50 ):
        # set operation mode "Position Control Mode (3)"
        self.set_operating_mode(3)
        # set velocity
        self.set_profile_velocity(velocity)
        # Enable Torque
        self.set_torque(1)
        # Write goal position
        self.set_goal_position(position)

        while 1:
            # Read present position
            present_position = self.get_present_position()
            #print("[ID:%04d] GoalPos:%04d  PresPos:%03d" % (self.id, position, dxl_present_position))
            # break if positon was reached
            if not abs(position - present_position) > DXL_MOVING_STATUS_THRESHOLD:
                break
        # Disable Torque
        self.set_torque(0)

    def goto_degree(self, degree, velocity = 50):

        units = int(degree * 4096/360 + 2048)
        self.goto_position(units, velocity)

        # 0.087891 Grad entspricht einer Unit

    def start_rotation(self, velocity=50):
        # set operation mode "Velocity Control Mode (1)"
        self.set_operating_mode(1)
        # IMPORTANT: First set torque and then velocity!!
        # Enable Torque
        self.set_torque(1)
        # set velocity
        self.set_goal_velocity(velocity)

    def stop_rotation(self):
        # Disable Torque
        self.set_torque(0) 



ds = DynamixelSystem()
#print(ds.get_motors())
motor1 = ds.get_motor(1)
motor2 = ds.get_motor(2)

# motor1.factory_reset()
# motor2.factory_reset()

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

#motor1.set_velocity_limit(50)
#motor1.start_rotation(-30)
#sleep(5)
#motor1.stop_rotation()

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


motor1.goto_degree(90)
motor2.goto_degree(90)