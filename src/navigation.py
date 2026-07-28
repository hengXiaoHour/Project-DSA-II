from backend.graph import Graph
from backend.hash_table import BuildingHashTable
from backend.tree import CategoryTree


class _NodeHashTable:
    def __init__(self, nodes):
        self._nodes = nodes

    def keys(self):
        return self._nodes.keys()

    def get(self, name):
        return self._nodes.get(name)

    def contains(self, name):
        return name in self._nodes


class Navigator:
    def __init__(self):
        self._nodes = {}
        self._edges = []
        self.hash_table = _NodeHashTable(self._nodes)
        self.building_info = BuildingHashTable()
        self.category_tree = CategoryTree()

    def add_node(self, name, lat, lng, category=None):
        self._nodes[name] = {"lat": lat, "lng": lng, "category": category}

    def remove_node(self, name):
        self._nodes.pop(name, None)
        self._edges = [e for e in self._edges if e["from"] != name and e["to"] != name]

    def update_node(self, name, lat=None, lng=None, new_name=None, category=None):
        if name not in self._nodes:
            return
        node = self._nodes[name]
        if lat is not None:
            node["lat"] = lat
        if lng is not None:
            node["lng"] = lng
        if category is not None:
            node["category"] = category
        if new_name is not None and new_name != name:
            self._nodes[new_name] = self._nodes.pop(name)
            for e in self._edges:
                if e["from"] == name:
                    e["from"] = new_name
                if e["to"] == name:
                    e["to"] = new_name

    def add_edge(self, from_name, to_name, weight=None, path=None):
        if from_name not in self._nodes or to_name not in self._nodes:
            return False
        if weight is None:
            weight = self._haversine(from_name, to_name)
        edge = {"from": from_name, "to": to_name, "weight": weight}
        if path:
            edge["path"] = path
        self._edges.append(edge)
        return True

    def remove_edge(self, from_name, to_name):
        for i, e in enumerate(self._edges):
            if (e["from"] == from_name and e["to"] == to_name) or \
               (e["from"] == to_name and e["to"] == from_name):
                self._edges.pop(i)
                return True
        return False

    def _build_graph(self):
        g = Graph()
        for name in self._nodes:
            g.add_vertex(name)
        for e in self._edges:
            g.add_edge(e["from"], e["to"], e["weight"])
        return g

    def shortest_path(self, start, end):
        if start not in self._nodes or end not in self._nodes:
            return None, float("inf")
        g = self._build_graph()
        return g.dijkstra(start, end)

    def bfs(self, start, end):
        if start not in self._nodes or end not in self._nodes:
            return None, float("inf")
        adj = {name: [] for name in self._nodes}
        for e in self._edges:
            adj.setdefault(e["from"], []).append((e["to"], e["weight"]))
            adj.setdefault(e["to"], []).append((e["from"], e["weight"]))
        visited = {start}
        queue = [(start, [start], 0)]
        while queue:
            current, path, cost = queue.pop(0)
            if current == end:
                return path, cost
            for neighbour, weight in adj.get(current, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, path + [neighbour], cost + weight))
        return None, float("inf")

    def dfs(self, start, end):
        if start not in self._nodes or end not in self._nodes:
            return None, float("inf")
        adj = {name: [] for name in self._nodes}
        for e in self._edges:
            adj.setdefault(e["from"], []).append((e["to"], e["weight"]))
            adj.setdefault(e["to"], []).append((e["from"], e["weight"]))
        visited = set()
        stack = [(start, [start], 0)]
        while stack:
            current, path, cost = stack.pop()
            if current == end:
                return path, cost
            if current in visited:
                continue
            visited.add(current)
            for neighbour, weight in adj.get(current, []):
                if neighbour not in visited:
                    stack.append((neighbour, path + [neighbour], cost + weight))
        return None, float("inf")

    def get_state(self):
        return {"nodes": dict(self._nodes), "edges": list(self._edges)}

    def load_state(self, data):
        self._nodes.clear()
        self._nodes.update(data.get("nodes", {}))
        self._edges.clear()
        self._edges.extend(data.get("edges", []))

    def _haversine(self, from_name, to_name):
        import math
        a = self._nodes.get(from_name)
        b = self._nodes.get(to_name)
        if not a or not b:
            return 1
        lat1, lon1 = math.radians(a["lat"]), math.radians(a["lng"])
        lat2, lon2 = math.radians(b["lat"]), math.radians(b["lng"])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return round(6371000 * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h)), 1)
