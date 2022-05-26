from data import *
import heapq

# 一致代价搜索 Uniform Cost Search
class UCS:
    def __init__(self, graph, stepshow=False, vis_node=None, vis_edge=None):
        self.graph = graph
        self.stepshow = stepshow # 与算法有关，是否访问边时将节点加入
        if stepshow:
            if vis_node is not None:
                self.vis_node = vis_node
            if vis_edge is not None:
                self.vis_edge = vis_edge

    def get_neighbors(self, node: Node):
        raise NotImplementedError()

    def add_node(self, node: Node):
        raise NotImplementedError()

    def add_edge(self, e, curnode):
        raise NotImplementedError()

    def vis_node(self, node: Node):
        pass
    
    def vis_edge(self, e, curnode):
        pass

    # 在优先级队列中寻找键
    def findkey(self, pq, key):
        for i in range(len(pq)):
            if pq[i][1] == key:
                return i
        return -1

    # 运行 UCS
    def run(self, q):

        explored = set()   # 是否被扩展
        visited = set()    # 是否被访问

        while len(q) > 0:
            top = heapq.heappop(q)
            top_priority = top[0]
            top_id = top[1]
            top_node = Node(self.graph, top_id)

            neighbors = self.get_neighbors(top_node)

            if top_id not in visited:
                visited.add(top_id)
                if self.add_node(top_node):
                    return  # 满足条件终止搜索
            
            explored.add(top_id)

            # 限制深度
            max_priority = top_priority + 1
            if max_priority not in link_limit.keys():
                continue

            for e in neighbors:
                neighbor = e["target"] if e["source"] == top_id else e["source"]
                priority = link_priority[e["relation"]]
                qidx = self.findkey(q, neighbor)

                flag = False
                if neighbor not in explored and qidx == -1:
                    priority = max(priority, max_priority)
                    heapq.heappush(q, [priority, neighbor])
                    flag = True
                elif qidx > -1 and priority < q[qidx][0]:
                    q[qidx][0] = priority
                    heapq.heapify(q)
                    flag = True
                
                if flag:
                    if self.stepshow and neighbor not in visited:  # 被访问
                        neighbor_node = Node(self.graph, neighbor)
                        self.get_neighbors(neighbor_node)  # 需要判别是否是核心节点
                        visited.add(neighbor)
                        if self.add_node(neighbor_node):
                            return
                    if self.add_edge(e, top_id):
                        return


class searchUCS(UCS):
    def __init__(self, graph, limitation, vis_node=None, vis_edge=None):
        self.node_limit = limitation["node"]
        self.edge_limit = limitation["edge"]
        self.subgraph = Subgraph(["id", "label", "style"], ["id", "source", "target", "label"])
        self.corenodes = []
        self.statdata = {"nodes": {}, "edges": {}}

        self.default_style = {}
        self.core_style = {"fill": "blue"}

        super().__init__(graph, True, vis_node, vis_edge)

    def get_neighbors(self, node: Node):
        if node.label == "IP" or node.label == "Cert":
            neighbors = node.queryNeighbors()
        else:
            neighbors = node.queryChildren()

        before = len(neighbors)
        node.iscore = coreasset(node.node_id, neighbors)
        neighbors = filter(node.node_id, neighbors)
        after = len(neighbors)
        print("%d" % before if before == after else "%d(%d)" % (before, after), end=" ")

        return toRecords(neighbors)

    def add_node(self, node: Node):

        # cut off
        if self.node_limit == 0:
            return True
        self.node_limit -= 1

        if node.label not in self.statdata["nodes"].keys():
            self.statdata["nodes"][node.label] = 1
        else:
            self.statdata["nodes"][node.label] += 1

        if node.iscore:
            self.corenodes.append(node.node_id)
            self.subgraph.addNode(
                {
                    "id": node.node_id,
                    "label": node.label + "_" + str(len(self.corenodes)),
                    "style": self.core_style,
                }
            )
        else:
            self.subgraph.addNode(
                {"id": node.node_id, "label": node.label, "style": self.default_style}
            )
        self.vis_node(node)

        return False

    def add_edge(self, e, curnode):

        if e["relation"] not in self.statdata["edges"].keys():
            self.statdata["edges"][e["relation"]] = 1
        else:
            self.statdata["edges"][e["relation"]] += 1

        self.subgraph.addEdge(
            {
                "id": str(e["id"]),
                "source": e["source"],
                "target": e["target"],
                "label": e["relation"],
            }
        )
        
        self.edge_limit -= 1
        self.vis_edge(e, curnode)
        if self.edge_limit == 0:
            return True
        return False

    def search_run(self, node_id):
        q = [[1, node_id]]
        super().run(q)


class pathUCS(UCS):
    def __init__(self, graph):
        # Critical Path cannot be longer than 4
        self.DEPTH_LIMIT = 4

        super().__init__(graph, False)

    def get_neighbors(self, node: Node):
        return toRecords(node.queryNeighbors())

    def add_node(self, node: Node):
        if node.node_id in self.targets:
            self.targets.remove(node.node_id)
            tpath = []
            tptr = node.node_id

            while tptr != self.source:
                tedge = self.edge_to[tptr]
                tpath.append(tedge["id"])
                tptr = tedge["prev"]
            tpath.reverse()

            if len(tpath) > self.DEPTH_LIMIT:
                print("%s: Not critical." % node.node_id)
            else:
                for edgeid in tpath:
                    self.visitedEdges.add(edgeid)
                self.targetPaths[node.node_id] = tpath
                print("%s: %s" % (node.node_id, str(tpath)))

        return len(self.targets) == 0

    def add_edge(self, e, curnode):
        neighbor = e["target"] if e["source"] == curnode else e["source"]
        self.edge_to[neighbor] = {"id": e["id"], "prev": curnode}

    def path_run(self, node_id, subset):
        self.source = node_id
        self.targets = set(subset)
        self.targets.remove(node_id)

        # Store the prev node
        self.edge_to = {}
        # Target Path
        self.targetPaths = {}
        # Visited Path
        self.visitedEdges = set()

        q = [[0, node_id]]
        super().run(q)

class subUCS(UCS):
    def __init__(self, graph, ifneighbors=False):
        self.subgraph = Subgraph(["id","style"],["id","source","target","relation"])
        self.ifneighbors = ifneighbors

        self.default_style = {}
        self.core_style = {"fill": "blue"}
        super().__init__(graph, False)

    def get_neighbors(self, node: Node):
        return toRecords(node.queryNeighbors())

    def add_node(self, node: Node):
        if node.node_id in self.targets:
            self.targets.remove(node.node_id)
            tptr = node.node_id
            self.subgraph.addNode({
                "id": tptr,
                "style": self.core_style
            })

            while tptr != self.source:
                tedge = self.edge_to[tptr]
                self.subgraph.addEdge({
                    "id": str(tedge["id"]),
                    "source": tedge["prev"],
                    "target": tptr,
                })
                if tptr != self.source:
                    self.subgraph.addNode({
                        "id": tedge["prev"],
                        "style": self.default_style
                    })
                tptr = tedge["prev"]

        return len(self.targets) == 0

    def add_edge(self, e, curnode):
        neighbor = e["target"] if e["source"] == curnode else e["source"]
        self.edge_to[neighbor] = {"id": e["id"], "prev": curnode}

    def sub_run(self, subset):
        self.source = subset[0]
        self.targets = set(subset)
        self.targets.remove(self.source)

        # Store the prev node
        self.edge_to = {}

        # Add source node into subgraph
        self.subgraph.addNode({
            "id": self.source,
            "style": self.core_style
        })

        q = [[0, self.source]]
        super().run(q)