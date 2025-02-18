class MockTrx:
    """
    Simulación de la clase Trx para pruebas sin un puerto físico.
    """
    def __init__(self, port):
        print(f"[MockTrx] Simulación iniciada en el puerto: {port}")

    def communication(self, value):
        print(f"[MockTrx] Simulando comunicación con valor: {value}")
        if value == "1":  # Simular respuesta para temperatura
            return b'25.5\r\n'
        elif value == "2":  # Simular respuesta para humedad
            return b'60.0\r\n'
        elif value == "3":  # Simular respuesta para presión
            return b'1013.25\r\n'
        elif value == "4":  # Simular respuesta para todo
            return b'25.5,60.0\r\n'
        else:
            raise Exception("[MockTrx] Comando no válido.")

    def close_port(self):
        print("[MockTrx] Simulación de cerrar puerto.")
        return False  # Simular que el puerto se cerró correctamente
