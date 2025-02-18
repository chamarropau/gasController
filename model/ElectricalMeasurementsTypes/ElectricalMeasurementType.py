from abc import abstractmethod

class ElectricalMeasurementType:
    def __init__(self, keithley, measurement_time):
        self.keithley = keithley 
        self.voltage = 0
        self.current = 0
        self.voltage_unit = "V"
        self.current_unit = "A"
        self.measurement_time = measurement_time
    
    @abstractmethod
    def run(self):
        pass

    def get_voltage(self):
        return str(self.voltage) + ' ' + str(self.voltage_unit)

    def get_current(self):
        return str(self.current) + ' ' + str(self.current_unit)
    
    
 