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


def _point_to_segment_distance(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.sqrt((px - ax) ** 2 + (py - ay) ** 2), ax, ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    cx, cy = ax + t * dx, ay + t * dy
    return math.sqrt((px - cx) ** 2 + (py - cy) ** 2), cx, cy


class Navigator:
    def __init__(self):
        self._nodes = {}
        self._walkways = []
        self.hash_table = _NodeHashTable(self._nodes)
        self.building_info = BuildingHashTable()
        self.category_tree = CategoryTree()

    def add_node(self, name, lat, lng, category=None):
        self._nodes[name] = {"lat": lat, "lng": lng, "category": category}

    def remove_node(self, name):
        self._nodes.pop(name, None)

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

    def add_walkway(self, points, name=None):
        if not name:
            name = f"W{len(self._walkways) + 1}"
        weight = self._walkway_length(points)
        self._walkways.append({"name": name, "points": points, "weight": weight})
        return name

    def remove_walkway(self, name):
        for i, w in enumerate(self._walkways):
            if w["name"] == name:
                self._walkways.pop(i)
                return True
        return False

    def _walkway_length(self, points):
        total = 0
        for i in range(len(points) - 1):
            total += self._haversine_coords(
                points[i][0], points[i][1],
                points[i + 1][0], points[i + 1][1],
            )
        return round(total, 1)

    def _snap_to_walkway(self, lat, lng):
        best_dist = float("inf")
        best_point = None
        best_walkway = None
        best_seg_idx = 0
        for w in self._walkways:
            pts = w["points"]
            for i in range(len(pts) - 1):
                d, cx, cy = _point_to_segment_distance(
                    lat, lng, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]
                )
                if d < best_dist:
                    best_dist = d
                    best_point = (cx, cy)
                    best_walkway = w["name"]
                    best_seg_idx = i
        return best_dist, best_point, best_walkway, best_seg_idx

    def _build_graph(self):
        g = Graph()

        walkway_nodes = {}
        node_counter = [0]

        for w in self._walkways:
            pts = w["points"]
            for i in range(len(pts) - 1):
                p1 = pts[i]
                p2 = pts[i + 1]
                key1 = f"_w_{w['name']}_{i}"
                key2 = f"_w_{w['name']}_{i + 1}"
                if key1 not in walkway_nodes:
                    walkway_nodes[key1] = {"lat": p1[0], "lng": p1[1]}
                    g.add_vertex(key1)
                if key2 not in walkway_nodes:
                    walkway_nodes[key2] = {"lat": p2[0], "lng": p2[1]}
                    g.add_vertex(key2)
                d = self._haversine_coords(p1[0], p1[1], p2[0], p2[1])
                g.add_edge(key1, key2, d)

        for nname, node in self._nodes.items():
            g.add_vertex(nname)
            _, snap_point, _, _ = self._snap_to_walkway(node["lat"], node["lng"])
            if snap_point:
                snap_key = f"_snap_{nname}"
                g.add_vertex(snap_key)
                walkway_nodes[snap_key] = {"lat": snap_point[0], "lng": snap_point[1]}
                d = self._haversine_coords(
                    node["lat"], node["lng"], snap_point[0], snap_point[1]
                )
                g.add_edge(nname, snap_key, d)

                nearest_wk = None
                nearest_dist = float("inf")
                for w in self._walkways:
                    pts = w["points"]
                    for i in range(len(pts) - 1):
                        sd, _, _ = _point_to_segment_distance(
                            snap_point[0], snap_point[1],
                            pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]
                        )
                        if sd < nearest_dist:
                            nearest_dist = sd
                            nearest_wk = w
                            nearest_seg = i

                if nearest_wk and nearest_dist < 0.0001:
                    wk_key1 = f"_w_{nearest_wk['name']}_{nearest_seg}"
                    wk_key2 = f"_w_{nearest_wk['name']}_{nearest_seg + 1}"
                    g.add_edge(snap_key, wk_key1, 0)
                    g.add_edge(snap_key, wk_key2, 0)

        return g

    def shortest_path(self, start, end):
        if start not in self._nodes or end not in self._nodes:
            return None, float("inf")
        g = self._build_graph()
        raw_path, cost = g.dijkstra(start, end)
        if not raw_path:
            return None, float("inf")
        display_path = [n for n in raw_path if not n.startswith("_")]
        return display_path, cost

    def get_state(self):
        return {
            "nodes": dict(self._nodes),
            "walkways": list(self._walkways),
        }

    def load_state(self, data):
        self._nodes.clear()
        self._nodes.update(data.get("nodes", {}))
        self._walkways.clear()
        self._walkways.extend(data.get("walkways", []))

    def _haversine_coords(self, lat1, lon1, lat2, lon2):
        lat1, lon1 = math.radians(lat1), math.radians(lon1)
        lat2, lon2 = math.radians(lat2), math.radians(lon2)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return round(6371000 * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h)), 1)
