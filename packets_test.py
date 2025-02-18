from packets.Keithley.KeithleyPyMeasure import KeithleyPyMeasure
from packets.Keithley.Keithley import Keithley
from packets.DataMeasurement.DataMeasurement import DataMeasurement
from packets.DataMeasurement.DataMeasurementFake import DataMeasurementFake
from packets.MassFlowDevice.MassFlowDevice import MassFlowDevice
from packets.MassFlowDevice.MassFlowDeviceFake import MassFlowDeviceFake

import time

from threading import Thread

def test_massflow():
    massflow = MassFlowDevice(id=3)
    # massflow = MassFlowDeviceFake(id=0)
    massflow.set_flow(0)
    massflow = MassFlowDevice(id=6)
    # massflow = MassFlowDeviceFake(id=0)
    massflow.set_flow(0)
    massflow = MassFlowDevice(id=9)
    # massflow = MassFlowDeviceFake(id=0)
    massflow.set_flow(0)
    print(massflow.get_flow())
    massflow.clear_flow()
    time.sleep(2)
    print(massflow.get_flow())

def test_datameasurement():
    datameasurement = DataMeasurement('COM4')
    # datameasurement = DataMeasurementFake('COM3')
    temp, hum  = datameasurement.get_all()
    print("Temperature: ", temp)
    print("Humidity: ", hum)
    datameasurement.close()

def test_keithley():
    config_1 = {'interface': 'Ethernet 3', 'ip': '192.168.100.2', 'mask' : '255.255.255.128', 'gateway' : '192.168.100.1'}
    config_2 = {'interface': 'Ethernet 4', 'ip': '192.168.100.130', 'mask': '255.255.255.128', 'gateway': '192.168.100.129'}

    keithley1 = KeithleyPyMeasure(config_1)
    keithley2 = KeithleyPyMeasure(config_2)
    # keithley = KeithleyFake(keythley_config)

    voltage_keth = keithley1.set_current(1, unit='mA')
    print("Setted Voltage: ", voltage_keth)

    voltage_keth = keithley2.set_current(1, unit='mA')
    print("Setted Voltage: ", voltage_keth)

    ######################################################


    voltage_keth = keithley1.set_voltage(1, unit='mV')
    print("Setted Current: ", voltage_keth)

    voltage_keth = keithley2.set_voltage(1, unit='mV')
    print("Setted Current: ", voltage_keth)

if __name__ == '__main__':
    test_massflow()