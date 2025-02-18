from model.ElectricalMeasurementsTypes.ElectricalMeasurementType import ElectricalMeasurementType
import time

class AutomaticIT(ElectricalMeasurementType):
    def __init__(self, keithley, \
                 voltage, voltage_unit, measurement_time, mode=None):
        super().__init__(keithley, measurement_time)
        self.voltage = voltage
        self.voltage_unit = voltage_unit
        self.measurement_time = measurement_time
        self.mode = mode

    def run(self, barrier=None, stop_event=None):
        factor = self.keithley.init_voltage_mode(unit=self.voltage_unit)
        i = self.keithley.set_voltage(self.voltage, factor)

        if barrier is not None:
            barrier.wait()

        init_time = time.time()
        prev_current = self.keithley.get_current()

        # self.keithley.add_measure(prev_current, self.voltage*factor, 0)

        while time.time() - init_time < self.measurement_time:
            if stop_event is not None and stop_event.is_set():
                break

            i = self.keithley.get_current()
            self.current = i

            # Establecer umbral dinámico basado en el valor absoluto de la corriente
            threshold = max(abs(prev_current) * 0.05, 1e-10)

            if abs(i - prev_current) > threshold:
                current_time = time.time() - init_time  # Tiempo transcurrido desde el inicio
                x = self.keithley.get_current()

                if self.mode is not None: 
                    self.keithley.add_measures_list(x, self.voltage*factor)

                else:
                    self.keithley.add_measures_list(x, self.voltage*factor, current_time)
                

            prev_current = i
            time.sleep(2)