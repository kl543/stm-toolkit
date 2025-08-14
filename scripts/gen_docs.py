#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os
import shutil
import html
from datetime import datetime
from urllib.parse import quote

REPO = os.environ.get("GITHUB_REPOSITORY", "kl543/stm-toolkit")
BRANCH = os.environ.get("DOCS_BRANCH", "main")

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
SRC_IMG_DIR = ROOT / "assets" / "img"
DOCS_DIR = ROOT / "docs"
DOCS_IMG_DIR = DOCS_DIR / "img"

DOCS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_IMG_DIR.mkdir(parents=True, exist_ok=True)

def url_nbviewer(rel_posix: str) -> str:
    # 对路径做 URL 编码（空格 -> %20）
    return f"https://nbviewer.org/github/{REPO}/blob/{BRANCH}/{quote(rel_posix)}"

def url_raw(rel_posix: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{quote(rel_posix)}"

def gather_notebooks():
    if not NB_DIR.exists():
        return []
    out = []
    for p in sorted(NB_DIR.glob("*.ipynb")):
        rel = p.relative_to(ROOT).as_posix()
        title = p.stem.replace("-", " ").replace("_", " ")
        out.append({
            "title": title,
            "nbviewer": url_nbviewer(rel),
            "raw": url_raw(rel),
        })
    return out

def gather_images(max_count=6):
    imgs = []
    if not SRC_IMG_DIR.exists():
        return imgs
    cand = sorted(SRC_IMG_DIR.glob("*.*"))
    for p in cand[:max_count]:
        dst = DOCS_IMG_DIR / p.name
        shutil.copy2(p, dst)
        imgs.append({
            "src": f"img/{p.name}",
            "alt": p.stem.replace("-", " "),
            "caption": p.stem.replace("-", " "),
        })
    return imgs

def render_html(nbs, imgs):
    css = """
    :root{--line:#e9e9e9;--muted:#666;--ink:#111}
    body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);line-height:1.6}
    header{background:#111;color:#fff;padding:28px 16px;text-align:center}
    main{max-width:1040px;margin:24px auto;padding:0 16px}
    .muted{color:#666}
    .card{border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:16px 0;background:#fff}
    .btn{display:inline-block;border:1px solid var(--line);padding:8px 12px;border-radius:10px;text-decoration:none;margin-right:8px}
    .btn:hover{background:#f6f6f6}
    .grid{display:grid;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:repeat(3,1fr)}}
    img{width:100%;height:auto;border-radius:12px;border:1px solid var(--line)}
    figcaption{font-size:12px;color:#666;margin-top:6px}
    footer{color:#666;font-size:12px;text-align:center;margin:24px 0}
    """

    nb_html = "".join(
        f"""<p><b>{html.escape(nb['title'])}</b><br>
        <a class="btn" href="{nb['nbviewer']}" target="_blank" rel="noopener">View (nbviewer)</a>
        <a class="btn" href="{nb['raw']}" target="_blank" rel="noopener">Download (.ipynb)</a></p>"""
        for nb in nbs
    ) or '<p class="muted">No notebooks found.</p>'

    img_html = "".join(
        f"""<figure><img src="{html.escape(im['src'])}" alt="{html.escape(im['alt'])}" loading="lazy">
        <figcaption>{html.escape(im['caption'])}</figcaption></figure>"""
        for im in imgs
    ) or '<p class="muted">No figures found.</p>'

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>STM Data Toolkit</title>
<link rel="stylesheet" href="https://unpkg.com/mvp.css">
<style>{css}</style>
</head>
<body>
<header><h1>STM Data Toolkit</h1><p class="muted">Minimal notebooks + selected figures</p></header>
<main>
<section class="card"><h2>Notebooks</h2>{nb_html}</section>
<section class="card"><h2>Selected Figures</h2><div class="grid">{img_html}</div></section>
</main>
<footer>Generated {now} · Source: https://github.com/{REPO}</footer>
</body></html>"""

def main():
    nbs = gather_notebooks()
    imgs = gather_images(max_count=6)
    html_out = render_html(nbs, imgs)
    (DOCS_DIR / "index.html").write_text(html_out, encoding="utf-8")
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Wrote docs/index.html · notebooks={len(nbs)} imgs={len(imgs)}")

if __name__ == "__main__":
    main()
