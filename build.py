#!/usr/bin/env python3
"""
Build script: fetch images for all characters, encode as base64,
inject into game_template.html, produce final index.html.
"""
import base64, io, json, re, sys, os, time, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from pairs_database import PAIRS, DISPLAY_NAMES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

CACHE_DIR = os.path.join(os.path.dirname(__file__), ".img_cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def cache_key(wiki, page):
    h = hashlib.md5(f"{wiki}/{page}".encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.jpg")


def fetch_fandom_image(wiki_subdomain, page_title):
    """Fetch the main image from a fandom wiki page via API."""
    ck = cache_key(wiki_subdomain, page_title)
    if os.path.exists(ck):
        with open(ck, "rb") as f:
            return f.read()

    api_url = f"https://{wiki_subdomain}.fandom.com/api.php"

    # Method 1: pageimages
    try:
        params = {
            "action": "query", "titles": page_title,
            "prop": "pageimages", "pithumbsize": 500, "format": "json",
        }
        resp = requests.get(api_url, params=params, headers=HEADERS, timeout=15)
        pages = resp.json().get("query", {}).get("pages", {})
        for page in pages.values():
            thumb = page.get("thumbnail", {}).get("source")
            if thumb:
                img_resp = requests.get(thumb, headers=HEADERS, timeout=15)
                if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                    with open(ck, "wb") as f:
                        f.write(img_resp.content)
                    return img_resp.content
    except Exception:
        pass

    # Method 2: parse infobox
    try:
        params2 = {
            "action": "parse", "page": page_title,
            "prop": "text", "format": "json",
        }
        resp = requests.get(api_url, params=params2, headers=HEADERS, timeout=15)
        html_text = resp.json().get("parse", {}).get("text", {}).get("*", "")
        img_urls = re.findall(r'src="(https://static\.wikia\.nocookie\.net/[^"]+)"', html_text)
        for url in img_urls:
            if any(x in url.lower() for x in ["icon", "logo", "symbol", "banner"]):
                continue
            clean_url = re.sub(r'/revision/latest/scale-to-width-down/\d+',
                               '/revision/latest/scale-to-width-down/400', url)
            img_resp = requests.get(clean_url, headers=HEADERS, timeout=15)
            if img_resp.status_code == 200 and len(img_resp.content) > 2000:
                with open(ck, "wb") as f:
                    f.write(img_resp.content)
                return img_resp.content
    except Exception:
        pass

    return None


def image_to_base64(img_bytes):
    """Crop to face/upper-body portrait, resize to 200x200, return base64 data URI."""
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    w, h = img.size
    # First: crop to upper portion (face/head area) - keep top 55%
    if h > w:  # Portrait orientation
        crop_h = int(h * 0.55)
        img = img.crop((0, 0, w, crop_h))
        w, h = img.size
    # Then square crop from center-top
    side = min(w, h)
    left = (w - side) // 2
    top = 0  # Anchor to top, not center
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((250, 250), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def generate_placeholder(name):
    colors = ["#e74c3c","#e67e22","#f1c40f","#2ecc71","#1abc9c","#3498db","#9b59b6","#e91e63"]
    color = colors[sum(ord(c) for c in name) % len(colors)]
    initials = name[0].upper()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
<rect width="200" height="200" fill="{color}"/>
<text x="100" y="120" font-size="80" fill="white" text-anchor="middle" font-family="Arial,sans-serif">{initials}</text>
</svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def fetch_character(wiki, page, display):
    """Fetch a single character image. Returns (wiki, page, data_uri)."""
    img_bytes = fetch_fandom_image(wiki, page)
    if img_bytes:
        try:
            return (wiki, page, image_to_base64(img_bytes))
        except Exception:
            pass
    return (wiki, page, generate_placeholder(display))


def main():
    # Collect all unique characters (skip emoji-only pairs)
    chars = {}  # (wiki, page) -> display_name
    emoji_pairs = {}  # store emoji data for emoji-mode pairs
    for p in PAIRS:
        key1 = (p["wiki1"], p["page1"])
        key2 = (p["wiki2"], p["page2"])
        if p["wiki1"] == "emoji":
            emoji_pairs[key1] = p.get("emoji1", "❓")
        else:
            chars[key1] = DISPLAY_NAMES.get(p["page1"], p["civil"])
        if p["wiki2"] == "emoji":
            emoji_pairs[key2] = p.get("emoji2", "❓")
        else:
            chars[key2] = DISPLAY_NAMES.get(p["page2"], p["undercover"])

    print(f"Fetching images for {len(chars)} unique characters...")
    print(f"(Cached images in {CACHE_DIR})")

    char_images = {}  # (wiki, page) -> data_uri
    done = 0
    total = len(chars)

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for (wiki, page), display in chars.items():
            f = executor.submit(fetch_character, wiki, page, display)
            futures[f] = (wiki, page, display)

        for future in as_completed(futures):
            wiki, page, display = futures[future]
            _, _, data_uri = future.result()
            char_images[(wiki, page)] = data_uri
            done += 1
            is_placeholder = data_uri.startswith("data:image/svg")
            status = "PLACEHOLDER" if is_placeholder else "OK"
            print(f"  [{done}/{total}] {display} ({wiki}) ... {status}")

    # Generate emoji SVGs for emoji-mode pairs
    for key, emoji in emoji_pairs.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
<rect width="200" height="200" rx="20" fill="#1a1a2e"/>
<text x="100" y="130" font-size="100" text-anchor="middle" font-family="Apple Color Emoji,Segoe UI Emoji,Noto Color Emoji,sans-serif">{emoji}</text>
</svg>'''
        char_images[key] = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

    # Build JSON data
    pairs_json = []
    for p in PAIRS:
        pairs_json.append({
            "civil": p["civil"],
            "undercover": p["undercover"],
            "universe1": p["universe1"],
            "universe2": p["universe2"],
            "archetype": p["archetype"],
            "mode": p.get("mode", "normal"),
            "hint": p.get("hint", ""),
            "emoji1": p.get("emoji1", ""),
            "emoji2": p.get("emoji2", ""),
            "civilImg": char_images.get((p["wiki1"], p["page1"]), ""),
            "undercoverImg": char_images.get((p["wiki2"], p["page2"]), ""),
        })

    json_str = json.dumps(pairs_json, ensure_ascii=False)

    # Count stats
    ok_count = sum(1 for v in char_images.values() if not v.startswith("data:image/svg"))
    ph_count = sum(1 for v in char_images.values() if v.startswith("data:image/svg"))
    print(f"\nImages: {ok_count} fetched, {ph_count} placeholders")

    # Read template and inject
    template_path = os.path.join(os.path.dirname(__file__), "game_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    output = template.replace("__PAIRS_DATA_JSON__", json_str)

    output_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n=== BUILD COMPLETE ===")
    print(f"Output: {output_path}")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Pairs: {len(pairs_json)}")
    print(f"Characters: {len(chars)}")


if __name__ == "__main__":
    main()
