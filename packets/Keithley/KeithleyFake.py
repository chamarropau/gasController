from packets.Keithley.EthernetConnection import EthernetConnection

import pyvisa as vs
import time

class KeithleyFake:
    """
    Class to control the Keithley device.
    """

    def __init__(self, keithley_config): # keithley_config = {'ip', 'interface', 'mask', 'gateway'}
        self.current = 0
        self.voltage = 0
        self.r = 100

    def reset_measurement(self):
        print("reset measurement")

    def set_current(self, current, time_delay=0.1, unit="mA"): # Unit is mA or uA or nA
        # print(f"Current set: {current}")

        if unit == "mA":
            self.current = current / 1000  
        elif unit == "uA":
            self.current = current / 1000000
        elif unit == "nA":
            self.current = current / 1000000000

        return self.r * self.current 

    def get_voltage(self):
        return self.r * self.current
    
    ##################################  I(V) METHODS  ##################################

    def set_voltage(self, voltage, time_delay=0.1, unit="V"): # Unit is V or mV or uV
        
        if unit == "V":
            self.voltage = voltage
        elif unit == "mV":
            self.voltage = voltage / 1000
        elif unit == "uV":
            self.voltage = voltage / 1000000
        
        return self.voltage / self.r


    def get_current(self):
        return self.voltage / self.r
