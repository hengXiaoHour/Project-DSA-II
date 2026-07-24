from .hashtable import HashTable
from .graph import Graph
from .tree import Tree, TreeNode
from .campus_data import build_campus


class Navigator:
    def __init__(self):
        self.hash_table, self.graph, self.tree_root = build_campus()
        self.tree = Tree(self.tree_root)

    def find_room(self, room_id):
        return self.hash_table.get(f"R_{room_id}")

    def find_building(self, building_id):
        return self.hash_table.get(f"B_{building_id}")

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
        return sorted([k.replace("B_", "") for k in self.hash_table.keys() if k.startswith("B_")])

    def show_campus_hierarchy(self):
        return str(self.tree)

    def get_all_rooms(self):
        return [v for k, v in self.hash_table.values() if isinstance(v, dict) and "room_id" in v.__dict__]
