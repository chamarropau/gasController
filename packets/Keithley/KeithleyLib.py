from pymeasure.instruments.keithley import Keithley2450
import pyvisa as vs
import time


def main():
    # Connect to the instrument
    keithley = Keithley2450("TCPIP0::192.168.100.2::inst0::INSTR")
    keithley.beep(65, 1)


    print(keithley.id)
    # Check connection
    if keithley != None:
        print("Connection successful")

    # Set the voltage source
    keithley.apply_current()                # Sets up to source current
    keithley.source_current_range = 10e-3   # Sets the source current range to 10 mA
    keithley.compliance_voltage = 10        # Sets the compliance voltage to 10 V
    keithley.source_current = 0.005
    keithley.enable_source()    
    print(keithley.voltage)


if __name__ == '__main__':
    # Connect to the instrument
    main()