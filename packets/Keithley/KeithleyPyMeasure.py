from packets.Keithley.EthernetConnection import EthernetConnection
from pymeasure.instruments.keithley import Keithley2450
from termcolor import colored
import pyvisa as vs
import time

class KeithleyPyMeasure:
    """
    Class to control the Keithley device.
    """
    def __init__(self, keithley_config): # keithley_config = {'ip', 'interface', 'mask', 'gateway'}
        EthernetConnection().ip_static_configuration(keithley_config['interface'], \
                                                        keithley_config['ip'], \
                                                        keithley_config['mask'], \
                                                        keithley_config['gateway'])
    
        self.addr = f"TCPIP0::{keithley_config['ip']}::inst0::INSTR"
        
        while True:
            try:
                self.inst = self.__device_configuration()
                break
            except Exception as e:
                print(e.__str__())
                print(f"{colored('[INFO]', 'blue')} Trying to connect again...")
                #time.sleep(30)

        self.mode = None

    def __device_configuration(self):
        self.manager = vs.ResourceManager()
        time.sleep(10)
        # Find the device in the list of resources
        resources = self.manager.list_resources()
        print(resources)
        print(self.addr)

        if self.addr in resources:
            return self.manager.open_resource(self.addr)
        
        self.manager.close()
        raise Exception(f"{colored('[ERROR]', 'red')} Error in connection. Please reset the Keithley device manually and try again.")
        
    def reset_measurement(self):
        self.inst.write("reset()")
        self.inst.write("smu.source.output = smu.OFF")

    def close(self):
        self.inst.close()
        self.manager.close()
        
    ##################################  V(I) METHODS  #########################################
    
    def __init_current_mode(self): # Apply a current and measure the voltage mode
        self.inst.write("reset()")
        self.inst.write("smu.source.func = smu.FUNC_DC_CURRENT")
        self.inst.write("smu.source.vlimit.level = 21")
        self.inst.write("smu.source.autorange = smu.ON")
        self.inst.write("smu.source.autodelay = smu.ON")
        self.inst.write("smu.measure.func = smu.FUNC_DC_VOLTAGE")
        self.inst.write("smu.measure.autorange = smu.ON")
        self.inst.write("smu.measure.nplc = 1")

    def set_current(self, current, time_delay=0.1, unit="mA"): # Unit is mA or uA or nA
        if self.mode != "current":
            self.__init_current_mode()
            self.mode = "current"

        if unit == "mA":
            current = current * 1e-3
        elif unit == "uA":
            current = current * 1e-6
        elif unit == "nA":
            current = current * 1e-9
        else:
            raise Exception("Invalid unit. Please use mA, uA or nA.")


        self.inst.write("smu.source.output = smu.ON")
        self.inst.write("smu.source.level = "+ str(current)) # Source level in A
        time.sleep(float(time_delay)) # TODO: Check if it is necessary
        self.inst.write("smu.measure.read()")

        # Grab the last reading
        v = self.inst.query(
            "print(defbuffer1.readings[defbuffer1.endindex])", delay=0.5)
    
        # .query returns a string, so it must be casted to a number
        return float(v)

    def get_voltage(self):
        # Grab the last reading
        if self.mode != "current":
            raise Exception("The device is not in current mode. Please set the current first.")

        v = self.inst.query(
            "print(defbuffer1.readings[defbuffer1.endindex])", delay=0.5)
    
        return float(v)
    
    ##################################  I(V) METHODS  #########################################
    
    def __init_voltage_mode(self): # Apply a voltage and measure the current mode
        self.inst.write("reset()")
        self.inst.write("smu.source.func = smu.FUNC_DC_VOLTAGE")
        self.inst.write("smu.source.autorange = smu.ON")
        self.inst.write("smu.source.autodelay = smu.ON")
        self.inst.write("smu.measure.func = smu.FUNC_DC_CURRENT")
        self.inst.write("smu.measure.autorange = smu.ON")
        self.inst.write("smu.measure.nplc = 1")

    def set_voltage(self, voltage, time_delay=0.1, unit="V"): # Unit is V or mV or uV
        if self.mode != "voltage":
            self.__init_voltage_mode()
            self.mode = "voltage"
        
        if unit == "mV":
            voltage = voltage * 1e-3
        elif unit == "uV":
            voltage = voltage * 1e-6
        elif unit == "V":
            pass
        else:
            raise Exception("Invalid unit. Please use V, mV or uV.")
        
        self.inst.write("smu.source.output = smu.ON")
        self.inst.write("smu.source.level = " + str(voltage)) # Voltage in V
        time.sleep(time_delay) # TODO: Check if it is necessary
        self.inst.write("smu.measure.read()")

        # Grab the last reading
        i = self.inst.query(
            "print(defbuffer1.readings[defbuffer1.endindex])", delay=0.5)
        
        return float(i)

    def get_current(self):
        if self.mode != "voltage":
            raise Exception("The device is not in voltage mode. Please set the voltage first.")
            
        # Grab the last reading
        i = self.inst.query(
            "print(defbuffer1.readings[defbuffer1.endindex])", delay=0.5)
        
        return float(i)
