from src.navigation.navigator import Navigator


class TestNavigator:
    def setup_method(self):
        self.nav = Navigator()

    def test_find_building(self):
        building = self.nav.find_building("Building A")
        assert building is not None
        assert building.name == "Building A"

    def test_find_building_library(self):
        building = self.nav.find_building("Library")
        assert building is not None
        assert building.name == "Library"

    def test_find_building_nicc(self):
        building = self.nav.find_building("NICC/CKCC")
        assert building is not None
        assert building.name == "NICC/CKCC"

    def test_bfs(self):
        path, cost = self.nav.bfs("Building A", "Building T")
        assert path is not None
        assert len(path) >= 2
        assert cost > 0
        assert path[0] == "Building A"
        assert path[-1] == "Building T"

    def test_dfs(self):
        path, cost = self.nav.dfs("Building A", "Building T")
        assert path is not None
        assert len(path) >= 2
        assert cost > 0

    def test_dijkstra(self):
        path, cost = self.nav.shortest_path("Building A", "Building T")
        assert path is not None
        assert len(path) >= 2
        assert cost > 0

    def test_no_path(self):
        self.nav.graph.remove_node("Building A")
        path, cost = self.nav.shortest_path("Building A", "Building T")
        assert path is None
        assert cost == float('inf')

    def test_get_buildings(self):
        buildings = self.nav.get_buildings()
        assert "Building A" in buildings
        assert "Library" in buildings
        assert "Entrance" in buildings
        assert len(buildings) == 11

    def test_campus_hierarchy(self):
        hierarchy = self.nav.show_campus_hierarchy()
        assert "RUPP Campus 1" in hierarchy
        assert "Building A" in hierarchy
        assert "Building B" in hierarchy
        assert "NICC/CKCC" in hierarchy