import pytest
from backend.graph import Graph


@pytest.fixture
def g():
    return Graph()


def test_add_vertex(g):
    g.add_vertex("A")
    assert "A" in g.vertices


def test_add_edge_creates_vertices(g):
    g.add_edge("A", "B", 10)
    assert "A" in g.vertices
    assert "B" in g.vertices


def test_add_edge_undirected(g):
    g.add_edge("A", "B", 10)
    assert ("B", 10) in g.vertices["A"]
    assert ("A", 10) in g.vertices["B"]


def test_dijkstra(g):
    g.add_edge("A", "B", 5)
    g.add_edge("B", "C", 3)
    g.add_edge("A", "C", 10)
    path, dist = g.dijkstra("A", "C")
    assert path == ["A", "B", "C"]
    assert dist == 8


def test_dijkstra_direct_path(g):
    g.add_edge("A", "B", 7)
    path, dist = g.dijkstra("A", "B")
    assert path == ["A", "B"]
    assert dist == 7


def test_dijkstra_no_path(g):
    g.add_vertex("A")
    g.add_vertex("B")
    path, dist = g.dijkstra("A", "B")
    assert path is None
    assert dist == float("inf")


def test_dijkstra_same_node(g):
    g.add_vertex("A")
    path, dist = g.dijkstra("A", "A")
    assert path == ["A"]
    assert dist == 0


def test_build_campus_graph():
    g = Graph.build_campus_graph()
    assert len(g.vertices) == 12
    assert "Library" in g.vertices
    assert "Building Stem" in g.vertices


def test_campus_dijkstra():
    g = Graph.build_campus_graph()
    path, dist = g.dijkstra("Library", "Building Stem")
    assert path == ["Library", "CKCC", "Building D", "Building Stem"]
    assert dist == 214


def test_campus_entrance_to_t():
    g = Graph.build_campus_graph()
    path, dist = g.dijkstra("Entrance", "Building T")
    assert dist == 555


def test_campus_b_to_library():
    g = Graph.build_campus_graph()
    path, dist = g.dijkstra("Building B", "Library")
    assert dist == 214


def test_duplicate_vertex(g):
    g.add_vertex("A")
    g.add_vertex("A")
    assert len(g.vertices) == 1
