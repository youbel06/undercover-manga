#!/usr/bin/env python3
"""V15b: Fix anime avatar display + full simulation fixes."""
import json

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Load avatar data and EMBED it inline (small enough at 176KB)
with open("avatars.json", "r", encoding="utf-8") as f:
    avatar_data = json.load(f)

# ═══════════════════════════════════════════════════════════
# FIX 1: Embed avatar images directly (they're only 176KB)
# Instead of relying on async fetch, inject data inline
# ═══════════════════════════════════════════════════════════

# Replace the loadAvatarImages function with pre-loaded data
old_loader = """var _avatarImagesCache = null;

async function loadAvatarImages() {"""

# Truncate: build a compact version
avatar_json_str = json.dumps(avatar_data, ensure_ascii=False)

new_loader = f"""var _avatarImagesCache = {avatar_json_str};

async function loadAvatarImages() {{
  // Already loaded inline
  return _avatarImagesCache;
"""

# Only replace the first line and function declaration
html = html.replace(
    "var _avatarImagesCache = null;\n\nasync function loadAvatarImages() {",
    f"var _avatarImagesCache = {avatar_json_str};\n\nasync function loadAvatarImages() {{\n  return _avatarImagesCache;"
)

# Hmm that might break the function body. Let me be more surgical.
# Actually, let's just set _avatarImagesCache at declaration time.
# The existing function will see it's already loaded and return early.

# Revert and do it properly
html = html.replace(
    f"var _avatarImagesCache = {avatar_json_str};\n\nasync function loadAvatarImages() {{\n  return _avatarImagesCache;",
    "var _avatarImagesCache = null;\n\nasync function loadAvatarImages() {"
)

# Simple approach: just replace `var _avatarImagesCache = null;`
html = html.replace(
    "var _avatarImagesCache = null;",
    "var _avatarImagesCache = " + avatar_json_str + ";"
)

# ═══════════════════════════════════════════════════════════
# FIX 2: Render anime avatars as <img> in cosmetics screen
# Override the cosmetics rendering to handle isPhoto avatars
# ═══════════════════════════════════════════════════════════

JS_FIX = r"""

// ===== V15b: FIX ANIME AVATAR RENDERING =====
var _origRenderCosmeticsV15b = renderCosmeticsScreen;
renderCosmeticsScreen = function() {
  _origRenderCosmeticsV15b();
  // Post-process: replace 📷 icons with real images for photo avatars
  var tabs = document.getElementById("cosm-tabs");
  var activeTab = tabs?.dataset.active || "avatars";
  if (activeTab !== "avatars") return;

  var grid = document.getElementById("cosm-grid");
  if (!grid) return;
  var items = grid.querySelectorAll(".cosmetic-item");
  items.forEach(function(item) {
    var nameEl = item.querySelector("div:last-child");
    var iconEl = item.querySelector(".ci-icon");
    if (!nameEl || !iconEl) return;
    var name = nameEl.textContent;
    // Find matching anime avatar
    var av = ALL_AVATARS.find(function(a) { return a.isPhoto && a.name === name; });
    if (av && _avatarImagesCache && _avatarImagesCache[av.imgKey]) {
      iconEl.innerHTML = "<img src=\"" + _avatarImagesCache[av.imgKey] + "\" style=\"width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:top\" />";
    }
  });

  // Also update the preview at top
  updateCosmeticsPreview();
};

function updateCosmeticsPreview() {
  var eq = getEquipped();
  var preview = document.getElementById("cosm-preview");
  if (!preview) return;
  // Check if equipped avatar is a photo avatar
  var av = ALL_AVATARS.find(function(a) { return a.isPhoto && a.icon !== eq.avatar && _avatarImagesCache && _avatarImagesCache[a.imgKey]; });
  // Check by stored ID
  if (eq.avatarId) {
    var photoAv = ALL_AVATARS.find(function(a) { return a.id === eq.avatarId && a.isPhoto; });
    if (photoAv && _avatarImagesCache && _avatarImagesCache[photoAv.imgKey]) {
      preview.innerHTML = "<img src=\"" + _avatarImagesCache[photoAv.imgKey] + "\" class=\"photo-avatar-lg\" />";
      return;
    }
  }
  // Fallback: show emoji
  if (preview.querySelector("img")) return; // already has image
  preview.textContent = eq.avatar;
}

// Patch equipCosmetic to store avatar ID for photo lookup
var _origEquipCosmetic = equipCosmetic;
equipCosmetic = function(type, id) {
  _origEquipCosmetic(type, id);
  if (type === "avatar") {
    if (!Economy._data.equipped) Economy._data.equipped = {};
    Economy._data.equipped.avatarId = id;
    Economy.save();
  }
};

// Patch getEquipped to include avatarId
var _origGetEquipped = getEquipped;
getEquipped = function() {
  var eq = _origGetEquipped();
  eq.avatarId = Economy._data?.equipped?.avatarId || null;
  return eq;
};

// ===== V15b: FIX ITEM MODAL FOR PHOTO AVATARS =====
var _origOpenItemModal = openItemModal;
openItemModal = function(opts) {
  _origOpenItemModal(opts);
  // If it's a photo avatar, replace preview with actual image
  if (opts.type === "avatar") {
    var av = ALL_AVATARS.find(function(a) { return a.id === opts.id && a.isPhoto; });
    if (av && _avatarImagesCache && _avatarImagesCache[av.imgKey]) {
      var preview = document.getElementById("im-preview");
      if (preview) {
        preview.innerHTML = "<img src=\"" + _avatarImagesCache[av.imgKey] + "\" style=\"width:80px;height:80px;border-radius:50%;object-fit:cover;object-position:top\" />";
      }
    }
  }
};
"""

html = html.replace("\n</script>", JS_FIX + "\n</script>")

# ═══════════════════════════════════════════════════════════
# FIX 3: Gacha close button always visible after all revealed
# ═══════════════════════════════════════════════════════════
# Already fixed in V14b with .gacha-actions div

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V15b patch applied! {len(html)//1024} KB")
# Note: avatars are now embedded inline, no need for separate avatars.json fetch
