# System Architecture — RUPP Campus Navigation

> Based on teacher's whiteboard diagram and Group 1 PBL Week 1 plan.

---

## System Overview (Teacher's Diagram)

```
                            ┌─────────┐
                            │  RUPP   │
                            │ Campus  │
                            └────┬────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Data Collection │
                        │  (Buildings,    │
                        │   Distances,    │
                        │   Coords)       │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  GRAPH (Navigation) │ │  TREE (Filtering)   │ │  HASH (Retrieval)   │
│  ─────────────────  │ │  ─────────────────  │ │  ─────────────────  │
│                     │ │                     │ │                     │
│ PURPOSE:            │ │ PURPOSE:            │ │ PURPOSE:            │
│ Model campus as     │ │ Organize buildings  │ │ Store building info │
│ network of paths    │ │ by category for     │ │ for instant access  │
│ for route finding   │ │ filtered browsing   │ │ by name             │
│                     │ │                     │ │                     │
│ USES:               │ │ USES:               │ │ USES:               │
│ • Dijkstra's algo   │ │ • BST/AVL tree      │ │ • Hash table        │
│   (shortest path)   │ │   (sorted access)   │ │   (chaining)        │
│ • BFS/DFS           │ │ • Category nodes    │ │ • O(1) average      │
│   (exploration)     │ │   (grouping)        │ │   lookup            │
│                     │ │                     │ │                     │
│ EXAMPLES:           │ │ EXAMPLES:           │ │ EXAMPLES:           │
│ → "STEM to Library" │ │ → "Show Academic"   │ │ → "Find CJCC info"  │
│ → finds shortest    │ │ → lists Academic    │ │ → returns coords,   │
│   weighted path     │ │   buildings         │ │   desriptions       │
└─────────┬───────────┘ └─────────┬───────────┘ └─────────┬───────────┘
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼
                        ┌───────────────┐
                        │   EVALUATOR   │
                        │  (Integrate)  │
                        │               │
                        │ Combines all  │
                        │ 3 DSA layers  │
                        │ into unified  │
                        │    system     │
                        └───────┬───────┘
                                │
                                ▼
                        ┌───────────────┐
                        │  UI + Testing │
                        │  (Campus Map) │
                        │               │
                        │ User selects  │
                        │ start & end   │
                        │ → see route   │
                        └───────────────┘
```
