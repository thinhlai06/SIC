"""Take screenshots of the running Gradio demo with Playwright + the installed Microsoft Edge (no browser download).

Usage: python screenshot_demo.py --url http://127.0.0.1:7860 --image sample.jpg --out evidence_figures/07_demo [--prefix u]
Produces: <prefix>01_demo_upload.png (empty page), <prefix>02_demo_result.png (after grading).
"""
import argparse
import os

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--url", default="http://127.0.0.1:7860")
ap.add_argument("--image", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--prefix", default="u")
ap.add_argument("--wait", type=int, default=120)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page(viewport={"width": 1280, "height": 1000}, device_scale_factor=1.5)
    pg.goto(a.url, wait_until="networkidle")
    pg.wait_for_timeout(1500)
    pg.screenshot(path=os.path.join(a.out, f"{a.prefix}01_demo_upload.png"), full_page=True)
    pg.set_input_files("input[type=file]", a.image)
    pg.wait_for_timeout(1500)
    pg.get_by_role("button", name="Grade image").click()
    pg.wait_for_selector("text=Predicted grade", timeout=a.wait * 1000)
    pg.wait_for_timeout(2500)
    pg.screenshot(path=os.path.join(a.out, f"{a.prefix}02_demo_result.png"), full_page=True)
    b.close()
print("screenshots saved in", a.out)
