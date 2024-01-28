from collections import defaultdict
import matplotlib.pyplot as plt
import heapq
from dijkstra import dijkstra
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append((to_node, weight))
        self.edges[to_node].append((from_node, weight))

    def get_card_V(self):
        return len(self.nodes)

    def get_adj_list(self, nodes):
        return self.edges[nodes]

'''def dijkstra(graph, start,end):
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    total_time = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.edges[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                total_time += weight
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, total_time, distances[end]'''

'''def find_shortest_path(graph, start, end):
    distances = dijkstra(graph, start)
    shortest_path = []
    current_node = end

    while current_node != start:
        shortest_path.append(current_node)
        for neighbor, weight in graph.edges[current_node]:
            if distances[current_node] == distances[neighbor] + weight:
                current_node = neighbor
                break

    shortest_path.append(start)
    return list(reversed(shortest_path))'''

def create_graph(data):
    graph = Graph()
    for row in data:
        graph.add_node(row[0])
        graph.add_node(row[1])
        graph.add_edge(row[0], row[1], row[2])
    return graph

# Sample data
'''data = [
    ("Walthamstow Central",	"Blackhorse Road",	3),
    ("Blackhorse Road",	"Tottenham Hale"	,3),
    ("Tottenham Hale",	"Seven Sisters"	,2),
    ("Seven Sisters"	,"Finsbury Park"	,5),
    ("Finsbury Park"	,"Highbury & Islington"	,2),
    ("Highbury & Islington"	,"King's Cross St. Pancras",	3),
    ("King's Cross St. Pancras",	"Euston",	2),
    ("Euston"	,"Warren Street"	,2),
    ("Warren Street",	"Oxford Circus"	,2),
    ("Oxford Circus"	,"Green Park"	,2),
    ("Green Park"	,"Victoria"	,2),
    ("Victoria"	,"Pimlico",	2),
    ("Pimlico"	,"Vauxhall"	,2),
    ("Vauxhall"	,"Stockwell",	3),
    ("Stockwell",	"Brixton",	2)
    # ... (add all the data here)
]
'''
data = [
        ("first node", "second node",10),
        ("first node", "third node", 2),
        ("third node","fourth node", 1),
        ("fourth node","second node",2)]
# Create the graph
graph = create_graph(data)
#graph.nodes is a set, we need to change that set into a list inorder to use the index function

# Find the shortest path between two stations
start_station = "third node"#input("Please Enter your Starting station name: ")
end_station = "Second node"#input("Please Enter your end station name: ")
node_list = list(graph.nodes)
s = node_list.index(start_station)
print(s)
#s = graph.nodes.index(start_station)
'''shortest_path = find_shortest_path(graph, start_station, end_station)

print("Shortest Path from", start_station, "to", end_station, ":", shortest_path)'''
output = dijkstra(graph,s)
print( output[0])
print( output[1])

'''x = (24,25,23,27)
print(plt.hist(x,2))'''
