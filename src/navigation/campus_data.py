from .models import Building, Floor, Room
from .hashtable import HashTable
from .graph import Graph
from .tree import TreeNode


def build_campus():
    campus_hash = HashTable()
    campus_graph = Graph()
    campus_tree = TreeNode("RUPP Campus 1")

    # ========== Building A ==========
    building_a = Building("A", "Building A")
    campus_hash.insert("B_A", building_a)
    node_a = TreeNode("Building A")
    campus_tree.add_child(node_a)

    floor_a1 = Floor("A1", "Floor 1", 1)
    floor_a1.add_room(Room("A101", "A101", 1, "lecture", 50))
    floor_a1.add_room(Room("A102", "A102", 1, "lab", 30))
    floor_a1.add_room(Room("A103", "A103", 1, "office", 10))
    floor_a1.add_room(Room("A104", "A104", 1, "restroom", 0))
    building_a.add_floor(floor_a1)
    campus_hash.insert("F_A1", floor_a1)
    node_a1 = TreeNode("Floor 1")
    node_a.add_child(node_a1)
    for r in floor_a1.rooms.values():
        node_a1.add_child(TreeNode(r.name))
        campus_hash.insert(f"R_{r.room_id}", r)
    campus_graph.add_edge("A101", "A102", 5)
    campus_graph.add_edge("A102", "A103", 4)
    campus_graph.add_edge("A103", "A104", 3)
    campus_graph.add_edge("A101", "A103", 10)

    floor_a2 = Floor("A2", "Floor 2", 2)
    floor_a2.add_room(Room("A201", "A201", 2, "lecture", 60))
    floor_a2.add_room(Room("A202", "A202", 2, "lab", 25))
    floor_a2.add_room(Room("A203", "A203", 2, "office", 8))
    building_a.add_floor(floor_a2)
    campus_hash.insert("F_A2", floor_a2)
    node_a2 = TreeNode("Floor 2")
    node_a.add_child(node_a2)
    for r in floor_a2.rooms.values():
        node_a2.add_child(TreeNode(r.name))
        campus_hash.insert(f"R_{r.room_id}", r)
    campus_graph.add_edge("A201", "A202", 5)
    campus_graph.add_edge("A202", "A203", 4)

    campus_graph.add_edge("A104", "STAIRS_A", 2)
    campus_graph.add_edge("STAIRS_A", "A201", 2)
    campus_graph.add_edge("A101", "ENTRY_A", 1)

    # ========== Building B ==========
    building_b = Building("B", "Building B")
    campus_hash.insert("B_B", building_b)
    node_b = TreeNode("Building B")
    campus_tree.add_child(node_b)

    floor_b1 = Floor("B1", "Floor 1", 1)
    floor_b1.add_room(Room("B101", "B101", 1, "lecture", 45))
    floor_b1.add_room(Room("B102", "B102", 1, "lab", 35))
    floor_b1.add_room(Room("B103", "B103", 1, "cafeteria", 100))
    building_b.add_floor(floor_b1)
    campus_hash.insert("F_B1", floor_b1)
    node_b1 = TreeNode("Floor 1")
    node_b.add_child(node_b1)
    for r in floor_b1.rooms.values():
        node_b1.add_child(TreeNode(r.name))
        campus_hash.insert(f"R_{r.room_id}", r)
    campus_graph.add_edge("B101", "B102", 5)
    campus_graph.add_edge("B102", "B103", 6)
    campus_graph.add_edge("B101", "ENTRY_B", 1)

    # ========== Inter-building connections ==========
    campus_graph.add_edge("ENTRY_A", "ENTRY_B", 20)
    campus_graph.add_edge("ENTRY_A", "MAIN_GATE", 10)
    campus_graph.add_edge("ENTRY_B", "MAIN_GATE", 15)

    campus_hash.insert("BUILDING_A", building_a)
    campus_hash.insert("BUILDING_B", building_b)
    campus_hash.insert("ROOT", campus_tree)

    return campus_hash, campus_graph, campus_tree
