#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate docs/index.html for stm-toolkit and copy selected images into docs/img.
- Lists all notebooks in notebooks/ with nbviewer + raw links
- Copies images from assets/img/ to docs/img/ (pick top N by name or all)
- Emits a minimal, clean index.html (no external build tools)
"""

from pathlib import Path
import os
import shutil
import html
from datetime import datetime

REPO = os.environ.get("GITHUB_REPOSITORY", "kl543/stm-toolkit")  # e.g., "kl543/stm-toolkit"
BRANCH = os.environ.get("DOCS_BRANCH", "main")

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"
SRC_IMG_DIR = ROOT / "assets" / "img"
DOCS_DIR = ROOT / "docs"
DOCS_IMG_DIR = DOCS_DIR / "img"

DOCS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_IMG_DIR.mkdir(parents=True, exist_ok=True)

def nbviewer_url(rel_path: str) -> str:
    return f"https://nbviewer.org/github/{REPO}/blob/{BRANCH}/{rel_path}"

def raw_url(rel_path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{rel_path}"

def gather_notebooks():
    if not NB_DIR.exists():
        return []
    nbs = sorted(p for p in NB_DIR.glob("*.ipynb"))
    out = []
    for p in nbs:
        rel = p.relative_to(ROOT).as_posix()
        title = p.stem.replace("-", " ").replace("_", " ")
        out.append({
            "title": title,
            "nbviewer": nbviewer_url(rel),
            "raw": raw_url(rel),
            "file": rel,
        })
    return out

def gather_images(max_count=6):
    imgs = []
    if SRC_IMG_DIR.exists():
        # 按名字排序，优先显示 stm-* / afm-*，你也可以自定义挑选规则
        cand = sorted(SRC_IMG_DIR.glob("*.*"))
        # 复制到 docs/img/ 并用相同文件名
        for p in cand[:max_count]:
            dst = DOCS_IMG_DIR / p.name
            shutil.copy2(p, dst)
            imgs.append({
                "src": f"img/{p.name}",
                "alt": p.stem.replace("-", " "),
                "caption": p.stem.replace("-", " "),
            })
    return imgs

def render_html(notebooks, images):
    # 极简样式（用 mvp.css 可删掉自带样式）
    css = """
    :root{--line:#e9e9e9;--muted:#666;--ink:#111}
    body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);line-height:1.6}
    header{background:#111;color:#fff;padding:28px 16px;text-align:center}
    nav{display:flex;gap:14px;justify-content:center;margin:10px 0 0}
    nav a{color:#fff;text-decoration:none;opacity:.9} nav a:hover{opacity:1}
    main{max-width:1040px;margin:24px auto;padding:0 16px}
    .muted{color:var(--muted)}
    .card{border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:16px 0;background:#fff}
    .btn{display:inline-block;border:1px solid var(--line);padding:8px 12px;border-radius:10px;text-decoration:none;margin-right:8px}
    .btn:hover{background:#f6f6f6}
    .grid{display:grid;gap:14px}
    @media(min-width:900px){.grid{grid-template-columns:repeat(3,1fr)}}
    figure{margin:0}
    img{width:100%;height:auto;border-radius:12px;border:1px solid var(--line)}
    figcaption{font-size:12px;color:#666;margin-top:6px}
    footer{color:var(--muted);font-size:12px;text-align:center;margin:24px 0}
    """

    nb_html = []
    for nb in notebooks:
        nb_html.append(f"""
        <p>
          <b>{html.escape(nb['title'])}</b><br>
          <a class="btn" href="{nb['nbviewer']}" target="_blank" rel="noopener">View (nbviewer)</a>
          <a class="btn" href="{nb['raw']}" target="_blank" rel="noopener">Download (.ipynb)</a>
        </p>""")

    img_html = []
    for im in images:
        img_html.append(f"""
        <figure>
          <img src="{html.escape(im['src'])}" alt="{html.escape(im['alt'])}" loading="lazy">
          <figcaption>{html.escape(im['caption'])}</figcaption>
        </figure>""")

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>STM Data Toolkit</title>
  <link rel="stylesheet" href="https://unpkg.com/mvp.css">
  <style>{css}</style>
</head>
<body>
  <header>
    <h1>STM Data Toolkit</h1>
    <p class="muted">Minimal notebooks + selected figures</p>
  </header>

  <main>
    <section class="card">
      <h2 style="margin-top:0">Notebooks</h2>
      {''.join(nb_html) if nb_html else '<p class="muted">No notebooks found.</p>'}
    </section>

    <section class="card">
      <h2 style="margin-top:0">Selected Figures</h2>
      <div class="grid">
        {''.join(img_html) if img_html else '<p class="muted">No figures found.</p>'}
      </div>
    </section>
  </main>

  <footer>Generated {now} · Source: https://github.com/{REPO}</footer>
</body>
</html>"""
    return html_doc

def main():
    notebooks = gather_notebooks()
    images = gather_images(max_count=6)
    html_out = render_html(notebooks, images)
    (DOCS_DIR / "index.html").write_text(html_out, encoding="utf-8")
    # 可选：防止 Jekyll 干预
    (DOCS_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"✅ Wrote {DOCS_DIR/'index.html'} with {len(notebooks)} notebooks and {len(images)} images.")

if __name__ == "__main__":
    main()
