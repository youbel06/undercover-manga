#!/usr/bin/env python3
"""V15: Anime avatars, progression timeline, aura levels, reactions, hall of fame."""
import json

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Load avatar metadata
with open("avatars_meta.json", "r") as f:
    avatars_meta = json.load(f)

CSS = """
/* ===== V15 ANIME PHOTO AVATARS ===== */
.photo-avatar{width:48px;height:48px;border-radius:50%;object-fit:cover;object-position:top}
.photo-avatar-lg{width:100px;height:100px;border-radius:50%;object-fit:cover;object-position:top;border:3px solid var(--border-glass)}

/* Aura levels */
.aura-5{box-shadow:0 0 10px rgba(255,255,255,0.2)}
.aura-10{box-shadow:0 0 15px rgba(0,212,255,0.3)}
.aura-20{box-shadow:0 0 20px rgba(239,68,68,0.4);animation:auraFlame 1.5s ease infinite}
@keyframes auraFlame{0%,100%{box-shadow:0 0 15px rgba(239,68,68,0.3)}50%{box-shadow:0 0 25px rgba(239,68,68,0.5)}}
.aura-30{animation:auraRainbow 3s linear infinite}
@keyframes auraRainbow{0%{box-shadow:0 0 20px rgba(239,68,68,0.4)}33%{box-shadow:0 0 20px rgba(34,197,94,0.4)}66%{box-shadow:0 0 20px rgba(59,130,246,0.4)}100%{box-shadow:0 0 20px rgba(239,68,68,0.4)}}
.aura-40{box-shadow:0 0 25px rgba(245,158,11,0.5);animation:auraGold 2s ease infinite}
@keyframes auraGold{0%,100%{box-shadow:0 0 20px rgba(245,158,11,0.4)}50%{box-shadow:0 0 35px rgba(245,158,11,0.6)}}
.aura-50{background:conic-gradient(from 0deg,rgba(59,130,246,0.3),rgba(168,85,247,0.3),rgba(239,68,68,0.3),rgba(245,158,11,0.3),rgba(59,130,246,0.3));animation:auraGalaxy 4s linear infinite;padding:4px}
@keyframes auraGalaxy{from{filter:hue-rotate(0)}to{filter:hue-rotate(360deg)}}

/* ===== V15 PROGRESSION TIMELINE ===== */
.timeline{width:100%;max-width:400px;position:relative;padding-left:30px}
.timeline::before{content:'';position:absolute;left:12px;top:0;bottom:0;width:2px;background:var(--border-glass)}
.tl-item{position:relative;padding:12px 0 12px 20px;cursor:pointer}
.tl-item::before{content:'';position:absolute;left:-22px;top:16px;width:14px;height:14px;
  border-radius:50%;background:var(--bg-card);border:2px solid var(--border-glass);z-index:1}
.tl-item.done::before{background:var(--accent-green);border-color:var(--accent-green)}
.tl-item.current::before{background:var(--accent-gold);border-color:var(--accent-gold);
  box-shadow:0 0 10px rgba(245,158,11,0.5);animation:pulse 1.5s ease infinite}
.tl-item.locked{opacity:0.4}
.tl-level{font-size:0.7rem;color:var(--accent-gold);font-weight:700;text-transform:uppercase}
.tl-title{font-weight:600;font-size:0.85rem;color:var(--text-bright)}
.tl-reward{font-size:0.75rem;color:var(--text-muted)}

/* ===== V15 REACTIONS ===== */
.reaction-fab{position:fixed;bottom:70px;right:12px;z-index:360;width:44px;height:44px;
  border-radius:50%;background:var(--bg-secondary);border:1px solid var(--border-glass);
  display:none;align-items:center;justify-content:center;font-size:1.2rem;cursor:pointer}
.reaction-fab.active{display:flex}
.reaction-wheel{position:fixed;bottom:120px;right:8px;z-index:361;display:none;
  flex-wrap:wrap;gap:6px;width:130px;background:var(--bg-secondary);border:1px solid var(--border-glass);
  border-radius:var(--radius-md);padding:8px;justify-content:center}
.reaction-wheel.show{display:flex}
.reaction-wheel button{width:40px;height:40px;border-radius:50%;border:none;
  background:var(--bg-card);font-size:1.3rem;cursor:pointer;transition:transform 0.2s}
.reaction-wheel button:hover{transform:scale(1.2)}
.reaction-bubble{position:absolute;top:-30px;left:50%;transform:translateX(-50%);
  font-size:1.5rem;animation:reactionFloat 2s ease forwards;pointer-events:none;z-index:10}
@keyframes reactionFloat{0%{opacity:1;transform:translateX(-50%) translateY(0) scale(1)}
  100%{opacity:0;transform:translateX(-50%) translateY(-40px) scale(1.5)}}

/* ===== V15 HALL OF FAME ===== */
.hof{width:100%;max-width:350px;margin:10px auto}
.hof-title{font-size:0.75rem;color:var(--accent-gold);text-transform:uppercase;letter-spacing:1px;text-align:center;margin-bottom:8px}
.hof-row{display:flex;align-items:center;gap:8px;padding:6px 10px;border-radius:var(--radius-sm);margin-bottom:4px}
.hof-row:first-child{background:rgba(245,166,35,0.08)}
.hof-medal{font-size:1.2rem;width:24px;text-align:center}
.hof-name{flex:1;font-size:0.8rem;font-weight:600;color:var(--text-bright)}
.hof-pts{font-size:0.75rem;color:var(--accent-gold)}
"""
html = html.replace("/* ===== APP CONTAINER ===== */", CSS + "\n/* ===== APP CONTAINER ===== */")

