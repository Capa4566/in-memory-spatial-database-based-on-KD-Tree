import pandas as pd
import numpy as np
from tabulate import tabulate

class KDTree:
    def __init__(self, points):
        # Initialize the KDTree with the given points
        self.points = points
        self.root = self.build_kd_tree(points)

    def build_kd_tree(self, points, depth=0):
        # Recursively build the KDTree
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

    def query_nearest_neighbor(self, query_point, type_code_prefix):
        # Find the nearest neighbor to the query_point with the given type code prefix
        best_point, best_dist = self._query_nearest_neighbor(self.root, query_point, 0, None, float('inf'), type_code_prefix)
        return best_point, best_dist

    def _query_nearest_neighbor(self, node, query_point, depth, best_point, best_dist, type_code_prefix):
        # Helper function to recursively find the nearest neighbor
        if node is None:
            return best_point, best_dist

        k = len(query_point)
        axis = depth % k

        next_branch = None
        opposite_branch = None

        if query_point[axis] < node['point'][axis]:
            next_branch = node['left']
            opposite_branch = node['right']
        else:
            next_branch = node['right']
            opposite_branch = node['left']

        best_point, best_dist = self._query_nearest_neighbor(next_branch, query_point, depth + 1, best_point, best_dist, type_code_prefix)

        if best_dist is None or self.haversine(query_point, (node['point'][0], node['point'][1])) < best_dist:
            if str(node['point'][3]).startswith(type_code_prefix):
                best_point = node['point']
                best_dist = self.haversine(query_point, (node['point'][0], node['point'][1]))

        if best_dist is None or abs(query_point[axis] - node['point'][axis]) < best_dist:
            best_point, best_dist = self._query_nearest_neighbor(opposite_branch, query_point, depth + 1, best_point, best_dist, type_code_prefix)

        return best_point, best_dist

    def haversine(self, point1, point2):
        # Calculate the great circle distance between two points
        lon1, lat1 = point1
        lon2, lat2 = point2
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

# Define a function to build the index
def IndexBuilding(file_path):
    data = pd.read_csv(file_path)
    points = list(zip(data['wgs_lat'], data['wgs_lng'], data['name'], data['type_code']))
    kdtree = KDTree(points)
    return kdtree

# Build the index using the IndexBuilding function
start_time = time.time()
index = IndexBuilding('Assignment2-2012_BIT_POI.csv')
index_build_time = time.time() - start_time

# Define a function for nearest neighbor query
def NNQuery(query_point, type_code_prefix, index):
    return index.query_nearest_neighbor(query_point, type_code_prefix)

# Perform the nearest neighbor query
query_point = (39.958, 116.311)
type_code_prefix = "1603"
start_time = time.time()
nearest_neighbor, dist = NNQuery(query_point, type_code_prefix, index)
nearest_query_time = time.time() - start_time
nearest_neighbor_data = [(nearest_neighbor[:2][0], nearest_neighbor[:2][1], nearest_neighbor[2], nearest_neighbor[3], dist)]
df2 = pd.DataFrame(nearest_neighbor_data, columns=['Latitude', 'Longitude', 'Name', 'Type Code', 'Distance (km)'])
df2

time_consumed2 = {"Index construction Time (s)": [index_build_time1], "Query Time (s)": [nearest_query_time]}
df0 = pd.DataFrame(time_consumed2)
df0