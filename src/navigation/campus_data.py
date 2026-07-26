from .hashtable import HashTable
from .graph import Graph
from .tree import TreeNode


def build_campus():
    campus_hash = HashTable()
    campus_graph = Graph()
    campus_tree = TreeNode("My Campus")
    return campus_hash, campus_graph, campus_tree
