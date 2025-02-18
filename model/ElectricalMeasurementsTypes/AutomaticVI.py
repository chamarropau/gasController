from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

import time
import numpy as np

class AutomaticVI(ElectricalMeasurementType): 
    def __init__(self, keithley, \
                 initial_current, initial_unit, final_current, final_unit, current_step, measurement_time, mode=None):
        super().__init__(keithley, measurement_time)
        self.initial_current = initial_current
        self.final_current = final_current
        self.current_step = current_step
        self.initial_unit = initial_unit
        self.final_unit = final_unit
        self.measurement_time = measurement_time
        self.mode = mode

    def run(self, barrier=None, stop_event=None):
        initialC = self.keithley.convert_current(self.initial_current, self.initial_unit)
        finalC = self.keithley.convert_current(self.final_current, self.final_unit)
        current_list = np.linspace(initialC, finalC, self.current_step)
        delay_time = float(self.measurement_time) / len(current_list)

        self.keithley.init_current_mode(unit=None)

        for n, current in enumerate(current_list):

            if stop_event is not None and stop_event.is_set():
                break

            v = self.keithley.set_current(current, factor=1)  

            self.keithley.add_measures_list(v, current)           

            self.voltage = v
            self.current = current

            if barrier is not None and n == 0:
                barrier.wait()

            time.sleep(delay_time)