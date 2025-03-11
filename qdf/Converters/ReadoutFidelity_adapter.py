import json
from xarray import Dataset
from qdf.Converters import QQAdapter
from numpy import array, expand_dims, moveaxis

# ** name rule: ExpName_dataConverter(), ExpName is the name you registered in formater.DSCoordNameRegister(). Example: FluxCavity_dataConverter(), etc.

class ReadoutFidelity_dataConverter(QQAdapter):
    """ Use `self.transformExecutor()` and get the dataset by `self.ds` """
    def __init__(self, file_path_or_dataset:str|Dataset):
        super().__init__(file_path_or_dataset, self.__getMyName__())

    def QB_adapter(self):
        
        data = []
        q_idx = []
        match self.meas_method:
            case "shot":
                # data edit
                for q in self.ods.data_vars:
                    q_idx.append(q)
                    data.append(expand_dims(self.ods[q].values,0).tolist()) # expand dimension at the first dim (repeat), we be replaced in the future.
                       
                
                # coordinates edit
                self.DSmaker.assign_coords({"mixer":self.ods.coords["mixer"].values,"repeat":array([0]),"prepared_state":self.ods.coords["prepared_state"].values,"index":self.ods.coords["index"].values,"q_idx":array(q_idx)})

                # data edit
                self.DSmaker.add_data({"voltage":array(data)})

            case "state":
                pass


        # attributes edit
        added_attrs = {"GeneralFormat":1}
        self.DSmaker.add_attrs(added_attrs, self.ods.attrs)

        # get dataset
        return self.DSmaker.export_dataset()
    

    def QM_adapter(self)->Dataset:
        from datetime import datetime
        match self.meas_method:
            case "shot":

                # ["q_idx", "repeat", "mixer", "prepared_state", "index"]
                # coordinates edit
                self.DSmaker.assign_coords({"q_idx":array(self.ods.coords["q_idx"]), "repeat":array([0]), "mixer":array(self.ods.coords["mixer"]), "prepared_state":array(self.ods.coords["prepared_state"]), "index":array(self.ods.coords["index"])})
            
                # data edit
                data = moveaxis(self.ods.values,2,-1)
                self.DSmaker.add_data({"voltage":expand_dims(data,1)})

        # attributes edit 
        added_attrs = {"execution_time":datetime.strptime(self.ods.attrs["start_time"], "%Y%m%d_%H%M%S").strftime("H%HM%MS%S"), "GeneralFormat":1, "end_time":datetime.strptime(self.ods.attrs["end_time"], "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")}
        self.DSmaker.add_attrs(added_attrs, self.ods.attrs, reverse_conflict_priority=True)
    
        # get dataset
        return self.DSmaker.export_dataset()
    

if __name__ == "__main__":
    # # QM 
    # # shot
    # path = "TestRawDataset/QM_rawdata/readout_fidelity/Shot/readout_fidelity_new.nc"
    # # Qblox
    # # Shot
    path = "TestRawDataset/Qblox_rawdata/ReadoutFidelity/Shot/SingleShot_20250220135236_new.nc"
    
    Cnvtr = ReadoutFidelity_dataConverter(file_path_or_dataset=path)
    Cnvtr.transformExecutor(print_only=True)
    print(Cnvtr.nds_path)

