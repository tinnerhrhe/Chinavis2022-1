import math
from priority import *
import pandas as pd
import heapq
import json

# run cleaning.py first for filtered data.
# from cleaning import *
# and use Nodefil.csv and Linkfil.csv
# it is better used in P2.

# use cleaned data
node = pd.read_csv("data/Node.csv")
link = pd.read_csv("data/Link.csv")

print("Load Data Complete.")

default_style = {}
core_style = {"fill": "blue"}

core_limit = 6
filter_limit = 20
filter_threshold = 100

# If it is core asset
def coreasset(neighbor):
    if len(neighbor) == 0:
        return False
    rel_cnt = neighbor.groupby(["relation"]).count()
    rel_pop = rel_cnt["target"].max() / len(neighbor)
    rel_top = rel_cnt["target"].idxmax()
    if rel_pop > 0.5 and link_priority[rel_top] == 4:
        return False
    if "r_dns_a" in rel_cnt.index.values and rel_cnt["target"]["r_dns_a"] > 2:
        return False
    if len(neighbor) <= core_limit:  # A small amount of neighbors should not be regarded as core asset.
        return False
    return True


# Filter the same nodes into a smaller number.
# For stability concern, we use head() instead of sample()
# group_filtered = log_{filter_threshold}^len(x)
def filter(neighbor):
    return neighbor.groupby(["relation"]).apply(
        lambda x: x.head(int(filter_limit * math.log(len(x), filter_threshold)))
        if len(x) > filter_threshold
        else x
    )


# Find key in the priority queue.
def findkey(pq, key):
    for i in range(len(pq)):
        if pq[i][1] == key:
            return i
    return -1


# Uniform Cost Search
# Will search for the closest distance near the target node.
def ucs(node_str, node_limit, edge_limit):
    # Store the data for Ant G6
    graphdata = {"nodes": [], "edges": []}

    # Store the core nodes and critical paths
    # TODO: implement critical paths (approximation)
    coredata = {"nodes": [], "paths": []}

    # Store the stat
    statdata = {"nodes": {}, "edges": {}}

    def addnode(node_type):
        if node_type not in statdata["nodes"].keys():
            statdata["nodes"][node_type] = 1
        else:
            statdata["nodes"][node_type] += 1

    def addedge(edge_type):
        if edge_type not in statdata["edges"].keys():
            statdata["edges"][edge_type] = 1
        else:
            statdata["edges"][edge_type] += 1

    # Sort the queue insertion by the link priority
    q = []
    # This will pop the smallest element.
    # The priority will only be defined by the priority of the edge.
    # initialize the priority = 2 -> 4 limit as initial and pop out remains 3
    heapq.heappush(q, [1, node_str])
    # Explored
    explored = set()
    # Core node count
    corecnt = 0

    while len(q) > 0:
        cnt = len(q)
        for _ in range(cnt):
            # Get the current priority
            closest_link_priority = q[0][0]
            closest_node = heapq.heappop(q)
            closest_node = closest_node[1]  # get the string
            label = closest_node.rsplit("_")[0]

            # Get the children of the node
            children = link[link["source"] == closest_node]

            # for IP and Cert, they are the leaves in the filtered graph.
            # And the relation is also at priority 1,
            # so an inverse push should be applies as well.
            if label == "IP" or label == "Cert":
                father = link[link["target"] == closest_node]
                neighbor = pd.merge(children, father, "outer")
            else:
                neighbor = children

            print(len(neighbor), end="")

            style = default_style
            is_core = coreasset(neighbor)
            if is_core:
                corecnt += 1
                label += "_" + str(corecnt)
                style = core_style

            # Set the node as explored,
            # only consider the centrality of the target node
            # instead of the interaction between nodes.
            if closest_node not in explored:
                # cut off
                if node_limit == 0:
                    break
                node_limit -= 1
                # the label of the node
                addnode(label)
                explored.add(closest_node)
                graphdata["nodes"].append(
                    {"id": closest_node, "label": label, "style": style}
                )
                if is_core:
                    coredata["nodes"].append(closest_node)

            # filter
            if len(neighbor) > filter_threshold:
                neighbor = filter(neighbor)
                print("(%d)" % len(neighbor), end="")
            print(" ", end="")

            # decrease the priority
            next_link_priority = closest_link_priority + 1
            if next_link_priority not in link_limit.keys():
                break

            # push the layer
            for lid, x in neighbor.iterrows():
                cur_link_source = x["source"]
                cur_link_target = x["target"]
                cur_link_relation = x["relation"]
                cur_tail = (
                    cur_link_source
                    if cur_link_target == closest_node
                    else cur_link_target
                )

                qidx = findkey(q, cur_tail)

                cur_link_priority = link_priority[x["relation"]]  # ground truth

                flag = False

                if cur_tail not in explored and qidx == -1:
                    if next_link_priority > cur_link_priority:
                        cur_link_priority = next_link_priority  # limited search
                    heapq.heappush(q, [cur_link_priority, cur_tail])
                    flag = True
                elif qidx > -1 and cur_link_priority < q[qidx][0]:  # comp with ground truth
                    q[qidx][0] = cur_link_priority
                    heapq.heapify(q)
                    flag = True

                if flag:
                    graphdata["edges"].append(
                        {
                            "id": str(lid),
                            "source": cur_link_source,
                            "target": cur_link_target,
                            "label": cur_link_relation,
                        }
                    )
                    addedge(cur_link_relation)
                    edge_limit -= 1
                    if edge_limit == 0:
                        break

            if edge_limit == 0:
                break

        if node_limit == 0:
            break
        if edge_limit == 0:
            break

    return graphdata, coredata, statdata


graph, core, stat = ucs(
    "IP_7e730b193c2496fc908086e8c44fc2dbbf7766e599fabde86a4bcb6afdaad66e",
    net_limit["small"]["node"],
    net_limit["small"]["edge"],
)

print("Data Mining Complete.")

with open("output/graph.json", "w") as f:
    f.write(json.dumps(graph))

print("Data Write Complete.")

print("Core cnt: %d" % len(core["nodes"]))
print(core["nodes"])

nodecnt = sum([stat["nodes"][t] for t in stat["nodes"].keys()])
edgecnt = sum([stat["edges"][t] for t in stat["edges"].keys()])
print("Node cnt: %d" % nodecnt)
print("Edge cnt: %d" % edgecnt)
print(stat)
