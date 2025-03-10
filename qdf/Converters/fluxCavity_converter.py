import json
from xarray import Dataset
from qdf.Converters.Converter import QQAdapter
from numpy import array, arange, moveaxis

# ** name rule: ExpName_dataConverter(), ExpName is the name you registered in formater.DSCoordNameRegister(). Example: FluxCavity_dataConverter(), etc.

class FluxCavity_dataConverter(QQAdapter):
    """ Use `self.transformExecutor()` and get the dataset by `self.ds` """
    def __init__(self, file_path:str):
        super().__init__()
        self.settings(file_path, self.__getMyName__())

    def QB_adapter(self):
        pass

    def QM_adapter(self)->Dataset:
        bias = array(self.ds.coords["flux"])
        freq_attr:dict = {}
        # coordinates edit
        self.DSmaker.assign_coords({"mixer":array(["I","Q"]),"bias":bias,"freq":array(self.ds.coords["frequency"]),"q_idx":array(list(self.ds.data_vars.keys()))})
        
        # data edit
        for q_ro in self.ds.data_vars:
            q = q_ro.split("_")[0]
            freq_attr[q] 
            freq_values = 2*bias.shape[0]*list(array(self.ds.coords["frequency"]))
            self.DSmaker.add_data({q:moveaxis(array(self.ds[q_ro]),1,-1)})
            

        # attributes edit
        added_attrs = {"execution_time":"H00M00S00", "dummy_coord":False, "idx_coord_tracks":json.dumps({})}
        self.DSmaker.add_attrs(added_attrs, self.ds.attrs)
    
        # get dataset
        return self.DSmaker.export_dataset()
    

if __name__ == "__main__":
    Cnvtr = FluxCavity_dataConverter(file_path="TestRawDataset/QM_rawdata/flux_dependent_cavity/Find_Flux_Period.nc")