import json
import pytest
from frontend.app import app


@pytest.fixture(autouse=True)
def reset_state():
    from frontend.app import nav
    nav._nodes.clear()
    nav._walkways.clear()
    yield
    nav._nodes.clear()
    nav._walkways.clear()


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["STATE_FILE"] = str(tmp_path / "test_state.json")
    with app.test_client() as c:
        c.post("/api/graph/load", json={"nodes": {}, "walkways": []})
        yield c


class TestGraphAPI:
    def test_get_graph_empty(self, client):
        resp = client.get("/api/graph")
        d = resp.get_json()
        assert d["nodes"] == {}
        assert d["walkways"] == []

    def test_add_node(self, client):
        resp = client.post("/api/nodes", json={"name": "X", "lat": 1, "lng": 2})
        assert resp.status_code == 201
        d = client.get("/api/graph").get_json()
        assert "X" in d["nodes"]

    def test_add_node_duplicate(self, client):
        client.post("/api/nodes", json={"name": "X", "lat": 1, "lng": 2})
        resp = client.post("/api/nodes", json={"name": "X", "lat": 3, "lng": 4})
        assert resp.status_code == 409

    def test_add_node_missing_name(self, client):
        resp = client.post("/api/nodes", json={"lat": 1, "lng": 2})
        assert resp.status_code == 400

    def test_delete_node(self, client):
        client.post("/api/nodes", json={"name": "X", "lat": 1, "lng": 2})
        resp = client.delete("/api/nodes/X")
        assert resp.status_code == 200
        d = client.get("/api/graph").get_json()
        assert "X" not in d["nodes"]

    def test_delete_nonexistent_node(self, client):
        resp = client.delete("/api/nodes/NONEXIST")
        assert resp.status_code == 404

    def test_update_node(self, client):
        client.post("/api/nodes", json={"name": "X", "lat": 1, "lng": 2})
        resp = client.put("/api/nodes/X", json={"lat": 10, "lng": 20, "category": "New"})
        assert resp.status_code == 200
        d = client.get("/api/nodes").get_json()
        assert d["X"]["lat"] == 10
        assert d["X"]["category"] == "New"

    def test_add_walkway(self, client):
        resp = client.post("/api/walkways", json={"points": [[0, 0], [1, 1]]})
        assert resp.status_code == 201
        d = client.get("/api/graph").get_json()
        assert len(d["walkways"]) == 1

    def test_add_walkway_too_few_points(self, client):
        resp = client.post("/api/walkways", json={"points": [[0, 0]]})
        assert resp.status_code == 400

    def test_delete_walkway(self, client):
        resp = client.post("/api/walkways", json={"points": [[0, 0], [1, 1]]})
        name = resp.get_json()["name"]
        resp = client.delete(f"/api/walkways/{name}")
        assert resp.status_code == 200
        d = client.get("/api/graph").get_json()
        assert len(d["walkways"]) == 0

    def test_delete_nonexistent_walkway(self, client):
        resp = client.delete("/api/walkways/NOPE")
        assert resp.status_code == 404

    def test_find_path_no_walkways(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 1, "lng": 1})
        resp = client.post("/api/find_path", json={"start": "A", "end": "B"})
        assert resp.status_code == 404

    def test_find_path_with_walkway(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 0.01, "lng": 0.01})
        client.post("/api/walkways", json={"points": [[0, 0], [0.005, 0.005], [0.01, 0.01]]})
        resp = client.post("/api/find_path", json={"start": "A", "end": "B"})
        d = resp.get_json()
        assert resp.status_code == 200
        assert "A" in d["path"]
        assert "B" in d["path"]
        assert d["cost"] >= 0

    def test_find_path_missing_node(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        resp = client.post("/api/find_path", json={"start": "A", "end": "NONEXIST"})
        assert resp.status_code == 404


class TestSaveLoad:
    def test_save_graph(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        resp = client.post("/api/graph/save")
        assert resp.status_code == 200
        d = resp.get_json()
        assert d["nodes"] == 1
        assert d["walkways"] == 0
        assert d["status"] == "ok"

    def test_load_save_cycle(self, client):
        state = {"nodes": {"X": {"lat": 5, "lng": 10}}, "walkways": []}
        client.post("/api/graph/load", json=state)
        d = client.get("/api/graph").get_json()
        assert d["nodes"]["X"]["lat"] == 5

    def test_load_clears_previous(self, client):
        client.post("/api/nodes", json={"name": "OLD", "lat": 0, "lng": 0})
        client.post("/api/graph/load", json={"nodes": {}, "walkways": []})
        d = client.get("/api/graph").get_json()
        assert "OLD" not in d["nodes"]


class TestBuildingInfo:
    def test_list_buildings(self, client):
        resp = client.get("/api/buildings")
        d = resp.get_json()
        assert len(d) == 12
        names = [b["name"] for b in d]
        assert "Library" in names

    def test_get_building(self, client):
        resp = client.get("/api/buildings/Library")
        d = resp.get_json()
        assert d["name"] == "Library"
        assert d["category"] == "Service"
        assert "Books" in d["services"]

    def test_get_building_not_found(self, client):
        resp = client.get("/api/buildings/NONEXIST")
        assert resp.status_code == 404

    def test_list_categories(self, client):
        resp = client.get("/api/categories")
        cats = resp.get_json()
        names = [c["name"] for c in cats]
        assert "Academic Buildings" in names
        assert "Services" in names
        assert "Administration" in names

    def test_categories_have_buildings(self, client):
        resp = client.get("/api/categories")
        cats = resp.get_json()
        academic = [c for c in cats if c["name"] == "Academic Buildings"][0]
        assert len(academic["buildings"]) == 7
        assert "Building A" in academic["buildings"]


class TestTree:
    def test_pre_order(self, client):
        resp = client.get("/api/tree/traversal/pre")
        d = resp.get_json()
        assert d["type"] == "pre"
        assert len(d["lines"]) == 15
        assert "RUPP Campus" in d["lines"][0]

    def test_post_order(self, client):
        resp = client.get("/api/tree/traversal/post")
        d = resp.get_json()
        assert d["type"] == "post"

    def test_level_order(self, client):
        resp = client.get("/api/tree/traversal/level")
        d = resp.get_json()
        assert d["type"] == "level"

    def test_invalid_traversal(self, client):
        resp = client.get("/api/tree/traversal/invalid")
        assert resp.status_code == 400

    def test_traversal_has_connectors(self, client):
        for t in ["pre", "post", "level"]:
            resp = client.get(f"/api/tree/traversal/{t}")
            d = resp.get_json()
            text = "".join(d["lines"])
            assert any(c in text for c in ["├", "└", "│"]), f"Missing connectors in {t}"


class TestAdjacency:
    def test_adjacency(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 0.001, "lng": 0.001})
        client.post("/api/walkways", json={"points": [[0, 0], [0.001, 0.001]]})
        resp = client.get("/api/adjacency")
        adj = resp.get_json()
        assert "A" in adj
        assert "B" in adj
