import os
import json
import pytest
from src.navigation.navigator import Navigator, haversine
from src.navigation.graph import Graph
from src.navigation.hashtable import HashTable
from src.navigation.tree import TreeNode, Tree


class TestHaversine:
    def test_known_distance(self):
        d = haversine(11.562, 104.891, 11.563, 104.892)
        assert 100 < d < 200

    def test_zero_distance(self):
        d = haversine(11.562, 104.891, 11.562, 104.891)
        assert d == 0

    def test_symmetry(self):
        d1 = haversine(11.56, 104.89, 11.57, 104.90)
        d2 = haversine(11.57, 104.90, 11.56, 104.89)
        assert abs(d1 - d2) < 1


class TestNavigatorCRUD:
    def setup_method(self):
        self.nav = Navigator()

    def test_empty_on_init(self):
        assert len(self.nav.hash_table) == 0
        assert len(self.nav.graph) == 0

    def test_add_node(self):
        ok = self.nav.add_node("Library", 11.562, 104.891)
        assert ok is True
        assert self.nav.hash_table.contains("Library")
        assert self.nav.graph.has_node("Library")

    def test_add_duplicate_node(self):
        self.nav.add_node("A", 11.56, 104.89)
        ok = self.nav.add_node("A", 11.57, 104.90)
        assert ok is False

    def test_remove_node(self):
        self.nav.add_node("A", 11.56, 104.89)
        ok = self.nav.remove_node("A")
        assert ok is True
        assert not self.nav.hash_table.contains("A")
        assert not self.nav.graph.has_node("A")

    def test_remove_missing_node(self):
        ok = self.nav.remove_node("Nope")
        assert ok is False

    def test_add_edge_auto_weight(self):
        self.nav.add_node("A", 11.562, 104.891)
        self.nav.add_node("B", 11.563, 104.892)
        ok = self.nav.add_edge("A", "B")
        assert ok is True
        neighbors = self.nav.graph.get_neighbors("A")
        assert len(neighbors) == 1
        assert neighbors[0][1] > 0

    def test_add_edge_custom_weight(self):
        self.nav.add_node("A", 11.56, 104.89)
        self.nav.add_node("B", 11.57, 104.90)
        ok = self.nav.add_edge("A", "B", 50)
        assert ok is True
        _, w = self.nav.graph.get_neighbors("A")[0]
        assert w == 50

    def test_add_edge_missing_node(self):
        ok = self.nav.add_edge("X", "Y")
        assert ok is False

    def test_remove_edge(self):
        self.nav.add_node("A", 11.56, 104.89)
        self.nav.add_node("B", 11.57, 104.90)
        self.nav.add_edge("A", "B")
        ok = self.nav.remove_edge("A", "B")
        assert ok is True
        assert len(self.nav.graph.get_neighbors("A")) == 0

    def test_update_node_position(self):
        self.nav.add_node("A", 11.56, 104.89)
        self.nav.update_node("A", lat=11.57, lng=104.90)
        data = self.nav.hash_table.get("A")
        assert data["lat"] == 11.57
        assert data["lng"] == 104.90

    def test_update_node_rename(self):
        self.nav.add_node("A", 11.56, 104.89)
        self.nav.add_node("B", 11.57, 104.90)
        self.nav.add_edge("A", "B", 10)
        self.nav.update_node("A", new_name="Alpha")
        assert not self.nav.hash_table.contains("A")
        assert self.nav.hash_table.contains("Alpha")
        assert self.nav.graph.has_node("Alpha")
        assert not self.nav.graph.has_node("A")
        neighbors = self.nav.graph.get_neighbors("Alpha")
        assert any(n == "B" for n, _ in neighbors)

    def test_update_node_category(self):
        self.nav.add_node("A", 11.56, 104.89)
        self.nav.update_node("A", category="Academic")
        data = self.nav.hash_table.get("A")
        assert data["category"] == "Academic"

    def test_get_state(self):
        self.nav.add_node("A", 11.56, 104.89)
        self.nav.add_node("B", 11.57, 104.90)
        self.nav.add_edge("A", "B", 50)
        state = self.nav.get_state()
        assert "A" in state["nodes"]
        assert "B" in state["nodes"]
        assert len(state["edges"]) == 1
        assert state["nodes"]["A"]["lat"] == 11.56

    def test_load_state(self):
        state = {
            "nodes": {
                "X": {"name": "X", "lat": 11.56, "lng": 104.89, "category": "Test"},
                "Y": {"name": "Y", "lat": 11.57, "lng": 104.90, "category": "Test"},
            },
            "edges": [{"from": "X", "to": "Y", "weight": 100}],
        }
        self.nav.load_state(state)
        assert self.nav.hash_table.contains("X")
        assert self.nav.hash_table.contains("Y")
        assert self.nav.graph.has_node("X")
        assert self.nav.graph.has_node("Y")
        path, cost = self.nav.shortest_path("X", "Y")
        assert cost == 100

    def test_get_buildings(self):
        self.nav.add_node("Z", 11.56, 104.89)
        self.nav.add_node("A", 11.57, 104.90)
        buildings = self.nav.get_buildings()
        assert buildings == sorted(["Z", "A"])

    def test_bfs_path(self):
        self._make_three_node_graph()
        path, cost = self.nav.bfs("A", "C")
        assert path is not None
        assert path[0] == "A"
        assert path[-1] == "C"

    def test_dfs_path(self):
        self._make_three_node_graph()
        path, cost = self.nav.dfs("A", "C")
        assert path is not None
        assert path[0] == "A"
        assert path[-1] == "C"

    def test_dijkstra_path(self):
        self._make_three_node_graph()
        path, cost = self.nav.shortest_path("A", "C")
        assert path is not None
        assert cost < 2000

    def test_no_path(self):
        self.nav.add_node("A", 11.56, 104.89)
        self.nav.add_node("B", 11.57, 104.90)
        path, cost = self.nav.shortest_path("A", "B")
        assert path is None
        assert cost == float("inf")

    def test_show_campus_hierarchy(self):
        self.nav.add_node("A", 11.56, 104.89, category="Academic")
        hierarchy = self.nav.show_campus_hierarchy()
        assert "My Campus" in hierarchy
        assert "Academic" in hierarchy
        assert "A" in hierarchy

    def _make_three_node_graph(self):
        self.nav.add_node("A", 11.562, 104.891)
        self.nav.add_node("B", 11.563, 104.892)
        self.nav.add_node("C", 11.564, 104.893)
        self.nav.add_edge("A", "B")
        self.nav.add_edge("B", "C")


