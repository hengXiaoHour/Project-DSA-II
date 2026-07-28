import json
import pytest
from frontend.app import app


@pytest.fixture(autouse=True)
def reset_state():
    from frontend.app import nav
    nav._nodes.clear()
    nav._edges.clear()
    yield
    nav._nodes.clear()
    nav._edges.clear()


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["STATE_FILE"] = str(tmp_path / "test_state.json")
    with app.test_client() as c:
        c.post("/api/graph/load", json={"nodes": {}, "edges": []})
        yield c


def load_sample(c):
    resp = c.get("/api/graph/sample")
    assert resp.status_code == 200
    c.post("/api/graph/load", json=resp.get_json())


class TestGraphAPI:
    def test_get_graph_empty(self, client):
        resp = client.get("/api/graph")
        d = resp.get_json()
        assert d["nodes"] == {}
        assert d["edges"] == []
        assert d["junctions"] == {}
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

    def test_add_edge(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 1, "lng": 1})
        resp = client.post("/api/edges", json={"from": "A", "to": "B", "weight": 50})
        assert resp.status_code == 201

    def test_add_edge_with_path(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 1, "lng": 1})
        path = [[0.2, 0.2], [0.5, 0.5]]
        resp = client.post("/api/edges", json={"from": "A", "to": "B", "weight": 50, "path": path})
        assert resp.status_code == 201
        d = client.get("/api/graph").get_json()
        edge = [e for e in d["edges"] if e.get("path")]
        assert len(edge) == 1
        assert edge[0]["path"] == path

    def test_add_edge_missing_node(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        resp = client.post("/api/edges", json={"from": "A", "to": "NONEXIST"})
        assert resp.status_code == 400

    def test_delete_edge(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 1, "lng": 1})
        client.post("/api/edges", json={"from": "A", "to": "B", "weight": 50})
        resp = client.delete("/api/edges", json={"from": "A", "to": "B"})
        assert resp.status_code == 200
        d = client.get("/api/graph").get_json()
        assert len(d["edges"]) == 0

    def test_delete_edge_reverse(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 1, "lng": 1})
        client.post("/api/edges", json={"from": "A", "to": "B", "weight": 50})
        resp = client.delete("/api/edges", json={"from": "B", "to": "A"})
        assert resp.status_code == 200

    def test_delete_nonexistent_edge(self, client):
        resp = client.delete("/api/edges", json={"from": "NOPE", "to": "NOPE"})
        assert resp.status_code == 404

    def test_find_path_dijkstra(self, client):
        load_sample(client)
        resp = client.post("/api/find_path", json={"start": "Library", "end": "Building Stem"})
        d = resp.get_json()
        assert d["path"] == ["Library", "CKCC", "Building D", "Building Stem"]
        assert d["cost"] == 214
        assert d["algorithm"] == "dijkstra"

    def test_find_path_no_route(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 1, "lng": 1})
        resp = client.post("/api/find_path", json={"start": "A", "end": "B"})
        assert resp.status_code == 404

    def test_find_path_missing_node(self, client):
        load_sample(client)
        resp = client.post("/api/find_path", json={"start": "Library", "end": "NONEXIST"})
        assert resp.status_code == 404


class TestSaveLoad:
    def test_save_graph(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        resp = client.post("/api/graph/save")
        assert resp.status_code == 200
        d = resp.get_json()
        assert d["nodes"] == 1
        assert d["edges"] == 0
        assert d["status"] == "ok"

    def test_save_with_paths(self, client):
        client.post("/api/nodes", json={"name": "A", "lat": 0, "lng": 0})
        client.post("/api/nodes", json={"name": "B", "lat": 1, "lng": 1})
        client.post("/api/edges", json={"from": "A", "to": "B", "weight": 50, "path": [[0.5, 0.5]]})
        resp = client.post("/api/graph/save")
        d = resp.get_json()
        assert d["nodes"] == 2
        assert d["edges"] == 1
        assert d["paths"] == 1

    def test_load_save_cycle(self, client):
        state = {"nodes": {"X": {"lat": 5, "lng": 10}}, "edges": []}
        client.post("/api/graph/load", json=state)
        d = client.get("/api/graph").get_json()
        assert d["nodes"]["X"]["lat"] == 5

    def test_load_sample(self, client):
        resp = client.get("/api/graph/sample")
        assert resp.status_code == 200
        d = resp.get_json()
        assert len(d["nodes"]) == 12
        assert len(d["edges"]) == 17

    def test_load_clears_previous(self, client):
        client.post("/api/nodes", json={"name": "OLD", "lat": 0, "lng": 0})
        client.post("/api/graph/load", json={"nodes": {}, "edges": []})
        d = client.get("/api/graph").get_json()
        assert "OLD" not in d["nodes"]


class TestBuildingInfo:
    def test_list_buildings(self, client):
        load_sample(client)
        resp = client.get("/api/buildings")
        d = resp.get_json()
        assert len(d) == 12
        names = [b["name"] for b in d]
        assert "Library" in names

    def test_get_building(self, client):
        load_sample(client)
        resp = client.get("/api/buildings/Library")
        d = resp.get_json()
        assert d["name"] == "Library"
        assert d["category"] == "Service"
        assert "Books" in d["services"]

    def test_get_building_not_found(self, client):
        resp = client.get("/api/buildings/NONEXIST")
        assert resp.status_code == 404

    def test_list_categories(self, client):
        load_sample(client)
        resp = client.get("/api/categories")
        cats = resp.get_json()
        names = [c["name"] for c in cats]
        assert "Academic Buildings" in names
        assert "Services" in names
        assert "Administration" in names

    def test_categories_have_buildings(self, client):
        load_sample(client)
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
        load_sample(client)
        resp = client.get("/api/adjacency")
        adj = resp.get_json()
        assert len(adj) == 12
        assert "Library" in adj
        assert len(adj["Library"]) >= 3

    def test_adjacency_includes_weight(self, client):
        load_sample(client)
        resp = client.get("/api/adjacency")
        adj = resp.get_json()
        lib_edges = adj["Library"]
        weights = [w for _, w in lib_edges]
        assert all(isinstance(w, (int, float)) for w in weights)
