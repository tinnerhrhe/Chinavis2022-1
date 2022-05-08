from ucs import *
import json
import copy

search = searchUCS(Graph(node, link), net_limit["small"])

search.search_run("IP_7e730b193c2496fc908086e8c44fc2dbbf7766e599fabde86a4bcb6afdaad66e")

print("Search Complete.")

subgraph = copy.deepcopy(search.subgraph)
with open("output/graph.json", "w") as f:
    outputgraph = {
        "nodes": toRecords(subgraph.nodes),
        "edges": toRecords(subgraph.edges),
    }
    f.write(json.dumps(outputgraph))

corenodes = copy.deepcopy(search.corenodes)

print("Core cnt: %d" % len(corenodes))

stat = search.statdata
nodecnt = sum([stat["nodes"][t] for t in stat["nodes"].keys()])
edgecnt = sum([stat["edges"][t] for t in stat["edges"].keys()])
print("Node cnt: %d" % nodecnt)
print("Edge cnt: %d" % edgecnt)

pathtracing = pathUCS(Graph(subgraph.getNodes(), subgraph.getEdges()))
pathtracing.path_run(corenodes[1], corenodes)

