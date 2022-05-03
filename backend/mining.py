from priority import *
import pandas as pd
import json

node = pd.read_csv('data/Node.csv')

link = pd.read_csv('data/Link.csv')

# If it is core asset
def coreasset(children):
    if len(children) == 0:
        return False
    rel_cnt = children.groupby(['relation']).count()
    rel_pop = rel_cnt['target'].max() / len(children)
    rel_top = rel_cnt['target'].idxmax()
    if rel_pop > 0.5 and link_priority[rel_top] == 4:
        return False
    if 'r_dns_a' in rel_cnt.index.values and rel_cnt['target']['r_dns_a'] > 2:
        return False
    return True

# depth limited search
def dls(node_str, limit):
    # terminate dls
    if limit == 0:
        return {}

    children = link[link['source']==node_str]
    children = children[['relation','target']]
    subgraph = {}

    # filter
    if len(children['relation'].unique()) == 1 and len(children) > 100:
        children = children.head(100)

    if coreasset(children):
        pass

    # dls
    for rowindex, x in children.iterrows():
        cur_link_target = x['target']
        cur_link_limit = link_limit[link_priority[x['relation']]]
        subgraph[cur_link_target] = dls(cur_link_target, limit - 1 if cur_link_limit > limit - 1 else cur_link_limit)
    return subgraph

graph = dls("Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9", 3)

with open('output/graph.json','w') as f:
    f.write(json.dumps(graph))