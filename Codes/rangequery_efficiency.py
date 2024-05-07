import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Your KDTree implementation

# Define a range query function
def range_query(kdtree, query_point, radius_km):
    # Perform the range query
    indices = kdtree.query_ball_point(query_point, radius_km)
    # Get the indexes, names, and type codes of the points within the specified radius
    result_indices = []
    for idx in indices:
        point = kdtree.points[idx]
        name = data.iloc[idx]['name']
        type_code = str(data.iloc[idx]['type_code'])  # Convert type_code to string type
        if type_code.startswith('5'):
            result_indices.append((idx, name, type_code))
    return result_indices

# Build the index using the custom index-building function
index = IndexBuilding('Assignment2-2012_BIT_POI.csv')

# Perform 20 range queries
query_point = [116.310, 39.955]
radius_km = 0.5
query_times_1 = []
for _ in range(20):
    start_time = time.time()
    result_indices = range_query(index, query_point, radius_km)
    query_time = time.time() - start_time
    query_times_1.append(query_time)

# Calculate the average index building time
average_range_query_time = sum(query_times_1) / len(query_times_1)

# Plot the query times
plt.figure(figsize=(10, 6))
plt.plot(range(1, 21), query_times_1, marker='o')
plt.axhline(y=average_range_query_time, color='r', linestyle='--', label='Average Time')
plt.text(1, average_range_query_time, f'Average Time: {average_range_query_time:.5f} s', color='r', va='bottom')
plt.xticks(range(1, 21, 1))
plt.xlabel('Query Number')
plt.ylabel('Query Time (s)')
plt.title('Range Query Time Efficiency Evaluation')
plt.legend()
plt.grid(True)
plt.show()