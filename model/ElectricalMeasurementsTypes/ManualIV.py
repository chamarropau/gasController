from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType
from time import time

class ManualIV(ElectricalMeasurementType):
    def __init__(self, keithley, voltage, voltage_unit, measurement_time):
        super().__init__(keithley, measurement_time)
        self.voltage = voltage
        self.voltage_unit = voltage_unit


    def run(self, barrier=None, stop_event=None):
        factor = self.keithley.init_voltage_mode(unit=self.voltage_unit)

        i = self.keithley.set_voltage(self.voltage, factor)
        self.current = i

        self.keithley.add_measures_list(i, self.voltage*factor)
        
        if barrier is not None:
            barrier.wait()

        


    