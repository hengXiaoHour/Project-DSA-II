# RUPP Campus Navigation — Interactive Graph Editor (V2)

A web-based interactive graph builder and shortest-path visualizer for **RUPP Campus 1**. Built with pure Python + Flask + Leaflet.js. Demonstrates **Graph (Dijkstra/BFS/DFS)**, **Hash Table** (O(1) lookup), and **Tree** (category hierarchy) data structures.

## Prerequisites

- **Python 3** — install from https://python.org (VS Code will prompt you if missing)
- **Git** (for clone method) — install from https://git-scm.com

## Quick Start

### Fresh setup (Linux/macOS)

```bash
git clone https://github.com/hengXiaoHour/Project-DSA-II.git
cd Project-DSA-II
git checkout V2
curl -fsSL https://raw.githubusercontent.com/hengXiaoHour/Project-DSA-II/main/setup/install.sh | bash
.venv/bin/python main.py
```

### Fresh setup (Windows)

Open the project in **VS Code**, then run in its integrated terminal:

```powershell
git checkout V2
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py
```

### After pulling updates

```bash
cd Project-DSA-II
git pull origin V2
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

Then open **http://localhost:5000** in your browser.

## How It Works

| Mode | What it does |
|---|---|
| **Move** | Drag pins to reposition — distances auto-update |
| **+Node** | Click the map, name your point — drops a Google Maps-style pin |
| **+Edge** | Click one pin, then another — creates a road with real Haversine distance |
| **Delete** | Click a pin or edge to remove it |
| **Navigate** | Pick start/end + algorithm (BFS/DFS/Dijkstra) — path highlights in color |

Click **Sample** to load the RUPP campus preset. Changes auto-save — they survive server restarts.

## Built With

- **Python 3** — Flask REST API
- **Leaflet.js** — Interactive map (OpenStreetMap tiles)
- **pytest + Playwright** — 68 tests (60 backend + 8 UI)

## Project Structure

```
├── main.py                  # Entry point
├── setup/                   # Install scripts + dependencies
├── src/navigation/          # 3 DSA layers (Graph, HashTable, Tree)
├── frontend/                # Flask API + Leaflet UI
├── tests/                   # Backend + Playwright tests
└── doc/                     # Sample dataset + architecture
```

## Team

**Group 1** — Heng Hour (Leader), Heng Pengly, Yos Sak, Han KimHeng, Sem VatanakPanha
