#!/usr/bin/env python3
"""
Audit images in index.html: check for placeholders/missing images,
retry fetching from fandom wikis, and report status.
"""
import json, re, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from pairs_database import PAIRS, DISPLAY_NAMES
from build import fetch_fandom_image, image_to_base64, generate_placeholder, CACHE_DIR

def main():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if not os.path.exists(index_path):
        print("index.html not found. Run build.py first.")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract PAIRS JSON from the file
    match = re.search(r'const PAIRS = (\[.*?\]);\s*\n', content, re.DOTALL)
    if not match:
        print("Could not find PAIRS data in index.html")
        return

    pairs = json.loads(match.group(1))
    print(f"Found {len(pairs)} pairs in index.html\n")

    total_imgs = 0
    ok_imgs = 0
    placeholder_imgs = 0
    missing_imgs = 0
    emoji_imgs = 0
    problems = []

    for i, pair in enumerate(pairs):
        for side, img_key, name_key in [("civil", "civilImg", "civil"), ("undercover", "undercoverImg", "undercover")]:
            total_imgs += 1
            img = pair.get(img_key, "")
            name = pair.get(name_key, "?")

            if not img:
                missing_imgs += 1
                problems.append(f"  MISSING: {name} (pair {i}: {pair['civil']} vs {pair['undercover']})")
            elif img.startswith("data:image/svg+xml"):
                # Check if it's an emoji SVG (intentional) or a placeholder (bad)
                if pair.get("emoji1") or pair.get("emoji2"):
                    emoji_imgs += 1
                elif "font-size" in img and "80" in img:
                    # Placeholder SVG with big letter
                    placeholder_imgs += 1
                    problems.append(f"  PLACEHOLDER: {name} (pair {i}: {pair['civil']} vs {pair['undercover']})")
                else:
                    emoji_imgs += 1  # Emoji SVG
            elif img.startswith("data:image/jpeg"):
                ok_imgs += 1
            else:
                ok_imgs += 1  # Other valid format

    print(f"=== IMAGE AUDIT REPORT ===")
    print(f"  Total images checked: {total_imgs}")
    print(f"  JPEG (OK):           {ok_imgs}")
    print(f"  Emoji SVGs:          {emoji_imgs}")
    print(f"  Placeholders:        {placeholder_imgs}")
    print(f"  Missing:             {missing_imgs}")
    print(f"  Success rate:        {(ok_imgs + emoji_imgs) / total_imgs * 100:.1f}%")

    if problems:
        print(f"\n  Problems ({len(problems)}):")
        for p in problems:
            print(p)
    else:
        print(f"\n  All images OK!")

    # Try to fix placeholders by retrying fetch
    if placeholder_imgs > 0 or missing_imgs > 0:
        print(f"\n  Attempting to fix {placeholder_imgs + missing_imgs} images...")
        print(f"  Run 'python build.py' to rebuild with fixes.")

    return placeholder_imgs + missing_imgs

if __name__ == "__main__":
    sys.exit(main() or 0)
