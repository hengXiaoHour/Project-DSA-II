import os
import json
import pytest
import subprocess
import time
import signal
import sys


def wait_for_server(url, timeout=15):
    import urllib.request
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url)
            return True
        except Exception:
            time.sleep(0.3)
    return False


@pytest.fixture(scope="module")
def server():
    import shutil
    sample_file = os.path.join(os.path.dirname(__file__), "..", "doc", "sample_campus.json")
    backup_file = "/tmp/sample_campus_backup.json"
    if os.path.exists(sample_file):
        shutil.copy2(sample_file, backup_file)

    proc = subprocess.Popen(
        [sys.executable, "-m", "frontend.app"],
        cwd=os.path.join(os.path.dirname(__file__), ".."),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    ready = wait_for_server("http://localhost:5000")
    if not ready:
        proc.kill()
        pytest.skip("Server failed to start")
    yield "http://localhost:5000"
    proc.terminate()
    proc.wait()
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, sample_file)
        os.remove(backup_file)


@pytest.fixture(scope="module")
def browser_context(server):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        yield context
        browser.close()


@pytest.fixture
def page(server, browser_context):
    page = browser_context.new_page()
    page.goto(server)
    page.wait_for_load_state("networkidle")
    yield page
    page.close()


class TestUIGraphEditor:
    def test_page_loads(self, page):
        title = page.title()
        assert "Graph Editor" in title
        assert page.locator("#map").is_visible()

    def test_has_mode_buttons(self, page):
        assert page.locator('button[data-mode="select"]').is_visible()
        assert page.locator('button[data-mode="add-node"]').is_visible()
        assert page.locator('button[data-mode="add-edge"]').is_visible()
        assert page.locator('button[data-mode="delete"]').is_visible()

    def test_has_navigation_controls(self, page):
        assert page.locator("#startSelect").is_visible()
        assert page.locator("#endSelect").is_visible()
        assert page.get_by_role("button", name="Go").is_visible()

    def test_add_node_via_api(self, page, server):
        import urllib.request
        data = json.dumps({"name": "TestNode", "lat": 11.562, "lng": 104.891}).encode()
        req = urllib.request.Request(
            f"{server}/api/nodes",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req)
        page.reload()
        page.wait_for_load_state("networkidle")
        assert page.locator("#nodeList").get_by_text("TestNode").is_visible()

    def test_add_and_find_path(self, page, server):
        import urllib.request

        def api(method, path, body=None):
            url = f"{server}{path}"
            data = json.dumps(body).encode() if body else None
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method=method)
            return json.loads(urllib.request.urlopen(req).read())

        api("POST", "/api/graph/load", {"nodes": {}, "edges": []})
        api("POST", "/api/nodes", {"name": "A", "lat": 11.562, "lng": 104.891})
        api("POST", "/api/nodes", {"name": "B", "lat": 11.563, "lng": 104.892})
        api("POST", "/api/nodes", {"name": "C", "lat": 11.564, "lng": 104.893})
        api("POST", "/api/edges", {"from": "A", "to": "B"})
        api("POST", "/api/edges", {"from": "B", "to": "C"})

        page.reload()
        page.wait_for_load_state("networkidle")

        page.select_option("#startSelect", "A")
        page.select_option("#endSelect", "C")
        page.get_by_role("button", name="Go").click()
        page.wait_for_timeout(500)

        bar = page.locator("#resultBar")
        bar_text = bar.text_content()
        assert "A" in bar_text
        assert "C" in bar_text
        assert "DIJKSTRA" in bar_text

    def test_edit_mode_toggle(self, page):
        page.locator('button[data-mode="add-node"]').click()
        assert page.locator('button[data-mode="add-node"].active').is_visible()

        page.locator('button[data-mode="select"]').click()
        assert page.locator('button[data-mode="select"].active').is_visible()

    def test_delete_node_via_ui(self, page, server):
        import urllib.request
        api = lambda m, p, b=None: urllib.request.urlopen(
            urllib.request.Request(
                f"{server}{p}",
                data=json.dumps(b).encode() if b else None,
                headers={"Content-Type": "application/json"},
                method=m,
            )
        )
        api("POST", "/api/graph/load", {"nodes": {}, "edges": []})
        api("POST", "/api/nodes", {"name": "DeleteMe", "lat": 11.56, "lng": 104.89})

        page.reload()
        page.wait_for_load_state("networkidle")
        assert page.locator("#nodeList").get_by_text("DeleteMe").is_visible()

        api("DELETE", "/api/nodes/DeleteMe")
        page.reload()
        page.wait_for_load_state("networkidle")
        assert not page.locator("#nodeList").get_by_text("DeleteMe").is_visible()

    def test_empty_state(self, page, server):
        import urllib.request, json
        api = lambda m, p, b=None: urllib.request.urlopen(
            urllib.request.Request(
                f"{server}{p}",
                data=json.dumps(b).encode() if b else None,
                headers={"Content-Type": "application/json"},
                method=m,
            )
        )
        api("POST", "/api/graph/load", {"nodes": {}, "edges": []})
        page.reload()
        page.wait_for_load_state("networkidle")
        hint = page.locator("#hintBar").text_content()
        assert "Mode" in hint
