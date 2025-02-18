import serial.tools.list_ports

# Obtener todos los puertos seriales disponibles
ports = serial.tools.list_ports.comports()

for port in ports:
    print(f"Puerto: {port.device} - Descripción: {port.description} - Manuf: {port.manufacturer}")