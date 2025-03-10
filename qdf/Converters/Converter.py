""" Transfrom the raw nc data measured by QM into Qblox form. And it's reversible which means: qm -> qblox -> qm is okay. """
""" Warning: Once you use it, the old nc will be modified and saved with the qblox format. It won't save a new nc for you. """
import os, json
from abc import ABC, abstractmethod
from xarray import open_dataset, Dataset, open_dataarray

from qdf.Formalizer import DatasetCompiler

class QQAdapter(ABC):
    """ QM, Qblox dataset bidirectional transformer. """
    def __init__( self ):
        self.__checkConverterName__()
        self.ds_is_general:bool = False
        self.DSmaker:DatasetCompiler = None
        self.__file_path:str = None
        self.__new_dataset:Dataset = None
        self.__old_dataset:Dataset = None
        self.__meas_method:str = "average"
        self.__data_type:str = "nc"
        self.__data_from:str = "qblox" # qblox | qm 
        self.__new_dataset_path:str = ""
    
    @property
    def file_path( self ):
        return self.__file_path
    @property
    def nds_path( self ):
        return self.__new_dataset_path
    @property
    def nds( self ):
        return self.__new_dataset
    @property
    def ods( self ):
        return self.__old_dataset
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
                        self.__old_dataset = open_dataarray(self.__file_path)
                        print("dataarray")
                        self.__data_from = self.__old_dataset.attrs["system"].lower()
                        self.__meas_method = self.__old_dataset.attrs["method"].lower()
                    except:
                        try:
                            self.__old_dataset = open_dataset(self.__file_path)
                            print("dataset")
                            self.__data_from = self.__old_dataset.attrs["system"].lower()
                            self.__meas_method = self.__old_dataset.attrs["method"].lower()
                        except:
                            raise TypeError("The given nc file is not a Dataset or DataArray so i cannot read it ...")
                case _:
                    raise ImportError(f"Data type = {self.__data_type} can't be handled so far.")
        elif isinstance(filepath_or_dataset, Dataset):
            self.__old_dataset = filepath_or_dataset
        else:
            raise TypeError("Arg 'filepath_or_dataset' must be a str or Dataset !")

        
        if "GeneralFormat" in self.__old_dataset.attrs:
            if self.__old_dataset.attrs["GeneralFormat"]:
                print("The given dataset is already a general format.")
                self.ds_is_general = True


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
    def transformExecutor(self, storing_path:str=None, print_only:bool=False):
        """ 
            If `print_only=True`, only show the new dataset on the terminal.\n
            While `print_only=False`, if `storing_path` was given, save the new dataset to this given path. Otherwise, overwrite the new dataset at the same path.
            * Notice: If you gave a dataset while you are using `settings()`, `storing_path` here must be given.
        """
        if not self.ds_is_general:
            match self.__data_from:
                case "qm":
                    self.__new_dataset = self.QM_adapter()
                case "qblox":
                    self.__new_dataset = self.QB_adapter()
            
            if print_only:
                print(self.__new_dataset)
                self.__old_dataset.close()
            else:
                self.__old_dataset.close()
                # 3. overwrite the file with new dataset  
                
                if storing_path is None:
                    if self.__file_path is None:
                        raise ValueError("Arg 'storing_path' must be given ! We don't know where to save it.")
                    else:
                        self.__new_dataset.to_netcdf(self.__file_path)
                        self.__new_dataset_path = self.__file_path
                else:
                    self.__new_dataset.to_netcdf(storing_path)
                    self.__new_dataset_path = storing_path

        else:
            print(self.__old_dataset)
            self.__new_dataset_path = self.__file_path


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
    d = open_dataarray("TestRawDataset/QM_rawdata/flux_dependent_cavity/AVG/Find_Flux_Period_new.nc")
    print(d.values)