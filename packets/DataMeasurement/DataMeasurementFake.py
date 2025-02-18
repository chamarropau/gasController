
class DataMeasurementFake:
    def __init__(self, port):
        pass

    def get_temperature(self):
        return '99'
        
    def get_humidity(self):
        return '45'
    
    def get_pressure(self):
        return '1000'
    
    def get_all(self):
        return '99', '45' 

    def close(self):
        pass

