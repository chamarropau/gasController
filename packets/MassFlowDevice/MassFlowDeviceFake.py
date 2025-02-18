from enum import Enum

import propar
import time
import serial.tools.list_ports

class MFC_IO(int, Enum):
    WRITE_FLUX = 206
    READ_FLUX_MEASURE = 205
    READ_CAPACITY_UNIT = 129   

class MassFlowDeviceFake:
    """
    Class to control the mass flow controller (MFC) device.
    """

    def __init__(self, id):
        self.id = id
        self.flow = 0
        print(f"{id} Wink wink :D")

        
    def set_flow(self, flow): 
        # print(f"Setting flow to {flow}")
        self.flow = flow
        
    def get_flow(self):
        return self.flow

    def clear_flow(self):
        print("Clearing flow")