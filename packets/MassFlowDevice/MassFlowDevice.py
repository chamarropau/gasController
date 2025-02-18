from enum import Enum
from termcolor import colored
import propar
import time
import serial.tools.list_ports

class MFC_IO(int, Enum):
    WRITE_FLUX = 206
    READ_FLUX_MEASURE = 205
    READ_CAPACITY_UNIT = 129   

class MassFlowDevice:
    """
    Class to control the mass flow controller (MFC) device.
    """
    
    def __init__(self, id):
        self.id = id
        self.instr = self.__device_configuration()
        self.instr.wink() 

    def __device_configuration(self):
        """Configuration of the device."""
        portCom = serial.tools.list_ports.comports()
        portCom = [comport.device for comport in portCom if comport.manufacturer == 'FTDI'] # FTDI is the manufacturer of the device
        
        for element in portCom:
            inst = propar.instrument(element, self.id)
            if(inst.readParameter(1) == None):
                raise Exception("Error in device connection. Adress may not be correct")
            else:
                return inst
        
    def set_flow(self, flow): 
        """Set the flow. (0-200)"""
        try:
            consistent = False
            ERROR_MFC = 0.05
            counter = 0
            while (counter < 20) and (not consistent):
                self.instr.writeParameter(MFC_IO.WRITE_FLUX, flow)
                buffer_value = self.instr.readParameter(MFC_IO.READ_FLUX_MEASURE)
                if abs(flow - buffer_value) < ERROR_MFC:
                    consistent = True
                else:
                    counter += 1
                    time.sleep(0.5)
                
                if counter == 20:
                    print(f"{colored('[WARN]','yellow')} Connection ERROR. Data inconsistent.")

            return self.instr.readParameter(MFC_IO.READ_FLUX_MEASURE), \
                self.instr.readParameter(MFC_IO.READ_CAPACITY_UNIT) # fMeasure, Capacity Unit
               
        except:
            self.instr.writeParameter(MFC_IO.WRITE_FLUX, 0.0)
            raise Exception("Wrong flow input.")
        
    def get_flow(self):
        """Get the flow."""
        try:   
            return self.instr.readParameter(MFC_IO.READ_FLUX_MEASURE), self.instr.readParameter(MFC_IO.READ_CAPACITY_UNIT)
        except:
            raise Exception("Error in reading flow.")
        
    def clear_flow(self):
        """Clear the flow."""
        try:
            self.instr.writeParameter(MFC_IO.WRITE_FLUX, 0.0)

        except:
            raise Exception("Error in clearing flow.")
