from packets.ExcelController.OutputExcel import OutputExcel
from model.ElectricalMeasurementsTypes.ManualVI import ManualVI
from model.ElectricalMeasurementsTypes.ManualIV import ManualIV
from model.ElectricalMeasurementsTypes.AutomaticVI import AutomaticVI
from model.ElectricalMeasurementsTypes.AutomaticIV import AutomaticIV
from model.ElectricalMeasurementsTypes.AutomaticVT import AutomaticVT
from model.ElectricalMeasurementsTypes.AutomaticIT import AutomaticIT
from model.DataManager import DataManager
from termcolor import colored
from threading import Thread, Barrier, Event
import time
import re


class ManualMode:
    def __init__(self, keithleys, mfc, mfcs_flows, sv_time):
        self.mfc = mfc
        self.mfcs_flows = mfcs_flows
        self.keithleys = keithleys
        self.electrical_measurement = None
        self.thread = None
        self.barrier = Barrier(2)
        self.data_manager = None
        self.stop_event = Event()
        self.sv_time = sv_time
        self.data = []

    def run(self):

        for mfc_name, mfc_flow in self.mfcs_flows.items():
            mfc_id = re.search(r'\d+', mfc_name).group()
            self.mfc.set_flow(mfc_id, mfc_flow)

        if self.electrical_measurement is not None:
            self.thread = Thread(target=self.electrical_measurement.run, args=(self.barrier, self.stop_event))
            self.thread.start()
            if self.data_manager is None:
                raise Exception(f"{colored('[ERROR]', 'red')} No data manager created. Use set_data_manager method after run mode")
            data = self.data_manager.run(self.barrier, saving_time=self.sv_time)
            self.thread.join()
            self.data.append(data)
            self.saving_data()
            return data
        else:
            raise Exception("No electrical measurement selected")

    def set_manual_VI_measurement(self, current, current_unit, measurement_time):
        self.electrical_measurement = ManualVI(self.keithleys[0], current, current_unit, measurement_time)

    
    def set_manual_IV_measurement(self, voltage, voltage_unit, measurement_time):
        self.electrical_measurement = ManualIV(self.keithleys[0], voltage, voltage_unit, measurement_time)
        
    
    def set_automatic_VI_measurement(self, initial_current, initial_unit, final_current, final_unit, n_points_current, measurement_time):
        self.electrical_measurement = AutomaticVI(self.keithleys[0], initial_current, initial_unit, final_current, final_unit, n_points_current, measurement_time)

    
    def set_automatic_IV_measurement(self, initial_voltage, initial_unit, final_voltage, final_unit, n_points_voltage, measurement_time):
        self.electrical_measurement = AutomaticIV(self.keithleys[0], initial_voltage, initial_unit, final_voltage, final_unit, n_points_voltage, measurement_time)

    
    def set_automatic_VT_measurement(self, current, current_unit, measurement_time):
        self.electrical_measurement = AutomaticVT(self.keithleys[0], current, current_unit, measurement_time)

    
    def set_automatic_IT_measurement(self, voltage, voltage_unit, measurement_time):
        self.electrical_measurement = AutomaticIT(self.keithleys[0], voltage, voltage_unit, measurement_time)


    def set_data_manager(self, mfc, data_measurement, measurement_time, ad_time, sv_time):
        self.data_manager = DataManager(mfc, [self.electrical_measurement], data_measurement, measurement_time, ad_time, sv_time)

    def saving_data(self):
        name = f"ManualMode_Measure_{time.strftime('%Y%m%d-%H%M%S')}.xlsx"
        output = OutputExcel(f"./data/{name}", self.data)
        output.save_excel()

        print(f"{colored('[STATUS]', 'green')} Data saved in {name}")