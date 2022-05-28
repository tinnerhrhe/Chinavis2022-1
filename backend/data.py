# 由于数据量较大（~688MB），
# 需要使用 pandas 数据工具加速查询。

import copy
import pandas as pd
import math
import numpy as np

# 关闭 SettingWithCopyWarning
pd.options.mode.chained_assignment = None

########## 加载数据 ##########

print("Loading Data...")

node = pd.read_csv("data/Node.csv")
link = pd.read_csv("data/Link.csv")
link["id"] = link.index

# 生成打分后的节点数据表
scorednode = copy.deepcopy(node)
scorednode = scorednode.dropna()
scorednode = scorednode.drop_duplicates('id', keep='first')
scorednode = scorednode[(scorednode['industry'] != '[]') |
                (scorednode['type'] != 'Domain')]
scorednode = scorednode.reset_index() #index和npy对应
score = np.load('score.npy')
score = pd.DataFrame(score, columns=['score'])
scorednode = pd.concat([scorednode, score], axis=1)
scorednode.set_index('id', inplace=True)
scorednode = scorednode[['name','type','industry','score']] # remove 'index' column

print("Load Data Complete.")
print("Scored Node: %d (%.2f%%)" % (len(scorednode), len(scorednode) / len(node) * 100))

#############################

# 记录访问节点
# # For copying DataFrame, the copy is default False.
remainnode = copy.deepcopy(scorednode) 
remainnode = remainnode.sort_values(by='score', ascending=False)

def removenode(node_id):
    global remainnode
    remainnode.drop(index=node_id, inplace=True, errors='ignore')

def getTopNode():
    return remainnode.iloc[0].name

#############################

from meta import *

# 筛选同类型节点的底数
FILTER_BASE = 20
# 筛选阈值
FILTER_THRESHOLD = 100
# 核心节点打分应当为 5% 以内
CORETOP = 5

def refreshcorethres():
    global corescorethres, remainnode
    # Rearrange remainnode.
    remainnode = remainnode.sort_values(by='score', ascending=False)
    # Calculate corescorethres by percentile.
    corescorethres = remainnode['score'].describe(percentiles=[(100 - CORETOP) / 100])[str(100 - CORETOP) + '%']
    print("Remaining Node: %d (%.2f%%), Threshold Score for Core node is %.2f" % (len(remainnode), len(remainnode) / len(scorednode) * 100, corescorethres))
refreshcorethres()

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

DEFAULT_SCORE = 10

def queryScore(node_id):
    if node_id in scorednode.index:
        return scorednode['score'][node_id]
    else:
        return DEFAULT_SCORE # Default score

def sort_by_score(curnode, neighbors):
    # filter by scorednode for mining.
    new_neighbors = neighbors[neighbors['source'].isin(scorednode.index) & neighbors['target'].isin(scorednode.index)]
    if len(new_neighbors) == 0:
        return neighbors  # keep some nodes to mine
    new_neighbors['neighbor'] = new_neighbors.apply(
        lambda x: 
        x['source'] if x['target'] == curnode 
        else x['target'], axis=1)
    new_neighbors['score'] = new_neighbors['neighbor'].apply(
        lambda x: scorednode['score'][x])
    return new_neighbors.sort_values(by='score', ascending=False)

# Filter the same nodes into a smaller number.
# For stability concern, we use head() instead of sample()
# group_filtered = log_{filter_threshold}^len(x)
def filter(curnode, neighbors):

    neighbors = sort_by_score(curnode, neighbors)

    # Filter is only used in searchUCS
    global remainnode
    # remainnode.drop(index=neighbors['neighbor'], inplace=True, errors='ignore')
    remainnode.drop(index=neighbors['source'], inplace=True, errors='ignore')
    remainnode.drop(index=neighbors['target'], inplace=True, errors='ignore')
    # remainnode = remainnode[(remainnode.index.isin(neighbors['source']) == False) & (remainnode.index.isin(neighbors['target']) == False)]

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
def coreasset(curnode, neighbors, limitation):
    if len(neighbors) == 0:
        return False
    rel_cnt = neighbors.groupby(["relation"]).count()
    rel_pop = rel_cnt["target"].max() / len(neighbors)
    rel_top = rel_cnt["target"].idxmax()
    if rel_pop > 0.5 and link_priority[rel_top] == 4:
        return False
    if "r_dns_a" in rel_cnt.index.values and rel_cnt["target"]["r_dns_a"] > 2:
        return False
    # 核心资产的邻居数目不得低于这个数值
    if len(neighbors) <= net_limit[limitation]['corelimit']:
        return False
    # 没有打分的节点不是核心节点
    if curnode not in scorednode.index:
        return False
    # 分数不够高的节点不是核心节点
    if scorednode['score'][curnode] < corescorethres:
        return False
    return True


def toRecords(neighbors):
    return neighbors.to_dict(orient="records")

# 查询产业，如果产业为空将返回 [""] 没有特殊处理，这将表示没有产业，可以被忽略。
def queryIndustry(node_id):
    return node[node['id']==node_id].iloc[0]['industry'][1:-1].replace("'","").replace(" ","").split(',')

#############################
