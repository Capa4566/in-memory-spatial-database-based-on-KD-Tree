import time
import matplotlib.pyplot as plt

# Define a nearest neighbor query function with time recording
def NNQuery(query_point, type_code_prefix, index):
    start_time = time.time()
    nearest_neighbor, dist = index.query_nearest_neighbor(query_point, type_code_prefix)
    end_time = time.time()
    query_time = end_time - start_time
    return nearest_neighbor, dist, query_time

# Run 20 queries and record the time
query_times_2 = []
for query_num in range(1, 21):
    nearest_neighbor, dist, query_time = NNQuery(query_point, type_code_prefix, index)
    query_times_2.append(query_time)

# Calculate the average index building time
average_query_times = sum(query_times_2) / len(query_times_2)

# Plot the query time results
plt.figure(figsize=(10, 6))
plt.plot(range(1, 21), query_times_2, marker='o')
plt.axhline(y=average_query_times, color='r', linestyle='--', label='Average Time')
plt.text(1, average_query_times, f'Average Time: {average_query_times:.5f} s', color='r', va='bottom')
plt.xticks(range(1, 21, 1))
plt.xlabel('Query Number')
plt.ylabel('Query Time (s)')
plt.title('KD-Tree Nearest Neighbour Query Time Evaluation')
plt.legend()
plt.grid(True)
plt.show()