import subprocess as sb
import time
from termcolor import colored

class EthernetConnection:
    """
    Class to configure the Ethernet connection of the Keithley instrument.
    """
    def ip_static_configuration(self, interface, ip, mask, gateway):
        command = (f"netsh interface ipv4 set address name=\"{interface}\" source=static address={gateway} mask={mask} gateway={gateway}")
        
        try:
            # Execute the command to configure static IP
            sb.run(command, shell=True, check=True)
            
            if self.__verify_connection(ip):
                print(f"{colored('[STATUS]', 'green')} Connection verified.")
            else:
                print(f"{colored('[WARN]', 'yellow')} Connection could not be verified. Please check network settings.")
                
        except sb.CalledProcessError as e:
            print("Error configuring static IP:", e)
        except Exception as e:
            print("An error occurred:", e)


    def __verify_connection(self, ip):
        """Verify the connection of the instrument."""
        try:
            # Ping the gateway
            response = sb.run(f"ping {ip} -n 3", shell=True, capture_output=True, text=True)
            return "recibidos = 0" not in response.stdout
       
        except sb.TimeoutExpired:
            raise Exception("Connection verification timed out.")
            
        except Exception as e:
            raise Exception("Error verifying connection:", e)


    def ip_dinamic_configuration(self, interface): # This function is not tested
        print("configuring dinamic IP addressing...")
        c = (f'netsh interface ipv4 set address name={interface} source = dhcp')
        sb.run(c, shell=True)