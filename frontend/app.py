from flask import Flask, jsonify, request, render_template
from src.navigation import Navigator

app = Flask(__name__)
nav = Navigator()

edges_data = [
    ("NICC/CKCC", "Building D", 64),
    ("NICC/CKCC", "Library", 115),
    ("Library", "Building A", 80),
    ("Building D", "Building B", 50),
    ("Building D", "Building Stem", 50),
    ("Building B", "Building Stem", 50),
    ("Building Stem", "Building C", 115),
    ("Building Stem", "Study Office", 85),
    ("Building C", "Building T", 35),
    ("Building C", "Canteen", 115),
    ("Building T", "Canteen", 115),
    ("Study Office", "Canteen", 35),
    ("Canteen", "Building A", 115),
    ("Study Office", "Building A", 115),
    ("Building A", "Entrance", 115),
]


@app.route("/")
def index():
    buildings = nav.get_buildings()
    return render_template("index.html", buildings=buildings, edges=edges_data)


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


@app.route("/api/graph")
def get_graph():
    buildings = nav.get_buildings()
    return jsonify({"buildings": buildings, "edges": edges_data})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)