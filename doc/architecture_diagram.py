import subprocess, os

HTML = r"""<!DOCTYPE html><html><body style="margin:20px;background:white;font-family:Arial,sans-serif;">
<div style="display:flex;flex-direction:column;align-items:center;gap:16px;">

<div style="background:#2B6CB0;color:white;padding:14px 40px;border-radius:8px;font-size:22px;font-weight:bold;">RUPP Campus</div>

<div style="width:2px;height:20px;background:#718096;"></div>
<div style="width:2px;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-top:10px solid #718096;"></div>

<div style="background:#EBF8FF;border:2px solid #3182CE;padding:12px 30px;border-radius:8px;font-size:14px;text-align:center;">
  <b>Data Collection</b><br>
  <span style="font-size:12px;color:#4A5568;">
    (12 Buildings, 17 Weighted Edges, Categories, Descriptions)
  </span>
</div>

<div style="width:2px;height:20px;background:#718096;"></div>
<div style="display:flex;gap:20px;">
  <div style="width:2px;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-top:10px solid #718096;"></div>
</div>

<div style="display:flex;gap:24px;">

  <!-- Graph -->
  <div style="background:#E6FFFA;border:2px solid #38B2AC;border-radius:8px;padding:14px;width:240px;font-size:12px;">
    <div style="text-align:center;font-weight:bold;font-size:14px;margin-bottom:6px;">GRAPH (Navigation)</div>
    <hr style="border:0;border-top:1px solid #81E6D9;">
    <div style="margin-top:4px;"><b>PURPOSE:</b></div>
    <div style="color:#4A5568;">Model campus pathways as a weighted network for shortest route.</div>
    <hr style="border:0;border-top:1px solid #81E6D9;">
    <div style="margin-top:4px;"><b>STRUCTURE:</b></div>
    <div style="color:#4A5568;">• Adjacency list (dict of lists)<br>• 12 vertices, 17 edges</div>
    <hr style="border:0;border-top:1px solid #81E6D9;">
    <div style="margin-top:4px;"><b>ALGORITHMS:</b></div>
    <div style="color:#4A5568;">• Dijkstra's algorithm<br>• Priority queue (heap) for min-distance extraction</div>
    <hr style="border:0;border-top:1px solid #81E6D9;">
    <div style="margin-top:4px;"><b>EXAMPLE:</b></div>
    <div style="color:#4A5568;">Library → CKCC → Building D → Stem = 214m</div>
  </div>

  <!-- Tree -->
  <div style="background:#FFF5F5;border:2px solid#FC8181;border-radius:8px;padding:14px;width:230px;font-size:12px;">
    <div style="text-align:center;font-weight:bold;font-size:14px;margin-bottom:6px;">TREE (Categorize)</div>
    <hr style="border:0;border-top:1px solid #FEB2B2;">
    <div style="margin-top:4px;"><b>PURPOSE:</b></div>
    <div style="color:#4A5568;">Organize buildings by category tree for filtered browsing.</div>
    <hr style="border:0;border-top:1px solid #FEB2B2;">
    <div style="margin-top:4px;"><b>STRUCTURE:</b></div>
    <div style="color:#4A5568;">• N-ary tree (multi-way tree)<br>• 1 root, 3 category, 11 building leaves</div>
    <hr style="border:0;border-top:1px solid #FEB2B2;">
    <div style="margin-top:4px;"><b>ALGORITHMS:</b></div>
    <div style="color:#4A5568;">• Pre-order<br>• Post-order<br>• Level-order (BFS queue)</div>
    <hr style="border:0;border-top:1px solid #FEB2B2;">
    <div style="margin-top:4px;"><b>EXAMPLE:</b></div>
    <div style="color:#4A5568;">"Show Academic Buildings"<br>→ Lists 7 academic buildings</div>
  </div>

  <!-- Hash Table -->
  <div style="background:#FAF5FF;border:2px solid #B794F4;border-radius:8px;padding:14px;width:230px;font-size:12px;">
    <div style="text-align:center;font-weight:bold;font-size:14px;margin-bottom:6px;">HASH TABLE (Lookup)</div>
    <hr style="border:0;border-top:1px solid #D6BCFA;">
    <div style="margin-top:4px;"><b>PURPOSE:</b></div>
    <div style="color:#4A5568;">Store & retrieve building info by name in O(1) time.</div>
    <hr style="border:0;border-top:1px solid #D6BCFA;">
    <div style="margin-top:4px;"><b>STRUCTURE:</b></div>
    <div style="color:#4A5568;">• Python dict (hash table)<br>• BuildingInfo objects as values</div>
    <hr style="border:0;border-top:1px solid #D6BCFA;">
    <div style="margin-top:4px;"><b>ALGORITHMS:</b></div>
    <div style="color:#4A5568;">• Hash function: built-in hash()<br>• Collision: open addressing</div>
    <hr style="border:0;border-top:1px solid #D6BCFA;">
    <div style="margin-top:4px;"><b>EXAMPLE:</b></div>
    <div style="color:#4A5568;">"Find Library"<br>→ Returns category, desc, services</div>
  </div>

</div>

<div style="width:2px;height:16px;background:#718096;"></div>
<div style="display:flex;gap:0;align-items:center;">
  <div style="width:calc(240px + 24px + 230px + 24px + 230px);height:2px;background:#718096;"></div>
</div>
<div style="width:2px;height:8px;background:#718096;"></div>
<div style="width:2px;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-top:10px solid #718096;"></div>

<div style="background:#EDF2F7;border:2px solid #718096;padding:12px 30px;border-radius:8px;font-size:14px;text-align:center;">
  <b>INTEGRATOR</b><br>
  <span style="font-size:12px;color:#4A5568;">(CampusNavigation System)</span><br>
  <span style="font-size:11px;color:#718096;">Combines all 3 DSA layers into unified UI / CLI</span>
</div>

<div style="width:2px;height:16px;background:#718096;"></div>
<div style="width:2px;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-top:10px solid #718096;"></div>

<div style="background:#F7FAFC;border:2px solid #A0AEC0;padding:12px 30px;border-radius:8px;font-size:14px;text-align:center;">
  <b>CLI MENU + UI (main.py)</b><br>
  <span style="font-size:12px;color:#4A5568;">
    1. Search Info &nbsp;|&nbsp; 2. Browse Category &nbsp;|&nbsp; 3. Shortest Path<br>
    4. Display Graph &nbsp;|&nbsp; 5. Exit
  </span>
</div>

</div></body></html>"""

path = os.path.join(os.path.dirname(__file__), "architecture_diagram.png")
html_path = os.path.join(os.path.dirname(__file__), "arch_render.html")
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
        await page.screenshot(path="{path}", full_page=True)
        await b.close()
asyncio.run(main())
"""
subprocess.run([os.path.join(os.path.dirname(__file__), "..", ".venv", "bin", "python"), "-c", code])
print(f"Saved: {path}")
