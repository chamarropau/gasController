from packets.ExcelController.ExcelController import ExcelController
from packets.ExcelController.OutputExcel import OutputExcel
from model.ElectricalMeasurementsTypes.AutomaticIV import AutomaticIV
from model.ElectricalMeasurementsTypes.AutomaticVI import AutomaticVI
from model.ElectricalMeasurementsTypes.AutomaticIT import AutomaticIT
from model.ElectricalMeasurementsTypes.AutomaticVT import AutomaticVT
from model.DataManager import DataManager
from threading import Thread, Barrier, Event
from termcolor import colored
import pandas as pd
import time
import re
import signal

class AutomaticMode:

    def __init__(self, keithley_selected, keithleys, mfc, data_measurement, excel_path, excel_sheet):
        self.keithley_selected = keithley_selected
        self.keithleys = keithleys
        self.mfc = mfc
        self.data_measurement = data_measurement
        self.electrical_measurement = None
        self.excel_path = excel_path
        self.excel_sheet = excel_sheet
        if keithley_selected == 1 or keithley_selected == 2:
            self.barrier = Barrier(2)
        else:
            self.barrier = Barrier(3)
        self.stop_event = Event()
        self.thread_1 = None
        self.thread_2 = None
        self.data = []
        self.start_time = None


    def run(self):
        print(f"\n\n{colored('[STATUS]', 'green')} STARTING AUTOMATIC MODE...\n\n")
        excel_controller = ExcelController()
        config, measurements = excel_controller.read_excel(self.excel_path, self.excel_sheet)

        try:
            for i, measurement in enumerate(measurements):
                print(f"\n\n{colored('[STATUS]', 'green')} STARTING MEASUREMENT {i+1}...\n\n")
                smu_1_mode = measurement.get_smu_mode("SMU1")
                smu_2_mode = measurement.get_smu_mode("SMU2")
                smu_1_value = measurement.get_smu_value("SMU1")
                smu_2_value = measurement.get_smu_value("SMU2")
                smu_1_unit = measurement.get_smu_unit("SMU1")
                smu_2_unit = measurement.get_smu_unit("SMU2")
                sv_time = measurement.get_sv_time()
                ad_time = measurement.get_ad_time()
                measurement_time = measurement.get_measurement_time()
                mfcs_flows = measurement.get_mfcs_flows()

                for mfc_name, mfc_flow in mfcs_flows.items():
                    mfc_id = config.get_mfc_id(mfc_name)
                    max_flow = config.get_mfc_max_flow(mfc_name)
                    self.mfc.set_flow(mfc_id, mfc_flow, max_flow)

                total_flow = self.mfc.get_sum_flow()
                print(f"{colored('[INFO]', 'blue')} Total flow: {total_flow} sccm")

                if total_flow > 200:
                    print(f"{colored('[WARNING]', 'yellow')} Skipping measurement {i+1} as total flow ({total_flow}) exceeds 200.\n")
                    continue 

                # Aquí se acumulan los datos de la medición
                measurement_data = []  # Lista para acumular datos de esta medición

                if self.keithley_selected == 1:
                    electrical_measurement = self.__get_electrical_measurement(smu_1_mode, smu_1_value, smu_1_unit, measurement_time, 0)
                    self.thread_1 = Thread(target=electrical_measurement.run, args=(self.barrier, self.stop_event))
                    self.thread_1.start()

                    data_manager = DataManager(self.mfc, [electrical_measurement], self.data_measurement, measurement_time, ad_time, sv_time)
                    if self.start_time is None:
                        self.start_time = time.time()
                    elapsed_time = time.time() - self.start_time

                    try:
                        data = data_manager.run(self.barrier, elapsed_time=elapsed_time, saving_time=sv_time)
                        self.data.append(data)  # Guardar datos en cada iteración

                        measurement_data.append(data)  # Acumulando datos de esta medición

                    except Exception as e:
                        print(f"{colored('[ERROR]', 'red')} Error in measurement {i+1} point: {e}")
                        # Guardar los datos acumulados hasta el fallo
                        self.data.append(measurement_data)  # Guardar lo acumulado hasta el fallo
                        break  # Salir del ciclo de la medición actual

                    finally:
                        self.thread_1.join()  # Asegurarse de que el hilo se cierre

        except Exception as e:
            print(f"\n\n{colored('[STATUS]', 'red')} Error occurred: {e}\n\n")
        finally:
            # Guardar los datos después de la ejecución completa (incluidos los acumulados)
            self.saving_data()
            self.stop_event.set()
            if self.thread_1 and self.thread_1.is_alive():
                self.thread_1.join()
            if self.thread_2 and self.thread_2.is_alive():
                self.thread_2.join()

            print(f"\n\n{colored('[STATUS]', 'green')} Program finished. Data saved.\n\n")

    def __get_electrical_measurement(self, smu_mode, smu_value, smu_unit, measurement_time, smu_id):
        electrical_mesurement = None
        if "/" in smu_value:  # AutomaticVI or AutomaticIV
            pattern = r"(\d+)-(\d+)/(\d+)"
            match = re.match(pattern, smu_value)
            initial_value = float(match.group(1))
            final_value = float(match.group(2))
            step = int(match.group(3))

            if smu_mode == "current":
                electrical_mesurement = AutomaticVI(self.keithleys[smu_id], initial_value, smu_unit, final_value, smu_unit, step, measurement_time, mode="automatic")
            else:
                electrical_mesurement = AutomaticIV(self.keithleys[smu_id], initial_value, smu_unit, final_value, smu_unit, step, measurement_time, mode="automatic")

        else:
            smu_value = float(smu_value)
            if smu_mode == "current":
                electrical_mesurement = AutomaticVT(self.keithleys[smu_id], smu_value, smu_unit, measurement_time, mode="automatic")
            else:
                electrical_mesurement = AutomaticIT(self.keithleys[smu_id], smu_value, smu_unit, measurement_time, mode="automatic")

        return electrical_mesurement

    def saving_data(self):

        name = f"Measure_{time.strftime('%Y%m%d-%H%M%S')}.xlsx"
        output = OutputExcel(f"./data/{name}", self.data)
        output.save_excel()

        if self.thread_1 and self.thread_1.is_alive():
            self.thread_1.join()
        if self.thread_2 and self.thread_2.is_alive():
            self.thread_2.join()

        
