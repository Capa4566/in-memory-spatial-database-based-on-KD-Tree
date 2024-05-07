import pandas as pd
from geopy.distance import geodesic
import time
import matplotlib.pyplot as plt

# Define a function to build the index
def IndexBuilding(file_path):
    data = pd.read_csv(file_path)
    points = list(zip(data['wgs_lat'], data['wgs_lng'], data['name'], data['type_code']))
    kdtree = KDTree(points)
    return kdtree

# Define a function for nearest neighbor query
def NNQuery(query_point, type_code_prefix, index):
    return index.query_nearest_neighbor(query_point, type_code_prefix)

# Define a function to evaluate query time for different data sizes
def EvaluateQueryTime(data_sizes):
    query_times = []
    for size in data_sizes:
        # Generate test datasets
        data = pd.read_csv('Assignment2-2012_BIT_POI.csv')  
        points = list(zip(data['wgs_lat'], data['wgs_lng'], data['name'], data['type_code']))
        data_subset = points[:size]

        # Build the index
        kdtree = KDTree(data_subset)

        # Perform the nearest neighbor query
        query_point = (39.958, 116.311)
        type_code_prefix = "1603"
        start_time = time.time()
        nearest_neighbor, dist = NNQuery(query_point, type_code_prefix, kdtree)
        query_time = time.time() - start_time

        query_times.append(query_time)
    return query_times

# Define data sizes for evaluation
data_sizes = [100, 500, 1000, 3000, 5000, 7000, 10000]

# Evaluate query time for different data sizes
query_times_kd_tree = EvaluateQueryTime(data_sizes)

# Plot the results for KD-Tree
plt.figure(figsize=(10, 6))
plt.plot(data_sizes, query_times_kd_tree, marker='o', label='KD-Tree')

# Define a function for the nearest neighbor query using scan
def NNScan(query_point, type_code_prefix_2, data):
    start_time = time.time()
    min_dist = float('inf')
    nearest_point = None

    for index, row in data.iterrows():
        type_code = str(row['type_code'])
        if type_code.startswith(str(type_code_prefix_2)):
            dist = geodesic((row['wgs_lat'], row['wgs_lng']), (query_point[1], query_point[0])).meters
            if dist < min_dist:
                min_dist = dist
                nearest_point = (index, row['name'], row['type_code'])

    end_time = time.time()
    query_time = end_time - start_time
    return query_time

# Generate test datasets
datasets = {}
for size in data_sizes:
    data = pd.read_csv('Assignment2-2012_BIT_POI.csv')  
    datasets[size] = data.head(size)

# Run queries for each dataset and record query times
query_point = [116.311, 39.958]  # BIT central building
type_code_prefix_2 = 1603
query_times_scan = {}
for size, data in datasets.items():
    query_times_scan[size] = NNScan(query_point, type_code_prefix_2, data)

# Plot the results for Scan
plt.plot(query_times_scan.keys(), query_times_scan.values(), marker='o', label='Scan')

# Finalize the plot
plt.xlabel('Data Size')
plt.ylabel('Query Time (seconds)')
plt.title('Query Time vs. Data Size')
plt.legend()
plt.grid(True)
plt.show()