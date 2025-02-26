from model.ManualMode import ManualMode
from model.AutomaticMode import AutomaticMode
from packets.DataMeasurement.DataMeasurement import DataMeasurement
from packets.DataMeasurement.DataMeasurementFake import DataMeasurementFake
from packets.Keithley.Keithley import Keithley
from packets.Keithley.KeithleyFake import KeithleyFake
from model.MassFlowController import MassFlowController

class Controller:
    def __init__(self, mode=None):
        self.mode = mode # This gonna be manual or automatic mode
        
        # KEITHLEY 1
        config_1 = {'interface': 'Ethernet 2', 'ip': '192.168.100.130', 'mask': '255.255.255.128', 'gateway': '192.168.100.129'}
        self.times1 = []

        # KEITHLEY 2
        config_2 = {'interface': 'Ethernet 4', 'ip': '192.168.100.2', 'mask': '255.255.255.128', 'gateway': '192.168.100.1'}
        self.times2 = []

        # Add Keithley to the list
        self.keithleys = [Keithley(config_1)]

        # self.data_measurement = DataMeasurement('COM4')
        self.data_measurement = DataMeasurement()
        # MFCs [3,6,9,12,16,20]
        self.mfc = MassFlowController([])
        self.mfc.clear_all_flows()

    def set_mode(self, mode, flows=None, keithley_selected=None, excel=None, sheet=None, sv_time=None, num_keithleys=None, output_excel=None, steps=None):
        if mode == "manual":
            if flows is None:
                flows = self.ask_for_flows()
            print(flows)
            self.mode = ManualMode(self.keithleys, self.mfc, flows, sv_time, output_excel, steps)

        elif mode == "automatic":
            if excel is None and sheet is None:
                excel = "./data/llibre_Input_Output_Estacio_gasos.xlsx"
                sheet = "data"
            self.mode = AutomaticMode(keithley_selected, self.keithleys, self.mfc, self.data_measurement, excel, sheet, num_keithleys, output_excel)

    def get_measurements(self):
        # If mode is ManualMode return 1, if it's AutomaticMode return 2, else return 0
        if isinstance(self.mode, ManualMode):
            # print("Measures", self.keithleys[0].get_measures())
            return self.keithleys[0].get_measures_list()
        
    def clean_measures(self):
        self.keithleys[0].clean_measures_list()

    def get_automatic_measures(self, keithley_selected):
        if not self.keithleys:
            return []

        count_keithley = self.get_num_keithleys()

        if keithley_selected == 1:
            return [self.keithleys[0].get_measures_list()]

        elif keithley_selected == 2:
            return [self.keithleys[min(1, count_keithley - 1)].get_measures_list()]

        elif keithley_selected == 3 and count_keithley >= 2:
            return [self.keithleys[0].get_measures_list(), self.keithleys[0].get_measures_list()]
        
        else:
            return []
    
    def set_manual_VI(self, current, current_unit, measurement_time):
        self.mode.set_manual_VI_measurement(current, current_unit, measurement_time)

    def set_manual_IV(self, voltage, voltage_unit, measurement_time):
        self.mode.set_manual_IV_measurement(voltage, voltage_unit, measurement_time)
        
    def set_automatic_VI(self, initial_current, initial_unit, final_current, final_unit, n_points_current, measurement_time): 
        self.mode.set_automatic_VI_measurement(initial_current, initial_unit, final_current, final_unit, n_points_current, measurement_time)

    def set_automatic_IV(self, initial_voltage, initial_unit, final_voltage, final_unit, n_points_voltage, measurement_time):
        self.mode.set_automatic_IV_measurement(initial_voltage, initial_unit, final_voltage, final_unit, n_points_voltage, measurement_time)

    def set_automatic_VT(self, current, current_unit, measurement_time):
        self.mode.set_automatic_VT_measurement(current, current_unit, measurement_time)

    def set_automatic_IT(self, voltage, voltage_unit, measurement_time):
        self.mode.set_automatic_IT_measurement(voltage, voltage_unit, measurement_time)

    def set_data_manager(self, measurement_time, ad_time, sv_time):
        self.mode.set_data_manager(self.mfc, self.data_measurement, measurement_time, ad_time, sv_time)

    def get_num_keithleys(self):
        return len(self.keithleys)

    def ask_for_flows(self):
        max_flows = {3: 200, 6: 200, 9: 200, 12: 200, 16: 200, 20: 20}
        
        # Ask the user to input the MFCs they want to use
        selection = input("Enter the MFC IDs you want to use, separated by commas: ")

        # Convert input into a list of integers
        selected_ids = [int(x.strip()) for x in selection.split(',')]

        print(f"Selected MFCs: {selected_ids}")
        
        while True:  # Repetir hasta que la suma de flujos sea <= 200
            # Create a dictionary to store the flows
            selected_flows = {}

            for id in selected_ids:
                # Ask the user to input the flow for each MFC
                flow = float(input(f"Enter the flow for MFC {id} (max: {max_flows[id]}): "))
                if flow > max_flows[id]:
                    print(f"Flow for MFC {id} is too high! Setting it to the maximum value...")
                    flow = max_flows[id]
                selected_flows[f"MFC{id}"] = flow

            # Calculate the total flow
            total_flow = sum(selected_flows.values())

            if total_flow > 200:
                print(f"\nThe total flow ({total_flow}) exceeds the limit of 200. Please adjust the flows again.\n")
            else:
                print(f"Selected flows: {selected_flows}")
                return selected_flows
        
        
    def run_mode(self):
        if self.mode is not None:
            return self.mode.run()
        else:
            print("No mode selected!")

    def shutdown(self):
        if self.keithleys is not None:
            for keithley in self.keithleys:
                if keithley is not None:
                    keithley.close()

        if self.data_measurement is not None:
            self.data_measurement.close()

        if self.mfc is not None:
            self.mfc.clear_all_flows()
            
        print("All devices closed!")

    def close_mfcs(self):
        if self.mfc is not None:
            self.mfc.clear_all_flows()
            
        print("All MFCs closed!")