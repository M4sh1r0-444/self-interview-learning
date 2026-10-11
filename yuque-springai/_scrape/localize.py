# -*- coding: utf-8 -*-
"""Download images, rewrite image URLs and internal doc links to local relative paths."""
import glob
import hashlib
import json
import os
import re
import time
import urllib.request

ROOT = r"D:\aiface\yuque-springai"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

plan = json.load(open(os.path.join(ROOT, "_scrape", "plan.json"), encoding="utf-8"))
slug2path = {p["slug"]: p["path"].rsplit("/", 1)[-1][3:-3] for p in plan}  # title without order prefix
# map slug -> full rel path (keep dirs)
slug2rel = {p["slug"]: p["path"] for p in plan}

# 0-index root intro renamed to 00
slug2rel["gvi7xfgq8bq0zenw"] = "00-项目介绍.md"

os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)

# ---- collect image urls ----
md_files = [f for f in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)]
img_re = re.compile(r'(!\[[^\]]*\]\()([^)\s]+)([^)]*\))')
html_img_re = re.compile(r'(<img[^>]+src=")([^"]+)(")')

url_map = {}  # url -> local filename
for f in md_files:
    text = open(f, encoding="utf-8").read()
    for m in img_re.finditer(text):
        url_map.setdefault(m.group(2), None)
    for m in html_img_re.finditer(text):
        url_map.setdefault(m.group(2), None)

print("distinct urls:", len(url_map))

def ext_of(url):
    m = re.search(r'\.(png|jpe?g|gif|svg|webp|bmp)([?#].*)?$', url, re.I)
    return "." + m.group(1).lower() if m else ".png"

fails = []
for url in url_map:
    h = hashlib.md5(url.encode()).hexdigest()[:10]
    fname = h + "-" + url.rsplit("/", 1)[-1].split("?")[0]
    fname = re.sub(r'[\\/:*?"<>|]', "_", fname)[:100]
    if not os.path.splitext(fname)[1]:
        fname += ext_of(url)
    dest = os.path.join(ROOT, "images", fname)
    if not os.path.exists(dest) or os.path.getsize(dest) == 0:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.javaguide.cn/"})
            with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as out:
                out.write(r.read())
            time.sleep(0.15)
        except Exception as e:
            fails.append((url, str(e)))
            continue
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        url_map[url] = fname

print("downloaded ok:", sum(1 for v in url_map.values() if v), "failed:", len(fails))
for u, e in fails:
    print("FAIL", u, e)

# ---- rewrite markdown ----
def rel_target(md_path, target):
    return os.path.relpath(target, os.path.dirname(md_path)).replace("\\", "/")

changed_files = 0
for f in md_files:
    rel_f = os.path.relpath(f, ROOT).replace("\\", "/")
    text = open(f, encoding="utf-8").read()
    orig = text

    def img_sub(m):
        url = m.group(2)
        local = url_map.get(url)
        if not local:
            return m.group(0)
        return m.group(1) + rel_target(f, os.path.join(ROOT, "images", local)) + m.group(3)

    text = img_re.sub(img_sub, text)

    def hsrc_sub(m):
        url = m.group(2)
        local = url_map.get(url)
        if not local:
            return m.group(0)
        return m.group(1) + rel_target(f, os.path.join(ROOT, "images", local)) + m.group(3)

    text = html_img_re.sub(hsrc_sub, text)

    # internal doc links: https://www.yuque.com/snailclimb/itdq8h/<slug>(/...) or relative /snailclimb/itdq8h/<slug>
    def link_sub(m):
        slug = m.group(2).split("/")[0]
        if slug in slug2rel:
            return m.group(1) + rel_target(f, os.path.join(ROOT, slug2rel[slug])) + m.group(3)
        return m.group(0)

    text = re.sub(r'(\]\()(?:https://www\.yuque\.com)?/snailclimb/itdq8h/([A-Za-z0-9]+[^)\s]*)(\))', link_sub, text)

    if text != orig:
        open(f, "w", encoding="utf-8", newline="\n").write(text)
        changed_files += 1

print("rewritten files:", changed_files)
