import json
import pickle
import random

import networkx as nx

with open('ma.json') as json_file:
    data = json.load(json_file)

G = nx.adjacency_graph(data)
print(len(G.nodes()))
unconn_nodes = [i for i in range(len(G.nodes())) if G.in_degree[i] == 0 or G.out_degree[i] == 0]
for i in unconn_nodes:
    G.remove_node(i)
print(len(G.nodes()))

NUM_VERT = 50

random.seed(2137)
idxs = random.sample(G.nodes(), NUM_VERT)
coords = [G.nodes()[i] for i in idxs]

dist_mx = [[float('inf') for _ in range(NUM_VERT)] for _ in range(NUM_VERT)]
vert_mx = [[[] for _ in range(NUM_VERT)] for _ in range(NUM_VERT)]

for i, idx1 in enumerate(idxs):
    for j, idx2 in enumerate(idxs):
        print(i, j)
        length, path_vertices = nx.single_source_dijkstra(G, idx1, idx2, weight='length')
        dist_mx[i][j] = length
        vert_mx[i][j] = path_vertices

with open('dist_mx', 'wb') as f:
    pickle.dump(dist_mx, f)

with open('vert_mx', 'wb') as f:
    pickle.dump(vert_mx, f)