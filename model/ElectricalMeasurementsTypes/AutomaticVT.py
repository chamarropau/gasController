from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType
import time

class AutomaticVT(ElectricalMeasurementType):
    def __init__(self, keithley, \
                 current, current_unit, measurement_time, mode=None):
        super().__init__(keithley, measurement_time)
        self.current = current
        self.current_unit = current_unit
        self.measurement_time = measurement_time
        self.mode = mode

    def run(self, barrier=None, stop_event=None):
        factor = self.keithley.init_current_mode(unit=self.current_unit)
        v = self.keithley.set_current(self.current, factor)
        
        if barrier is not None:
            barrier.wait()

        init_time = time.time()
        prev_voltage = self.keithley.get_voltage()

        # self.keithley.add_measure(prev_voltage, self.current*factor, 0)

        while time.time() - init_time < self.measurement_time:
            if stop_event is not None and stop_event.is_set():
                break

            v = self.keithley.get_voltage()
            self.voltage = v

            # Establecer umbral dinámico basado en el valor absoluto del voltaje
            threshold = max(abs(prev_voltage) * 0.05, 1e-10)

            if abs(v - prev_voltage) > 0.0001:
                current_time = time.time() - init_time  # Tiempo transcurrido desde el inicio
                x = self.keithley.get_voltage()

                if self.mode is not None:
                    self.keithley.add_measures_list(x, self.current*factor)

                else:
                    self.keithley.add_measures_list(x, self.current*factor, current_time)

            prev_voltage = v
            time.sleep(2)