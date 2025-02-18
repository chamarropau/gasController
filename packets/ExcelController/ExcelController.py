from packets.ExcelController.Configuration import Configuration
from packets.ExcelController.Measurement import Measurement
from termcolor import colored
import pandas as pd
import re

class ExcelController:
    def __init__(self):
        pass

    def read_excel(self, excel_path, sheet_name):
        self.excel_path = excel_path
        df = pd.read_excel(excel_path, sheet_name=sheet_name, skiprows=1)
        mfcs_columns = [col for col in df.columns if col.startswith("mfc")]
        smus_columns = [col for col in df.columns if col.startswith("v(V)") or col.startswith("i(A)")]
        smus_columns = list(zip(smus_columns[::2], smus_columns[1::2]))
        measurements = []
        config = None
        
        for index, row in df.iterrows():
            
            if row["tipus"] == "CONFIG":
                mfcs_flows = {}
                for mfc in mfcs_columns:
                    if not df.isna().loc[index][mfc]:
                        max_gas_flow = self.__format_floats(row[mfc]) 
                        gas_ppm = self.__format_floats(df.loc[index+1][mfc]) 
                        gas_type = df.loc[index+2][mfc]
                        id = re.search(r'\d+', mfc).group()
                        mfcs_flows[mfc.upper()] = {"id" : int(id), "max_flow": float(max_gas_flow), "ppm": float(gas_ppm), "type": gas_type}

                config = Configuration(mfcs_flows)

            elif row["tipus"] == "MESURA":
                measurement_time = self.__extract_time(row["temps"])
                mfcs_flows = {}
                for mfc in mfcs_columns:
                    if not df.isna().loc[index][mfc]:
                        gas_flow = self.__format_floats(row[mfc]) 
                    else:
                        gas_flow = 0
                        
                    mfcs_flows[mfc.upper()] = float(gas_flow)

                smu_measurements = {}
                for index, smu_column in enumerate(smus_columns):
                    smu_values = {}
                    current_value =  self.__format_floats(row[smu_column[1]])
                    voltage_value =  self.__format_floats(row[smu_column[0]])
                    
                    if current_value != 'nan' and voltage_value != 'nan':
                        raise Exception("Current and voltage values can't be both different from 0")
                    elif current_value != 'nan':
                        smu_values["value"] = current_value.split(' ')[0]
                        smu_values["unit"] = current_value.split(' ')[1]
                        smu_values["mode"] = "current"
                    else:
                        smu_values["value"] = voltage_value.split(' ')[0]
                        smu_values["unit"] = voltage_value.split(' ')[1]
                        smu_values["mode"] = "voltage"

                    smu_measurements[f"SMU{index+1}"] = smu_values
                        
                ad_time = self.__extract_time(row['ad_time'])
                sv_time = self.__extract_time(row['sv_time'])    
    
                measurement = Measurement(measurement_time, mfcs_flows, smu_measurements, ad_time, sv_time)
                measurements.append(measurement)
                
            elif row["tipus"] == "FINAL":
                print(f"\n{colored('[INFO]', 'blue')} Excel read successfully\n")

        return config, measurements # Configuration(), [Measurement(), Measurement(), ...]

    def __extract_time(self, str_time):
        labels = {"w" : 604800, "d" : 86400, "h" : 3600, "m" : 60, "s" : 1}
        
        if pd.isna(str_time):
            return 0
        matches = re.findall(r'(\d+)([wdhms])', str_time)
        total_sec = sum(map(lambda x: float(x[0]) * labels[x[1]], matches))
        return total_sec

    def __format_floats(self, str_float):
        str_float = str(str_float)
        return str_float.replace(',', '.')                                                                                                                                                                                            

if __name__ == "__main__":
    excelcontroller = ExcelController()
    pipeline = excelcontroller.read_excel("C:\\Users\\Pau\\Desktop\\ACME\\gasControl\\MFC\\gasControl\\data\\llibre_Input_Output_Estacio_gasos.xlsx")
    print(pipeline)