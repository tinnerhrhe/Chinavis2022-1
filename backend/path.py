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
    edges['priority'] = edges['label'].apply(lambda x: link_priority[x])


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
    children = edges[edges["source"]==v][["id","target","priority"]].rename(columns={"target":"neighbor"})
    parents = edges[edges["target"]==v][["id","source","priority"]].rename(columns={"source":"neighbor"})
    neighbors = pd.concat([children, parents])
    return neighbors

# Find key in the priority queue.
def findkey(pq, key):
    for i in range(len(pq)):
        if pq[i][1] == key:
            return i
    return -1

# The User will select one core node to start with.
def path(source):
    targets = copy.deepcopy(core)
    targets = set(targets)
    targets.remove(source)

    # Target Path
    targetPaths = {}
    # Visited Path
    visitedPaths = set()
    
    # The explored node will not be expanded.
    explored = set()

    # EdgeTo dict
    edgeTo = {node: {"id": -1, "prev": ""} for node in nodes}

    # Priority Queue
    q = []
    # Push source into queue, in 4 jump range.
    heapq.heappush(q, [0, source])

    # Garantee that the graph is connected.
    while len(q) > 0:

        minp = heapq.heappop(q)
        minprio = minp[0]
        minnode = minp[1]

        neighbors = adj(minnode)


        if minnode in targets:
            targets.remove(minnode)
            tpath = []
            tptr = minnode

            while tptr != source:
                tedge = edgeTo[tptr]
                tpath.append(tedge["id"])
                tptr = tedge["prev"]
            tpath.reverse()

            if len(tpath) > DEPTH_LIMIT:
                print("%s: Not critical." % minnode)
            else:
                for edgeid in tpath:
                    visitedPaths.add(edgeid)
                targetPaths[minnode] = tpath
                print("%s: %s" % (minnode, str(tpath)))
        
        if len(targets) == 0:
            print("Search Completed.")
            break

        explored.add(minnode)
        nextprio = minprio + 1
        if nextprio not in link_limit.keys():
            continue

        for _, x in neighbors.iterrows():
            curid = x["id"]
            curnode = x["neighbor"]
            curprio = x["priority"]
            qidx = findkey(q, curnode)

            if curnode not in explored and qidx == -1:
                if nextprio > curprio:
                    curprio = nextprio
                heapq.heappush(q, [curprio, curnode])
                edgeTo[curnode] = {"id": curid, "prev": minnode}
            elif qidx > -1 and curprio < q[qidx][0]:
                q[qidx][0] = curprio
                heapq.heapify(q)
                edgeTo[curnode] = {"id": curid, "prev": minnode}
        
    return targetPaths, list(visitedPaths)


targetPaths, visitedPaths = path('Domain_64858fd6f643a9e2c4440686a3032ba8acc7dcea774c0f0a6d093fa66b39a0b8')

with open("output/paths.json","w") as f:
    f.write(json.dumps(targetPaths))
with open("output/visitedpaths.json","w") as f:
    f.write(json.dumps(visitedPaths))

print("Path File Generated.")