import json
from xarray import Dataset
from qdf.Converters import QQAdapter
from numpy import array, expand_dims

# ** name rule: ExpName_dataConverter(), ExpName is the name you registered in formater.DSCoordNameRegister(). Example: FluxCavity_dataConverter(), etc.

class SpinEchoT2_dataConverter(QQAdapter):
    """ Use `self.transformExecutor()` and get the dataset by `self.ds` """
    def __init__(self, file_path_or_dataset:str|Dataset):
        super().__init__(file_path_or_dataset, self.__getMyName__())

    def QB_adapter(self):
        time_attr:dict = {}
        spin_num_attr:dict = {}
        data = []
        q_idx = []
        match self.meas_method:
            case "average":
                # data edit
                for q in self.ods.data_vars:
                    if "_" not in q:
                        q_idx.append(q)
                        data.append(list(self.ods[q].values))
                        time_attr[q] = list(self.ods[f"{q}_x"].values[0][0])
                        spin_num_attr[q] = float(self.ods[q].attrs["spin_num"])
                        
                
                # coordinates edit
                self.DSmaker.assign_coords({"mixer":array(["I","Q"]),"repeat":array(self.ods.coords["repeat"]),"time":array(self.ods.coords["idx"]),"q_idx":array(q_idx)})
                
                # data edit
                self.DSmaker.add_data({"voltage":array(data)})

            case "shot":
                # data edit
                for q in self.ods.data_vars:
                    if "_" not in q:
                        q_idx.append(q)
                        data.append(list(self.ods[q].values))
                        time_attr[q] = list(self.ods[f"{q}_x"].values[0][0][0][0])
                        spin_num_attr[q] = float(self.ods[q].attrs["spin_num"])
                
                # coordinates edit
                self.DSmaker.assign_coords({"mixer":self.ods.coords["mixer"].values,"prepared_state":self.ods.coords["prepared_state"].values,"repeat":self.ods.coords["repeat"].values,"index":self.ods.coords["index"].values,"time":self.ods.coords["time_idx"].values,"q_idx":array(q_idx)})

                # data edit
                self.DSmaker.add_data({"voltage":array(data)})

            case "state":
                pass


        # attributes edit
        added_attrs = {"time":json.dumps(time_attr), "GeneralFormat":1, "spin_num":json.dumps(spin_num_attr)}
        self.DSmaker.add_attrs(added_attrs, self.ods.attrs)

        # get dataset
        return self.DSmaker.export_dataset()
    

    def QM_adapter(self)->Dataset:
        time_attr:dict = {}
        spin_num_attr:dict = {}
        from datetime import datetime
        match self.meas_method:
            case "average":

                # ["q_idx", "mixer", "repeat", "time"]
                # coordinates edit
                self.DSmaker.assign_coords({"mixer":array(["I","Q"]),"repeat":array([0]),"time":array(self.ods.coords["time"]),"q_idx":array(self.ods.coords["q_idx"])})
            
                # data edit
                self.DSmaker.add_data({"voltage":expand_dims(self.ods.values,2)})

                # attributes edit
                for idx, q_ro in enumerate(array(self.ods.coords["q_idx"])):
                    time_attr[q_ro] = array(self.ods.coords["time"].values*1e-9).tolist() 
                    spin_num_attr[q_ro] = 1.0

                    
        added_attrs = {"execution_time":datetime.strptime(self.ods.attrs["start_time"], "%Y%m%d_%H%M%S").strftime("H%HM%MS%S"), "time":json.dumps(time_attr), "GeneralFormat":1, "end_time":datetime.strptime(self.ods.attrs["end_time"], "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S"), "spin_num":json.dumps(spin_num_attr)}
        self.DSmaker.add_attrs(added_attrs, self.ods.attrs, reverse_conflict_priority=True)
        
        # get dataset
        return self.DSmaker.export_dataset()
    

if __name__ == "__main__":
    # # QM 
    # # average
    # path = "TestRawDataset/QM_rawdata/SpinEchoT2/AVG/SpinEchoT2_stat_new.nc"
    # # Qblox
    # # average
    path = "TestRawDataset/Qblox_rawdata/SpinEcho/AVG/SpinEcho_20250225234448_new.nc"
    # # Shot
    # path = "TestRawDataset/Qblox_rawdata/SpinEcho/Shot/SpinEcho_20250220143313_new.nc"
    
    Cnvtr = SpinEchoT2_dataConverter(file_path_or_dataset=path)
    Cnvtr.transformExecutor(print_only=True)
    print(Cnvtr.nds_path)

