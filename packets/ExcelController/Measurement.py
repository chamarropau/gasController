
class Measurement():
    def __init__(self, measurement_time, mfcs_flows, smu_values, ad_time, sv_time):
        self._measurement_time = measurement_time
        self._mfcs_flows = mfcs_flows # {"MFC1": flow1, "MFC2": flow2, ...}
        self._smu_values = smu_values # {"SMU1": {"value" : value, "mode":"voltage/current"}, ...}
        self._ad_time = ad_time
        self._sv_time = sv_time

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"\n\nMEASUREMENT: \nmeasurement_time: {self._measurement_time}, \nad_time: {self._ad_time}, \nsv_time: {self._sv_time}, \nmfcs: {str(self._mfcs_flows)}, \nsmus: {str(self._smu_values)}"
    
    def get_measurement_time(self):
        return self._measurement_time

    def get_smu_mode(self, id): # id = SMU1, SMU2, ...
        return self._smu_values[id]["mode"] # "voltage" or "current"

    def get_smu_value(self, id): # id = SMU1, SMU2, ...
        return self._smu_values[id]["value"]

    def get_smu_unit(self, id): # id = SMU1, SMU2, ...
        return self._smu_values[id]["unit"]
    
    def get_ad_time(self):
        return self._ad_time
    
    def get_sv_time(self):
        return self._sv_time

    def get_mfcs_flows(self):
        return self._mfcs_flows