class TestGraphPersistence:
    def test_save_load_roundtrip(self, tmp_path):
        nav = Navigator()
        nav.add_node("A", 11.56, 104.89, category="Cat1")
        nav.add_node("B", 11.57, 104.90, category="Cat2")
        nav.add_edge("A", "B", 50)

        saved = nav.get_state()
        nav2 = Navigator()
        nav2.load_state(saved)

        assert nav2.hash_table.contains("A")
        assert nav2.hash_table.contains("B")
        assert nav2.hash_table.get("A")["category"] == "Cat1"
        path, cost = nav2.shortest_path("A", "B")
        assert cost == 50


class TestGraph:
    def test_add_node(self):
        g = Graph()
        g.add_node("A")
        assert g.has_node("A") is True

    def test_add_edge(self):
        g = Graph()
        g.add_edge("A", "B", 5)
        assert g.has_node("A") and g.has_node("B")
        assert g.get_neighbors("A") == [("B", 5)]

    def test_shortest_path_direct(self):
        g = Graph()
        g.add_edge("A", "B", 3)
        path, cost = g.shortest_path("A", "B")
        assert path == ["A", "B"]
        assert cost == 3

    def test_shortest_path_multi(self):
        g = Graph()
        g.add_edge("A", "B", 4)
        g.add_edge("B", "C", 3)
        g.add_edge("A", "C", 10)
        path, cost = g.shortest_path("A", "C")
        assert path == ["A", "B", "C"]
        assert cost == 7

    def test_no_path(self):
        g = Graph()
        g.add_node("A")
        g.add_node("B")
        path, cost = g.shortest_path("A", "B")
        assert path is None
        assert cost == float("inf")

    def test_remove_node(self):
        g = Graph()
        g.add_edge("A", "B", 2)
        g.remove_node("A")
        assert g.has_node("A") is False
        assert g.has_node("B") is True

    def test_bfs(self):
        g = Graph()
        g.add_edge("A", "B", 1)
        g.add_edge("B", "C", 1)
        path, _ = g.bfs("A", "C")
        assert path == ["A", "B", "C"]

    def test_dfs(self):
        g = Graph()
        g.add_edge("A", "B", 1)
        g.add_edge("B", "C", 1)
        path, _ = g.dfs("A", "C")
        assert path is not None
        assert path[0] == "A"
        assert path[-1] == "C"


