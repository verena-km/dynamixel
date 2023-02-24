import serial
import crcmod
import struct

serial_port = serial.Serial('/dev/ttyUSB0', baudrate=57600, timeout=0.05)

packet_id = 1
packet_length = 3
instruction = 1

packet = bytearray(0xff, 0xff, 0xfd, 0x00, packet_id, packet_length, 0, instruction)
