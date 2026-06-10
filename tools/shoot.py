"""Screenshot the live Strum surfaces into img/ for the marketing site.

Re-run any time a surface improves:
    ~/Documents/Projects/bank-tracker/.venv/bin/python tools/shoot.py

Shoots at a phone-ish 430px width so the images sit naturally in the
How-it-works step cards. The dashboard shot injects representative sample
data (it's the real UI; the numbers are staged so the screens read alive
rather than empty)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://www.strumworks.com"
OUT = Path(__file__).resolve().parent.parent / "img"
OUT.mkdir(exist_ok=True)

VIEWPORT = {"width": 430, "height": 880}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport=VIEWPORT, device_scale_factor=2)

    # 1. The signup form, as the world sees it.
    page.goto(f"{BASE}/start/", wait_until="networkidle")
    page.screenshot(path=str(OUT / "how-1-start.png"))
    print("shot: how-1-start.png")

    # 2. The success moment — the number reveal. (Real success view,
    #    staged values; a live shot would buy a number per screenshot.)
    page.evaluate("""() => {
        document.getElementById('formview').style.display = 'none';
        document.getElementById('s-head').textContent = "You're in, Malcolm.";
        document.getElementById('s-number').textContent = '(403) 555-0182';
        document.getElementById('successview').style.display = 'block';
        window.scrollTo(0, 0);
    }""")
    page.screenshot(path=str(OUT / "how-2-number.png"))
    print("shot: how-2-number.png")

    # 3. The dashboard — real UI, representative numbers.
    page.goto(f"{BASE}/dash/", wait_until="networkidle")
    page.evaluate("""() => {
        ['loading','err'].forEach(id => document.getElementById(id).classList.add('hidden'));
        document.getElementById('headline').textContent = 'Hi Malcolm — Malcolm Fitness is live.';
        document.getElementById('brandname').textContent = 'Malcolm Fitness';
        document.getElementById('who').textContent = 'Malcolm';
        document.getElementById('number').textContent = '(403) 555-0182';
        document.getElementById('plan').textContent = 'Starter — thanks for playing';
        document.getElementById('m-clients').style.width = '60%';
        document.getElementById('n-clients').textContent = '3 of 5';
        document.getElementById('m-msgs').style.width = '24%';
        document.getElementById('n-msgs').textContent = '12 of 50 sent';
        document.getElementById('view').classList.remove('hidden');
        window.scrollTo(0, 0);
    }""")
    page.screenshot(path=str(OUT / "how-3-dash.png"))
    print("shot: how-3-dash.png")

    browser.close()
print("done.")
