import pandas as pd
from geopy.distance import geodesic

def RangeScan(query_range, type_code_prefix_1, file_path):
    query_point, radius = query_range
    data = pd.read_csv(file_path)
    points_within_radius = []
    count = 0  # Counter for points within radius

    for index, row in data.iterrows():
        dist = geodesic((row['wgs_lat'], row['wgs_lng']), (query_point[1], query_point[0])).meters
        type_code = str(row['type_code'])  # Convert type_code to string for comparison
        if dist <= radius and type_code.startswith(str(type_code_prefix_1)):
            points_within_radius.append((index, row['name'], row['type_code']))
            count += 1

    return points_within_radius, count

def NNScan(query_point, type_code_prefix_2, file_path):
    data = pd.read_csv(file_path)
    min_dist = float('inf')
    nearest_point = None

    for index, row in data.iterrows():
        type_code = str(row['type_code'])  # Convert type_code to string for comparison
        if type_code.startswith(str(type_code_prefix_2)):
            dist = geodesic((row['wgs_lat'], row['wgs_lng']), (query_point[1], query_point[0])).meters
            if dist < min_dist:
                min_dist = dist
                nearest_point = (index, row['name'], row['type_code'])

    return [nearest_point] if nearest_point is not None else []

# Example usage
query_range = ([116.310, 39.955], 500)  # BIT south door and 500 meters radius
type_code_prefix_1 = 5
type_code_prefix_2 = 1603
file_path = 'Assignment2-2012_BIT_POI.csv'

# Range query
res_range, count = RangeScan(query_range, type_code_prefix_1, file_path)
range_query_data = [(index, name, type_code) for index, name, type_code in res_range]
df_range_query = pd.DataFrame(range_query_data, columns=['Index', 'Name', 'Type Code'])
df_range_query

# Nearest neighbor query
query_point = [116.311, 39.958]  # BIT central building
res_nn = NNScan(query_point, type_code_prefix_2, file_path)
nn_query_data = [(index, name, type_code) for index, name, type_code in res_nn]
df_nn_query = pd.DataFrame(nn_query_data, columns=['Index', 'Name', 'Type Code'])
df_nn_query