class TestHashTable:
    def test_insert_and_get(self):
        ht = HashTable()
        ht.insert("A101", "Room A101")
        assert ht.get("A101") == "Room A101"

    def test_get_missing_key(self):
        ht = HashTable()
        with pytest.raises(KeyError):
            ht.get("nonexistent")

    def test_delete(self):
        ht = HashTable()
        ht.insert("key1", "val1")
        ht.delete("key1")
        assert ht.contains("key1") is False

    def test_contains(self):
        ht = HashTable()
        ht.insert("foo", "bar")
        assert ht.contains("foo") is True
        assert ht.contains("baz") is False

    def test_keys_and_values(self):
        ht = HashTable()
        ht.insert("a", 1)
        ht.insert("b", 2)
        assert set(ht.keys()) == {"a", "b"}
        assert set(ht.values()) == {1, 2}

    def test_len(self):
        ht = HashTable()
        assert len(ht) == 0
        ht.insert("x", 10)
        assert len(ht) == 1


class TestTree:
    def test_tree_node_add_child(self):
        root = TreeNode("Root")
        child = TreeNode("Child")
        root.add_child(child)
        assert child.parent == root
        assert child in root.children

    def test_get_path(self):
        root = TreeNode("Campus")
        b1 = TreeNode("B1")
        f1 = TreeNode("F1")
        r = TreeNode("R101")
        root.add_child(b1)
        b1.add_child(f1)
        f1.add_child(r)
        assert r.get_path() == ["Campus", "B1", "F1", "R101"]

    def test_find(self):
        root = TreeNode("Root")
        child = TreeNode("Target")
        root.add_child(child)
        tree = Tree(root)
        assert tree.find("Target") == child
        assert tree.find("Nope") is None

    def test_get_level(self):
        root = TreeNode("Root")
        c1 = TreeNode("C1")
        c2 = TreeNode("C2")
        root.add_child(c1)
        c1.add_child(c2)
        assert root.get_level() == 0
        assert c1.get_level() == 1
        assert c2.get_level() == 2

    def test_is_leaf(self):
        root = TreeNode("Root")
        leaf = TreeNode("Leaf")
        root.add_child(leaf)
        assert leaf.is_leaf() is True
        assert root.is_leaf() is False

    def test_get_all_nodes(self):
        root = TreeNode("Root")
        c1 = TreeNode("C1")
        c2 = TreeNode("C2")
        root.add_child(c1)
        root.add_child(c2)
        tree = Tree(root)
        assert len(tree.get_all_nodes()) == 3


