from pymeasure.instruments.keithley import Keithley2450
from packets.Keithley.EthernetConnection import EthernetConnection
from termcolor import colored
import pyvisa as vs
import time

class Keithley:
    """
    Class to control the Keithley 2450 device using pymeasure.
    """
    def __init__(self, keithley_config):  # keithley_config = {'ip', 'interface', 'mask', 'gateway'}
        # Set up the Ethernet connection
        EthernetConnection().ip_static_configuration(keithley_config['interface'], \
                                                        keithley_config['ip'], \
                                                        keithley_config['mask'], \
                                                        keithley_config['gateway'])
        self.addr = f"TCPIP0::{keithley_config['ip']}::inst0::INSTR"
        
        while True:
            try:
                self.__device_configuration()  # Initialize the Keithley 2450 using pymeasure
                break
            except Exception as e:
                print(e.__str__())
                print(f"{colored('[INFO]', 'blue')} Trying to connect again in 5 seconds...")
                time.sleep(5)

        self.mode = None
        # List of tuples [(x,y),(x,y)...] where x will be the dependent variable and y the independent variable.
        # This list will be cleared after each measurement
        self.measures_list = []


    def __device_configuration(self):
        try: 
            self.keithley = Keithley2450(self.addr, timeout=20000)  # Initialize the Keithley 2450 using pymeasure
            
            if self.keithley is None:
                raise Exception(f"{colored('[ERROR]', 'red')} Could not find the Keithley device. Please check the connection.")
            
            #self.keithley.beep(880, 0.5)  # A short beep at 880 Hz (A5 note) for 0.5 seconds
            #self.keithley.beep(660, 0.3)  # Another beep at 660 Hz (E5 note) for 0.3 seconds

            # self.keithley.beep(261, 0.5)  # C4
            # self.keithley.beep(261, 0.5)  # C4
            # self.keithley.beep(392, 0.5)  # G4
            # self.keithley.beep(392, 0.5)  # G4
            # self.keithley.beep(440, 0.5)  # A4
            # self.keithley.beep(440, 0.5)  # A4
            # self.keithley.beep(392, 1.0)  # G4 (hold longer)

            
            self.keithley.reset()  # Reset the instrument
        except vs.VisaIOError as e:
            raise Exception(f"{colored('[ERROR]', 'red')} Could not find the Keithley device. Please check the connection.")


    def reset_measurement(self):
        self.keithley.reset()  # Reset the instrument
        #self.keithley.disable_source()  # Disable the source (equivalent to smu.source.output = smu.OFF)
        self.keithley.use_front_terminals()  # Usa los terminales frontales

    def close(self):
        self.keithley.shutdown()  # Shut down the instrument

    ##################################  V(I) METHODS  #########################################

    def init_current_mode(self, unit):  # Apply current and measure voltage
        self.reset_measurement()
        self.keithley.apply_current()  # Set the Keithley to source current mode
        self.keithley.measure_voltage(nplc=0.01)
        #self.keithley.source_current_range = 10e-3  # Set current range (e.g., 10 mA)
        self.keithley.compliance_voltage = 21  # Set voltage compliance to 21 V
        self.keithley.enable_source()  # Enable the source

        factor = 0
        # Convert current based on the specified unit
        if unit == "mA":
            factor = 1e-3
        elif unit == "uA":
            factor = 1e-6
        elif unit == "nA":
            factor = 1e-9
        elif unit == None:
            factor = 1
        else:
            raise Exception("Invalid unit. Please use mA, uA, or nA.")
        
        return factor
    
    def convert_current(self, current, unit):
        #8 Print current and unit
        factor = 0
        if unit == "mA":
            factor = 1e-3
        elif unit == "uA":
            factor = 1e-6
        elif unit == "nA":
            factor = 1e-9
        else:
            raise Exception("Invalid unit. Please use mA, uA, or nA.")
        
        return current * factor

    def set_current(self, current, factor):  # Unit: mA, uA, or nA
        if self.mode != "current":
            self.mode = "current"

        self.keithley.source_current = current * factor
        voltage = self.keithley.voltage

        return voltage

    def get_voltage(self):
        return self.keithley.voltage  # Return the last measured voltage

    ##################################  I(V) METHODS  #########################################

    def init_voltage_mode(self, unit):  # Apply voltage and measure current
        self.reset_measurement()
        self.keithley.apply_voltage()  # Set the Keithley to source voltage mode
        self.keithley.measure_current(nplc=0.01)
        #self.keithley.source_voltage_range = 10  # Set voltage range (10 V in this example)
        self.keithley.compliance_current = 0.1  # Set current compliance to 21 mA
        self.keithley.enable_source()  # Enable the source

        # Convert voltage based on the specified unit
        factor = 0
        if unit == "mV":
            factor =  1e-3
        elif unit == "uV":
            factor =  1e-6
        elif unit == "V":
            factor = 1
        elif unit == None:
            factor = 1
        else:
            raise Exception("Invalid unit. Please use V, mV, or uV.")
        
        return factor
    
    def convert_voltage(self, voltage, unit):
        factor = 0
        if unit == "mV":
            factor =  1e-3
        elif unit == "uV":
            factor =  1e-6
        elif unit == "V":
            factor = 1
        else:
            raise Exception("Invalid unit. Please use V, mV, or uV.")
        
        return voltage * factor

    def set_voltage(self, voltage, factor=1):  # Unit: V, mV, uV
        if self.mode != "voltage":
            self.mode = "voltage"

        self.keithley.source_voltage = voltage * factor
        current = self.keithley.current

        return current

        # Measure current across the DUT 
        #return self.keithley.current
        
    def add_measures_list(self, X, Y, time=None):
        if time is None:
            self.measures_list.append((X,Y))
        else:
            self.measures_list.append((X,Y,time))

    def clean_measures_list(self):
        self.measures_list.clear()

    def get_measures_list(self):
        return self.measures_list

    def get_current(self):
        return self.keithley.current  # Return the last measured current


def main():
    # Configuración de la conexión al Keithley 2450
    config = {'interface': 'Ethernet', 'ip': '192.168.100.130', 'mask': '255.255.255.128', 'gateway': '192.168.100.129'}

    # Inicialización del objeto Keithley
    try:
        keithley_device = Keithley(config)
        print("[INFO] Dispositivo Keithley inicializado correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo inicializar el dispositivo Keithley: {e}")
        return

    # Ejemplo de uso del método set_voltage
    try:
        voltage = 1.0  # Valor de voltaje deseado
        voltage_unit = "V"  # Unidad de voltaje (V, mV o uV)
        
        # Llamar al método set_voltage
        init = time.time()
        current = keithley_device.set_voltage(voltage, unit=voltage_unit)
        final = time.time()

        print(final-init)
        
        print(f"Voltaje aplicado: {voltage}{voltage_unit}")
        print(f"Corriente medida: {current} A")
    except Exception as e:
        print(f"[ERROR] No se pudo configurar el voltaje: {e}")
    finally:
        # Asegurarse de cerrar la conexión con el dispositivo
        keithley_device.close()
        print("[INFO] Conexión cerrada.")

# Ejecutar el main si el script se ejecuta directamente
if __name__ == "__main__":
    main()