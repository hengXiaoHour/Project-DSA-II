import json
import os
from flask import Flask, jsonify, request, render_template
from src.navigation import Navigator

app = Flask(__name__)
nav = Navigator()
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "doc", "sample_campus.json")


def _load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            data = json.load(f)
            if data.get("nodes"):
                nav.load_state(data)
                return True
    return False


def _save_state():
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
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
    ok = nav.add_edge(from_name, to_name, weight)
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


@app.route("/api/find_path", methods=["POST"])
def find_path():
    data = request.json
    start = data.get("start")
    end = data.get("end")
    algorithm = data.get("algorithm", "dijkstra")

    if algorithm == "bfs":
        path, cost = nav.bfs(start, end)
    elif algorithm == "dfs":
        path, cost = nav.dfs(start, end)
    else:
        path, cost = nav.shortest_path(start, end)

    if path:
        return jsonify({"path": path, "cost": cost, "algorithm": algorithm})
    return jsonify({"path": None, "cost": None, "algorithm": algorithm, "error": "No path found"}), 404


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
    _save_state()
    return jsonify({"status": "ok", "path": os.path.abspath(STATE_FILE)})


if __name__ == "__main__":
    _load_state()
    app.run(debug=True, host="0.0.0.0", port=5000)
