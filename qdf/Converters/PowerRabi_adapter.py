import json
from xarray import Dataset
from qdf.Converters import QQAdapter
from numpy import array, expand_dims

# ** name rule: ExpName_dataConverter(), ExpName is the name you registered in formater.DSCoordNameRegister(). Example: FluxCavity_dataConverter(), etc.

class PowerRabi_dataConverter(QQAdapter):
    """ Use `self.transformExecutor()` and get the dataset by `self.ds` """
    def __init__(self, file_path_or_dataset:str|Dataset):
        super().__init__(file_path_or_dataset, self.__getMyName__())

    def QB_adapter(self):
        var_attr = {}
        data = []
        q_idx = []
        match self.meas_method:
            case "average":
                # coordinates edit
                if self.ods.attrs["rabi_type"].lower() in ["detune_power"]: 
                    
                    # data edit
                    for q in self.ods.data_vars:
                        if "_" not in q:
                            q_idx.append(q)
                            var_attr[q] = (self.ods.data_vars[f"{q}_freq"].values[0][0]).tolist()
                            data.append(self.ods.data_vars[q].values.tolist())
                    self.DSmaker.assign_coords({"q_idx":array(q_idx), "mixer":array(["I","Q"]), "freq":array(self.ods.coords["freq_idx"]), "pi_amp":array(self.ods.coords["pi_amp"])})
                    added_attrs = {"frequency":json.dumps(var_attr)}
                else:
                    # data edit
                    for q in self.ods.data_vars:
                        if "_" not in q:
                            q_idx.append(q)
                            var_attr[q] = (self.ods.data_vars[f"{q}_variable"].values[0]).tolist()
                            data.append(expand_dims(self.ods.data_vars[q].values,1).tolist())
                    
                    self.DSmaker.assign_coords({"q_idx":array(q_idx), "mixer":array(["I","Q"]), "freq":array([0]), "pi_amp":array(self.ods.coords["var_idx"])})
                    added_attrs = {"pi_amp":json.dumps(var_attr)}
                
            case "shot":
                # ["q_idx", "mixer", "freq", "prepared_state", "index", "pi_amp"]
                # coordinates edit
                if self.ods.attrs["rabi_type"].lower() in ["detune_power"]: 
                    
                    # data edit
                    for q in self.ods.data_vars:
                        if "_" not in q:
                            q_idx.append(q)
                            var_attr[q] = (self.ods.data_vars[f"{q}_freq"].values[0][0][0][0]).tolist()
                            data.append(self.ods.data_vars[q].values.tolist())
                    self.DSmaker.assign_coords({"q_idx":array(q_idx), "mixer":array(["I","Q"]), "freq":array(self.ods.coords["freq_idx"]), "prepared_state":array(self.ods.coords["prepared_state"]), "index":array(self.ods.coords["index"]), "pi_amp":array(self.ods.coords["pi_amp"])})
                    added_attrs = {"frequency":json.dumps(var_attr)}
                else:
                    # data edit
                    for q in self.ods.data_vars:
                        if "_" not in q:
                            q_idx.append(q)
                            var_attr[q] = (self.ods.data_vars[f"{q}_variable"].values[0][0][0]).tolist()
                            data.append(expand_dims(self.ods.data_vars[q].values,1).tolist())
                    
                    self.DSmaker.assign_coords({"q_idx":array(q_idx), "mixer":array(["I","Q"]), "freq":array([0]), "prepared_state":array(self.ods.coords["prepared_state"]), "index":array(self.ods.coords["index"]), "pi_amp":array(self.ods.coords["var_idx"])})
                    added_attrs = {"pi_amp":json.dumps(var_attr)}

        
        self.DSmaker.add_data({"voltage":array(data)})
        # attributes edit
        added_attrs.update({"GeneralFormat":1})
        self.DSmaker.add_attrs(added_attrs, self.ods.attrs)                           
    
        # get dataset
        return self.DSmaker.export_dataset()
        

    def QM_adapter(self)->Dataset:
        from datetime import datetime
        freq_attr:dict = {}
        # ["q_idx", "mixer", "freq", "pi_amp"]
        match self.meas_method:
            case "average":
                # coordinates edit
                self.DSmaker.assign_coords({"q_idx":array(self.ods.coords["q_idx"]), "mixer":array(["I","Q"]), "freq":array(self.ods.coords["frequency"]), "pi_amp":array(self.ods.coords["amplitude"])})
            
                # data edit
                for idx, q_ro in enumerate(array(self.ods.coords["q_idx"])):
                    if self.ods.coords["q_idx"].shape[0] > 1:
                        freq_attr[q_ro] = (self.ods.attrs["ref_xy_LO"][idx] + self.ods.attrs["ref_xy_IF"][idx] + array(array(self.ods.coords["frequency"]))).tolist() 
                    else:
                        freq_attr[q_ro] = (self.ods.attrs["ref_xy_LO"] + self.ods.attrs["ref_xy_IF"] + array(array(self.ods.coords["frequency"]))).tolist() 

                self.DSmaker.add_data({"voltage":self.ods.values})


        # attributes edit
        added_attrs = {"execution_time":datetime.strptime(self.ods.attrs["start_time"], "%Y%m%d_%H%M%S").strftime("H%HM%MS%S"), "frequency":json.dumps(freq_attr), "GeneralFormat":1}
        self.DSmaker.add_attrs(added_attrs, self.ods.attrs)                           
    
        # get dataset
        return self.DSmaker.export_dataset()
    

if __name__ == "__main__":

    # # QM
    # # average
    # path = "TestRawDataset/QM_rawdata/detuned_power_rabi/AVG/detuned_power_rabi_new.nc"
    # # Shot
    

    # # Qblox
    # # average
    # path = "TestRawDataset/Qblox_rawdata/PowerRabi/AVG/PowerRabi_20250219174424_new.nc"
    # # shot
    path = "TestRawDataset/Qblox_rawdata/PowerRabi/Shot/PowerRabi_20250219174541_new.nc"
    
    
    Cnvtr = PowerRabi_dataConverter(file_path_or_dataset=path)
    Cnvtr.transformExecutor(storing_path="TestRawDataset/Qblox_rawdata/PowerRabi/Shot/PowerRabi_generalFormat.nc")
    print(Cnvtr.nds_path)
    