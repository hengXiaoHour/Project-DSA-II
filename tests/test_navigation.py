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
    nav.add_walkway([[11.5, 104.8], [11.6, 104.9]])
    nav.remove_node("A")
    assert not nav.hash_table.contains("A")


def test_update_node(nav):
    nav.add_node("A", 11.5, 104.8)
    nav.update_node("A", lat=20.0, lng=30.0, category="Admin")
    d = nav.hash_table.get("A")
    assert d["lat"] == 20.0
    assert d["lng"] == 30.0
    assert d["category"] == "Admin"


def test_add_walkway(nav):
    name = nav.add_walkway([[0, 0], [1, 1]])
    assert name is not None
    state = nav.get_state()
    assert len(state["walkways"]) == 1


def test_add_walkway_custom_name(nav):
    name = nav.add_walkway([[0, 0], [1, 1]], "MyPath")
    assert name == "MyPath"


def test_remove_walkway(nav):
    name = nav.add_walkway([[0, 0], [1, 1]])
    assert nav.remove_walkway(name)
    assert len(nav._walkways) == 0


def test_remove_nonexistent_walkway(nav):
    assert not nav.remove_walkway("NOPE")


def test_shortest_path(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 0.001, 0.001)
    nav.add_node("C", 0.002, 0.002)
    nav.add_walkway([[0, 0], [0.001, 0.001], [0.002, 0.002]])
    path, cost = nav.shortest_path("A", "C")
    assert path is not None
    assert "A" in path
    assert "C" in path
    assert cost >= 0


def test_shortest_path_no_walkways(nav):
    nav.add_node("A", 0, 0)
    nav.add_node("B", 1, 1)
    path, cost = nav.shortest_path("A", "B")
    assert path is None
    assert cost == float("inf")


def test_shortest_path_missing_node(nav):
    nav.add_node("A", 0, 0)
    path, cost = nav.shortest_path("A", "NONEXIST")
    assert path is None


def test_get_state(nav):
    nav.add_node("A", 0, 0, "Test")
    nav.add_walkway([[0, 0], [1, 1]])
    state = nav.get_state()
    assert "nodes" in state
    assert "walkways" in state
    assert state["nodes"]["A"]["category"] == "Test"
    assert len(state["walkways"]) == 1


def test_load_state(nav):
    data = {
        "nodes": {"X": {"lat": 1, "lng": 2, "category": "Cat"}},
        "walkways": [{"name": "W1", "points": [[0, 0], [1, 1]], "weight": 157}],
    }
    nav.load_state(data)
    assert nav.hash_table.contains("X")
    assert len(nav._walkways) == 1


def test_load_state_clears_previous(nav):
    nav.add_node("OLD", 0, 0)
    data = {"nodes": {}, "walkways": []}
    nav.load_state(data)
    assert not nav.hash_table.contains("OLD")


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
