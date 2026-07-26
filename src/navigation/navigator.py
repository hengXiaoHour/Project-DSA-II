import math
from .hashtable import HashTable
from .graph import Graph
from .tree import Tree, TreeNode
from .campus_data import build_campus


def haversine(lat1, lng1, lat2, lng2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class Navigator:
    def __init__(self):
        self.hash_table, self.graph, self.tree_root = build_campus()
        self.tree = Tree(self.tree_root)

    def add_node(self, name, lat, lng, category=None):
        if self.hash_table.contains(name):
            return False
        data = {"name": name, "lat": lat, "lng": lng, "category": category or "Uncategorized"}
        self.hash_table.insert(name, data)
        self.graph.add_node(name)
        cat_node = self.tree_root.find(data["category"])
        if cat_node is None:
            cat_node = TreeNode(data["category"])
            self.tree_root.add_child(cat_node)
        cat_node.add_child(TreeNode(name))
        return True

    def remove_node(self, name):
        if not self.hash_table.contains(name):
            return False
        data = self.hash_table.get(name)
        self.hash_table.delete(name)
        self.graph.remove_node(name)
        cat_node = self.tree_root.find(data["category"])
        if cat_node:
            to_remove = [c for c in cat_node.children if c.name == name]
            for c in to_remove:
                cat_node.children.remove(c)
        return True

    def update_node(self, name, lat=None, lng=None, new_name=None, category=None):
        if not self.hash_table.contains(name):
            return False
        data = self.hash_table.get(name)
        old_cat = data["category"]
        if lat is not None:
            data["lat"] = lat
        if lng is not None:
            data["lng"] = lng
        if category is not None:
            data["category"] = category
        if new_name is not None and new_name != name:
            data["name"] = new_name
            self.hash_table.insert(new_name, data)
            self.hash_table.delete(name)
            adj = dict(self.graph.adjacency_list[name])
            self.graph.add_node(new_name)
            for neighbor, w in adj.items():
                self.graph.add_edge(new_name, neighbor, w)
            self.graph.remove_node(name)
            if old_cat == category or category is None:
                cat_node = self.tree_root.find(old_cat)
                if cat_node:
                    for c in cat_node.children:
                        if c.name == name:
                            c.name = new_name
                            break
            if category and category != old_cat:
                old_cat_node = self.tree_root.find(old_cat)
                if old_cat_node:
                    old_cat_node.children = [c for c in old_cat_node.children if c.name != name]
                new_cat_node = self.tree_root.find(category)
                if new_cat_node is None:
                    new_cat_node = TreeNode(category)
                    self.tree_root.add_child(new_cat_node)
                new_cat_node.add_child(TreeNode(new_name))
        else:
            if category and category != old_cat:
                old_cat_node = self.tree_root.find(old_cat)
                if old_cat_node:
                    old_cat_node.children = [c for c in old_cat_node.children if c.name != name]
                new_cat_node = self.tree_root.find(category)
                if new_cat_node is None:
                    new_cat_node = TreeNode(category)
                    self.tree_root.add_child(new_cat_node)
                new_cat_node.add_child(TreeNode(name))
        return True

    def add_edge(self, from_name, to_name, weight=None):
        if not self.hash_table.contains(from_name) or not self.hash_table.contains(to_name):
            return False
        if weight is None:
            a = self.hash_table.get(from_name)
            b = self.hash_table.get(to_name)
            weight = round(haversine(a["lat"], a["lng"], b["lat"], b["lng"]))
        if weight <= 0:
            weight = 1
        self.graph.add_edge(from_name, to_name, weight)
        return True

    def remove_edge(self, from_name, to_name):
        if not self.graph.has_node(from_name) or not self.graph.has_node(to_name):
            return False
        self.graph.remove_edge(from_name, to_name)
        return True

    def find_room(self, room_id):
        return self.hash_table.get(f"R_{room_id}")

    def find_building(self, name):
        return self.hash_table.get(name)

    def find_floor(self, floor_id):
        return self.hash_table.get(f"F_{floor_id}")

    def bfs(self, start, end):
        return self.graph.bfs(start, end)

    def dfs(self, start, end):
        return self.graph.dfs(start, end)

    def shortest_path(self, start_room, end_room):
        path, cost = self.graph.shortest_path(start_room, end_room)
        return path, cost

    def get_buildings(self):
        return sorted(self.hash_table.keys())

    def show_campus_hierarchy(self):
        return str(self.tree)

    def get_all_rooms(self):
        return [v for k, v in self.hash_table.values() if isinstance(v, dict) and "room_id" in v.__dict__]

    def get_state(self):
        nodes = {}
        for name in self.hash_table.keys():
            nodes[name] = self.hash_table.get(name)
        edges = []
        seen = set()
        for node, neighbors in self.graph.adjacency_list.items():
            for neighbor, w in neighbors.items():
                key = tuple(sorted([node, neighbor]))
                if key not in seen:
                    seen.add(key)
                    edges.append({"from": node, "to": neighbor, "weight": w})
        return {"nodes": nodes, "edges": edges}

    def load_state(self, state):
        self.hash_table = HashTable()
        self.graph = Graph()
        self.tree_root = TreeNode("My Campus")
        self.tree = Tree(self.tree_root)
        for name, data in state.get("nodes", {}).items():
            self.hash_table.insert(name, data)
            self.graph.add_node(name)
            cat_node = self.tree_root.find(data.get("category", "Uncategorized"))
            if cat_node is None:
                cat_node = TreeNode(data.get("category", "Uncategorized"))
                self.tree_root.add_child(cat_node)
            cat_node.add_child(TreeNode(name))
        for edge in state.get("edges", []):
            self.graph.add_edge(edge["from"], edge["to"], edge["weight"])

    def get_node(self, name):
        return self.hash_table.get(name) if self.hash_table.contains(name) else None
