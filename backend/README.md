# Smart Building Mapping and Navigation System for RUPP Campus 1

**Using Graphs, Hash Tables, and Trees**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Data Structure 1: Graph — Navigation Layer](#data-structure-1-graph--navigation-layer)
4. [Data Structure 2: Hash Table — Information Layer](#data-structure-2-hash-table--information-layer)
5. [Data Structure 3: Tree — Categorization Layer](#data-structure-3-tree--categorization-layer)
6. [How They Work Together](#how-they-work-together)
7. [Complexity Analysis](#complexity-analysis)
8. [Test Cases & Verification](#test-cases--verification)
9. [Sample Program Output](#sample-program-output)
10. [How to Run](#how-to-run)

---

## Project Overview

This project implements a **Smart Building Mapping and Navigation System** for the Royal University of Phnom Penh (RUPP) Campus 1. It demonstrates the practical application of three fundamental data structures working in concert:

| Data Structure | Role | Purpose |
|---------------|------|---------|
| **Graph** | Navigation Layer | Finding shortest paths between buildings |
| **Hash Table** | Information Layer | O(1) lookup of building details |
| **Tree** | Categorization Layer | Hierarchical browsing by category |

The program provides a CLI menu-driven interface allowing users to search building information, browse locations by category, and find the shortest path between any two campus locations.

---

## System Overview

```
                            ┌─────────┐
                            │  RUPP   │
                            │ Campus  │
                            └────┬────┘
                                 │
                                 ▼
                        ┌──────────────────────┐
                        │   Data Collection    │
                        │  (12 Buildings, 17   │
                        │   Weighted Edges,    │
                        │   Categories, Desc)  │
                        └─────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
┌─────────────────────────┐ ┌─────────────────────┐ ┌──────────────────────┐
│  GRAPH (Navigation)     │ │  TREE (Categorize)  │ │  HASH TABLE (Lookup) │
│  ────────────────────   │ │  ────────────────   │ │  ──────────────────  │
│                         │ │                     │ │                      │
│ PURPOSE:                │ │ PURPOSE:            │ │ PURPOSE:             │
│ Model campus pathways   │ │ Organize buildings  │ │ Store & retrieve     │
│ as a weighted network   │ │ by category tree    │ │ building info by     │
│ for shortest route      │ │ for filtered browse │ │ name in O(1) time    │
│                         │ │                     │ │                      │
│ STRUCTURE:              │ │ STRUCTURE:          │ │ STRUCTURE:           │
│ • Adjacency list        │ │ • N-ary tree        │ │ • Python dict        │
│   (dict of lists)       │ │   (multi-way tree)  │ │   (hash table)       │
│ • 12 vertices, 17 edges │ │ • 1 root node       │ │ • BuildingInfo       │
│                         │ │ • 3 category nodes  │ │   objects as values  │
│ ALGORITHMS:             │ │ • 11 building leaves│ │                      │
│ • Dijkstra's algo       │ │                     │ │ ALGORITHMS:          │
│   (shortest path)       │ │ ALGORITHMS:         │ │ • Hash function:     │
│ • Priority queue (heap) │ │ • Pre-order         │ │   built-in hash()    │
│   for min-distance      │ │ • Post-order        │ │ • Collision:         │
│   extraction            │ │ • Level-order (BFS) │ │   open addressing    │
│                         │ │                     │ │                      │
│ EXAMPLES:               │ │ EXAMPLES:           │ │ EXAMPLES:            │
│ → "Library to Stem"     │ │ → "Show Academic"   │ │ → "Find Library"     │
│ → Library → CKCC →      │ │ → lists 7 academic  │ │ → returns category,  │
│   Building D → Stem     │ │   buildings         │ │   desc, services     │
│   Distance = 214        │ │                     │ │                      │
└───────────┬─────────────┘ └──────────┬──────────┘ └───────────┬──────────┘
            │                          │                        │
            └──────────────────────────┼────────────────────────┘
                                       │
                                       ▼
                             ┌──────────────────┐
                             │   INTEGRATOR     │
                             │ (CampusNavigation│
                             │     System)      │
                             │                  │
                             │ Combines all 3   │
                             │ DSA layers into  │
                             │ unified CLI app  │
                             └───────┬──────────┘
                                     │
                                     ▼
                             ┌──────────────────┐
                             │  CLI MENU + UI   │
                             │  (main.py)       │
                             │                  │
                             │ 1. Search Info   │
                             │ 2. Browse Cat.   │
                             │ 3. Shortest Path │
                             │ 4. Display Graph │
                             │ 5. Exit          │
                             └──────────────────┘
```

---

## Data Structure 1: Graph — Navigation Layer

### File: `graph.py`

### Representation

The campus is modelled as a **weighted undirected graph** using an **adjacency list** (Python dictionary of lists). Each vertex stores a list of `(neighbour, weight)` tuples.

### Vertices (12 campus locations)

Building A, Building B, Building C, Building D, Building Stem, Building T, Library, NICC, CKCC, Study Office, Canteen, Entrance

### Edges (17 edges)

| Edge | Weight |
|------|--------|
| Entrance ↔ Building A | 90 |
| Building A ↔ Library | 60 |
| Building A ↔ Building Stem | 230 |
| Library ↔ NICC | 60 |
| Library ↔ CKCC | 100 |
| Library ↔ Building D | 240 |
| Library ↔ Building Stem | 240 |
| NICC ↔ CKCC | 80 |
| Building D ↔ CKCC | 64 |
| Building B ↔ Building D | 50 |
| Building B ↔ Building Stem | 50 |
| Building D ↔ Building Stem | 50 |
| Study Office ↔ Building Stem | 85 |
| Study Office ↔ Canteen | 60 |
| Building C ↔ Building T | 40 |
| Building C ↔ Canteen | 90 |
| Building T ↔ Canteen | 90 |

### Algorithm: Dijkstra's Shortest Path

Dijkstra's algorithm finds the shortest path from a source vertex to all other vertices in a weighted graph with non-negative weights.

#### Pseudocode

```
function Dijkstra(Graph, source, target):
    dist[source] = 0
    for each vertex v in Graph:
        if v != source:
            dist[v] = INFINITY
        prev[v] = NULL
        pq.insert(v, dist[v])

    while pq is not empty:
        u = pq.extract_min()
        if u == target:
            break
        for each neighbour v of u:
            alt = dist[u] + weight(u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                pq.decrease_key(v, alt)

    return reconstruct_path(prev, target), dist[target]
```

#### Implementation Details

- Uses **`heapq`** (binary heap priority queue) for efficient `O(log V)` minimum extraction.
- **Lazy deletion**: outdated entries in the heap are skipped when popped.
- **Early exit**: stops as soon as the target is reached.

---

## Data Structure 2: Hash Table — Information Layer

### File: `hash_table.py`

### Representation

Uses a **Python dictionary** as a hash table. Each key is the building name (string), and each value is a `BuildingInfo` object containing:

- `name` — Building name
- `category` — Category classification
- `description` — Brief description
- `services` — List of available services

### Why a Dictionary is a Hash Table

Python's `dict` is implemented as a **hash table** with:
- **Hash function**: Built-in `hash()` on the string key
- **Collision resolution**: Open addressing with quadratic probing (CPython 3.x)
- **Amortised O(1)** average-case lookup, insert, and delete

### Building Data (12 entries)

Each building has been stored with category, description, and services as specified in the requirements.

---

## Data Structure 3: Tree — Categorization Layer

### File: `tree.py`

### Representation

A **multi-way tree** (general tree) where:
- **Root**: "RUPP Campus"
- **Internal nodes** (branches): Category names
- **Leaf nodes**: Individual building names

### Tree Structure

```
RUPP Campus
├── Academic Buildings
│   ├── Building A
│   ├── Building B
│   ├── Building C
│   ├── Building D
│   ├── Building Stem
│   ├── Building T
│   └── CKCC
├── Services
│   ├── Library
│   ├── NICC
│   └── Canteen
└── Administration
    └── Study Office
```

### Traversals Implemented

| Traversal | Order | Use Case |
|-----------|-------|----------|
| **Pre-order** | Root → Children (recursive) | Displaying the tree hierarchy |
| **Post-order** | Children → Root (recursive) | Demonstrating alternative traversal |
| **Level-order** | Breadth-first (queue-based) | Demonstrating BFS traversal |

---

## How They Work Together

The three data structures address different concerns of the navigation system, and together provide a complete solution:

### 1. Search (Hash Table + Tree)
When a user searches for a building, the **hash table** provides instant O(1) lookup of its details. Simultaneously, the **tree** tells us which category the building belongs to, giving context.

### 2. Browse (Tree + Hash Table)
The user selects a category from the **tree**. The tree returns all building names under that category. Each name can then be looked up in the **hash table** for full details.

### 3. Navigate (Graph)
Once the user knows where they want to go, the **graph** layer computes the shortest path using Dijkstra's algorithm. The path is displayed as a human-readable route with total distance.

### Data Flow Example

```
User: "Find path from Library to Building Stem"

 1. Hash Table verifies both locations exist
 2. Graph runs Dijkstra(Library, Building Stem)
 3. Path returned: Library → CKCC → Building D → Building Stem
 4. Total distance: 214
```

### Integration Points

| Operation | Graph | Hash Table | Tree |
|-----------|-------|------------|------|
| Search building | — | O(1) lookup | Category context |
| Browse by category | — | Detail lookup per building | Category → building list |
| Find shortest path | Dijkstra's algorithm | Validate locations exist | — |
| Display graph | Adjacency list | — | — |

---

## Complexity Analysis

### Graph Layer

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Add vertex | O(1) | O(V) |
| Add edge | O(1) | O(E) |
| Dijkstra (binary heap) | O((V + E) log V) | O(V) |
| Display adjacency list | O(V + E) | O(1) auxiliary |

Where: V = number of vertices (12), E = number of edges (17 in one direction, 34 total directed)

### Hash Table Layer

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Insert | O(1) amortised | O(n) |
| Search | O(1) average / O(n) worst-case | O(1) auxiliary |
| Delete | O(1) amortised | O(1) auxiliary |

Where: n = number of entries (12)

### Tree Layer

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Pre-order traversal | O(n) | O(h) recursion stack |
| Post-order traversal | O(n) | O(h) recursion stack |
| Level-order traversal | O(n) | O(w) queue width |
| Get buildings in category | O(k) where k = category size | O(1) |

Where: n = total nodes (15), h = tree height (3), w = max width (8)

### Overall Program

| Action | Effective Complexity |
|--------|---------------------|
| Load all structures | O(V + E + n) |
| Full menu cycle | User-driven, each operation independent |

---

## Test Cases & Verification

### Test Case 1: Library → Building Stem

```
Expected:
Library
→ CKCC
→ Building D
→ Building Stem

Distance = 214
```

**Verification:**
- Library to CKCC = 100
- CKCC to Building D = 64
- Building D to Building Stem = 50
- **Total = 100 + 64 + 50 = 214** ✓

### Test Case 2: Entrance → Building T

```
Expected:
Entrance
→ Building A
→ Building Stem
→ Study Office
→ Canteen
→ Building T

Distance = 555
```

**Verification:**
- Entrance to Building A = 90
- Building A to Building Stem = 230
- Building Stem to Study Office = 85
- Study Office to Canteen = 60
- Canteen to Building T = 90
- **Total = 90 + 230 + 85 + 60 + 90 = 555** ✓

### Test Case 3: Building B → Library

```
Expected:
Building B
→ Building D
→ CKCC
→ Library

Distance = 214
```

**Verification:**
- Building B to Building D = 50
- Building D to CKCC = 64
- CKCC to Library = 100
- **Total = 50 + 64 + 100 = 214** ✓

---

## Sample Program Output

```
Initialising RUPP Campus Navigation System...
  [✓] Building campus graph (adjacency list)...
  [✓] Loading building information (hash table)...
  [✓] Building category tree...
  System ready!

===========================================
  SMART RUPP CAMPUS NAVIGATION SYSTEM
===========================================
  1. Search Building Information
  2. Browse Buildings by Category
  3. Find Shortest Path
  4. Display Campus Graph
  5. Exit
===========================================
  Enter your choice (1-5): 1

--- SEARCH BUILDING INFORMATION ---
Enter building name: Library

==================================================
  Building    : Library
  Category    : Service
  Description : University library and student study area
  Services    : Books, Reading Area, Research
==================================================

  [Hash Table] O(1) lookup complete.

  Press Enter to continue...
```

---

## How to Run

### Prerequisites
- Python 3.x

### Execution

```bash
python main.py
```

Or run each module individually for isolated testing:

```bash
python graph.py        # Test the graph layer alone
python hash_table.py   # Test the hash table alone
python tree.py         # Test the tree layer alone
python main.py         # Run the full application
```

---

## File Structure

```
CampusNavigation/
│
├── main.py          # CLI menu, integrates all layers
├── graph.py         # Graph class, adjacency list, Dijkstra
├── hash_table.py    # BuildingInfo, BuildingHashTable
├── tree.py          # TreeNode, CategoryTree, traversals
└── README.md        # This file
```

---

*Project completed as part of Data Structures and Algorithms coursework.*
*Royal University of Phnom Penh — Smart Campus Initiative*
