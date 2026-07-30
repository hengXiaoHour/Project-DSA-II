# Project Architecture

```
Project-DSA-II/
├── backend/                    # Core DSA layer implementations
│   ├── graph.py                # Graph (adjacency list, Dijkstra, BFS/DFS)
│   ├── hash_table.py           # Hash Table (O(1) building lookup)
│   └── tree.py                 # Category Tree (pre/post/level-order traversal)
│
├── frontend/                   # Web UI (Flask + Leaflet)
│   ├── app.py                  # Flask API endpoints
│   ├── templates/
│   │   └── index.html          # Single-page UI (map, tabs, toolbar)
│   └── static/                 # (optional static assets)
│
├── src/
│   └── navigation.py           # Navigator — integrates Graph + HashTable + Tree
│
├── tests/                      # Pytest test suite (91 tests)
│   ├── test_graph.py
│   ├── test_hash_table.py
│   ├── test_tree.py
│   ├── test_navigation.py
│   └── test_api.py
│
├── setup/                       # One-liner install scripts
│   ├── install.sh               # Linux/macOS (curl | bash)
│   └── install.ps1              # Windows PowerShell
│
├── script_dev/                  # Dev helper scripts
│   ├── push.py                  # git add + commit + push to V2
│   └── pull.py                  # git pull from V2
│
├── doc/                         # Data & docs
│   ├── state.json               # Current campus state (auto-saved)
│   ├── sample_campus.json       # Default sample campus data
│   └── ARCHITECTURE.md          # This file
│
├── main.py                      # Entry point
├── requirements.txt             # Flask, pytest, playwright
└── README.md
```

## Three DSA Layers

| Layer | File | Purpose | Operations |
|---|---|---|---|
| **Graph** | `backend/graph.py` | Campus path network | Dijkstra, BFS, DFS, adjacency list |
| **Hash Table** | `backend/hash_table.py` | O(1) building info lookup | insert, search, get_all |
| **Tree** | `backend/tree.py` | Category hierarchy | pre-order, post-order, level-order |

## Data Flow

```
User clicks map/tabs
        ↓
Frontend (index.html) ──fetch──→ Flask API (app.py)
        ↓                              ↓
   Leaflet map                   Navigator (navigation.py)
   + sidebar                           ↓
                                  Graph + HashTable + Tree
                                  (backend/ directory)
```

## UI Tabs

| Tab | Content | DSA Layer |
|---|---|---|
| **Nodes** | Building list with categories | Hash Table |
| **Info** | Building details (description, services) | Hash Table |
| **Tree** | Category tree traversals | Tree |
| **Graph** | Adjacency list (dropdown filter) | Graph |

## Toolbar

- **Navigation mode** (default): From→To selectors, Dijkstra [Go], Network/Edges toggles
- **Edit Mode toggle**: Enables dropdown with move/+node/-node/+joint/-joint/+path/-path/clear/save/sample/load
