import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, print_undirected_edges
from dijkstra import dijkstra
import matplotlib.pyplot as plt
import math
# file handler
file_path = 'London Underground data.xlsx'  # file name and path
df = pd.read_excel(file_path, header=None)

# creating a mapping between station names and integers
stations = set(df[1].unique()) | set(df[2].unique())
station_to_index = {station: index for index, station in enumerate(stations)}
index_to_station = {index: station for station, index in station_to_index.items()}

# creating the graph using AdjacencyListGraph class from library code
num_stations = len(stations)
tube_graph = AdjacencyListGraph(card_V=num_stations, directed=False, weighted=True, multi_graph=True)
#EXCEL file shows single entry for both A-B and B-A travel. Therefore the graph is marked as undirected
# TFL rails is a multi graph which can be seen by the circle and the district lines which connect Monument and TowerHill

# populate the graph with edges from the valid rows in the XLSX file
for _, row in df.iterrows():
    if not isinstance(row[2], str):
        continue
    source = station_to_index[row[1]]  # source station index
    destination = station_to_index[row[2]]  # destination station index
    duration = row[3]  # 4th column is the duration
    line = row[0]
    # skip entry if there is no duration, source or destination station
    if not math.isnan(duration):
        # Insert edges into the graph
        tube_graph.insert_edge(source, destination, duration, line)

retained_graph = kruskal(tube_graph)
deleted_edges = []
for i in range(num_stations):
    deleted_edges.append(list())
print("Below are all the effected routes")
not_feasable = True
for u in range(1,num_stations):
        for edge in tube_graph.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                data = retained_graph.find_edge(u,v)
                if data is None:
                    not_feasable = False
                    #deleted_edges[u].append(v)
                    u_station = index_to_station[u]
                    v_station = index_to_station[v]
                    print(u_station,"--", v_station)
#print(deleted_edges)
if not_feasable:
    print("It is not feasible to delete any route as the connectivity will be lost otherwise.")

Total_distances = []
stops_list =[]
# Iterate through all station pairs
for start_idx in range(1,num_stations):
    # Find the shortest path and number of stops between station pairs
    d, pi = dijkstra(retained_graph, start_idx)
    for i in d:
        if not math.isnan(i) and not math.isinf(i):
            Total_distances.append(i)
    for end_idx in range(1,num_stations):
        if start_idx != end_idx:  # Avoid calculating stops for the same station
            # Reconstruct the shortest path
            stops = 0
            current_station_index = end_idx
            path = []
            while current_station_index is not None:
                stops += 1
                path.append(current_station_index)
                current_station_index = pi[current_station_index]
            start_station_name = index_to_station[start_idx]
            end_station_name = index_to_station[end_idx]
            #print(f"{start_station_name},{end_station_name}: {path}")
            # Append the number of stops to the stops_list
            stops_list.append(stops)
# Generate a histogram
plt.figure(figsize=(10, 6))
#print(type(Total_distances))
#print(Total_distances)
plt.hist(Total_distances, bins=max(stops_list)+1, edgecolor='black')
plt.xlabel('Minimum distance in minutes')
plt.ylabel('Number of Station Pairs')
plt.title('Distribution of minimum distance Made between Station Pairs')
plt.grid(True)
plt.show()
plt.figure(figsize=(10, 6))
plt.hist(stops_list, bins=max(stops_list)+1, edgecolor='black')
plt.xlabel('Minimum distance in Number of Stops')
plt.ylabel('Number of Station Pairs')
plt.title('Distribution of minimum stops Made between Station Pairs')
plt.grid(True)
plt.show()
