from ucs import *
import json
import copy
import shutil
import os

# Cache Data for displaying

outputdir = 'output'
if os.path.islink(outputdir):
    outputdir = os.readlink(outputdir)

def main_run(source, limitation, ord):
    print("----------------------------")
    print("Searching Order %d on %s" % (ord, source))

    cachedir = outputdir + '/' + str(ord)
    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)

    # Refresh Threshold every run
    refreshcorethres()

    search = searchUCS(Graph(node, link), limitation)

    search.search_run(source)

    print("Search Complete.")

    subgraph = copy.deepcopy(search.subgraph)
    with open(cachedir + "/graph.json", "w") as f:
        outputgraph = {
            "nodes": toRecords(subgraph.nodes),
            "edges": toRecords(subgraph.edges),
        }
        f.write(json.dumps(outputgraph))

    corenodes = copy.deepcopy(search.corenodes)
    with open(cachedir + "/core.json", "w") as f:
        f.write(json.dumps(corenodes))

    print("Core cnt: %d" % len(corenodes))

    stat = search.statdata
    nodecnt = sum([stat["nodes"][t] for t in stat["nodes"].keys()])
    edgecnt = sum([stat["edges"][t] for t in stat["edges"].keys()])
    print("Node cnt: %d" % nodecnt)
    print("Edge cnt: %d" % edgecnt)
    with open(cachedir + "/stat.json", "w") as f:
        f.write(json.dumps(stat))

    print("Path Searching...")

    # for corenode in corenodes:
    #     pathtracing = pathUCS(Graph(subgraph.getNodes(), subgraph.getEdges()))
    #     pathtracing.path_run(corenode, corenodes)

    #     with open(cachedir + "/path-" + corenode + ".json", "w") as f:
    #         f.write(json.dumps(pathtracing.targetPaths))

    #     with open(cachedir + "/visitedPaths-" + corenode + ".json", "w") as f:
    #         f.write(json.dumps(list(pathtracing.visitedEdges)))

    # print("Path Search Complete.")

    print("Coregraph Searching ...")

    subgraph = copy.deepcopy(search.subgraph)
    corenodes = copy.deepcopy(search.corenodes)

    coresearching = subUCS(Graph(subgraph.getNodes(), subgraph.getEdges()))
    coresearching.sub_run(corenodes)

    with open(cachedir + "/coregraph.json", "w") as f:
        outputgraph = {
            "nodes": toRecords(coresearching.subgraph.nodes),
            "edges": toRecords(coresearching.subgraph.edges),
        }
        f.write(json.dumps(outputgraph))
    
    print("Coregraph Search Complete.")

    print("Coregraph with neighbors Searching ...")

    subgraph = copy.deepcopy(search.subgraph)

    coreneighsearching = subUCS(Graph(subgraph.getNodes(), subgraph.getEdges()), True)
    coreneighsearching.sub_run(corenodes)

    with open(cachedir + "/subgraph.json", "w") as f:
        outputgraph = {
            "nodes": toRecords(coreneighsearching.subgraph.nodes),
            "edges": toRecords(coreneighsearching.subgraph.edges),
        }
        f.write(json.dumps(outputgraph))

    print("Coregraph with neighbors Search Complete.")

# Clear the output directory
if os.path.isdir(outputdir):
    shutil.rmtree(outputdir)
os.mkdir(outputdir)
with open(outputdir + "/.gitkeep", "w") as f:
    pass

# Problem 1
for i in range(len(evidence)):
    main_run(evidence[i][0], evidence[i][1], i)

# Problem 2
# Top node in the remaining nodes.
# In case some nodes failed to mine,
# Make auxiliary solutions for that.
for i in range(5, 8):
    main_run(getTopNode(), 'large', i)

for i in range(8, 11):
    main_run(getTopNode(), 'medium', i)

for i in range(11, 14):
    main_run(getTopNode(), 'small', i)