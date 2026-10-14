import networkx as nx

class LineageGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id, node_type="table", **attrs):
        self.graph.add_node(node_id, node_type=node_type, **attrs)

    def add_edge(self, source, target, transformation="", job=""):
        self.graph.add_edge(source, target, transformation=transformation, job=job)

    def upstream(self, node_id, depth=None):
        if node_id not in self.graph:
            return []
        result = []
        for pred in nx.ancestors(self.graph, node_id):
            if depth:
                path_len = nx.shortest_path_length(self.graph, pred, node_id)
                if path_len <= depth:
                    result.append(pred)
            else:
                result.append(pred)
        return result

    def downstream(self, node_id, depth=None):
        if node_id not in self.graph:
            return []
        result = []
        for succ in nx.descendants(self.graph, node_id):
            if depth:
                path_len = nx.shortest_path_length(self.graph, node_id, succ)
                if path_len <= depth:
                    result.append(succ)
            else:
                result.append(succ)
        return result

    def to_json(self):
        return {
            "nodes": [{"id": n, **self.graph.nodes[n]} for n in self.graph.nodes],
            "edges": [{"source": u, "target": v, **self.graph.edges[u, v]}
                      for u, v in self.graph.edges],
        }
