import os
os.environ['MKL_NUM_THREADS'] = "4"
os.environ["OMP_NUM_THREADS"] = "4" # export OMP_NUM_THREADS=4
os.environ["OPENBLAS_NUM_THREADS"] = "4" # export OPENBLAS_NUM_THREADS=4 
import numpy as np
import datetime as dt
import struct
import sys
import time
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering as AggloCluster
from utilities import clusters
import joblib
import torch 


from params_training import *




outfileList = []

ndays = 1
outfileListFile = []
files = []

transform_dir = ("Data/synthetic-DAS/train-syntheticDAS/CWT-edDAS")


files = os.listdir(transform_dir)
files.sort()
files=files[:10]


nfiles = len(files)
print(files[-1])
sample = torch.load(transform_dir + '/' + files[-1])
print(sample.shape)

n_features = sample.shape[2]
sps = 50
samplingRate = 50
secondsPerWindowOffset = sample.shape[1]
nChannels = sample.shape[0]
nSamples = secondsPerWindowOffset * int(sps / samplingRate)
nSamples = nSamples //2
print(nSamples)

trainingData = np.empty((nChannels, nSamples * nfiles, n_features), dtype=np.float64)
print(trainingData.shape)
print(nfiles)

for index, file in enumerate(files):
  file = transform_dir + '/' + file
  trainingData[:,(index * nSamples):((index + 1) * nSamples),:] = np.array(torch.load(file))[:,::2, :]
print("training data shape before reshape", trainingData.shape)
# Clustering
trainingData = np.reshape(trainingData, (nChannels * nSamples * nfiles, -1))
print(trainingData.shape)

dir = 'Data/synthetic-DAS/train-syntheticDAS/ClusteringResults'
stats_dict = {}
for i in range(2,10):
    # K-means
    kmeans = KMeans(init='k-means++', n_clusters=i, n_init=10)
    kmeans.fit(trainingData)
    
    data_labels = kmeans.labels_
    print(trainingData.shape)
    print(data_labels.shape)

    stats = clusters.evaluate_cluster(trainingData, data_labels)
    data_labels = np.reshape(data_labels, (nChannels, nSamples, -1))
    np.save(f'{dir}/cluster_labels_k={i}', data_labels)
    np.save(f'{dir}/cluster_centers_k={i}', kmeans.cluster_centers_)
    stats_dict[f'cluster{i}'] = stats
    print(f'stats for {i} are {stats}')
joblib.dump(stats_dict, f'{dir}/cluster_stats.pkl')