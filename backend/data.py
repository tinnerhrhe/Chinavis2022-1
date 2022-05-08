# 由于数据量较大（~688MB），
# 需要使用 pandas 数据工具加速查询。

import pandas as pd
import math

########## 加载数据 ##########

print("Loading Data...")

node = pd.read_csv("data/Node.csv")
link = pd.read_csv("data/Link.csv")
link["id"] = link.index

print("Load Data Complete.")

#############################

from meta import *

# 核心资产的邻居数目不得低于这个数值
CORE_LIMIT = 6
# 筛选同类型节点的底数
FILTER_BASE = 20
# 筛选阈值
FILTER_THRESHOLD = 100

# 图：预期使用 pandas 存储
class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


class Subgraph(Graph):
    def __init__(self):
        super().__init__(
            pd.DataFrame(columns=["id", "label", "style"]),
            pd.DataFrame(columns=["id", "source", "target", "label"]),
        )

    def addNode(self, n):
        self.nodes = self.nodes.append(pd.Series(n), ignore_index=True)

    def addEdge(self, e):
        self.edges = self.edges.append(pd.Series(e), ignore_index=True)

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
def filter(neighbors):
    if len(neighbors) > FILTER_THRESHOLD:
        return (
            neighbors.groupby(["relation"])
            .apply(
                lambda x: x.head(int(FILTER_BASE * math.log(len(x), FILTER_THRESHOLD)))
                if len(x) > FILTER_THRESHOLD
                else x.head(len(x))  # dummy trick, could be better.
            )
            .droplevel(0)
        )
    else:
        return neighbors


# 是否是核心资产
def coreasset(neighbors):
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
    return True


def toRecords(neighbors):
    return neighbors.to_dict(orient="records")


#############################
