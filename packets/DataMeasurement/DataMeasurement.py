from packets.DataMeasurement.Trx import Trx
from packets.DataMeasurement.MockTrx import MockTrx
import time

class DataMeasurement:

    def __init__(self, port=None):
        if port is None:
            self.trx = MockTrx(port)
        else:
            self.trx = Trx(port)
        self.last_temp = 0
        self.last_hum = 0

    def get_temperature(self):
        comm = "1" 
        # time.sleep(0.25)
        data_recieved = self.trx.communication(comm)
        temp = data_recieved[0]
        return temp
        
    def get_humidity(self):
        comm = "2" 
        # time.sleep(0.25)
        data_recieved = self.trx.communication(comm)
        hum = data_recieved[0]
        return hum
    
    def get_pressure(self):
        comm = "3" 
        # time.sleep(0.25)
        data_recieved = self.trx.communication(comm)
        press = data_recieved[0]
        return press
    
    def get_all(self):
        comm = "4"

        for i in range(3):
            time.sleep(0.25) # 0.25
            try:
                data_recieved = self.trx.communication(comm)
                temp = data_recieved[0]
                hum = data_recieved[1]
                break
            except:
                if i == 2:
                    temp = self.last_temp
                    hum = self.last_hum
                    return temp, hum
    
        self.last_hum = hum
        self.last_temp = temp
        return temp, hum
        
    def close(self):
        self.trx.close_port()

