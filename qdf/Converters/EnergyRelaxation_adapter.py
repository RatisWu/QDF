import json
from xarray import Dataset
from qdf.Converters.Converter import QQAdapter
from numpy import array, expand_dims

# ** name rule: ExpName_dataConverter(), ExpName is the name you registered in formater.DSCoordNameRegister(). Example: FluxCavity_dataConverter(), etc.

class EnergeRelaxation_dataConverter(QQAdapter):
    """ Use `self.transformExecutor()` and get the dataset by `self.ds` """
    def __init__(self, file_path_or_dataset:str|Dataset):
        super().__init__()
        self.settings(file_path_or_dataset, self.__getMyName__())

    def QB_adapter(self):
        time_attr:dict = {}
        if self.meas_method == "average":
            data = []
            q_idx = []
            # data edit
            for q in self.ods.data_vars:
                if "_" not in q:
                    q_idx.append(q)
                    data.append(list(self.ods[q].values))
                    time_attr[q] = list(self.ods[f"{q}_x"].values[0][0])
                    
            
            # coordinates edit
            self.DSmaker.assign_coords({"mixer":array(["I","Q"]),"repeat":array(self.ods.coords["repeat"]),"time":array(self.ods.coords["idx"]),"q_idx":array(q_idx)})
            
            # data edit
            self.DSmaker.add_data({"voltage":array(data)})

            # attributes edit
            added_attrs = {"execution_time":"H00M00S00", "time":json.dumps(time_attr), "GeneralFormat":1}
            self.DSmaker.add_attrs(added_attrs, self.ods.attrs)
    
        # get dataset
        return self.DSmaker.export_dataset()
    

    def QM_adapter(self)->Dataset:
        time_attr:dict = {}
        from datetime import datetime
        if self.meas_method == "average":

            # ["q_idx", "mixer", "repeat", "time"]
            # coordinates edit
            self.DSmaker.assign_coords({"mixer":array(["I","Q"]),"repeat":array([0]),"time":array(self.ods.coords["time"]),"q_idx":array(self.ods.coords["q_idx"])})
        
            # data edit
            self.DSmaker.add_data({"voltage":expand_dims(self.ods.values,2)})

            # attributes edit
            for idx, q_ro in enumerate(array(self.ods.coords["q_idx"])):
                time_attr[q_ro] = array(self.ods.coords["time"].values*1e-9).tolist() 
            added_attrs = {"execution_time":"H00M00S00", "time":json.dumps(time_attr), "GeneralFormat":1, "end_time":datetime.strptime(self.ods.attrs["end_time"], "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")}
            self.DSmaker.add_attrs(added_attrs, self.ods.attrs, reverse_conflict_priority=True)
    
        # get dataset
        return self.DSmaker.export_dataset()
    

if __name__ == "__main__":
    # QM
    path = "TestRawDataset/QM_rawdata/T1/AVG/T1_new.nc"
    # Qblox
    # path = "TestRawDataset/Qblox_rawdata/T1/AVG/T1_20250220134804_new.nc"
    
    Cnvtr = EnergeRelaxation_dataConverter(file_path_or_dataset=path)
    Cnvtr.transformExecutor(print_only=True)

