import pandas as pd
import json
import copy
import heapq
import math

from priority import *

with open("output/graph.json", "r") as f:
    graph = json.load(f)
    nodes = pd.json_normalize(graph, record_path="nodes")
    nodes = nodes["id"].to_list()
    edges = pd.json_normalize(graph, record_path="edges")
    edges['weight'] = edges['label'].apply(lambda x: link_priority[x])


# Please control the number of core nodes.
with open("output/core.json") as f:
    core = json.load(f)

# Treat as undirected graph
# Since the related IP and Cert violate the tree structure
# The whole graph should be treated as a graph

# MDDA (Multiple Destination Dijkstra's Algorithm) with Limited Depth
# Termination Condition: All targets are reached.

# Another UCS.
# https://www.aaai.org/ocs/index.php/SOCS/SOCS11/paper/viewFile/4017/4357
# It seems UCS and Dijkstra are same.

# Four Layer Limit
DEPTH_LIMIT = 4

# Get the adjecent nodes (neighbors)
# without considering the direction.
def adj(v):
    children = edges[edges["source"]==v][["id","target","weight"]].rename({"target":"neighbor"})
    parents = edges[edges["target"]==v][["id","source","weight"]].rename({"source":"neighbor"})
    neighbors = pd.concat([children, parents])
    return neighbors

# The User will select one core node to start with.
def path(source):
    targets = copy.deepcopy(core)
    targets = set(targets)
    targets.remove(source)
    
    # The explored node will not be expanded.
    explored = set()

    # EdgeTo dict
    edgeTo = {node: {"id": -1, "prev": ""} for node in nodes}

    # Priority Queue
    pq = [[0, source]]

    # Garantee that the graph is connected.
    while len(pq) > 0:

        minp = heapq.heappop(pq)
        mindist = minp[0]
        minnode = minp[1]

        neighbors = adj(minnode)

        for _, x in neighbors.iterrows():
            x["neighbor"]


path('Domain_64858fd6f643a9e2c4440686a3032ba8acc7dcea774c0f0a6d093fa66b39a0b8')