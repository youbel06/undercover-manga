#!/usr/bin/env python3
"""Fetch anime character avatars for profile system."""
import base64, io, json, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))
from build import fetch_fandom_image, CACHE_DIR, HEADERS
from PIL import Image

AVATARS = [
    {"id":"av_naruto","name":"Naruto","wiki":"naruto","page":"Naruto Uzumaki","price":0},
    {"id":"av_goku","name":"Goku","wiki":"dragonball","page":"Goku","price":0},
    {"id":"av_luffy","name":"Luffy","wiki":"onepiece","page":"Monkey D. Luffy","price":0},
    {"id":"av_deku","name":"Deku","wiki":"myheroacademia","page":"Izuku Midoriya","price":0},
    {"id":"av_tanjiro","name":"Tanjiro","wiki":"kimetsu-no-yaiba","page":"Tanjiro Kamado","price":0},
    {"id":"av_pikachu","name":"Pikachu","wiki":"pokemon","page":"Pikachu","price":0},
    {"id":"av_sasuke","name":"Sasuke","wiki":"naruto","page":"Sasuke Uchiha","price":100},
    {"id":"av_vegeta","name":"Vegeta","wiki":"dragonball","page":"Vegeta","price":100},
    {"id":"av_zoro","name":"Zoro","wiki":"onepiece","page":"Roronoa Zoro","price":100},
    {"id":"av_ichigo","name":"Ichigo","wiki":"bleach","page":"Ichigo Kurosaki","price":100},
    {"id":"av_eren","name":"Eren","wiki":"attackontitan","page":"Eren Yeager","price":100},
    {"id":"av_levi","name":"Levi","wiki":"attackontitan","page":"Levi Ackerman","price":100},
    {"id":"av_bakugo","name":"Bakugo","wiki":"myheroacademia","page":"Katsuki Bakugo","price":100},
    {"id":"av_killua","name":"Killua","wiki":"hunterxhunter","page":"Killua Zoldyck","price":100},
    {"id":"av_gojo","name":"Gojo","wiki":"jujutsu-kaisen","page":"Satoru Gojo","price":200},
    {"id":"av_aizen","name":"Aizen","wiki":"bleach","page":"Sousuke Aizen","price":200},
    {"id":"av_sukuna","name":"Sukuna","wiki":"jujutsu-kaisen","page":"Sukuna","price":200},
    {"id":"av_light","name":"Light","wiki":"deathnote","page":"Light Yagami","price":200},
    {"id":"av_l","name":"L","wiki":"deathnote","page":"L (character)","price":200},
    {"id":"av_saitama","name":"Saitama","wiki":"onepunchman","page":"Saitama","price":200},
    {"id":"av_rengoku","name":"Rengoku","wiki":"kimetsu-no-yaiba","page":"Kyojuro Rengoku","price":-1},
    {"id":"av_edward","name":"Edward","wiki":"fma","page":"Edward Elric","price":-1},
    {"id":"av_gon","name":"Gon","wiki":"hunterxhunter","page":"Gon Freecss","price":-1},
    {"id":"av_spike","name":"Spike","wiki":"cowboy-bebop","page":"Spike Spiegel","price":-1},
]

def crop_avatar(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    w, h = img.size
    if h > w:
        crop_h = int(h * 0.45)
        img = img.crop((0, 0, w, crop_h))
        w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    img = img.crop((left, 0, left + side, side))
    img = img.resize((150, 150), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=75)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def main():
    results = {}
    print(f"Fetching {len(AVATARS)} anime avatars...")

    def fetch_one(av):
        img = fetch_fandom_image(av["wiki"], av["page"])
        if img:
            return av["id"], crop_avatar(img)
        return av["id"], None

    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch_one, av): av for av in AVATARS}
        for f in as_completed(futs):
            av = futs[f]
            aid, data = f.result()
            status = "OK" if data else "FAILED"
            print(f"  {av['name']}: {status}")
            if data:
                results[aid] = data

    # Write avatars.json
    with open("avatars.json", "w", encoding="utf-8") as f:
        json.dump(results, f)

    # Write avatar metadata for the template
    meta = []
    for av in AVATARS:
        meta.append({
            "id": av["id"], "name": av["name"],
            "price": av["price"], "hasImage": av["id"] in results,
            "imgKey": av["id"],
        })
    with open("avatars_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f)

    size = os.path.getsize("avatars.json") / 1024
    print(f"\navatars.json: {size:.0f} KB ({len(results)}/{len(AVATARS)} images)")

if __name__ == "__main__":
    main()
