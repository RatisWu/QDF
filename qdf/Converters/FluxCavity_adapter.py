import json
from xarray import Dataset
from qdf.Converters.Converter import QQAdapter
from numpy import array

# ** name rule: ExpName_dataConverter(), ExpName is the name you registered in formater.DSCoordNameRegister(). Example: FluxCavity_dataConverter(), etc.

class FluxCavity_dataConverter(QQAdapter):
    """ Use `self.transformExecutor()` and get the dataset by `self.ds` """
    def __init__(self, file_path_or_dataset:str|Dataset):
        super().__init__()
        self.settings(file_path_or_dataset, self.__getMyName__())

    def QB_adapter(self):
        pass

    def QM_adapter(self)->Dataset:
        freq_attr:dict = {}
        # coordinates edit
        self.DSmaker.assign_coords({"mixer":array(["I","Q"]),"bias":array(self.ods.coords["flux"]),"freq":array(self.ods.coords["frequency"]),"q_idx":array(self.ods.coords["q_idx"])})
    
        # data edit
        for idx, q_ro in enumerate(array(self.ods.coords["q_idx"])):
            freq_attr[q_ro] = (self.ods.attrs["ro_LO"][idx] + self.ods.attrs["ro_IF"][idx] + array(array(self.ods.coords["frequency"]))).tolist() 

        self.DSmaker.add_data({"voltage":self.ods.values})


        # attributes edit
        added_attrs = {"execution_time":"H00M00S00", "frequency":json.dumps(freq_attr), "GeneralFormat":1}
        self.DSmaker.add_attrs(added_attrs, self.ods.attrs)                           
    
        # get dataset
        return self.DSmaker.export_dataset()
    

if __name__ == "__main__":

    Cnvtr = FluxCavity_dataConverter(file_path_or_dataset="TestRawDataset/QM_rawdata/flux_dependent_cavity/AVG/Find_Flux_Period_new.nc")
    Cnvtr.transformExecutor(storing_path="TestRawDataset/QM_rawdata/flux_dependent_cavity/AVG/Find_Flux_Period_generalForm.nc")
    