from ucs import *
import json
import copy

# Cache Data for displaying

for i in range(len(evidence)):
    source = evidence[i][0]
    limitation = evidence[i][1]
    cachedir = 'output/' + str(i)
    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)

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

    for corenode in corenodes:
        pathtracing = pathUCS(Graph(subgraph.getNodes(), subgraph.getEdges()))
        pathtracing.path_run(corenode, corenodes)

        with open(cachedir + "/path-" + corenode + ".json", "w") as f:
            f.write(json.dumps(pathtracing.targetPaths))

        with open(cachedir + "/visitedPaths-" + corenode + ".json", "w") as f:
            f.write(json.dumps(list(pathtracing.visitedEdges)))

    print("Path Search Complete.")

    print("Coregraph Searching ...")

    subgraph = copy.deepcopy(search.subgraph)

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