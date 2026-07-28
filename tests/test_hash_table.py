from backend.hash_table import BuildingHashTable, BuildingInfo


class TestBuildingInfo:
    def test_create(self):
        b = BuildingInfo("A", "Academic", "desc", ["Svc1", "Svc2"])
        assert b.name == "A"
        assert b.category == "Academic"
        assert b.services == ["Svc1", "Svc2"]

    def test_services_as_single_string(self):
        b = BuildingInfo("A", "Cat", "desc", "Single")
        assert b.services == ["Single"]


class TestBuildingHashTable:
    def test_populated(self):
        ht = BuildingHashTable()
        assert len(ht.table) > 0

    def test_search_exact(self):
        ht = BuildingHashTable()
        info = ht.search("Library")
        assert info is not None
        assert info.name == "Library"
        assert info.category == "Service"

    def test_search_case_insensitive(self):
        ht = BuildingHashTable()
        info = ht.search("library")
        assert info is not None
        assert info.name == "Library"

    def test_search_not_found(self):
        ht = BuildingHashTable()
        assert ht.search("NonExistent") is None

    def test_get_all_buildings(self):
        ht = BuildingHashTable()
        all_b = ht.get_all_buildings()
        assert len(all_b) == 12

    def test_all_categories_present(self):
        ht = BuildingHashTable()
        cats = {b.category for b in ht.get_all_buildings()}
        assert "Academic" in cats
        assert "Service" in cats
        assert "Administration" in cats
        assert "Access Point" in cats

    def test_building_a(self):
        ht = BuildingHashTable()
        info = ht.search("Building A")
        assert info.category == "Academic"

    def test_canteen(self):
        ht = BuildingHashTable()
        info = ht.search("Canteen")
        assert info.category == "Service"
        assert "Food" in info.services

    def test_study_office(self):
        ht = BuildingHashTable()
        info = ht.search("Study Office")
        assert info.category == "Administration"

    def test_entrance(self):
        ht = BuildingHashTable()
        info = ht.search("Entrance")
        assert info.category == "Access Point"
