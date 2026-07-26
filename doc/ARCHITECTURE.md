# System Architecture — Interactive Graph Editor + Navigator

## Overview

A web-based interactive graph builder and pathfinding visualizer. Users build a graph by clicking on a map, connect nodes with edges, and run Dijkstra/BFS/DFS — all three DSA layers operate on the user's live data.

---

## Project Structure

```
Project-DSA-II/
├── main.py                         # Flask entry point
├── setup/
│   └── requirements.txt            # Python dependencies
├── src/
│   └── navigation/
│       ├── __init__.py
│       ├── campus_data.py          # Empty state builder (data now user-created)
│       ├── graph.py                # Graph ADT (adjacency list)
│       │   ├── add_node / add_edge / remove_node / remove_edge
│       │   ├── bfs / dfs / shortest_path (Dijkstra)
│       │   └── get_neighbors / has_node / __len__
│       ├── hashtable.py            # HashTable with chaining
│       │   ├── insert / get / delete / contains
│       │   └── keys / values / __len__
│       ├── models.py               # Building/Floor/Room (legacy)
│       ├── navigator.py            # CRUD orchestration + Haversine
│       │   ├── add/remove/update node
│       │   ├── add/remove edge (auto Haversine distance)
│       │   ├── get_state / load_state (persistence)
│       │   └── bfs / dfs / shortest_path
│       └── tree.py                 # TreeNode + Tree (category hierarchy)
├── frontend/
│   ├── app.py                      # Flask REST API
│   │   ├── /api/nodes              # GET/POST/DELETE/PUT
│   │   ├── /api/edges              # POST/DELETE
│   │   ├── /api/find_path          # BFS/DFS/Dijkstra
│   │   └── /api/graph/*            # load/save/sample
│   └── templates/
│       └── index.html              # Leaflet graph editor UI
│           ├── Move / +Node / +Edge / Delete modes
│           ├── Google Maps-style pin markers
│           ├── Edge labels with real Haversine distance
│           └── Color-coded path highlighting
├── tests/
│   ├── test_navigator.py           # 60 tests (Navigator, Graph, HashTable, Tree, API)
│   └── test_ui.py                  # 8 Playwright UI tests
├── doc/
│   ├── ARCHITECTURE.md
│   ├── sample_campus.json          # RUPP preset + persistent state
│   └── opencode_agent/             # Agent cross-session context
└── .workflow/                      # Agent internal
```

---

## Three DSA Layers

### 1. Graph (`src/navigation/graph.py`)
- Adjacency list representation
- **Dijkstra** (shortest_path) — priority queue, O((V+E) log V)
- **BFS** — queue-based, unweighted shortest path
- **DFS** — stack-based, pathfinding
- Edge weights are real distances (Haversine)

### 2. HashTable (`src/navigation/hashtable.py`)
- Chaining collision resolution
- O(1) average lookup for node metadata
- Stores name, lat, lng, category for each node

### 3. Tree (`src/navigation/tree.py`)
- TreeNode with parent/children
- Categories automatically organize nodes into hierarchy
- `find`, `get_path`, `get_level`, `get_all_nodes`

---

## Data Flow

```
User clicks map  →  Leaflet click event
                         ↓
              Fetch API (POST /api/nodes)
                         ↓
              Navigator.add_node()
                  ├── HashTable.insert(name → metadata)
                  ├── Graph.add_node(name)
                  └── Tree (category → node)
                         ↓
              _save_state() → doc/sample_campus.json
                         ↓
              loadGraphFromApi() → re-render map
```

Pathfinding flow:
```
User selects start/end + algo → POST /api/find_path
                                      ↓
                              Navigator.shortest_path()
                                      ↓
                              Graph.dijkstra()
                                      ↓
                              Return path + cost
                                      ↓
                              Highlight path on map
```

---

## Key Decisions

| Decision | Why |
|---|---|
| No hardcoded data | User builds graph from scratch via map |
| Haversine distances | Real distance from lat/lng, no fake numbers |
| Auto-save on every change | State survives server restart |
| Pin icons over circles | Google Maps-style, visually clearer |
| Categories → Tree | Auto-organizes nodes into hierarchy |
| `setup/requirements.txt` | Dependencies in dedicated setup folder |
