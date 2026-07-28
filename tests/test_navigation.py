import pytest
from src.navigation import Navigator


@pytest.fixture
def nav():
    return Navigator()


def test_add_node(nav):
    nav.add_node("A", 11.5, 104.8, "Academic")
    assert nav.hash_table.contains("A")
    assert nav.hash_table.get("A")["lat"] == 11.5
    assert nav.hash_table.get("A")["category"] == "Academic"


def test_remove_node(nav):
    nav.add_node("A", 11.5, 104.8)
    nav.add_node("B", 11.6, 104.9)
    nav.add_edge("A", "B", 50)
    nav.remove_node("A")
    assert not nav.hash_table.contains("A")
    assert len(nav._edges) == 0


def test_update_node(nav):
    nav.add_node("A", 11.5, 104.8)
    nav.update_node("A", lat=20.0, lng=30.0, category="Admin")
    d = nav.hash_table.get("A")
    assert d["lat"] == 20.0
    assert d["lng"] == 30.0
    assert d["category"] == "Admin"


def test_rename_node_updates_edges(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    nav.add_edge("A", "B", 50)
    nav.update_node("A", new_name="A2")
    assert not nav.hash_table.contains("A")
    assert nav.hash_table.contains("A2")
    path, cost = nav.shortest_path("A2", "B")
    assert path == ["A2", "B"]
    assert cost == 50


def test_add_edge(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    assert nav.add_edge("A", "B", 100)
    state = nav.get_state()
    assert len(state["edges"]) == 1
    assert state["edges"][0]["weight"] == 100


def test_add_edge_missing_node(nav):
    nav.add_node("A", 0, 0)
    assert not nav.add_edge("A", "NONEXIST", 100)


def test_add_edge_with_path(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    path = [[0.1, 0.1], [0.2, 0.2]]
    assert nav.add_edge("A", "B", 100, path)
    state = nav.get_state()
    edge = state["edges"][0]
    assert edge["path"] == path
    assert edge["weight"] == 100


def test_remove_edge(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    nav.add_edge("A", "B", 50)
    assert nav.remove_edge("A", "B")
    assert len(nav._edges) == 0


def test_remove_edge_reverse_direction(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    nav.add_edge("A", "B", 50)
    assert nav.remove_edge("B", "A")
    assert len(nav._edges) == 0


def test_remove_nonexistent_edge(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    assert not nav.remove_edge("A", "B")


def test_shortest_path(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    nav.add_node("C", 2, 2)
    nav.add_edge("A", "B", 50)
    nav.add_edge("B", "C", 30)
    nav.add_edge("A", "C", 100)
    path, cost = nav.shortest_path("A", "C")
    assert path == ["A", "B", "C"]
    assert cost == 80


def test_shortest_path_no_route(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    path, cost = nav.shortest_path("A", "B")
    assert path is None
    assert cost == float("inf")


def test_shortest_path_missing_node(nav):
    nav.add_node("A", 0, 0)
    path, cost = nav.shortest_path("A", "NONEXIST")
    assert path is None


def test_bfs(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    nav.add_node("C", 2, 2)
    nav.add_edge("A", "B", 50)
    nav.add_edge("B", "C", 30)
    path, cost = nav.bfs("A", "C")
    assert path == ["A", "B", "C"]
    assert cost == 80


def test_dfs(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    nav.add_node("C", 2, 2)
    nav.add_edge("A", "B", 50)
    nav.add_edge("B", "C", 30)
    path, cost = nav.dfs("A", "C")
    assert path is not None


def test_get_state(nav):
    nav.add_node("A", 0, 0, "Test")
    nav.add_edge("A", "A", 0)
    state = nav.get_state()
    assert "nodes" in state
    assert "edges" in state
    assert state["nodes"]["A"]["category"] == "Test"


def test_load_state(nav):
    data = {
        "nodes": {"X": {"lat": 1, "lng": 2, "category": "Cat"}},
        "edges": [{"from": "X", "to": "X", "weight": 10}],
    }
    nav.load_state(data)
    assert nav.hash_table.contains("X")
    assert len(nav._edges) == 1


def test_load_state_clears_previous(nav):
    nav.add_node("OLD", 0, 0)
    data = {"nodes": {}, "edges": []}
    nav.load_state(data)
    assert not nav.hash_table.contains("OLD")


def test_load_state_preserves_paths(nav):
    data = {
        "nodes": {"A": {"lat": 0, "lng": 0}, "B": {"lat": 1, "lng": 1}},
        "edges": [{"from": "A", "to": "B", "weight": 50, "path": [[0.5, 0.5]]}],
    }
    nav.load_state(data)
    assert nav._edges[0]["path"] == [[0.5, 0.5]]


def test_hash_table_keys(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    keys = list(nav.hash_table.keys())
    assert "A" in keys
    assert "B" in keys
    assert len(keys) == 2


def test_hash_table_get(nav):
    nav.add_node("A", 0, 0, "Cat")
    assert nav.hash_table.get("A")["category"] == "Cat"
    assert nav.hash_table.get("NONEXIST") is None


def test_hash_table_contains(nav):
    nav.add_node("A", 0, 0)
    assert nav.hash_table.contains("A")
    assert not nav.hash_table.contains("NONEXIST")
