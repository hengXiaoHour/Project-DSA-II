from .models import Building
from .hashtable import HashTable
from .graph import Graph
from .tree import TreeNode


def build_campus():
    campus_hash = HashTable()
    campus_graph = Graph()
    campus_tree = TreeNode("RUPP Campus 1")

    building_names = [
        "Building A",
        "Building B",
        "Building C",
        "Building D",
        "Building Stem",
        "Building T",
        "NICC/CKCC",
        "Library",
        "Canteen",
        "Study Office",
        "Entrance",
    ]

    for name in building_names:
        building = Building(name, name)
        campus_hash.insert(f"B_{name}", building)
        node = TreeNode(name)
        campus_tree.add_child(node)

    edges = [
        ("NICC/CKCC", "Building D", 64),
        ("NICC/CKCC", "Library", 115),
        ("Library", "Building A", 80),
        ("Building D", "Building B", 50),
        ("Building D", "Building Stem", 50),
        ("Building B", "Building Stem", 50),
        ("Building Stem", "Building C", 115),
        ("Building Stem", "Study Office", 85),
        ("Building C", "Building T", 35),
        ("Building C", "Canteen", 115),
        ("Building T", "Canteen", 115),
        ("Study Office", "Canteen", 35),
        ("Canteen", "Building A", 115),
        ("Study Office", "Building A", 115),
        ("Building A", "Entrance", 115),
    ]

    for a, b, w in edges:
        campus_graph.add_edge(a, b, w)

    campus_hash.insert("ROOT", campus_tree)

    return campus_hash, campus_graph, campus_tree