import subprocess, os

ASCII = r"""
                        ┌─────────┐
                        │  RUPP   │
                        │ Campus  │
                        └────┬────┘
                             │
                             ▼
                    ┌────────────────────────┐
                    │     Data Collection    │
                    │  (12 Buildings, 17     │
                    │   Weighted Edges,      │
                    │   Categories, Desc)    │
                    └──────────┬─────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
┌─────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  GRAPH (Navigation) │ │ TREE (Categorize)│ │ HASH TABLE (Tbl)│
│─────────────────────│ │──────────────────│ │──────────────────│
│ PURPOSE:            │ │ PURPOSE:         │ │ PURPOSE:         │
│ Model campus paths  │ │ Organize builds  │ │ Store & retrieve │
│ as weighted network │ │ by category tree │ │ info by name     │
│ for shortest route  │ │ for filtered     │ │ in O(1) time     │
│                     │ │ browsing         │ │                  │
│ STRUCTURE:          │ │ STRUCTURE:       │ │ STRUCTURE:       │
│ • Adj list (dict)   │ │ • N-ary tree     │ │ • Python dict    │
│ • 12 verts, 17 edges│ │ • 1 root, 3 cat  │ │ • BuildingInfo   │
│                     │ │ • 11 building    │ │   objects        │
│                     │ │   leaves         │ │                  │
│ ALGORITHMS:         │ │ ALGORITHMS:      │ │ ALGORITHMS:      │
│ • Dijkstra          │ │ • Pre-order      │ │ • Hash fn: hash()│
│ • Priority queue    │ │ • Post-order     │ │ • Collision:     │
│   (heap)            │ │ • Level-order    │ │   open addressing│
│                     │ │   (BFS)          │ │                  │
│ EXAMPLE:            │ │ EXAMPLE:         │ │ EXAMPLE:         │
│ Library to Stem     │ │ "Show Academic"  │ │ "Find Library"   │
│ = 214m              │ │ → lists 7 builds │ │ → cat, desc, svc │
└────────┬────────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                      │                     │
         └──────────────────────┼─────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │    INTEGRATOR        │
                    │ (CampusNavigation    │
                    │      System)         │
                    │                      │
                    │ Combines all 3 DSA   │
                    │ layers into unified  │
                    │ UI / CLI             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   CLI MENU + UI      │
                    │      (main.py)       │
                    │                      │
                    │ 1. Search Info       │
                    │ 2. Browse Category   │
                    │ 3. Shortest Path     │
                    │ 4. Display Graph     │
                    │ 5. Exit              │
                    └──────────────────────┘
"""

HTML = f"""<!DOCTYPE html><html><head>
<style>
body {{ margin:0; background:white; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
pre {{
    font-family: "Courier New", "Liberation Mono", monospace;
    font-size: 13px;
    line-height: 1.2;
    color: #1a1a1a;
    padding: 30px;
    margin: 0;
}}
</style></head><body>
<pre>{ASCII}</pre>
</body></html>"""

base = os.path.dirname(__file__)
html_path = os.path.join(base, "arch_render.html")
png_path = os.path.join(base, "architecture_diagram.png")

with open(html_path, "w") as f:
    f.write(HTML)

code = f"""
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page()
        await page.goto("file://{html_path}")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="{png_path}", full_page=True)
        await b.close()
asyncio.run(main())
"""
subprocess.run([os.path.join(base, "..", ".venv", "bin", "python"), "-c", code])
os.remove(html_path)
print(f"Saved: {png_path}")
