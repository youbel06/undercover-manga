#!/usr/bin/env python3
"""
Aggressive image fetcher: tries multiple strategies to get character images.
Strategies: Fandom API → Fandom parse → Jikan API → Wikipedia → styled placeholder
"""
import base64, io, json, os, re, sys, hashlib, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from pairs_database import PAIRS, DISPLAY_NAMES

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".img_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_key(wiki, page):
    h = hashlib.md5(f"{wiki}/{page}".encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.jpg")

def try_fandom_api(wiki, page):
    """Strategy 1: Fandom pageimages API."""
    try:
        url = f"https://{wiki}.fandom.com/api.php"
        params = {"action":"query","titles":page,"prop":"pageimages","pithumbsize":500,"format":"json"}
        r = requests.get(url, params=params, headers=HEADERS, timeout=12)
        pages = r.json().get("query",{}).get("pages",{})
        for p in pages.values():
            thumb = p.get("thumbnail",{}).get("source")
            if thumb:
                img = requests.get(thumb, headers=HEADERS, timeout=12)
                if img.status_code == 200 and len(img.content) > 1000:
                    return img.content
    except: pass
    return None

def try_fandom_parse(wiki, page):
    """Strategy 2: Parse fandom page HTML for infobox image."""
    try:
        url = f"https://{wiki}.fandom.com/api.php"
        params = {"action":"parse","page":page,"prop":"text","format":"json"}
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        html = r.json().get("parse",{}).get("text",{}).get("*","")
        urls = re.findall(r'src="(https://static\.wikia\.nocookie\.net/[^"]+)"', html)
        for u in urls:
            if any(x in u.lower() for x in ["icon","logo","symbol","banner","flag"]): continue
            clean = re.sub(r'/revision/latest/scale-to-width-down/\d+','/revision/latest/scale-to-width-down/500',u)
            img = requests.get(clean, headers=HEADERS, timeout=12)
            if img.status_code == 200 and len(img.content) > 2000:
                return img.content
    except: pass
    return None

def try_alt_names(wiki, page, display):
    """Strategy 3: Try alternative page names."""
    alts = set()
    # First name only
    parts = page.split()
    if len(parts) > 1:
        alts.add(parts[0])
        alts.add(parts[-1])
    # Display name
    if display and display != page:
        alts.add(display)
    # Without parentheses
    base = re.sub(r'\s*\(.*?\)', '', page).strip()
    if base != page: alts.add(base)

    for alt in alts:
        if alt == page: continue
        result = try_fandom_api(wiki, alt)
        if result: return result
    return None

def try_jikan(name):
    """Strategy 4: Jikan MAL API for anime characters."""
    try:
        r = requests.get(f"https://api.jikan.moe/v4/characters?q={name}&limit=1",
                         headers=HEADERS, timeout=10)
        data = r.json().get("data",[])
        if data:
            img_url = data[0].get("images",{}).get("jpg",{}).get("image_url")
            if img_url:
                img = requests.get(img_url, headers=HEADERS, timeout=10)
                if img.status_code == 200 and len(img.content) > 1000:
                    return img.content
    except: pass
    return None

def try_wikipedia(name):
    """Strategy 5: Wikipedia pageimages."""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {"action":"query","titles":name,"prop":"pageimages","pithumbsize":500,"format":"json"}
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        pages = r.json().get("query",{}).get("pages",{})
        for p in pages.values():
            thumb = p.get("thumbnail",{}).get("source")
            if thumb:
                img = requests.get(thumb, headers=HEADERS, timeout=10)
                if img.status_code == 200 and len(img.content) > 1000:
                    return img.content
    except: pass
    return None

def fetch_aggressive(wiki, page, display):
    """Try all strategies in order."""
    ck = cache_key(wiki, page)
    if os.path.exists(ck):
        with open(ck, "rb") as f:
            return f.read()

    if wiki == "emoji":
        return None  # Emoji pairs don't need images

    # Strategy 1: Fandom API
    result = try_fandom_api(wiki, page)
    if result:
        with open(ck, "wb") as f: f.write(result)
        return result

    # Strategy 2: Parse HTML
    result = try_fandom_parse(wiki, page)
    if result:
        with open(ck, "wb") as f: f.write(result)
        return result

    # Strategy 3: Alt names
    result = try_alt_names(wiki, page, display)
    if result:
        with open(ck, "wb") as f: f.write(result)
        return result

    # Strategy 4: Jikan (anime chars only)
    time.sleep(0.35)  # Jikan rate limit
    result = try_jikan(display or page)
    if result:
        with open(ck, "wb") as f: f.write(result)
        return result

    # Strategy 5: Wikipedia
    result = try_wikipedia(page)
    if result:
        with open(ck, "wb") as f: f.write(result)
        return result

    return None

def main():
    # Collect chars that are missing from cache
    chars = {}
    for p in PAIRS:
        if p["wiki1"] != "emoji":
            chars[(p["wiki1"], p["page1"])] = DISPLAY_NAMES.get(p["page1"], p["civil"])
        if p["wiki2"] != "emoji":
            chars[(p["wiki2"], p["page2"])] = DISPLAY_NAMES.get(p["page2"], p["undercover"])

    missing = []
    cached = 0
    for (wiki, page), display in chars.items():
        ck = cache_key(wiki, page)
        if os.path.exists(ck):
            cached += 1
        else:
            missing.append((wiki, page, display))

    print(f"Total characters: {len(chars)}")
    print(f"Already cached: {cached}")
    print(f"Missing: {len(missing)}")

    if not missing:
        print("\nAll images cached! Nothing to fetch.")
        return 0

    print(f"\nFetching {len(missing)} missing images aggressively...")
    fetched = 0
    failed = []

    for i, (wiki, page, display) in enumerate(missing):
        result = fetch_aggressive(wiki, page, display)
        status = "OK" if result else "FAILED"
        if result:
            fetched += 1
        else:
            failed.append(f"{display} ({wiki}/{page})")
        print(f"  [{i+1}/{len(missing)}] {display} ({wiki}) ... {status}")

    print(f"\n=== AGGRESSIVE FETCH REPORT ===")
    print(f"  Fetched: {fetched}/{len(missing)}")
    print(f"  Still missing: {len(failed)}")
    if failed:
        print(f"\n  Failed characters:")
        for f in failed:
            print(f"    - {f}")

    return len(failed)

if __name__ == "__main__":
    sys.exit(main())
