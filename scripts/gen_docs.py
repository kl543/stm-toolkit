#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate a simple docs page for STM Toolkit:
- Lists notebooks in /notebooks with "View (nbviewer)" and "Download (.ipynb)".
- Shows selected figures from assets/img as a responsive grid.
- Uses a shared site header if _site-header.html exists in repo root or parent.
- Falls back to a minimal inline header with links to your main site.
"""

import os
from datetime import datetime
from urllib.parse import quote

# ---- repo-specific config (change repo_name if你改了仓库名) ----
OWNER     = "kl543"
REPO_NAME = "stm-toolkit"
BRANCH    = "main"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
NB_DIR = os.path.join(ROOT, "notebooks")
IMG_DIR = os.path.join(ROOT, "assets", "img")
OUT_HTML = os.path.join(ROOT, "index.html")

MAIN_SITE = "https://kl543.github.io"
PROJECTS_URL = f"{MAIN_SITE}/projects.html"

def load_site_header():
    """
    优先读取仓库根或上层目录的 _site-header.html；
    若不存在，返回内置兜底页眉（含五个导航）。
    """
    candidates = [
        os.path.join(ROOT, "_site-header.html"),
        os.path.join(os.path.dirname(ROOT), "_site-header.html"),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    # fallback header（与主站风格保持一致）
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>STM Data Toolkit — Kaiming Liu</title>
<style>
:root{{--line:#e9e9e9;--muted:#666;--ink:#111;--bg:#0f0f10}}
body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);line-height:1.6}}
header{{background:#111;color:#fff;padding:30px 16px;text-align:center}}
nav{{display:flex;gap:14px;justify-content:center;margin:10px 0 0}}
nav a{{color:#fff;text-decoration:none;opacity:.9}} nav a:hover{{opacity:1}}
.container{{max-width:1040px;margin:24px auto;padding:0 16px}}
.muted{{color:var(--muted)}}
.card{{border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:16px 0;background:#fff}}
h1,h2,h3{{margin:.2rem 0 .6rem}}
.btn{{display:inline-block;border:1px solid var(--line);padding:8px 12px;border-radius:10px;text-decoration:none;margin-right:8px;color:#111}}
.btn:hover{{background:#f6f6f6}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}}
.thumb{{border:1px solid var(--line);border-radius:12px;padding:6px;background:#fff}}
.thumb img{{width:100%;height:auto;display:block;border-radius:8px}}
.center{{text-align:center}}
.backline{{margin:6px 0 0;}}
</style>
</head>
<body>
<header>
  <h1>STM Data Toolkit</h1>
  <div class="muted">Minimal notebooks + selected figures</div>
  <div class="backline"><a href="{PROJECTS_URL}" style="color:#fff;text-decoration:underline;">Back to Projects</a></div>
  <nav>
    <a href="{MAIN_SITE}/index.html">About</a>
    <a href="{MAIN_SITE}/interests.html">Interests</a>
    <a href="{MAIN_SITE}/projects.html"><b>Projects</b></a>
    <a href="{MAIN_SITE}/coursework.html">Coursework</a>
    <a href="{MAIN_SITE}/contact.html">Contact</a>
  </nav>
</header>
"""

def list_notebooks():
    os.makedirs(NB_DIR, exist_ok=True)
    files = [f for f in os.listdir(NB_DIR) if f.lower().endswith(".ipynb")]
    files.sort()
    items = []
    for nb in files:
        # nbviewer 和 raw 下载链接
        path = f"notebooks/{quote(nb)}"
        nbviewer = f"https://nbviewer.org/github/{OWNER}/{REPO_NAME}/blob/{BRANCH}/{path}"
        download = f"https://raw.githubusercontent.com/{OWNER}/{REPO_NAME}/{BRANCH}/{path}"
        items.append((nb, nbviewer, download))
    return items

def list_images():
    imgs = []
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                imgs.append(f"assets/img/{f}")
    imgs.sort()
    return imgs

def build_html():
    header = load_site_header()

    nb_items = list_notebooks()
    img_items = list_images()
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html = [header, '<main class="container">']

    # Notebooks
    html.append('<section class="card">')
    html.append('<h2>Notebooks</h2>')
    if nb_items:
        for name, view_url, dl_url in nb_items:
            label = os.path.splitext(name)[0].replace("-", " ")
            html.append('<div style="margin:10px 0;">')
            html.append(f'<b>{label}</b><br/>')
            html.append(f'<a class="btn" href="{view_url}">View (nbviewer)</a>')
            html.append(f'<a class="btn" href="{dl_url}">Download (.ipynb)</a>')
            html.append('</div>')
    else:
        html.append('<div class="muted">No notebooks yet.</div>')
    html.append('</section>')

    # Figures
    html.append('<section class="card">')
    html.append('<h2>Selected Figures</h2>')
    if img_items:
        html.append('<div class="grid">')
        for rel in img_items:
            html.append('<div class="thumb">')
            html.append(f'<img src="{rel}" alt="figure" loading="lazy" />')
            html.append('</div>')
        html.append('</div>')
    else:
        html.append('<div class="muted">No figures yet.</div>')
    html.append('</section>')

    html.append(f'<div class="center muted" style="margin:24px 0;">Last updated: {now_str}</div>')
    html.append('</main></body></html>')
    return "\n".join(html)

def main():
    html = build_html()
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[stm-toolkit] Wrote {OUT_HTML}")

if __name__ == "__main__":
    main()
