from termcolor import colored
import time

class DataManager:
    def __init__(self, mfc, electrical_types, data_measurement, measurement_time, ad_time, sv_time):
        self.mfc = mfc
        self.electrical_types = electrical_types
        self.data_measurement = data_measurement
        self.measurement_time = measurement_time
        self.ad_time = ad_time
        self.sv_time = sv_time

        self.data = {}
        for mfc_id in mfc.get_ids():
            self.data[f"MFC{mfc_id}"] = []

        self.data["Temperature"] = []
        self.data["Humidity"] = []
        self.data["Time"] = []
        
        for i, _ in enumerate(self.electrical_types):
            self.data[f"Voltage_{i+1}"] = []  
            self.data[f"Current_{i+1}"] = []

    def get_data(self, init_time):
        data = {}
        measure_time = time.time() - init_time
        temp, hum = self.data_measurement.get_all()
        mfcs_flows = {}
        smus_values = {}
        
        for mfc_id in self.mfc.get_ids():
            mfc_flow, mfc_unit = self.mfc.get_flow(mfc_id)
            mfcs_flows[f"MFC{mfc_id}"] = f"{mfc_flow} {mfc_unit}"
        
        for i, el_type in enumerate(self.electrical_types):
            voltage = el_type.get_voltage()
            current = el_type.get_current()

            smus_values[f"Voltage_{i+1}"] = voltage
            smus_values[f"Current_{i+1}"] = current

        data["Time"] = measure_time
        data["Temperature"] = temp
        data["Humidity"] = hum
        data["MFCs"] = mfcs_flows
        data["SMUs"] = smus_values

        return data


    def print_data(self, data):
        # measure_time = data["Time"]
        # print(f"\n-------------------- Measurement at time: {round(measure_time,2)} --------------------\n")
        # temp, hum = data["Temperature"], data["Humidity"]
        # print(f"> Temperature: {temp} ºC")
        # print(f"> Humidity: {hum} %")
        
        # for mfc_id in data["MFCs"].keys():
        #     mfc_flow = data["MFCs"][mfc_id]
        #     print(f"> {mfc_id}: {mfc_flow}")
        
        # for i, el_type in enumerate(self.electrical_types):
        #     voltage = data["SMUs"][f"Voltage_{i+1}"]
        #     current = data["SMUs"][f"Current_{i+1}"]
        #     print(f"> Voltage_{i+1}: {voltage}")
        #     print(f"> Current_{i+1}: {current}")
        
        print()


    def save_data(self, data_in):
        measure_time = data_in["Time"]
        print(f"\n{colored('[STATUS]', 'green')} Saved at time: {round(measure_time, 2)}\n")
        self.data["Time"].append(measure_time)
        temp, hum = data_in["Temperature"], data_in["Humidity"]
        self.data["Temperature"].append(temp)
        self.data["Humidity"].append(hum)
        
        for mfc_id in data_in["MFCs"].keys():
            mfc_flow = data_in["MFCs"][mfc_id]
            self.data[mfc_id].append(mfc_flow)
            
        for i, el_type in enumerate(self.electrical_types):
            voltage = data_in["SMUs"][f"Voltage_{i+1}"]
            current = data_in["SMUs"][f"Current_{i+1}"]
            self.data[f"Voltage_{i+1}"].append(voltage)
            self.data[f"Current_{i+1}"].append(current)

        print()

    def run(self, barrier = None, stop_event = None):
        # Wait all electrical types to start before starting the measurement
        if barrier is not None:
            barrier.wait()
        init_time = time.time()
        data = self.get_data(init_time)
        self.save_data(data)
        last_ad_time = init_time
        last_sv_time = init_time
        
        while time.time() - init_time < self.measurement_time:

            ad_time_computed = (time.time() - last_ad_time >= self.ad_time)
            sv_time_computed = (time.time() - last_sv_time >= self.sv_time)

            if ad_time_computed or sv_time_computed: 
                data = self.get_data(init_time)

                if ad_time_computed:
                    self.print_data(data)
                    last_ad_time = last_ad_time + self.ad_time

                if sv_time_computed:
                    self.save_data(data)
                    last_sv_time = last_sv_time + self.sv_time

                
        data = self.get_data(init_time)
        self.save_data(data) 
        
        return self.data