class TestAPI:
    def setup_method(self):
        from frontend.app import app as flask_app
        flask_app.config["TESTING"] = True
        flask_app.STATE_FILE = "/tmp/test_graph_state.json"
        self.client = flask_app.test_client()
        self.client.post("/api/graph/load", json={"nodes": {}, "edges": []})

    def teardown_method(self):
        import os
        if os.path.exists("/tmp/test_graph_state.json"):
            os.remove("/tmp/test_graph_state.json")

    def _add_node(self, name, lat=11.56, lng=104.89):
        return self.client.post("/api/nodes", json={"name": name, "lat": lat, "lng": lng})

    def test_list_nodes_empty(self):
        r = self.client.get("/api/nodes")
        assert r.status_code == 200
        assert r.get_json() == {}

    def test_add_node(self):
        r = self._add_node("Library")
        assert r.status_code == 201
        data = r.get_json()
        assert data["name"] == "Library"

    def test_add_duplicate_node(self):
        self._add_node("A")
        r = self._add_node("A")
        assert r.status_code == 409

    def test_add_node_no_name(self):
        r = self.client.post("/api/nodes", json={"lat": 11.56, "lng": 104.89})
        assert r.status_code == 400

    def test_delete_node(self):
        self._add_node("A")
        r = self.client.delete("/api/nodes/A")
        assert r.status_code == 200

    def test_delete_missing_node(self):
        r = self.client.delete("/api/nodes/Nope")
        assert r.status_code == 404

    def test_update_node(self):
        self._add_node("A")
        r = self.client.put("/api/nodes/A", json={"lat": 11.57, "lng": 104.90})
        assert r.status_code == 200
        nodes = self.client.get("/api/nodes").get_json()
        assert nodes["A"]["lat"] == 11.57

    def test_rename_node(self):
        self._add_node("A")
        self._add_node("B")
        self.client.post("/api/edges", json={"from": "A", "to": "B", "weight": 10})
        r = self.client.put("/api/nodes/A", json={"new_name": "Alpha"})
        assert r.status_code == 200
        nodes = self.client.get("/api/nodes").get_json()
        assert "Alpha" in nodes
        assert "A" not in nodes
        g = self.client.get("/api/graph").get_json()
        edges = g["edges"]
        assert any(e["from"] == "Alpha" or e["to"] == "Alpha" for e in edges)

    def test_add_edge(self):
        self._add_node("A")
        self._add_node("B")
        r = self.client.post("/api/edges", json={"from": "A", "to": "B"})
        assert r.status_code == 201

    def test_add_edge_no_nodes(self):
        r = self.client.post("/api/edges", json={"from": "X", "to": "Y"})
        assert r.status_code == 400

    def test_delete_edge(self):
        self._add_node("A")
        self._add_node("B")
        self.client.post("/api/edges", json={"from": "A", "to": "B"})
        r = self.client.delete("/api/edges", json={"from": "A", "to": "B"})
        assert r.status_code == 200

    def test_find_path(self):
        self._add_node("A", 11.562, 104.891)
        self._add_node("B", 11.563, 104.892)
        self._add_node("C", 11.564, 104.893)
        self.client.post("/api/edges", json={"from": "A", "to": "B"})
        self.client.post("/api/edges", json={"from": "B", "to": "C"})
        r = self.client.post("/api/find_path", json={"start": "A", "end": "C", "algorithm": "dijkstra"})
        assert r.status_code == 200
        data = r.get_json()
        assert data["path"] == ["A", "B", "C"]
        assert data["cost"] > 0

    def test_find_path_no_route(self):
        self._add_node("A")
        self._add_node("B")
        r = self.client.post("/api/find_path", json={"start": "A", "end": "B"})
        assert r.status_code == 404

    def test_save_load_cycle(self):
        self._add_node("X", 11.56, 104.89)
        self._add_node("Y", 11.57, 104.90)
        self.client.post("/api/edges", json={"from": "X", "to": "Y", "weight": 99})
        # verify state file exists (auto-saved on CRUD)
        import os
        state_file = os.path.join(os.path.dirname(__file__), "..", "doc", "sample_campus.json")
        assert os.path.exists(state_file)
        # load into fresh nav by posting empty then loading
        self.client.post("/api/graph/load", json={"nodes": {}, "edges": []})
        empty = self.client.get("/api/graph").get_json()
        assert len(empty["nodes"]) == 0

    def test_get_graph(self):
        self._add_node("A")
        self._add_node("B")
        self.client.post("/api/edges", json={"from": "A", "to": "B", "weight": 50})
        r = self.client.get("/api/graph")
        data = r.get_json()
        assert len(data["nodes"]) == 2
        assert len(data["edges"]) == 1

    def test_update_node_category(self):
        self._add_node("A")
        r = self.client.put("/api/nodes/A", json={"category": "Academic"})
        assert r.status_code == 200
        nodes = self.client.get("/api/nodes").get_json()
        assert nodes["A"]["category"] == "Academic"
