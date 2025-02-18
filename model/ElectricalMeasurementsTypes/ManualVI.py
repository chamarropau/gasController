from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType

class ManualVI(ElectricalMeasurementType):
    def __init__(self, keithley, current, current_unit, measurement_time):
        super().__init__(keithley, measurement_time)
        self.current = current
        self.current_unit = current_unit

    def run(self, barrier=None, stop_event=None):
        
        factor = self.keithley.init_current_mode(unit=self.current_unit)

        v = self.keithley.set_current(self.current, factor)
        self.voltage = v

        self.keithley.add_measures_list(v, self.current*factor)

        if barrier is not None:
            barrier.wait()

