import json
import os
from flask import Flask, jsonify, request, render_template
from src.navigation import Navigator

app = Flask(__name__)
nav = Navigator()
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "doc", "state.json")


def _get_state_path():
    return app.config.get("STATE_FILE", STATE_FILE)


def _load_state():
    path = _get_state_path()
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
            if data.get("nodes"):
                nav.load_state(data)
                return True
    return False


def _save_state():
    path = _get_state_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(nav.get_state(), f, indent=2)


@app.route("/")
def index():
    _load_state()
    return render_template("index.html")


@app.route("/api/nodes", methods=["GET"])
def list_nodes():
    nodes = {}
    for name in nav.hash_table.keys():
        nodes[name] = nav.hash_table.get(name)
    return jsonify(nodes)


@app.route("/api/nodes", methods=["POST"])
def add_node():
    data = request.json
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name is required"}), 400
    lat = data.get("lat")
    lng = data.get("lng")
    if lat is None or lng is None:
        return jsonify({"error": "lat and lng are required"}), 400
    if nav.hash_table.contains(name):
        return jsonify({"error": "Node already exists"}), 409
    nav.add_node(name, lat, lng, data.get("category"))
    _save_state()
    return jsonify({"status": "ok", "name": name}), 201


@app.route("/api/nodes/<name>", methods=["DELETE"])
def delete_node(name):
    if not nav.hash_table.contains(name):
        return jsonify({"error": "Node not found"}), 404
    nav.remove_node(name)
    _save_state()
    return jsonify({"status": "ok"})


@app.route("/api/nodes/<name>", methods=["PUT"])
def update_node(name):
    if not nav.hash_table.contains(name):
        return jsonify({"error": "Node not found"}), 404
    data = request.json
    nav.update_node(
        name,
        lat=data.get("lat"),
        lng=data.get("lng"),
        new_name=data.get("new_name"),
        category=data.get("category"),
    )
    _save_state()
    return jsonify({"status": "ok"})


@app.route("/api/edges", methods=["POST"])
def add_edge():
    data = request.json
    from_name = data.get("from")
    to_name = data.get("to")
    if not from_name or not to_name:
        return jsonify({"error": "from and to are required"}), 400
    weight = data.get("weight")
    path = data.get("path")
    ok = nav.add_edge(from_name, to_name, weight, path)
    if not ok:
        return jsonify({"error": "Both nodes must exist"}), 400
    _save_state()
    return jsonify({"status": "ok"}), 201


@app.route("/api/edges", methods=["DELETE"])
def delete_edge():
    data = request.json
    from_name = data.get("from")
    to_name = data.get("to")
    if not from_name or not to_name:
        return jsonify({"error": "from and to are required"}), 400
    ok = nav.remove_edge(from_name, to_name)
    if not ok:
        return jsonify({"error": "Edge not found"}), 404
    _save_state()
    return jsonify({"status": "ok"})


@app.route("/api/junctions", methods=["GET"])
def list_junctions():
    return jsonify(nav._junctions)


@app.route("/api/junctions", methods=["POST"])
def add_junction():
    data = request.json
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name is required"}), 400
    lat = data.get("lat")
    lng = data.get("lng")
    if lat is None or lng is None:
        return jsonify({"error": "lat and lng are required"}), 400
    nav.add_junction(name, lat, lng)
    _save_state()
    return jsonify({"status": "ok", "name": name}), 201


@app.route("/api/junctions/<name>", methods=["DELETE"])
def delete_junction(name):
    if name not in nav._junctions:
        return jsonify({"error": "Junction not found"}), 404
    nav.remove_junction(name)
    _save_state()
    return jsonify({"status": "ok"})


@app.route("/api/junctions/<name>", methods=["PUT"])
def update_junction(name):
    if name not in nav._junctions:
        return jsonify({"error": "Junction not found"}), 404
    data = request.json
    nav.update_junction(
        name,
        lat=data.get("lat"),
        lng=data.get("lng"),
        new_name=data.get("new_name"),
    )
    _save_state()
    return jsonify({"status": "ok"})


@app.route("/api/walkways", methods=["GET"])
def list_walkways():
    return jsonify(nav._walkways)


