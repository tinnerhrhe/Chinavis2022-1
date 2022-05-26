# 由于数据量较大（~688MB），
# 需要使用 pandas 数据工具加速查询。

import pandas as pd
import math
import os
import numpy as np

########## 加载数据 ##########

print("Loading Data...")

node = pd.read_csv("data/Node.csv")
link = pd.read_csv("data/Link.csv")
link["id"] = link.index

# 生成打分后的节点数据表
if os.path.isfile("data/scorednode.csv"):
    print("Use cached data/scorednode.csv")
    scorednode = pd.read_csv("data/scorednode.csv", index_col='id')
else:
    print("Generating data/scorednode.csv")
    scorednode = node.dropna()
    scorednode = scorednode.drop_duplicates('id', keep='first')
    scorednode = scorednode[(scorednode['industry'] != '[]') |
                    (scorednode['type'] != 'Domain')]
    scorednode = scorednode.reset_index() #index和npy对应
    score = np.load('score.npy')
    score = pd.DataFrame(score, columns=['score'])
    scorednode = pd.concat([node, score], axis=1)
    scorednode.set_index('id', inplace=True)
    scorednode.to_csv('data/scorednode.csv')

print("Load Data Complete.")

#############################

from meta import *

# 核心资产的邻居数目不得低于这个数值
CORE_LIMIT = 6
# 筛选同类型节点的底数
FILTER_BASE = 20
# 筛选阈值
FILTER_THRESHOLD = 50
# 核心节点打分应当为 5% 以内
CORETOP = 5
corescorethres = scorednode['score'].describe(percentiles=[(100 - CORETOP) / 100])[str(100 - CORETOP) + '%']
print("Threshold Score for Core node is %.2f" % corescorethres)

# 图：预期使用 pandas 存储
class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


class Subgraph(Graph):
    def __init__(self, nodecols, edgecols):
        super().__init__(
            pd.DataFrame(columns=nodecols),
            pd.DataFrame(columns=edgecols),
        )

    # DataFrame.append() is deprecated.

    def addNode(self, n):
        self.nodes = pd.concat([self.nodes, pd.DataFrame.from_records([n])])

    def addEdge(self, e):
        self.edges = pd.concat([self.edges, pd.DataFrame.from_records([e])])

    def getNodes(self):
        return self.nodes.rename(columns={"label": "type"})

    def getEdges(self):
        return self.edges.rename(columns={"label": "relation"})


class Node:
    def __init__(self, graph, node_id):
        self.node_id = node_id
        self.graph = graph
        self.label = self.getLabel(node_id)

    def getLabel(self, node_id):
        return node_id.rsplit("_")[0]

    def queryChildren(self):
        return self.graph.edges[self.graph.edges["source"] == self.node_id]

    def queryParents(self):
        return self.graph.edges[self.graph.edges["target"] == self.node_id]

    def queryNeighbors(self):
        return pd.concat([self.queryChildren(), self.queryParents()])


# Filter the same nodes into a smaller number.
# For stability concern, we use head() instead of sample()
# group_filtered = log_{filter_threshold}^len(x)
def filter(curnode, neighbors):
    # filter by scorednode for mining.
    neighbors = neighbors[neighbors['source'].isin(scorednode.index) & neighbors['target'].isin(scorednode.index)]
    if len(neighbors) == 0:
        return neighbors[['id', 'relation', 'source', 'target']]
    neighbors['neighbor'] = neighbors.apply(lambda x: x['source'] if x['target'] == curnode else x['target'], axis=1)
    neighbors['score'] = neighbors['neighbor'].apply(lambda x: scorednode['score'][x])
    neighbors = neighbors.sort_values(by='score', ascending=False)

    if len(neighbors) > FILTER_THRESHOLD:
        neighbors = neighbors.groupby(["relation"]).apply(
            lambda x: x.head(int(FILTER_BASE * math.log(len(x), FILTER_THRESHOLD)))
            if len(x) > FILTER_THRESHOLD
            else x
        )
        # dummy index drop
        if isinstance(neighbors.index[0], tuple): neighbors = neighbors.droplevel(0)
        return neighbors[['id', 'relation', 'source', 'target']]
    else:
        return neighbors[['id', 'relation', 'source', 'target']]


# 是否是核心资产
def coreasset(curnode, neighbors):
    if len(neighbors) == 0:
        return False
    rel_cnt = neighbors.groupby(["relation"]).count()
    rel_pop = rel_cnt["target"].max() / len(neighbors)
    rel_top = rel_cnt["target"].idxmax()
    if rel_pop > 0.5 and link_priority[rel_top] == 4:
        return False
    if "r_dns_a" in rel_cnt.index.values and rel_cnt["target"]["r_dns_a"] > 2:
        return False
    if len(neighbors) <= CORE_LIMIT:
        return False
    if scorednode['score'][curnode] < corescorethres:
        return False
    return True


def toRecords(neighbors):
    return neighbors.to_dict(orient="records")


#############################
