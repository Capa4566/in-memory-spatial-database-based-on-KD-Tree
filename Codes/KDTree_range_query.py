import pandas as pd
import numpy as np
from tabulate import tabulate
import time

class KDTree:
    def __init__(self, points):
        self.points = points
        self.tree = self.build_kd_tree(points)

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

    def query_ball_point(self, query_point, radius):
        indices = []
        self._query_ball_point(self.tree, query_point, radius, indices, depth=0)
        return indices

    def _query_ball_point(self, node, query_point, radius, indices, depth):
        if node is None:
            return
        
        k = len(query_point)
        axis = depth % k
        axis_dist = abs(query_point[axis] - node['point'][axis])

        if axis_dist <= radius:
            dist = self.haversine(query_point, node['point'])
            if dist <= radius:
                indices.append(self.points.index(node['point']))

        if query_point[axis] - radius < node['point'][axis]:
            self._query_ball_point(node['left'], query_point, radius, indices, depth + 1)
        if query_point[axis] + radius > node['point'][axis]:
            self._query_ball_point(node['right'], query_point, radius, indices, depth + 1)
    
    def haversine(self, point1, point2):
        lon1, lat1 = point1
        lon2, lat2 = point2
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

def IndexBuilding(file_path):
    # Read the dataset
    data = pd.read_csv(file_path)
    # Extract longitude and latitude information
    points = data[['wgs_lng', 'wgs_lat']].values.tolist()
    # Build the KD tree index
    kdtree = KDTree(points)
    return kdtree

# Modify the range query function
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
start_time = time.time()
index = IndexBuilding('Assignment2-2012_BIT_POI.csv')
index_build_time2 = time.time() - start_time

# Define a range query function
query_point = [116.310, 39.955]
radius_km = 0.5

# Perform the range query
start_time = time.time()
result_indices = range_query(index, query_point, radius_km)
range_query_time = time.time() - start_time

# Output result
df1 = pd.DataFrame(result_indices, columns=['Index', 'Name', 'Type Code'])
print(f"Number of points within {radius_km} kilometers of the query point: {len(df1)}")
df1

time_consumed1 = {"Index construction Time (s)": [index_build_time2], "Query Time (s)": [range_query_time]}
df11 = pd.DataFrame(time_consumed1)
df11