@app.route("/api/walkways", methods=["POST"])
def add_walkway():
    data = request.json
    from_jct = data.get("from")
    to_jct = data.get("to")
    if not from_jct or not to_jct:
        return jsonify({"error": "from and to are required"}), 400
    path = data.get("path")
    ok = nav.add_walkway(from_jct, to_jct, path)
    if not ok:
        return jsonify({"error": "Both junctions must exist"}), 400
    _save_state()
    return jsonify({"status": "ok"}), 201


@app.route("/api/walkways", methods=["DELETE"])
def delete_walkway():
    data = request.json
    from_jct = data.get("from")
    to_jct = data.get("to")
    if not from_jct or not to_jct:
        return jsonify({"error": "from and to are required"}), 400
    ok = nav.remove_walkway(from_jct, to_jct)
    if not ok:
        return jsonify({"error": "Walkway not found"}), 404
    _save_state()
    return jsonify({"status": "ok"})


@app.route("/api/find_path", methods=["POST"])
def find_path():
    data = request.json
    start = data.get("start")
    end = data.get("end")
    path, cost = nav.shortest_path(start, end)
    if path:
        return jsonify({"path": path, "cost": round(cost), "algorithm": "dijkstra"})
    return jsonify({"path": None, "cost": None, "algorithm": "dijkstra", "error": "No path found"}), 404


@app.route("/api/graph", methods=["GET"])
def get_graph():
    return jsonify(nav.get_state())


@app.route("/api/graph/load", methods=["POST"])
def load_graph():
    data = request.json
    nav.load_state(data)
    _save_state()
    return jsonify({"status": "ok"})


@app.route("/api/graph/sample", methods=["GET"])
def get_sample():
    sample_path = os.path.join(os.path.dirname(__file__), "..", "doc", "sample_campus.json")
    if os.path.exists(sample_path):
        with open(sample_path) as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Sample not found"}), 404

@app.route("/api/graph/save", methods=["POST"])
def save_graph():
    state = nav.get_state()
    _save_state()
    num_nodes = len(state.get("nodes", {}))
    num_edges = len(state.get("edges", []))
    num_paths = sum(1 for e in state.get("edges", []) if e.get("path"))
    num_junctions = len(state.get("junctions", {}))
    num_walkways = len(state.get("walkways", []))
    return jsonify({
        "status": "ok",
        "path": os.path.abspath(_get_state_path()),
        "nodes": num_nodes,
        "edges": num_edges,
        "paths": num_paths,
        "junctions": num_junctions,
        "walkways": num_walkways,
    })


@app.route("/api/buildings", methods=["GET"])
def list_buildings():
    buildings = []
    for info in nav.building_info.get_all_buildings():
        buildings.append({
            "name": info.name,
            "category": info.category,
            "description": info.description,
            "services": info.services,
        })
    return jsonify(buildings)


@app.route("/api/buildings/<name>", methods=["GET"])
def get_building(name):
    info = nav.building_info.search(name)
    if not info:
        return jsonify({"error": "Building not found"}), 404
    return jsonify({
        "name": info.name,
        "category": info.category,
        "description": info.description,
        "services": info.services,
    })


@app.route("/api/categories", methods=["GET"])
def list_categories():
    cats = []
    for cat in nav.category_tree.get_categories():
        buildings = nav.category_tree.get_buildings_in_category(cat)
        cats.append({"name": cat, "buildings": buildings})
    return jsonify(cats)


@app.route("/api/tree/traversal/<traversal_type>", methods=["GET"])
def tree_traversal(traversal_type):
    if traversal_type == "pre":
        lines = nav.category_tree.pre_order()
    elif traversal_type == "post":
        lines = nav.category_tree.post_order()
    elif traversal_type == "level":
        lines = nav.category_tree.level_order()
    else:
        return jsonify({"error": "Invalid traversal type"}), 400
    return jsonify({"type": traversal_type, "lines": lines})


@app.route("/api/adjacency", methods=["GET"])
def get_adjacency():
    g = nav._build_graph()
    return jsonify(g.vertices)


if __name__ == "__main__":
    _load_state()
    app.run(debug=True, host="0.0.0.0", port=5000)
