# Variante mit namedtuple

from collections import namedtuple

ControlTableEntry = namedtuple('ControlTableEntry',['name', 'address', 'size', 'access', 'initial_value', 'min_value', 'max_value', 'unit'])

MODEL_NUMBER =      ControlTableEntry('Model Number', 0, 2, 'R', 1060, None, None, None)
MODEL_INFORMATION = ControlTableEntry('Model Information', 2, 4, 'R', None, None, None, None)
FIRMWARE_VERSION =  ControlTableEntry('Firmware Version',  6, 1, 'R', None, None, None, None)
ID =                ControlTableEntry('ID', 7, 1, 'RW', 1, 0 , 252 , None)
DRIVE_MODE        = ControlTableEntry('Drive Mode', 10, 1, 'RW', 0 , 0 , 5 , None)
OPERATING_MODE    = ControlTableEntry('Operating Mode', 11, 1, 'RW', 3, 0 , 16, None)
HOMING_OFFSET     = ControlTableEntry('Homing Offset', 20, 4, 'RW', 0, -1044479 , 1044479 , '0.1 [pulse]')
MOVING_THRESHOLD  = ControlTableEntry('Moving Threshold', 24, 4, 'RW', 10, 0, 1023, '0.2229 [rev/min]')
VELOCITY_LIMIT    = ControlTableEntry('Velocity Limit', 44, 4, 'RW', 265 , 0 , 1023, '0.2229 [rev/min]')
MAX_POSITION_LIMIT= ControlTableEntry('Max Position Limit', 48, 4, 'RW', 0, 0, 4095, '0.1 [pulse]')
MIN_POSITION_LIMIT= ControlTableEntry('Min Position Limit', 52, 4, 'RW', 0, 0, 4095, '0.1 [pulse]')

TORQUE_ENABLE     = ControlTableEntry('Torque Enable', 64, 1, 'RW', 0, 0, 1, None)
LED               = ControlTableEntry('LED', 65, 1, 'RW', 0, 0, 1, None)
GOAL_VELOCITY     = ControlTableEntry('Goal Velocity', 104, 4, 'RW', None, "-VELOCITY_LIMIT" , "+VELOCITY_LIMIT", '0.2229 [rev/min]')
PROFILE_ACCELERATION = ControlTableEntry('Profile Acceleration', 108, 4, 'RW', 0, 0, 32767, 'TODO')
PROFILE_VELOCITY  = ControlTableEntry('Profile Velocity', 112, 4, 'RW', 0, 0 , 32767, '0.2229 [rev/min]') 
GOAL_POSITION     = ControlTableEntry('Goal Position', 116, 4, 'RW', None, "-MIN_POSITION_LIMIT" , "+MAX_POSITION_LIMIT", '0.1 [pulse]')
REALTIME_TICK     = ControlTableEntry('Reatime Tick', 120, 2, 'R', None, 0, 32.767, "1 [msec]")
MOVING            = ControlTableEntry('Moving', 122, 1, 'R', 0, 0, 1, None)
MOVING_STATUS     = ControlTableEntry('Moving Status', 122, 1, 'R', 0, None, None, None)
PRESENT_VELOCITY = ControlTableEntry('Present Velocity', 128, 4, 'R', None, None,None, '0.229 [rev/min]')
PRESENT_POSITION  = ControlTableEntry('Present Position', 132, 4, 'R', None, None,None, '0.1 [pulse]')
PRESENT_TEMPERATURE  = ControlTableEntry('Present Temperature', 146, 4, 'R', None, None,None, '1 [°C]')




# print(MODEL_INFORMATION.size)


#https://stackoverflow.com/questions/4045161/should-i-use-a-class-or-dictionary
#https://www.youtube.com/watch?v=a6zkPCrXCM4

# Variante mit Dictionary

# CT= {'MODEL_NUMBER':     {'address': 0,
#                             'size': 2,
#                             'access': 'R',
#                             'initial_value': 1060,
#                             'min_value': None,
#                             'max_value': None},
#     'MODEL_INFORMATION': {'address': 2,
#                             'size': 4,
#                             'access': 'R',
#                             'initial_value': None,
#                             'min_value': None,
#                             'max_value': None},
#     'FIRMWARE_VERSION':  {'address': 6,
#                             'size': 1,
#                             'access': 'R', 
#                             'initial_value': None,
#                             'min_value': None,
#                             'max_value': None},
#     'ID':                {'address': 7,
#                             'size': 1,
#                             'access': 'RW',
#                             'initial_value': 1,
#                             'min_value': 0,
#                             'max_value': 252}, 
#     'DRIVE_MODE':        {'address': 10,
#                             'size': 1,
#                             'access': 'RW',
#                             'initial_value': 0,
#                             'min_value': 0,
#                             'max_value': 5}, 
#     'OPERATING_MODE':    {'address': 11,
#                             'size': 1,
#                             'access': 'RW',
#                             'initial_value': 3,
#                             'min_value': 0, 
#                             'max_value': 16}, 
#     'VELOCITY_LIMIT':    {'address': 44,
#                             'size': 4,
#                             'access': 'RW',
#                             'initial_value': 265,
#                             'min_value': 0,
#                             'max_value': 1023}, 
#     'TORQUE_ENABLE':     {'address': 64,
#                             'size': 1,
#                             'access': 'RW',
#                             'initial_value': 0,
#                             'min_value': 0,
#                             'max_value': 1}, 
#     'LED':               {'address': 65,
#                             'size': 1,
#                             'access': 'RW',
#                             'initial_value': 0,
#                             'min_value': 0,
#                             'max_value': 1}, 
#     'GOAL_VELOCITY':     {'address': 104,
#                             'size': 4, 
#                             'access': 'RW',
#                             'initial_value': None, 
#                             'min_value': "-VELOCITY_LIMIT", 
#                             'max_value': "+VELOCITY_LIMIT"}, 
#     'PROFILE_VELOCITY':  {'address': 112,
#                             'size': 4,
#                             'access': 'RW',
#                             'initial_value': 0, 
#                             'min_value': 0,
#                             'max_value': 32767},
#     'GOAL_POSITION':     {'address': 116,
#                             'size': 4,
#                             'access': 'RW',
#                             'initial_value': None, 
#                             'min_value': "MIN_POSITION_LIMIT",
#                             'max_value': "MAX_POSITION_LIMIT"},
#     'PRESENT_POSITION':  {'address': 132,
#                             'size': 4, 
#                             'access': 'R', 
#                             'initial_value': None,
#                             'min_value': None}
#                 }