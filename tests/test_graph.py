from src.navigation.graph import Graph


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
        assert cost == float('inf')

    def test_remove_node(self):
        g = Graph()
        g.add_edge("A", "B", 2)
        g.remove_node("A")
        assert g.has_node("A") is False
        assert g.has_node("B") is True
