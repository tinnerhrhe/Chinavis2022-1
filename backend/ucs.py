from queue import PriorityQueue
from priority import *
from cleaning import *
import pandas as pd
import heapq
import json

# use cleaned data
node = nodefil
link = linkfil

default_style = {}
core_style = {"fill": "blue"}

filter_limit = 20

# If it is core asset
def coreasset(children):
    if len(children) == 0:
        return False
    rel_cnt = children.groupby(["relation"]).count()
    rel_pop = rel_cnt["target"].max() / len(children)
    rel_top = rel_cnt["target"].idxmax()
    if rel_pop > 0.5 and link_priority[rel_top] == 4:
        return False
    if "r_dns_a" in rel_cnt.index.values and rel_cnt["target"]["r_dns_a"] > 2:
        return False
    return True


# Uniform Cost Search
# Will search for the closest distance near the target node.
def ucs(node_str, node_limit):

    # Store the data for Ant G6
    graphdata = {"nodes": [], "edges": []}

    # Sort the queue insertion by the link priority
    q = []
    # This will pop the smallest element.
    # The priority will only be defined by the priority of the edge.
    # initialize the priority = 2 -> 3 limit
    heapq.heappush(q, (2, node_str))
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
            node_limit -= 1
            if node_limit == 0:
                break

            # Get the children of the node
            children = link[link["source"] == node_str]
            children = children[["relation", "target"]]

            label = node_str.rsplit("_")[0]
            style = default_style
            if coreasset(children):
                corecnt += 1
                label += "_" + str(corecnt)
                style = core_style

            # Set the node as explored,
            # only consider the centrality of the target node
            # instead of the interaction between nodes.
            if closest_node in explored:
                explored.add(closest_node)
                graphdata["nodes"].append(
                    {"id": closest_node, "label": label, "style": style}
                )

            # filter
            if len(children['relation'].unique()) == 1 and len(children) > 100:
                children = children.head(filter_limit)

            # decrease the priority
            next_link_priority = closest_link_priority + 1
            if next_link_priority not in link_limit.keys():
                break

            # push the layer
            for _, x in children.iterrows():
                cur_link_target = x['target']
                if cur_link_target not in explored:
                    cur_link_priority = link_priority[x['relation']]
                    if cur_link_priority > next_link_priority:
                        next_link_priority = cur_link_priority
                    heapq.heappush(q, (next_link_priority, cur_link_target))
                    graphdata["edges"].append({"source": closest_node, "target": cur_link_target})
        
        if node_limit == 0:
            break

    return graphdata


graph = ucs(
    "Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9",
    net_limit["small"]["node"],
)

with open('output/graph.json','w') as f:
    f.write(json.dumps(graph))

