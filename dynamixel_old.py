from dynamixel_sdk import PortHandler, PacketHandler
from dynamixel_sdk import COMM_SUCCESS
from time import sleep


ADDR_OPERATING_MODE         = 11
ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_MODEL_NUMBER          = 116
ADDR_PRESENT_POSITION       = 132
ADDR_ID = 7


DXL_MOVING_STATUS_THRESHOLD = 20 


class Dynamixel(object):
    def __init__(self, device='/dev/ttyUSB0', baudrate = 57600, id=1 ):
        self.device = device
        self.baudrate = baudrate
        self.id = id
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

    def __del__(self):
        print("deleted")
        self.portHandler.closePort() 

    def set_id(self, id):

        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.id, ADDR_ID, id)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))



    def ping(self):
        dxl_model_number, dxl_comm_result, dxl_error = self.packetHandler.ping(self.portHandler, self.id)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] ping Succeeded. Dynamixel model number : %d" % (self.id, dxl_model_number))        

    def led_on(self):
        self.packetHandler.write1ByteTxRx(self.portHandler, self.id, 65, 1)

    def led_off(self):
        self.packetHandler.write1ByteTxRx(self.portHandler, self.id, 65, 0)



    def goto_position(self,position):

        # set operation mode "Position Control Mode (3)"
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.id, ADDR_OPERATING_MODE, 3)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))   

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.id, ADDR_TORQUE_ENABLE, 1)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

        # Write goal position
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.id, ADDR_GOAL_POSITION, position)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

        while 1:
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.id, ADDR_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

            print("[ID:%04d] GoalPos:%04d  PresPos:%03d" % (self.id, position, dxl_present_position))

            if not abs(position - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                break


dm2 = Dynamixel(id=2)
dm1 = Dynamixel(id=1)

dm1.led_on()
sleep(1)
dm1.led_off()
dm2.led_on()
sleep(1)
dm1.led_on()
dm2.led_off()
sleep(1)
dm1.led_off()


# for pos in [3000,20,2000,50]:
#     dm.goto_position(pos)

# dm.goto_position(200)

