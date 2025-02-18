from packets.MassFlowDevice.MassFlowDevice import MassFlowDevice
from packets.MassFlowDevice.MassFlowDeviceFake import MassFlowDeviceFake

import warnings
from termcolor import colored

class MassFlowController:
    """
    Class to control multiple mass flow controllers
    """

    def __init__(self, massflow_ids): # List of massflow ids to connect to
        # self.mfcs = [MassFlowDeviceFake(id) for id in massflow_ids]
        self.mfcs = [MassFlowDevice(id) for id in massflow_ids] 
        
    def set_flow(self, id, flow, max_flow=None):

        if max_flow is not None:
            if flow > max_flow:
                print(f"\n{colored('[WARN]', 'yellow')} MFC{id}: Flow is higher than the maximum flow. Setting maximum flow instead.\n")
                flow = max_flow

        for mfc in self.mfcs:
            if int(mfc.id) == int(id):
                return mfc.set_flow(flow)

    def set_no_error_flow(self, id, flow):
        for mfc in self.mfcs:
            if mfc.id == id:
                return mfc.set_flow(flow)

    def clear_flow(self, id):
        for mfc in self.mfcs:
            if mfc.id == id:
                return mfc.set_flow(0)
            
    def clear_all_flows(self):
        for mfc in self.mfcs:
            mfc.set_flow(0)

    def get_flow(self, id): 
        for mfc in self.mfcs:
            if mfc.id == id:
                return mfc.get_flow()

    def get_all_flows(self):
        return {mfc.id: mfc.get_flow() for mfc in self.mfcs}

    def get_ids(self):
        return [mfc.id for mfc in self.mfcs]
    
    def get_sum_flow(self):
        return sum([mfc.get_flow() for mfc in self.mfcs])
    
    
