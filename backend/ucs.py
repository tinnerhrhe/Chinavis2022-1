from sklearn import neighbors
from priority import *
import pandas as pd
import heapq
import json

# run cleaning.py first for filtered data.
# from cleaning import *

# use cleaned data
node = pd.read_csv('data/Node.csv')
link = pd.read_csv('data/Link.csv')

print("Load Data Complete.")

default_style = {}
core_style = {"fill": "blue"}

filter_limit = 10

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
def ucs(node_str, node_limit, edge_limit):

    # Store the data for Ant G6
    graphdata = {"nodes": [], "edges": []}

    # Sort the queue insertion by the link priority
    q = []
    # This will pop the smallest element.
    # The priority will only be defined by the priority of the edge.
    # initialize the priority = 2 -> 4 limit as initial
    heapq.heappush(q, (1, node_str))
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
            closest_node = closest_node[1] # get the string
            node_limit -= 1
            if node_limit == 0: break
            
            # the label of the node
            label = closest_node.rsplit("_")[0]

            # Get the children of the node
            children = link[link["source"] == closest_node]

            # for IP and Cert, they are the leaves in the filtered graph.
            # And the relation is also at priority 1,
            # so an inverse push should be applies as well.
            if label == 'IP' or label == 'Cert':
                father = link[link["target"] == closest_node]
                neighbor = pd.merge(children, father, 'outer')
            else:
                neighbor = children

            print(len(neighbor), end=" ")

            style = default_style
            if coreasset(neighbor):
                corecnt += 1
                label += "_" + str(corecnt)
                style = core_style

            # Set the node as explored,
            # only consider the centrality of the target node
            # instead of the interaction between nodes.
            if closest_node not in explored:
                explored.add(closest_node)
                graphdata["nodes"].append(
                    {"id": closest_node, "label": label, "style": style}
                )

            # filter
            if len(neighbor['relation'].unique()) == 1 and len(neighbor) > 100:
                neighbor = neighbor.head(filter_limit)

            # decrease the priority
            next_link_priority = closest_link_priority + 1
            if next_link_priority not in link_limit.keys(): break

            # push the layer
            for _, x in neighbor.iterrows():
                cur_link_source = x['source']
                cur_link_target = x['target']
                cur_tail = cur_link_source if cur_link_target == closest_node else cur_link_target
                if cur_tail not in explored:
                    cur_link_priority = link_priority[x['relation']]
                    if next_link_priority > cur_link_priority:
                        cur_link_priority = next_link_priority
                    heapq.heappush(q, (cur_link_priority, cur_tail))
                    graphdata["edges"].append({"source": cur_link_source, "target": cur_link_target})
                    edge_limit -= 1
                    if edge_limit == 0: break
            
            if edge_limit == 0: break
        
        if node_limit == 0: break
        if edge_limit == 0: break

    return graphdata


graph = ucs(
    "Domain_b10f98a9b53806ccd3a5ee45676c7c09366545c5b12aa96955cde3953e7ad058",
    net_limit["small"]["node"],
    net_limit["small"]["edge"]
)

print("Data Mining Complete.")

with open('output/graph.json','w') as f:
    f.write(json.dumps(graph))

print("Data Write Complete.")