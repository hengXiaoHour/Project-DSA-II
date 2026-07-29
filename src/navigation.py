import math
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
        self._junctions = {}
        self._walkways = []
        self.hash_table = _NodeHashTable(self._nodes)
        self.building_info = BuildingHashTable()
        self.category_tree = CategoryTree()

    def add_node(self, name, lat, lng, category=None):
        self._nodes[name] = {"lat": lat, "lng": lng, "category": category}
        self._snap_building(name)

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
        if lat is not None or lng is not None:
            self._snap_building(new_name or name)

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

    def add_junction(self, name, lat, lng):
        self._junctions[name] = {"lat": lat, "lng": lng}
        for node_name in self._nodes:
            self._snap_building(node_name)

    def remove_junction(self, name):
        self._junctions.pop(name, None)
        self._walkways = [w for w in self._walkways if w["from"] != name and w["to"] != name]
        for node_name in self._nodes:
            self._snap_building(node_name)

    def update_junction(self, name, lat=None, lng=None, new_name=None):
        if name not in self._junctions:
            return
        jct = self._junctions[name]
        if lat is not None:
            jct["lat"] = lat
        if lng is not None:
            jct["lng"] = lng
        if new_name is not None and new_name != name:
            self._junctions[new_name] = self._junctions.pop(name)
            for w in self._walkways:
                if w["from"] == name:
                    w["from"] = new_name
                if w["to"] == name:
                    w["to"] = new_name
            for node_name in self._nodes:
                if self._nodes[node_name].get("nearest_junction") == name:
                    self._nodes[node_name]["nearest_junction"] = new_name
        for node_name in self._nodes:
            self._snap_building(node_name)

    def add_walkway(self, from_jct, to_jct, path=None):
        if from_jct not in self._junctions or to_jct not in self._junctions:
            return False
        weight = self._haversine_coords(
            self._junctions[from_jct]["lat"], self._junctions[from_jct]["lng"],
            self._junctions[to_jct]["lat"], self._junctions[to_jct]["lng"],
        )
        walkway = {"from": from_jct, "to": to_jct, "weight": weight}
        if path:
            walkway["path"] = path
        self._walkways.append(walkway)
        for node_name in self._nodes:
            self._snap_building(node_name)
        return True

    def remove_walkway(self, from_jct, to_jct):
        for i, w in enumerate(self._walkways):
            if (w["from"] == from_jct and w["to"] == to_jct) or \
               (w["from"] == to_jct and w["to"] == from_jct):
                self._walkways.pop(i)
                for node_name in self._nodes:
                    self._snap_building(node_name)
                return True
        return False

    def get_nearest_junction(self, name):
        node = self._nodes.get(name)
        if not node:
            return None
        best = None
        best_dist = float("inf")
        for jname, jct in self._junctions.items():
            d = self._haversine_coords(node["lat"], node["lng"], jct["lat"], jct["lng"])
            if d < best_dist:
                best_dist = d
                best = jname
        return best

    def _nearest_point_on_walkway(self, lat, lng, j1_name, j2_name):
        j1 = self._junctions[j1_name]
        j2 = self._junctions[j2_name]
        ax, ay = j1["lng"], j1["lat"]
        bx, by = j2["lng"], j2["lat"]
        px, py = lng, lat
        abx, aby = bx - ax, by - ay
        denom = abx * abx + aby * aby
        if denom == 0:
            t = 0
        else:
            t = ((px - ax) * abx + (py - ay) * aby) / denom
        t = max(0, min(1, t))
        qx, qy = ax + t * abx, ay + t * aby
        dist = self._haversine_coords(lat, lng, qy, qx)
        return dist, qy, qx, j1_name, j2_name, t

    def _snap_building(self, name):
        node = self._nodes.get(name)
        if not node or not self._walkways:
            return
        for key in ["snap_lat", "snap_lng", "snap_j1", "snap_j2", "snap_t"]:
            node.pop(key, None)
        best_dist = float("inf")
        best = None
        for w in self._walkways:
            dist, qlat, qlng, j1, j2, t = self._nearest_point_on_walkway(
                node["lat"], node["lng"], w["from"], w["to"])
            if dist < best_dist:
                best_dist = dist
                best = (qlat, qlng, j1, j2, t)
        if best:
            node["snap_lat"] = best[0]
            node["snap_lng"] = best[1]
            node["snap_j1"] = best[2]
            node["snap_j2"] = best[3]
            node["snap_t"] = best[4]

    def _build_junction_graph(self):
        g = Graph()
        for jname in self._junctions:
            g.add_vertex(jname)
        for w in self._walkways:
            g.add_edge(w["from"], w["to"], w["weight"])
        for nname, node in self._nodes.items():
            if "snap_lat" in node and "snap_j1" in node:
                snap_name = f"_snap_{nname}"
                g.add_vertex(snap_name)
                d_snap = self._haversine_coords(
                    node["lat"], node["lng"], node["snap_lat"], node["snap_lng"])
                g.add_edge(nname, snap_name, d_snap)
                for jkey in ["snap_j1", "snap_j2"]:
                    jname = node.get(jkey)
                    if jname and jname in self._junctions:
                        d = self._haversine_coords(
                            node["snap_lat"], node["snap_lng"],
                            self._junctions[jname]["lat"], self._junctions[jname]["lng"])
                        g.add_edge(snap_name, jname, d)
            elif node.get("nearest_junction"):
                jname = node["nearest_junction"]
                if jname in self._junctions:
                    g.add_vertex(nname)
                    d = self._haversine_coords(
                        node["lat"], node["lng"],
                        self._junctions[jname]["lat"], self._junctions[jname]["lng"])
                    g.add_edge(nname, jname, d)
        return g

    def _build_graph(self):
        if self._junctions and self._walkways:
            return self._build_junction_graph()
        g = Graph()
        for name in self._nodes:
            g.add_vertex(name)
        for e in self._edges:
            g.add_edge(e["from"], e["to"], e["weight"])
        return g

    def shortest_path_adjacency(self):
        g = self._build_graph()
        names = sorted(self._nodes.keys())
        adj = {n: [] for n in names}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                _, cost = g.dijkstra(a, b)
                if cost != float("inf"):
                    adj[a].append((b, round(cost)))
                    adj[b].append((a, round(cost)))
        for n in names:
            adj[n].sort(key=lambda x: x[0])
        return adj

    def shortest_path(self, start, end):
        if start not in self._nodes or end not in self._nodes:
            return None, float("inf")
        g = self._build_graph()
        return g.dijkstra(start, end)

    def bfs(self, start, end):
        if start not in self._nodes or end not in self._nodes:
            return None, float("inf")
        g = self._build_graph()
        visited = {start}
        queue = [(start, [start], 0)]
        while queue:
            current, path, cost = queue.pop(0)
            if current == end:
                return path, cost
            for neighbour, weight in g.vertices.get(current, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, path + [neighbour], cost + weight))
        return None, float("inf")

    def dfs(self, start, end):
        if start not in self._nodes or end not in self._nodes:
            return None, float("inf")
        g = self._build_graph()
        visited = set()
        stack = [(start, [start], 0)]
        while stack:
            current, path, cost = stack.pop()
            if current == end:
                return path, cost
            if current in visited:
                continue
            visited.add(current)
            for neighbour, weight in g.vertices.get(current, []):
                if neighbour not in visited:
                    stack.append((neighbour, path + [neighbour], cost + weight))
        return None, float("inf")

    def get_state(self):
        return {
            "nodes": dict(self._nodes),
            "edges": list(self._edges),
            "junctions": dict(self._junctions),
            "walkways": list(self._walkways),
        }

    def load_state(self, data):
        self._nodes.clear()
        self._nodes.update(data.get("nodes", {}))
        self._edges.clear()
        self._edges.extend(data.get("edges", []))
        self._junctions.clear()
        self._junctions.update(data.get("junctions", {}))
        self._walkways.clear()
        self._walkways.extend(data.get("walkways", []))

    def _haversine_coords(self, lat1, lon1, lat2, lon2):
        lat1, lon1 = math.radians(lat1), math.radians(lon1)
        lat2, lon2 = math.radians(lat2), math.radians(lon2)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return round(6371000 * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h)), 1)

    def _haversine(self, from_name, to_name):
        a = self._nodes.get(from_name)
        b = self._nodes.get(to_name)
        if not a or not b:
            return 1
        return self._haversine_coords(a["lat"], a["lng"], b["lat"], b["lng"])
