from utilities import cwt
import os
import numpy as np

#directory where DAS data is located 
DAS_data_directory = "./DAS_data/05"

#dir where transforms will be saved 
out_dir = "CWT_4Min/09"
file_list = os.listdir(DAS_data_directory)
sorted_list = sorted(file_list)

#sub sample 50hz data to 2hz data  
def sub_sample(data):
    data =np.reshape(data, (data.shape[0], 25, -1))
    return np.mean(data, axis=1)

#load one file to check n_channels and n_samples
sample_data = np.load(sorted_list[0])

#parameters for cwt
dt =0.5
dj =0.5
w0 =8
minSpaceFrq = 0.002
maxSpaceFrq = 0.12
n_features = 30
n_samples = sample_data.shape[1]

n_channels = sample_data.shape[0]
samples_per_second = 2
samples_per_sub_sample = 1
space_log = np.logspace(np.log10(minSpaceFrq), np.log10(maxSpaceFrq), n_features)
time_scales= cwt.get_scales(dt, dj, w0, n_samples)


for file in sorted_list:
    data = np.load(DAS_data_directory + '/' + file)
    #take a 4 minute window 
    data = data[:, :12000]
    #subsample to half a second 
    data = sub_sample(data)
    
    sub_sample_data = False


    transform = cwt.transform_window(data, n_channels, samples_per_second, samples_per_sub_sample, space_log, time_scales, subsampling=sub_sample_data)

    filename = file.split(".")[0]
    np.save(out_dir + "/" + "cwt_" + filename, transform)