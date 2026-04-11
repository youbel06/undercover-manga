#!/usr/bin/env python3
"""Fix wiki page names that failed to fetch."""

import re

REPLACEMENTS = {
    # URL-encoded special chars -> proper unicode
    "S%C5%8Dsuke Aizen": "Sousuke Aizen",
    "Neji Hy%C5%ABga": "Neji Hyūga",
    "Hinata Hy%C5%ABga": "Hinata Hyūga",
    "Kaguya %C5%8Ctsutsuki": "Kaguya Ōtsutsuki",
    "T%C5%8Dshir%C5%8D Hitsugaya": "Tōshirō Hitsugaya",
    "Yoruichi Shih%C5%8Din": "Yoruichi Shihōin",
    # AOT pages without (Anime) suffix
    "Eren Yeager (Anime)": "Eren Yeager",
    "Mikasa Ackerman (Anime)": "Mikasa Ackerman",
    "Levi Ackerman (Anime)": "Levi Ackerman",
    "Armin Arlert (Anime)": "Armin Arlert",
    "Zeke Yeager (Anime)": "Zeke Yeager",
    "Marco Bott (Anime)": "Marco Bott",
    # FMA fixes
    "Scar (2003 Anime)": "Scar",
    "Father (Homunculus)": "Father",
    # Other
    "Ryomen Sukuna": "Sukuna",
    "Vinsmoke Sanji": "Sanji",
    "Tetsuo Shima": "Tetsuo Shima",  # keep as-is, akira wiki
}

with open("pairs_database.py", "r", encoding="utf-8") as f:
    content = f.read()

for old, new in REPLACEMENTS.items():
    if old != new:
        content = content.replace(f'"{old}"', f'"{new}"')
        print(f"  Replaced: {old} -> {new}")

with open("pairs_database.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\nDone!")