# Add progression screen, reaction elements, HoF section
html = html.replace(
    '  <!-- ===== CREDITS SCREEN ===== -->',
    '  <!-- ===== PROGRESSION SCREEN ===== -->\n'
    '  <div id="screen-progression" class="screen" style="padding-top:50px">\n'
    '    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen(\'screen-profile\')">←</button>\n'
    '    <h2>📈 Progression</h2>\n'
    '    <div class="timeline" id="progression-timeline"></div>\n'
    '  </div>\n\n'
    '  <!-- ===== CREDITS SCREEN ===== -->'
)

# Add progression button to profile
html = html.replace(
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-cosmetics\')">🎨 Personnalisation</button>',
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-cosmetics\')">🎨 Personnalisation</button>'
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-progression\')">📈 Progression</button>'
)

# Add HoF to splash (after daily challenge)
html = html.replace(
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-history\')">Historique</button>',
    '<div class="hof" id="hof-section"></div>\n'
    '    <button class="btn btn-ghost" onclick="showScreen(\'screen-history\')">Historique</button>'
)

# Add reaction elements
html = html.replace(
    '<!-- ===== BOTTOM NAV ===== -->',
    '<!-- ===== REACTIONS ===== -->\n'
    '<div class="reaction-fab" id="reaction-fab" onclick="toggleReactions()">😄</div>\n'
    '<div class="reaction-wheel" id="reaction-wheel"></div>\n\n'
    '<!-- ===== BOTTOM NAV ===== -->'
)

# Update sw.js cache list
html_sw = open("sw.js", "r").read()
html_sw = html_sw.replace(
    "const ASSETS = ['./', './index.html', './images.json'];",
    "const ASSETS = ['./', './index.html', './images.json', './avatars.json'];"
)
html_sw = html_sw.replace("'uc-lelox-v13'", "'uc-lelox-v15'")
open("sw.js", "w").write(html_sw)

# ═══════════════════════════════════════════════════════════
# JavaScript
# ═══════════════════════════════════════════════════════════
AVATARS_META_JS = json.dumps(avatars_meta)

