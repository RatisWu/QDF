""" Transfrom the raw nc data measured by QM into Qblox form. And it's reversible which means: qm -> qblox -> qm is okay. """
""" Warning: Once you use it, the old nc will be modified and saved with the qblox format. It won't save a new nc for you. """
import os, json
from abc import ABC, abstractmethod
from xarray import open_dataset, Dataset

from qdf.Formalizer import DatasetCompiler

class QQAdapter(ABC):
    """ QM, Qblox dataset bidirectional transformer. """
    def __init__( self ):
        self.__checkConverterName__()
        self.DSmaker:DatasetCompiler = None
        self.__file_path:str = None
        self.__dataset:Dataset = None
        self.__meas_method:str = "average"
        self.__data_type:str = "nc"
        self.__data_from:str = "qblox" # qblox | qm 
    
    @property
    def file_path( self ):
        return self.__file_path
    @property
    def ds( self ):
        return self.__dataset
    @property
    def data_type( self ):
        return self.__data_type
    @property
    def data_from( self ):
        return self.__data_from
    @property
    def meas_method( self ):
        return self.__meas_method

    """ prepare settings, built-in """
    def settings(self, filepath_or_dataset:str|Dataset, exp_name:str):
        """ Import:\n 1. raw data path or a dataset,\n  2. exp_name (`qcat.utility.formater.DSCoordNameRegister()` for more details.),\n 3. data_from in ['qblox', 'qm']   """
        if isinstance(filepath_or_dataset, str): 
            self.__file_path = filepath_or_dataset
            self.__data_type = os.path.split(filepath_or_dataset)[-1].split(".")[-1]

            match self.__data_type:
                case 'nc':
                    try:
                        self.__dataset = open_dataset(self.__file_path)
                    except:
                        try:
                            self.__dataset = open_dataarray(self.__file_path)
                        except:
                            raise TypeError("The given nc file is not a Dataset or DataArray so i cannot read it ...")
                case _:
                    raise ImportError(f"Data type = {self.__data_type} can't be handled so far.")
        elif isinstance(filepath_or_dataset, Dataset):
            self.__dataset = filepath_or_dataset
        else:
            raise TypeError("Arg 'filepath_or_dataset' must be a str or Dataset !")

        
        self.__data_from = self.__dataset.attrs["system"]
        self.__meas_method = self.__dataset.attrs["method"].lower()

        self.DSmaker = DatasetCompiler(exp_name,method=self.__meas_method)
            
               
    """ get exp name, built-in """
    def __getMyName__( self )->str:
        return self.__class__.__name__.split("_")[0]
    
    """ Check the name rules for dataConverter """
    def __checkConverterName__( self ):
        myName = self.__class__.__name__

        if "_" not in myName:
            raise NameError("Your name didn't follow the name rules. I can't see `_` in your name.")

        if myName.split("_")[-1] != "dataConverter":
            raise NameError("Your name didn't follow the name rules. It must be 'dataConverter' right after the '_', Ex. FluxCavity_dataConverter, etc. ")

       
    """ Executor function, built-in"""     
    def transformExecutor(self, storing_path:str=None):
        
        match self.__data_from:
            case "qm":
                self.__dataset = self.QM_adapter()
            case "qblox":
                self.__dataset = self.QB_adapter()

        # 3. overwrite the file with new dataset  
        if storing_path is not None or self.__file_path is None:
            if storing_path is None:
                raise ValueError("Arg 'storing_path' must be given !")
            else:
                self.__dataset.to_netcdf(storing_path)

        else:
            new_name = os.path.basename(self.__file_path).split(".")[0] + "_QMtoQblox_1" + f".{self.data_type}"
            self.__dataset.to_netcdf(os.path.join(os.path.split(self.__file_path)[0],new_name))


    """ Develop case by case """
    @abstractmethod
    def QM_adapter( self ):
        """ transform the dataset. """
        pass

    @abstractmethod
    def QB_adapter( self ):
        """ transform the dataset. """
        pass

             
if __name__ == "__main__":
    from xarray import open_dataarray

    d = open_dataarray("TestRawDataset/QM_rawdata/flux_dependent_cavity/Find_Flux_Period.nc")
    print(d)