import os
from xarray import open_dataarray, open_dataset


# raw_data_folder = "/Users/ratiswu/Documents/GitHub/QDF/TestRawDataset/Qblox_rawdata"

# nc_files = [os.path.join(raw_data_folder,name) for name in os.listdir(raw_data_folder) if (os.path.isfile(os.path.join(raw_data_folder,name)) and name.split(".")[-1] == "nc")]
# sub_folders = [os.path.join(raw_data_folder,name) for name in os.listdir(raw_data_folder) if os.path.isdir(os.path.join(raw_data_folder,name))]
# method_folders = []

# for sub_folder in sub_folders:
#     for name in os.listdir(sub_folder):
#         if os.path.isfile(os.path.join(sub_folder,name)) and name.split(".")[-1] == "nc":
#             nc_files.append(os.path.join(sub_folder,name))
#         elif os.path.isdir(os.path.join(sub_folder,name)):
#             method_folders.append(os.path.join(sub_folder,name))


# for mathod_folder in method_folders:
#     method = os.path.split(mathod_folder)[-1]
#     nc_files = [os.path.join(mathod_folder,name) for name in os.listdir(mathod_folder) if (os.path.isfile(os.path.join(mathod_folder,name)) and name.split(".")[-1] == "nc")]
#     for a_nc_file in nc_files:
#         ds = open_dataset(a_nc_file)
#         ds.attrs["system"] = os.path.split(raw_data_folder)[-1].split("_")[0]
    
#         if method.lower() == 'shot':
#             ds.attrs["method"] = "shot"
#         elif method.lower() == "avg":
#             ds.attrs["method"] = "average"
            
#         ds.to_netcdf(a_nc_file.split(".")[0]+"_new"+".nc")
#         ds.close() 

da = open_dataarray("TestRawDataset/QM_rawdata/flux_dependent_cavity/AVG/Find_Flux_Period.nc")
da.attrs["system"] = "QM"
da.attrs["method"] = "average"
da.to_netcdf("TestRawDataset/QM_rawdata/flux_dependent_cavity/AVG/Find_Flux_Period_new.nc")