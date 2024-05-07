import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def RangeScan(query_range, type_code_prefix_1, file_path):
    wgs_lng_min, wgs_lat_min, wgs_lng_max, wgs_lat_max = query_range
    data = pd.read_csv(file_path)
    points_within_range = data[(data['wgs_lng'] >= wgs_lng_min) & 
                                (data['wgs_lng'] <= wgs_lng_max) & 
                                (data['wgs_lat'] >= wgs_lat_min) & 
                                (data['wgs_lat'] <= wgs_lat_max) & 
                                (data['type_code'].astype(str).str.startswith(type_code_prefix_1))]
    return points_within_range

def IndexBuilding(file_path):
    data = pd.read_csv('Assignment2-2012_BIT_POI.csv')
    return data

def range_query(index, query_point, radius_km):
    wgs_lng, wgs_lat = query_point
    data = index
    points_within_radius = data[((data['wgs_lng'] - wgs_lng)**2 + (data['wgs_lat'] - wgs_lat)**2)**0.5 <= radius_km]
    return points_within_radius

# Define the query range and type code prefix
query_range = [116.310, 39.955, 116.33, 39.97]
type_code_prefix_1 = '5'

# Create different sizes of test datasets
data_sizes = [100, 500, 1000, 3000, 5000, 7000, 10000]
query_times_range_query = []
query_times_ranges_scan = []

for size in data_sizes:
    # Create a test dataset
    test_data = pd.DataFrame({
        'name': ['Point{}'.format(i) for i in range(size)],
        'type_code': np.random.randint(1, 2000, size=size),
        'wgs_lat': np.random.uniform(39.9, 40.0, size=size),
        'wgs_lng': np.random.uniform(116.3, 116.4, size=size)
    })
    test_data.to_csv('test_data_{}.csv'.format(size), index=False)
    
    # Build the index
    index = IndexBuilding('test_data_{}.csv'.format(size))

    # Perform range query
    query_point = [116.310, 39.955]
    radius_km = 0.05
    start_time = time.time()
    result_indices = range_query(index, query_point, radius_km)
    range_query_time = time.time() - start_time

    query_times_range_query.append((size, range_query_time))

    # Run the query and calculate the query time
    start_time = time.time()
    RangeScan(query_range, type_code_prefix_1, 'test_data_{}.csv'.format(size))
    end_time = time.time()
    query_times_ranges_scan.append((size, end_time - start_time))

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(*zip(*query_times_range_query), marker='o', label='K-D Tree Spatial Index')
plt.plot(*zip(*query_times_ranges_scan), marker='o', label='Brute-Force')

plt.xlabel('Data Size')
plt.ylabel('Query Time (s)')
plt.title('Range Query Time With And Without K-D Tree Spatial Index When The Data Size Varies')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()