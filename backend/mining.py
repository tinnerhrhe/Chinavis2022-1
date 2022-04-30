from priority import *
import pandas as pd
import json

node = pd.read_csv('data/Node.csv')

link = pd.read_csv('data/Link.csv')

# depth limited search
def dls(node_str, limit):
    # terminate dls
    if limit == 0:
        return {}

    children = link[link['source']==node_str]
    subgraph = {}

    # filter
    if len(children['relation'].unique()) == 1 and len(children) > 100:
        children = children.head(2)
    
    # dls
    for rowindex, x in children.iterrows():
        cur_link_target = x['target']
        cur_link_limit = link_limit[link_priority[x['relation']]]
        subgraph[cur_link_target] = dls(cur_link_target, limit - 1 if cur_link_limit > limit - 1 else cur_link_limit)
    return subgraph

graph = dls("Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9", 3)

with open('output/graph.json','w') as f:
    f.write(json.dumps(graph))