JS = """

// ===== V15 ANIME PHOTO AVATARS =====
var ANIME_AVATAR_META = """ + AVATARS_META_JS + """;
var _avatarImagesCache = null;

async function loadAvatarImages() {
  if (_avatarImagesCache) return _avatarImagesCache;
  try {
    // Try IndexedDB
    var cached = await new Promise(function(resolve) {
      try {
        var req = indexedDB.open("uc_avatars", 1);
        req.onupgradeneeded = function(e) { e.target.result.createObjectStore("av"); };
        req.onsuccess = function(e) {
          var tx = e.target.result.transaction("av","readonly");
          var g = tx.objectStore("av").get("all");
          g.onsuccess = function() { resolve(g.result || null); };
          g.onerror = function() { resolve(null); };
        };
        req.onerror = function() { resolve(null); };
      } catch(e) { resolve(null); }
    });
    if (cached) { _avatarImagesCache = cached; return cached; }
    var resp = await fetch("avatars.json");
    if (resp.ok) {
      _avatarImagesCache = await resp.json();
      // Save to IDB
      try {
        var req = indexedDB.open("uc_avatars", 1);
        req.onupgradeneeded = function(e) { e.target.result.createObjectStore("av"); };
        req.onsuccess = function(e) { e.target.result.transaction("av","readwrite").objectStore("av").put(_avatarImagesCache, "all"); };
      } catch(e) {}
      return _avatarImagesCache;
    }
  } catch(e) {}
  return {};
}

function getAnimeAvatarSrc(avatarId) {
  if (!_avatarImagesCache) return "";
  return _avatarImagesCache[avatarId] || "";
}

// Preload
setTimeout(function() { loadAvatarImages(); }, 3000);

// Add anime avatars to ALL_AVATARS
ANIME_AVATAR_META.forEach(function(av) {
  if (!ALL_AVATARS.find(function(a){return a.id===av.id})) {
    var rarity = av.price === 0 ? "common" : av.price <= 100 ? "rare" : av.price <= 200 ? "epic" : "legendary";
    ALL_AVATARS.push({
      id: av.id, icon: "📷", name: av.name, rarity: rarity,
      isPhoto: true, imgKey: av.imgKey, price: av.price
    });
  }
});


// ===== V15 AURA BY LEVEL =====
function getAuraClass(level) {
  if (level >= 50) return "aura-50";
  if (level >= 40) return "aura-40";
  if (level >= 30) return "aura-30";
  if (level >= 20) return "aura-20";
  if (level >= 10) return "aura-10";
  if (level >= 5) return "aura-5";
  return "";
}


// ===== V15 PROGRESSION TIMELINE =====
var MILESTONES = [
  {level:1,title:"Rookie",reward:"Avatar Ninja + 500💎"},
  {level:3,title:"Anime Classique",reward:"Mode débloqué + 50💎"},
  {level:5,title:"Frame Flammes",reward:"Cadre animé + gacha"},
  {level:8,title:"Avatar Sabreur",reward:"Nouvel avatar"},
  {level:10,title:"Initié",reward:"+5% gemmes, mode Shōnen"},
  {level:15,title:"Avatar Dragon",reward:"Particules sur avatar"},
  {level:20,title:"Aura Flammes",reward:"Aura nv.2 + 100💎"},
  {level:21,title:"Chasseur",reward:"Rôle Fantôme débloqué"},
  {level:25,title:"Avatar Sorcier",reward:"Effets carte de rôle"},
  {level:30,title:"Aura Arc-en-ciel",reward:"Aura nv.3 + 200💎"},
  {level:31,title:"Expert",reward:"Rôle Détective débloqué"},
  {level:40,title:"Avatar Sharingan",reward:"Frame Arc-en-ciel + 300💎"},
  {level:50,title:"Maître",reward:"Tous modes + avatar légendaire + 500💎"},
  {level:51,title:"Légende",reward:"Badge Légende + frame Cosmos + gemmes illimitées gacha"},
];

function renderProgression() {
  var tl = document.getElementById("progression-timeline");
  if (!tl) return;
  tl.innerHTML = "";
  var myLevel = Economy?.data?.level || 1;
  MILESTONES.forEach(function(m) {
    var item = document.createElement("div");
    var state = myLevel >= m.level ? "done" : myLevel >= m.level - 2 ? "current" : "locked";
    item.className = "tl-item " + state;
    item.innerHTML = "<div class=\\"tl-level\\">Niveau " + m.level + "</div>" +
      "<div class=\\"tl-title\\">" + m.title + "</div>" +
      "<div class=\\"tl-reward\\">" + m.reward + "</div>";
    if (state === "locked") {
      item.onclick = function() { showToast("Plus que " + (m.level - myLevel) + " niveaux !"); };
    }
    tl.appendChild(item);
  });
}


// ===== V15 REACTIONS =====
var reactionWheelOpen = false;
var REACTIONS = ["😮","😂","🤔","😈","😱","👀"];

function toggleReactions() {
  reactionWheelOpen = !reactionWheelOpen;
  var wheel = document.getElementById("reaction-wheel");
  wheel.classList.toggle("show", reactionWheelOpen);
  if (reactionWheelOpen && wheel.children.length === 0) {
    REACTIONS.forEach(function(emoji) {
      var btn = document.createElement("button");
      btn.textContent = emoji;
      btn.onclick = function() { sendReaction(emoji); };
      wheel.appendChild(btn);
    });
  }
}

async function sendReaction(emoji) {
  reactionWheelOpen = false;
  document.getElementById("reaction-wheel").classList.remove("show");
  showToast(emoji, 1500);
  // Send via Supabase if in MP game
  if (sb && mpRoomId && mpPlayerId) {
    var gs = (await sb.from("game_state").select("reactions").eq("room_id", mpRoomId).single()).data;
    var reactions = (gs?.reactions) || {};
    reactions[mpPlayerId] = {emoji: emoji, ts: Date.now()};
    await sb.from("game_state").update({reactions: reactions}).eq("room_id", mpRoomId);
  }
}


// ===== V15 HALL OF FAME =====
async function renderHallOfFame() {
  var section = document.getElementById("hof-section");
  if (!section) return;
  if (!sb) {
    section.innerHTML = "";
    return;
  }
  try {
    var res = await sb.from("leaderboard").select("username,avatar_emoji,rank_points").order("rank_points",{ascending:false}).limit(3);
    var data = res.data || [];
    if (!data.length) { section.innerHTML = ""; return; }
    var medals = ["🥇","🥈","🥉"];
    var h = "<div class=\\"hof-title\\">Hall of Fame</div>";
    data.forEach(function(p, i) {
      h += "<div class=\\"hof-row\\"><span class=\\"hof-medal\\">" + medals[i] + "</span>" +
        "<span style=\\"font-size:1.1rem\\">" + (p.avatar_emoji||"🕵️") + "</span>" +
        "<span class=\\"hof-name\\">" + p.username + "</span>" +
        "<span class=\\"hof-pts\\">" + p.rank_points + " pts</span></div>";
    });
    section.innerHTML = h;
    section.style.cursor = "pointer";
    section.onclick = function() { showScreen("screen-mp-leaderboard"); };
  } catch(e) { section.innerHTML = ""; }
}


// ===== V15 ADMIN FULL UNLOCK =====
var _origCheckAdminV15 = checkAdminCode;
checkAdminCode = function() {
  _origCheckAdminV15();
  // If admin activated, unlock all anime avatars
  if (Economy._data.isAdmin) {
    ANIME_AVATAR_META.forEach(function(av) {
      if (!Economy._data.gachaCollection) Economy._data.gachaCollection = [];
      if (!Economy._data.gachaCollection.find(function(c){return c.name===av.name})) {
        Economy._data.gachaCollection.push({icon:"📷",name:av.name,type:"avatar",rarity:"legendary"});
      }
    });
    Economy.save();
  }
};


// ===== V15 PATCHES =====
var _prevShowScreenV15 = showScreen;
showScreen = function(id) {
  _prevShowScreenV15(id);
  if (id === "screen-progression") renderProgression();
  if (id === "screen-splash") { initSupabase().then(function(){renderHallOfFame()}).catch(function(){}); }
  // Show/hide reaction FAB during MP game
  var rfab = document.getElementById("reaction-fab");
  if (rfab) rfab.classList.toggle("active", id === "screen-mp-game");
};

// Load avatar images early
document.addEventListener("DOMContentLoaded", function() { loadAvatarImages(); });
"""

html = html.replace("\n</script>", JS + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"V15 patch applied! {len(html)//1024} KB")
