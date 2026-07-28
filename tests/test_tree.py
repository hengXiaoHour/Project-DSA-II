from backend.tree import CategoryTree


class TestCategoryTree:
    def test_root(self):
        t = CategoryTree()
        assert t.root.name == "RUPP Campus"

    def test_categories(self):
        t = CategoryTree()
        cats = t.get_categories()
        assert "Academic Buildings" in cats
        assert "Services" in cats
        assert "Administration" in cats

    def test_academic_buildings(self):
        t = CategoryTree()
        buildings = t.get_buildings_in_category("Academic Buildings")
        assert len(buildings) == 7
        assert "Building A" in buildings
        assert "Building Stem" in buildings
        assert "CKCC" in buildings

    def test_services_buildings(self):
        t = CategoryTree()
        buildings = t.get_buildings_in_category("Services")
        assert len(buildings) == 3
        assert "Library" in buildings
        assert "NICC" in buildings
        assert "Canteen" in buildings

    def test_admin_buildings(self):
        t = CategoryTree()
        buildings = t.get_buildings_in_category("Administration")
        assert buildings == ["Study Office"]

    def test_category_not_found(self):
        t = CategoryTree()
        assert t.get_buildings_in_category("NONEXIST") == []

    def test_category_case_insensitive(self):
        t = CategoryTree()
        b1 = t.get_buildings_in_category("Academic Buildings")
        b2 = t.get_buildings_in_category("academic buildings")
        assert b1 == b2


class TestTraversals:
    def test_pre_order_length(self):
        t = CategoryTree()
        lines = t.pre_order()
        assert len(lines) == 15

    def test_pre_order_root_first(self):
        t = CategoryTree()
        lines = t.pre_order()
        assert lines[0] == "RUPP Campus"

    def test_post_order_root_last(self):
        t = CategoryTree()
        lines = t.post_order()
        assert lines[-1] == "RUPP Campus"

    def test_level_order_root_first(self):
        t = CategoryTree()
        lines = t.level_order()
        assert lines[0] == "RUPP Campus"

    def test_connectors_present(self):
        t = CategoryTree()
        for method in ["pre_order", "post_order", "level_order"]:
            lines = getattr(t, method)()
            text = "".join(lines)
            assert any(c in text for c in ["├", "└", "│"]), f"Missing connectors in {method}"
