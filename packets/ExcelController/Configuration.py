class Configuration(): 
    def __init__(self, mfcs_flows): # mfcs_flows: {"MFC2": {"id" : id, "max_flow" : max_flow, "ppm" : ppm, "unit" : unit, "gas_type"} ... }
        self._mfcs_flows = mfcs_flows


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"\nCONFIGURATION: mfcs: {str(self._mfcs_flows)}"

    def get_mfc_id(self, mfc_name):
        return self._mfcs_flows[mfc_name]["id"]
    
    def get_mfc_max_flow(self, mfc_name):
        return self._mfcs_flows[mfc_name]["max_flow"]
    