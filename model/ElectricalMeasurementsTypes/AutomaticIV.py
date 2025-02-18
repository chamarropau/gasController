from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

import time
import numpy as np

class AutomaticIV(ElectricalMeasurementType):
    def __init__(self, keithley, \
                 initial_voltage, initial_unit, final_voltage, final_unit, voltage_step, measurement_time, mode=None):
        super().__init__(keithley, measurement_time)
        self.initial_voltage = initial_voltage
        self.final_voltage = final_voltage
        self.voltage_step = voltage_step
        self.initial_unit = initial_unit
        self.final_unit = final_unit
        self.measurement_time = measurement_time
        self.n_points = self.voltage_step
        self.mode = mode

    def run(self, barrier=None, stop_event=None):
        initialV = self.keithley.convert_voltage(self.initial_voltage, self.initial_unit)
        finalV = self.keithley.convert_voltage(self.final_voltage, self.final_unit)
        voltage_list = np.linspace(initialV, finalV, self.voltage_step)
        delay_time = float(self.measurement_time) / len(voltage_list)

        self.keithley.init_voltage_mode(unit=None)

        for n, voltage in enumerate(voltage_list):

            if stop_event is not None and stop_event.is_set():
                break
            
            i = self.keithley.set_voltage(voltage, factor=1)

            self.keithley.add_measures_list(i, voltage)
            
            self.voltage = voltage
            self.current = i

            if barrier is not None and n == 0:
                barrier.wait()

            time.sleep(delay_time)
            

