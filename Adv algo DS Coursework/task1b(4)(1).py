import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
import matplotlib.pyplot as plt
import numpy as np

file_path = 'London Underground data.xlsx'  #file path
df = pd.read_excel(file_path, header=None)

# create a mapping between station names and integers
stations = set(df[1].unique()) | set(df[2].unique())
station_to_index = {station: index for index, station in enumerate(stations)}
index_to_station = {index: station for station, index in station_to_index.items()}

# create the graph using the given AdjacencyListGraph class
num_stations = len(stations)
tube_graph = AdjacencyListGraph(card_V=num_stations, directed=True, weighted=True)

# populate the graph with edges from the valid rows in the XLSX file
for _, row in df.iterrows():
    source = station_to_index[row[1]]
    destination = station_to_index[row[2]]
    duration = row[3]

    # check if the edge already exists
    if not tube_graph.has_edge(source, destination):
        # Insert edges into the graph
        tube_graph.insert_edge(source, destination, duration)

# get source and destination stations from the user
start_station_name = input("Enter the source station: ").strip()
end_station_name = input("Enter the destination station: ").strip()

# convert station names to indices
start_station_index = station_to_index.get(start_station_name)
end_station_index = station_to_index.get(end_station_name)

# check if the provided station names are valid
if start_station_index is None or end_station_index is None:
    print("Invalid start or end station.")
else:
    # find the shortest path and duration from start station using Dijkstra's algorithm
    d, pi = dijkstra(tube_graph, start_station_index)

    # reconstruct the shortest path
    shortest_path_indices = []
    current_station_index = end_station_index
    while current_station_index is not None:
        shortest_path_indices.insert(0, current_station_index)
        current_station_index = pi[current_station_index]

    if shortest_path_indices:
        shortest_path_names = [index_to_station[index] for index in shortest_path_indices]
        total_duration = d[end_station_index]
        print(f"Shortest Path from {start_station_name} to {end_station_name}: {shortest_path_names}")
        print(f"Total Duration (minutes): {total_duration}")
        # calculate journey times between all station pairs
        journey_times = []
        for n in range(len(shortest_path_names)):
            source_index = shortest_path_indices[n]
            destination_index = shortest_path_indices[n - 1]
            if source_index != destination_index:
                if d[destination_index] is not None:
                    journey_times.append(d[destination_index])
        # filter out non-finite values from journey_times
        journey_times = [time for time in journey_times if np.isfinite(time)]
        # plot histogram of journey times
        plt.hist(journey_times, bins=20, color='blue', alpha=0.7)
        plt.xlabel('Journey Time (minutes)')
        plt.ylabel('Frequency')
        plt.title('Histogram of Journey Times between Station Pairs')
        plt.show()
    else:
        print(f"No valid path from {start_station_name} to {end_station_name}.")
