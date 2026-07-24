from src.navigation.navigator import Navigator


class TestNavigator:
    def setup_method(self):
        self.nav = Navigator()

    def test_find_room(self):
        room = self.nav.find_room("A101")
        assert room is not None
        assert room.room_id == "A101"

    def test_find_building(self):
        building = self.nav.find_building("A")
        assert building is not None
        assert building.building_id == "A"

    def test_find_floor(self):
        floor = self.nav.find_floor("A1")
        assert floor is not None
        assert floor.floor_id == "A1"

    def test_shortest_path_same_building(self):
        path, cost = self.nav.shortest_path("A101", "A103")
        assert path is not None
        assert len(path) >= 2
        assert cost > 0

    def test_shortest_path_across_buildings(self):
        path, cost = self.nav.shortest_path("A101", "B103")
        assert path is not None
        assert len(path) >= 2

    def test_campus_hierarchy(self):
        hierarchy = self.nav.show_campus_hierarchy()
        assert "RUPP Campus 1" in hierarchy
        assert "Building A" in hierarchy
        assert "Building B" in hierarchy
