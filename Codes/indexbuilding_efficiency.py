import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

class KDTree:
    def __init__(self, points):
        self.points = points
        self.root = self.build_kd_tree(points)

    def build_kd_tree(self, points, depth=0):
        if len(points) == 0:
            return None

        k = len(points[0])
        axis = depth % k
        points_sorted = sorted(points, key=lambda x: x[axis])

        median = len(points_sorted) // 2
        node = {
            'point': points_sorted[median],
            'left': self.build_kd_tree(points_sorted[:median], depth + 1),
            'right': self.build_kd_tree(points_sorted[median + 1:], depth + 1)
        }
        return node

# Create an empty KDTree object
kdtree = KDTree([])

# Define a function for building the index
def IndexBuilding(file_path):
    data = pd.read_csv(file_path)
    points = list(zip(data['wgs_lat'], data['wgs_lng'], data['name'], data['type_code']))
    return points

# Test the efficiency of index building
index_building_times = []
for _ in range(20):
    start_time = time.time()
    points = IndexBuilding('Assignment2-2012_BIT_POI.csv')
    kdtree = KDTree(points)  # Create KDTree object here
    end_time = time.time()
    index_building_times.append(end_time - start_time)

# Calculate the average index building time
average_index_building_time = sum(index_building_times) / len(index_building_times)

# Plot the efficiency evaluation result
plt.figure(figsize=(10, 6))
plt.plot(range(1, 21), index_building_times, marker='o')
plt.axhline(y=average_index_building_time, color='r', linestyle='--', label='Average Time')
plt.text(1, average_index_building_time, f'Average Time: {average_index_building_time:.5f} s', color='r', va='bottom')
plt.xticks(range(1, 21, 1))
plt.xlabel('Index Building Run')
plt.ylabel('Time (s)')
plt.title('Efficiency Evaluation of Index Building')
plt.legend()
plt.grid(True)
plt.show()