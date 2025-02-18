import serial

class Trx():

    '''
    class Trx:
        this class make a search of available ports to be used. You have to 
        select to which port you want to connect.
        Modify the speed as you want in configure_serial, changing the baudrate. 
    '''

    def __init__(self, port):
        self.serialPort = self.__initialization(port)
        
    
    # GET PORTS was deleted bc we started to use serial module to get the ports
    # GET MANUFACTURER was deleted bc was not used

    def __configure_serial(self, port_of_connection):
        '''
        ENG From the string parameter "port_of_connection", try to open the port. if success, it 
        returns true, meaning that the port is open, on the contrary, it returns false.
        '''
        serialPort = serial.Serial(port=port_of_connection, baudrate=115200,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    timeout = 1)
        if serialPort is None:
            serialPort.open()

        serialbool = serialPort.isOpen()
        return serialPort, serialbool
    
        
    def close_port(self):
        '''
        CAT Reb un objecte port pyserial, intenta tancar-lo
        i retorna el boolean True si es queda obert, False si esta tancat
        
        ENG Receives an pyserial object,and try to close it. 
        it returns true if the port is closed. On te contrary it returns false
        '''
        self.serialPort.close()
        serialbool = self.serialPort.isOpen()
        return serialbool
    

    def communication(self, value):
        '''
        Parameters
        ----------
        value : TYPE
            DESCRIPTION.
        '''
        
        val = str(value)
        val = val.encode('utf-8') # codifica el value a enviar pel port
        self.serialPort.write(val)
        response = self.serialPort.readline()
                     
        if ((response == b'') or (response == b'\r\n')):
            raise Exception("No response from device.")
            
        return response
    

    def __initialization(self, port):        
        
        serialPort, serialbool = self.__configure_serial(port.upper())
        
        if serialbool == False:
            raise Exception("Cannot open specified port.")
        
        return serialPort