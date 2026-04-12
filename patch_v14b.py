#!/usr/bin/env python3
"""V14b: Fix mpQuickMatch, add preview modals for avatars/frames."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# CSS for avatar/frame preview modal
# ═══════════════════════════════════════════════════════════
CSS = """
/* ===== V14b ITEM PREVIEW MODAL ===== */
.item-modal{position:fixed;top:0;left:0;width:100%;height:100%;z-index:500;
  background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity 0.3s}
.item-modal.open{opacity:1;pointer-events:auto}
.item-modal-card{background:var(--bg-secondary);border:1px solid var(--border-glass);
  border-radius:var(--radius-xl);padding:28px;text-align:center;max-width:320px;width:90%}
.item-modal-preview{width:100px;height:100px;border-radius:50%;margin:0 auto 12px;
  display:flex;align-items:center;justify-content:center;font-size:3rem}
.item-modal-name{font-size:1.1rem;font-weight:700;color:var(--text-bright);margin-bottom:4px}
.item-modal-rarity{font-size:0.75rem;margin-bottom:8px}
.item-modal-rarity.common{color:#9ca3af}
.item-modal-rarity.rare{color:#3b82f6}
.item-modal-rarity.epic{color:#a855f7}
.item-modal-rarity.legendary{color:#f59e0b}
.item-modal-desc{font-size:0.8rem;color:var(--text-muted);margin-bottom:12px}
.item-modal-price{font-size:1.1rem;color:var(--accent-gold);font-weight:700;margin-bottom:14px}
.item-modal-actions{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
"""
html = html.replace("/* ===== APP CONTAINER ===== */", CSS + "\n/* ===== APP CONTAINER ===== */")

# Add item modal HTML
html = html.replace(
    '<!-- ===== TOAST ===== -->',
    '<!-- ===== ITEM PREVIEW MODAL ===== -->\n'
    '<div class="item-modal" id="item-modal">\n'
    '  <div class="item-modal-card">\n'
    '    <div class="item-modal-preview" id="im-preview"></div>\n'
    '    <div class="item-modal-name" id="im-name"></div>\n'
    '    <div class="item-modal-rarity" id="im-rarity"></div>\n'
    '    <div class="item-modal-desc" id="im-desc"></div>\n'
    '    <div class="item-modal-price" id="im-price"></div>\n'
    '    <div class="item-modal-actions" id="im-actions"></div>\n'
    '  </div>\n'
    '</div>\n\n'
    '<!-- ===== TOAST ===== -->'
)

# ═══════════════════════════════════════════════════════════
# JavaScript
# ═══════════════════════════════════════════════════════════
JS = r"""

// ===== V14b: FIX mpQuickMatch =====
async function mpQuickMatch() {
  if (!await mpEnsurePlayer()) { renderMpProfileForm(); return; }
  showToast("Recherche d'une partie...");
  var res = await sb.from("rooms").select("*").eq("status", "waiting").limit(5);
  var rooms = res.data || [];
  if (rooms.length > 0) {
    var room = rooms[Math.floor(Math.random() * rooms.length)];
    document.getElementById("mp-join-code").value = room.code;
    await mpJoinRoom();
  } else {
    showToast("Aucune partie trouvée, création...");
    await mpCreateRoom();
  }
}


// ===== V14b: ITEM PREVIEW MODAL (avatars, frames, colors) =====
function openItemModal(opts) {
  // opts: {icon, name, rarity, desc, price, owned, type, id, cls}
  var preview = document.getElementById("im-preview");
  preview.textContent = opts.icon || "?";
  preview.className = "item-modal-preview";
  if (opts.cls) preview.classList.add("anime-avatar", opts.cls);
  if (opts.bgColor) preview.style.background = opts.bgColor;

  document.getElementById("im-name").textContent = opts.name || "";
  var rarityEl = document.getElementById("im-rarity");
  var stars = opts.rarity === "legendary" ? "★★★★★" : opts.rarity === "epic" ? "★★★★★" : opts.rarity === "rare" ? "★★★★" : "★★★";
  rarityEl.textContent = stars;
  rarityEl.className = "item-modal-rarity " + (opts.rarity || "common");
  document.getElementById("im-desc").textContent = opts.desc || "";

  var priceEl = document.getElementById("im-price");
  var actionsEl = document.getElementById("im-actions");

  if (opts.equipped) {
    priceEl.textContent = "✓ Équipé";
    actionsEl.innerHTML = "<button class=\"btn btn-ghost\" onclick=\"closeItemModal()\">Fermer</button>";
  } else if (opts.owned) {
    priceEl.textContent = "Possédé";
    actionsEl.innerHTML = "<button class=\"btn btn-primary\" onclick=\"equipFromModal('" + opts.type + "','" + opts.id + "')\">Équiper</button>" +
      "<button class=\"btn btn-ghost\" onclick=\"closeItemModal()\">Fermer</button>";
  } else if (opts.gachaOnly) {
    priceEl.textContent = "🎰 Gacha uniquement";
    actionsEl.innerHTML = "<button class=\"btn btn-primary\" onclick=\"closeItemModal();showScreen('screen-gacha')\">Aller au Gacha</button>" +
      "<button class=\"btn btn-ghost\" onclick=\"closeItemModal()\">Fermer</button>";
  } else {
    priceEl.textContent = (opts.price || 0) + " 💎";
    actionsEl.innerHTML = "<button class=\"btn btn-primary\" onclick=\"buyFromModal('" + opts.type + "','" + opts.id + "'," + (opts.price||0) + ")\">Acheter</button>" +
      "<button class=\"btn btn-ghost\" onclick=\"closeItemModal()\">Annuler</button>";
  }

  document.getElementById("item-modal").classList.add("open");
  SoundFX.click();
}

function closeItemModal() {
  document.getElementById("item-modal").classList.remove("open");
}

function equipFromModal(type, id) {
  equipCosmetic(type, id);
  closeItemModal();
  showToast("Équipé !");
}

function buyFromModal(type, id, price) {
  if (type === "avatar") {
    // Buy avatar directly
    if (!Economy.spendGems(price)) { showToast("Pas assez de gemmes !"); return; }
    if (!Economy._data.gachaCollection) Economy._data.gachaCollection = [];
    var av = ALL_AVATARS.find(function(a){return a.id===id});
    if (av && !Economy._data.gachaCollection.find(function(c){return c.name===av.name})) {
      Economy._data.gachaCollection.push({icon:av.icon, name:av.name, type:"avatar", rarity:av.rarity});
    }
    Economy.save();
    equipCosmetic("avatar", id);
  } else if (type === "frame") {
    if (!Economy.spendGems(price)) { showToast("Pas assez de gemmes !"); return; }
    if (!Economy._data.ownedFrames) Economy._data.ownedFrames = [];
    if (!Economy._data.ownedFrames.includes(id)) Economy._data.ownedFrames.push(id);
    Economy.save();
    equipCosmetic("frame", id);
  } else if (type === "color") {
    if (!Economy.spendGems(price)) { showToast("Pas assez de gemmes !"); return; }
    if (!Economy._data.ownedColors) Economy._data.ownedColors = [];
    if (!Economy._data.ownedColors.includes(id)) Economy._data.ownedColors.push(id);
    Economy.save();
  }
  closeItemModal();
  showToast("Acheté et équipé ! 🎉");
  renderCosmeticsScreen();
}


// ===== V14b: PATCH cosmetics screen to use modal =====
var _origRenderCosmeticsV14b = renderCosmeticsScreen;
renderCosmeticsScreen = function() {
  _origRenderCosmeticsV14b();
  // Re-bind clicks on cosmetic items to open modal
  document.querySelectorAll("#cosm-grid .cosmetic-item").forEach(function(item) {
    // Remove existing onclick and add modal opener
    var origClick = item.onclick;
    item.onclick = function(e) {
      e.preventDefault();
      // Determine what item this is from the DOM
      var icon = item.querySelector(".ci-icon")?.textContent || "?";
      var name = item.querySelector("div:last-child")?.textContent || "?";
      var isEquipped = item.classList.contains("equipped");
      var isLocked = item.classList.contains("locked");

      // Find matching avatar/frame
      var tabs = document.getElementById("cosm-tabs");
      var activeTab = tabs?.dataset.active || "avatars";

      if (activeTab === "avatars") {
        var av = ALL_AVATARS.find(function(a){return a.icon===icon || a.name===name});
        if (av) {
          var owned = ownsCosmetic("avatar", av.id) || av.rarity === "common";
          var gachaOnly = av.rarity === "epic" || av.rarity === "legendary";
          var price = av.rarity === "rare" ? 150 : av.rarity === "common" ? 50 : 0;
          openItemModal({
            icon:av.icon, name:av.name, rarity:av.rarity,
            desc:"Avatar " + av.rarity, price:price,
            owned:owned, equipped:isEquipped, gachaOnly:gachaOnly && !owned,
            type:"avatar", id:av.id, cls:av.cls||""
          });
        }
      } else if (activeTab === "frames") {
        var fr = ALL_FRAMES.find(function(f){return f.name===name});
        if (fr) {
          var ownedF = ownsCosmetic("frame", fr.id) || fr.rarity === "common";
          var gachaOnlyF = fr.rarity === "legendary";
          var priceF = fr.rarity === "rare" ? 100 : fr.rarity === "epic" ? 200 : 0;
          openItemModal({
            icon:"🖼️", name:fr.name, rarity:fr.rarity,
            desc:"Cadre de profil " + fr.rarity, price:priceF,
            owned:ownedF, equipped:isEquipped, gachaOnly:gachaOnlyF && !ownedF,
            type:"frame", id:fr.id
          });
        }
      }
    };
  });
};
"""

html = html.replace("\n</script>", JS + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"V14b patch applied! {len(html)//1024} KB")
