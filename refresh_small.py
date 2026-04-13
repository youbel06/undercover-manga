#!/usr/bin/env python3
"""Refresh small/placeholder images by deleting cache entries and re-fetching."""
import os, hashlib, json
from pairs_database import PAIRS

CACHE_DIR = '.img_cache'

with open('images.json','r',encoding='utf-8') as f:
    imgs = json.load(f)

to_refresh = []
for i, p in enumerate(PAIRS):
    for slot, key, w, pg, name in [
        ('c', f'c{i}', p.get('wiki1',''), p.get('page1',''), p['civil']),
        ('u', f'u{i}', p.get('wiki2',''), p.get('page2',''), p['undercover']),
    ]:
        if w == 'emoji' or w == 'none':
            continue
        v = imgs.get(key, '')
        # SVG placeholder or very small JPEG data URI (< 4000 chars ~ 3KB)
        if v.startswith('data:image/svg') or len(v) < 5000:
            h = hashlib.md5(f'{w}/{pg}'.encode()).hexdigest()
            path = os.path.join(CACHE_DIR, f'{h}.jpg')
            if os.path.exists(path):
                sz = os.path.getsize(path)
                if sz < 5000:
                    to_refresh.append((w, pg, name, path, sz))
                    try:
                        os.remove(path)
                    except Exception:
                        pass

print(f'Removed {len(to_refresh)} small cached images for re-fetch:')
for w, pg, name, path, sz in to_refresh[:30]:
    print(f'  {name} ({w}/{pg}) was {sz}B')
