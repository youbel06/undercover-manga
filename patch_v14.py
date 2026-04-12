#!/usr/bin/env python3
"""V14: Multiplayer UX overhaul, theme preview modal, anime avatars."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS
# ═══════════════════════════════════════════════════════════
CSS = """
/* ===== V14 MP CARDS ===== */
.mp-option-cards{display:flex;flex-direction:column;gap:12px;width:100%;max-width:380px;margin-top:12px}
.mp-option-card{background:var(--bg-card);border:1px solid var(--border-glass);border-radius:var(--radius-lg);
  padding:18px;cursor:pointer;transition:all 0.2s;display:flex;align-items:center;gap:14px}
.mp-option-card:hover{border-color:var(--accent-gold);transform:translateY(-2px);box-shadow:var(--shadow-md)}
.mp-option-card .oc-icon{font-size:2rem;flex-shrink:0}
.mp-option-card .oc-info{flex:1}
.mp-option-card .oc-title{font-weight:700;font-size:0.95rem;color:var(--text-bright)}
.mp-option-card .oc-desc{font-size:0.75rem;color:var(--text-muted);margin-top:2px}

/* Lobby share button */
.mp-share-row{display:flex;gap:8px;justify-content:center;margin:8px 0}
.mp-share-btn{display:flex;align-items:center;gap:6px;padding:8px 14px;border-radius:var(--radius-sm);
  background:var(--bg-card);border:1px solid var(--border-glass);cursor:pointer;font-size:0.8rem;
  color:var(--text-primary);transition:all 0.2s}
.mp-share-btn:hover{border-color:var(--accent-gold)}

/* Lobby host settings */
.mp-host-settings{background:var(--bg-card);border:1px solid var(--border-glass);border-radius:var(--radius-md);
  padding:12px;margin-top:10px;width:100%;max-width:350px}
.mp-host-settings label{display:flex;justify-content:space-between;align-items:center;
  font-size:0.8rem;color:var(--text-muted);margin-bottom:8px}
.mp-host-settings select{background:var(--bg-secondary);border:1px solid var(--border-glass);
  border-radius:var(--radius-sm);padding:6px 10px;color:var(--text-bright);font-size:0.8rem}

/* MP game header */
.mp-game-header{display:flex;justify-content:space-between;align-items:center;width:100%;max-width:400px;
  padding:8px 0;margin-bottom:10px;border-bottom:1px solid var(--border-glass)}
.mp-phase-badge{padding:4px 12px;border-radius:12px;font-size:0.75rem;font-weight:600}
.mp-phase-badge.reveal{background:rgba(59,130,246,0.15);color:var(--accent-civil)}
.mp-phase-badge.discuss{background:rgba(245,166,35,0.15);color:var(--accent-gold)}
.mp-phase-badge.vote{background:rgba(233,69,96,0.15);color:var(--accent-undercover)}

/* Alive players strip */
.mp-alive-strip{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:8px 0}
.mp-alive-chip{display:flex;align-items:center;gap:4px;padding:4px 8px;border-radius:12px;
  background:var(--bg-card);font-size:0.7rem;color:var(--text-muted)}
.mp-alive-chip.eliminated{opacity:0.3;text-decoration:line-through}

/* ===== V14 THEME PREVIEW MODAL ===== */
.theme-modal{position:fixed;top:0;left:0;width:100%;height:100%;z-index:500;
  background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity 0.3s}
.theme-modal.open{opacity:1;pointer-events:auto}
.theme-modal-card{background:var(--bg-secondary);border:1px solid var(--border-glass);
  border-radius:var(--radius-xl);padding:24px;text-align:center;max-width:340px;width:90%;
  animation:slideInUp 0.3s ease}
.theme-modal-icon{font-size:3rem;margin-bottom:8px}
.theme-modal-name{font-size:1.2rem;font-weight:700;color:var(--text-bright);margin-bottom:4px}
.theme-modal-desc{font-size:0.8rem;color:var(--text-muted);margin-bottom:14px}
.theme-modal-actions{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}

/* ===== V14 ANIME AVATARS ===== */
.anime-avatar{position:relative;display:flex;align-items:center;justify-content:center;border-radius:50%;overflow:hidden}
.anime-avatar .aa-emoji{position:relative;z-index:1}
.anime-avatar.ninja{background:linear-gradient(135deg,#1e3a5f,#0f1f3d)}
.anime-avatar.ninja::after{content:'';position:absolute;width:100%;height:100%;background:radial-gradient(circle at 50% 80%,rgba(100,149,237,0.3),transparent);animation:smokeAnim 3s ease infinite}
@keyframes smokeAnim{0%,100%{opacity:0.3;transform:translateY(0)}50%{opacity:0.6;transform:translateY(-5px)}}
.anime-avatar.saber{background:linear-gradient(135deg,#5f1e1e,#3d0f0f)}
.anime-avatar.saber::after{content:'';position:absolute;width:2px;height:60%;background:linear-gradient(transparent,#fff,transparent);animation:bladeFlash 2s ease infinite;transform:rotate(-30deg)}
@keyframes bladeFlash{0%,100%{opacity:0}50%{opacity:0.6}}
.anime-avatar.mage{background:linear-gradient(135deg,#3b1f5f,#1f0f3d)}
.anime-avatar.mage::after{content:'';position:absolute;width:100%;height:100%;background:radial-gradient(circle,rgba(168,85,247,0.3) 0%,transparent 70%);animation:magicPulse 2s ease infinite}
@keyframes magicPulse{0%,100%{transform:scale(0.8);opacity:0.3}50%{transform:scale(1.2);opacity:0.6}}
.anime-avatar.shinigami{background:linear-gradient(135deg,#1a1a1a,#000)}
.anime-avatar.shinigami::after{content:'';position:absolute;width:100%;height:100%;box-shadow:inset 0 0 20px rgba(100,100,100,0.3);animation:darkAura 2.5s ease infinite}
@keyframes darkAura{0%,100%{box-shadow:inset 0 0 15px rgba(100,100,100,0.2)}50%{box-shadow:inset 0 0 25px rgba(100,100,100,0.4)}}
.anime-avatar.dragon{background:linear-gradient(135deg,#92400e,#78350f)}
.anime-avatar.dragon::after{content:'';position:absolute;bottom:0;width:100%;height:40%;background:linear-gradient(transparent,rgba(239,68,68,0.3));animation:flameWave 1.5s ease infinite}
@keyframes flameWave{0%,100%{opacity:0.3;transform:scaleY(0.8)}50%{opacity:0.6;transform:scaleY(1.2)}}
.anime-avatar.kunoichi{background:linear-gradient(135deg,#831843,#4a1028)}
.anime-avatar.kunoichi::after{content:'';position:absolute;width:100%;height:100%;background:radial-gradient(circle at 70% 20%,rgba(249,168,212,0.4),transparent 50%);animation:petalGlow 3s ease infinite}
@keyframes petalGlow{0%,100%{opacity:0.3}50%{opacity:0.6}}
.anime-avatar.lightning{background:linear-gradient(135deg,#854d0e,#713f12)}
.anime-avatar.lightning::after{content:'';position:absolute;width:100%;height:100%;background:linear-gradient(45deg,transparent 40%,rgba(250,204,21,0.4) 50%,transparent 60%);animation:boltFlash 1s ease infinite}
@keyframes boltFlash{0%,80%,100%{opacity:0}85%{opacity:1}}
.anime-avatar.water{background:linear-gradient(135deg,#0e7490,#065666)}
.anime-avatar.water::after{content:'';position:absolute;bottom:0;width:120%;height:30%;background:rgba(34,211,238,0.2);border-radius:50%;animation:waveMove 2s ease infinite}
@keyframes waveMove{0%,100%{transform:translateX(-10%) scaleY(1)}50%{transform:translateX(10%) scaleY(1.3)}}
.anime-avatar.flame{background:linear-gradient(135deg,#c2410c,#9a3412)}
.anime-avatar.flame::after{content:'';position:absolute;bottom:0;width:100%;height:50%;background:linear-gradient(transparent,rgba(251,146,60,0.4),rgba(239,68,68,0.3));animation:flameWave 1.2s ease infinite}
.anime-avatar.fox{background:linear-gradient(135deg,#c2410c,#78350f)}
.anime-avatar.fox::after{content:'';position:absolute;width:100%;height:100%;background:radial-gradient(circle,rgba(251,146,60,0.3) 30%,transparent 70%);animation:foxAura 2s ease infinite}
@keyframes foxAura{0%,100%{transform:scale(0.9);opacity:0.3}50%{transform:scale(1.1);opacity:0.5}}
"""
html = html.replace("/* ===== APP CONTAINER ===== */", CSS + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. Replace MP menu HTML with card-based layout
# ═══════════════════════════════════════════════════════════
old_mp_menu = '''  <div id="screen-mp-menu" class="screen" style="padding-top:50px">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-splash')">←</button>
    <h2>🌐 Multijoueur</h2>
    <div class="mp-status" id="mp-status"><div class="dot offline"></div><span>Connexion...</span></div>
    <div id="mp-profile-section"></div>
    <div style="display:flex;flex-direction:column;gap:10px;width:100%;max-width:300px;margin-top:16px;">
      <button class="btn btn-primary" onclick="mpCreateRoom()">Créer un salon</button>
      <div style="display:flex;gap:8px;max-width:300px;margin:0 auto">
        <input type="text" id="mp-join-code" placeholder="CODE" maxlength="6" style="flex:1;background:var(--bg-card);border:1px solid var(--border-glass);border-radius:var(--radius-sm);padding:12px;color:var(--text-bright);font-size:1.2rem;text-align:center;letter-spacing:4px;text-transform:uppercase">
        <button class="btn btn-primary" onclick="mpJoinRoom()">Rejoindre</button>
      </div>
      <button class="btn btn-ghost" onclick="showScreen('screen-mp-leaderboard')">🏆 Classement</button>
    </div>
  </div>'''

new_mp_menu = '''  <div id="screen-mp-menu" class="screen" style="padding-top:50px">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-splash')">←</button>
    <h2>🌐 Multijoueur</h2>
    <div class="mp-status" id="mp-status"><div class="dot offline"></div><span>Connexion...</span></div>
    <div id="mp-profile-section"></div>
    <div class="mp-option-cards">
      <div class="mp-option-card" onclick="mpCreateRoom()">
        <div class="oc-icon">🏠</div>
        <div class="oc-info"><div class="oc-title">Créer un salon</div><div class="oc-desc">Lance une partie et invite tes amis</div></div>
      </div>
      <div class="mp-option-card" style="flex-direction:column;align-items:stretch">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px">
          <div class="oc-icon">🔑</div>
          <div class="oc-info"><div class="oc-title">Rejoindre un salon</div><div class="oc-desc">Entre le code partagé par ton ami</div></div>
        </div>
        <div style="display:flex;gap:8px">
          <input type="text" id="mp-join-code" placeholder="ENTRER LE CODE" maxlength="6" style="flex:1;background:var(--bg-secondary);border:1px solid var(--border-glass);border-radius:var(--radius-sm);padding:12px;color:var(--text-bright);font-size:1.1rem;text-align:center;letter-spacing:4px;text-transform:uppercase;font-family:var(--font-display)">
          <button class="btn btn-primary" onclick="mpJoinRoom()" style="white-space:nowrap">REJOINDRE</button>
        </div>
      </div>
      <div class="mp-option-card" onclick="mpQuickMatch()">
        <div class="oc-icon">⚡</div>
        <div class="oc-info"><div class="oc-title">Partie rapide</div><div class="oc-desc">Rejoins une partie publique disponible</div></div>
      </div>
    </div>
    <div style="display:flex;gap:10px;margin-top:14px">
      <button class="btn btn-ghost" onclick="showScreen('screen-mp-leaderboard')">🏆 Classement</button>
    </div>
  </div>'''

html = html.replace(old_mp_menu, new_mp_menu)

# ═══════════════════════════════════════════════════════════
# 3. Replace MP lobby with share + host settings
# ═══════════════════════════════════════════════════════════
old_lobby = '''  <div id="screen-mp-lobby" class="screen" style="padding-top:50px">
    <button class="btn btn-icon btn-ghost back-btn" onclick="mpLeaveRoom()">←</button>
    <h2>Salon</h2>
    <div class="mp-code" id="mp-room-code" onclick="mpCopyCode()">------</div>
    <div style="font-size:0.75rem;color:var(--text-muted);text-align:center">Partage ce code</div>
    <div class="mp-player-list" id="mp-player-list"></div>
    <div id="mp-host-controls" style="display:none;margin-top:12px">
      <button class="btn btn-primary btn-large" id="mp-start-btn" onclick="mpStartGame()" disabled>LANCER</button>
    </div>
    <button class="btn btn-primary" id="mp-ready-btn" onclick="mpToggleReady()" style="margin-top:12px">PRÊT</button>
  </div>'''

new_lobby = '''  <div id="screen-mp-lobby" class="screen" style="padding-top:50px">
    <button class="btn btn-icon btn-ghost back-btn" onclick="mpLeaveRoom()">←</button>
    <h2>Salon de jeu</h2>
    <div class="mp-code" id="mp-room-code" onclick="mpCopyCode()">------</div>
    <div class="mp-share-row">
      <button class="mp-share-btn" onclick="mpCopyCode()">📋 Copier</button>
      <button class="mp-share-btn" onclick="mpShareRoom()">📤 Partager</button>
    </div>
    <div class="mp-player-list" id="mp-player-list"></div>
    <div id="mp-host-settings-area" style="display:none">
      <div class="mp-host-settings">
        <label>Mode <select id="mp-mode-select" onchange="mpUpdateSettings()">
          <option value="normal">Anime Mix</option><option value="shonen">Shōnen</option>
          <option value="casual">Casual</option><option value="jeux_video">Jeux Vidéo</option>
        </select></label>
        <label>Manches <select id="mp-rounds-select" onchange="mpUpdateSettings()">
          <option value="3">3</option><option value="5" selected>5</option><option value="7">7</option>
        </select></label>
        <label>Timer discussion <select id="mp-timer-select" onchange="mpUpdateSettings()">
          <option value="30">30s</option><option value="60" selected>60s</option><option value="90">90s</option>
        </select></label>
      </div>
    </div>
    <div id="mp-host-controls" style="display:none;margin-top:12px">
      <button class="btn btn-primary btn-large" id="mp-start-btn" onclick="mpStartGame()" disabled>LANCER LA PARTIE</button>
    </div>
    <button class="btn btn-primary" id="mp-ready-btn" onclick="mpToggleReady()" style="margin-top:12px">✓ PRÊT</button>
    <button class="btn btn-ghost" onclick="mpLeaveRoom()" style="margin-top:8px;font-size:0.8rem">Quitter le salon</button>
  </div>'''

html = html.replace(old_lobby, new_lobby)

# ═══════════════════════════════════════════════════════════
# 4. Add theme preview modal HTML
# ═══════════════════════════════════════════════════════════
html = html.replace(
    '<!-- ===== TOAST ===== -->',
    '<!-- ===== THEME PREVIEW MODAL ===== -->\n'
    '<div class="theme-modal" id="theme-modal">\n'
    '  <div class="theme-modal-card">\n'
    '    <div class="theme-modal-icon" id="tm-icon"></div>\n'
    '    <div class="theme-modal-name" id="tm-name"></div>\n'
    '    <div class="theme-modal-desc" id="tm-desc"></div>\n'
    '    <div style="font-size:1.1rem;color:var(--accent-gold);font-weight:700;margin-bottom:12px" id="tm-price"></div>\n'
    '    <div class="theme-modal-actions" id="tm-actions"></div>\n'
    '  </div>\n'
    '</div>\n\n'
    '<!-- ===== TOAST ===== -->'
)

# ═══════════════════════════════════════════════════════════
# 5. JavaScript
# ═══════════════════════════════════════════════════════════
JS = r"""

// ===== V14 MP SHARE =====
function mpShareRoom() {
  var text = "Rejoins ma partie Undercover Lelox !\nCode : " + (mpRoomCode||"") + "\nhttps://youbel06.github.io/undercover-manga/";
  if (navigator.share) {
    navigator.share({title:"Undercover Lelox", text:text}).catch(function(){});
  } else {
    mpCopyCode();
    showToast("Lien copié !");
  }
}

function mpUpdateSettings() {
  // Host updates room settings (not persisted yet, local only)
  GameState.currentMode = document.getElementById("mp-mode-select")?.value || "normal";
}

// Patch renderMpLobby to show host settings
var _origRenderMpLobbyV14 = renderMpLobby;
renderMpLobby = async function() {
  await _origRenderMpLobbyV14();
  var hsa = document.getElementById("mp-host-settings-area");
  if (hsa) hsa.style.display = mpIsHost ? "block" : "none";
};


// ===== V14 THEME PREVIEW MODAL =====
var _themePreviewOriginal = null;

function openThemeModal(themeId, themeName, themeIcon, price, owned) {
  _themePreviewOriginal = Economy.data.selectedTheme;
  document.getElementById("tm-icon").textContent = themeIcon;
  document.getElementById("tm-name").textContent = themeName;
  document.getElementById("tm-desc").textContent = "Transforme toute l'interface avec cette palette unique";
  var priceEl = document.getElementById("tm-price");
  var actionsEl = document.getElementById("tm-actions");

  // Apply preview
  applyTheme(themeId);

  if (owned) {
    var isActive = Economy.data.selectedTheme === themeId || _themePreviewOriginal === themeId;
    priceEl.textContent = isActive ? "✓ Thème actif" : "Possédé";
    actionsEl.innerHTML = (isActive ? "" : "<button class=\"btn btn-primary\" onclick=\"confirmThemeActivate('" + themeId + "')\">Activer</button>") +
      "<button class=\"btn btn-ghost\" onclick=\"closeThemeModal()\">Fermer</button>";
  } else {
    priceEl.textContent = price + " 💎";
    actionsEl.innerHTML = "<button class=\"btn btn-primary\" onclick=\"buyAndActivateTheme('" + themeId + "'," + price + ")\">Acheter et activer</button>" +
      "<button class=\"btn btn-ghost\" onclick=\"closeThemeModal()\">Annuler</button>";
  }

  document.getElementById("theme-modal").classList.add("open");
}

function closeThemeModal() {
  document.getElementById("theme-modal").classList.remove("open");
  // Revert to original theme if not purchased
  if (_themePreviewOriginal !== null) applyTheme(_themePreviewOriginal);
}

function confirmThemeActivate(id) {
  applyTheme(id);
  _themePreviewOriginal = id;
  document.getElementById("theme-modal").classList.remove("open");
  showToast("Thème activé !");
  renderShop();
}

function buyAndActivateTheme(id, price) {
  if (Economy.buyTheme(id, price)) {
    applyTheme(id);
    _themePreviewOriginal = id;
    document.getElementById("theme-modal").classList.remove("open");
    showToast("Thème acheté et activé ! 🎨");
    renderShop();
  }
}


// ===== V14 ANIME AVATARS =====
var ANIME_AVATARS = [
  {id:"ninja",icon:"🥷",name:"Ninja Furtif",rarity:"common",cls:"ninja"},
  {id:"saber",icon:"⚔️",name:"Sabreur",rarity:"common",cls:"saber"},
  {id:"mage",icon:"🔮",name:"Sorcier",rarity:"common",cls:"mage"},
  {id:"shinigami",icon:"💀",name:"Shinigami",rarity:"common",cls:"shinigami"},
  {id:"dragon_av",icon:"🐉",name:"Dragon",rarity:"common",cls:"dragon"},
  {id:"kunoichi",icon:"🌸",name:"Kunoichi",rarity:"common",cls:"kunoichi"},
  {id:"lightning_av",icon:"⚡",name:"Foudre Dorée",rarity:"rare",cls:"lightning"},
  {id:"water",icon:"🌊",name:"Maître de l'Eau",rarity:"rare",cls:"water"},
  {id:"flame",icon:"🔥",name:"Flamme Éternelle",rarity:"rare",cls:"flame"},
  {id:"fox_av",icon:"🦊",name:"Renard à Neuf Queues",rarity:"rare",cls:"fox"},
  {id:"sharingan",icon:"👁️",name:"Œil du Destin",rarity:"epic",cls:"shinigami"},
  {id:"void_av",icon:"⚫",name:"Void Absolu",rarity:"epic",cls:"shinigami"},
  {id:"blood_moon",icon:"🌙",name:"Lune de Sang",rarity:"epic",cls:"shinigami"},
  {id:"demon_king",icon:"👑",name:"Roi des Démons",rarity:"legendary",cls:"dragon"},
  {id:"infinity",icon:"🌟",name:"Dieu Caché",rarity:"legendary",cls:"mage"},
  {id:"legend_blade",icon:"⚔️",name:"Lame Légendaire",rarity:"legendary",cls:"saber"},
];

// Merge with existing ALL_AVATARS
ANIME_AVATARS.forEach(function(av) {
  if (!ALL_AVATARS.find(function(a){return a.id===av.id})) {
    ALL_AVATARS.push(av);
  }
});

// Update gacha items to include anime avatars
ANIME_AVATARS.forEach(function(av) {
  var pool = GACHA_ITEMS[av.rarity];
  if (pool && !pool.find(function(i){return i.name===av.name})) {
    pool.push({icon:av.icon, name:av.name, type:"avatar"});
  }
});


// ===== V14 PATCH: Theme shop uses modal =====
// Override renderShop theme section
var _origRenderShopV14 = renderShop;
renderShop = function() {
  _origRenderShopV14();
  // Re-render themes with modal onclick
  var grid = document.getElementById("shop-themes");
  if (!grid) return;
  grid.innerHTML = "";
  var allThemes = SHOP_THEMES.slice();
  // Add extra themes
  [{id:"forest",name:"Forest Spirit 🌿",icon:"🌿",price:150},
   {id:"sunset",name:"Sunset Duel 🌅",icon:"🌅",price:200},
   {id:"ice",name:"Ice Realm ❄️",icon:"❄️",price:150},
   {id:"blood",name:"Blood Moon 🔴",icon:"🔴",price:250},
   {id:"blueberry",name:"Blueberry 🫐",icon:"🫐",price:150},
   {id:"rosegold",name:"Rose Gold 🌹",icon:"🌹",price:200},
   {id:"mint",name:"Mint Fresh 🌿",icon:"🌿",price:150},
   {id:"midnight",name:"Midnight 🌙",icon:"🌙",price:100},
   {id:"ocean",name:"Ocean 🌊",icon:"🌊",price:150},
   {id:"cherry",name:"Cherry 🍒",icon:"🍒",price:200}
  ].forEach(function(t) {
    if (!allThemes.find(function(x){return x.id===t.id})) allThemes.push(t);
  });

  allThemes.forEach(function(t) {
    var owned = Economy.ownsTheme(t.id);
    var active = Economy.data.selectedTheme === t.id;
    var card = document.createElement("div");
    card.className = "shop-card" + (owned ? " owned" : "");
    if (active) card.style.borderColor = "var(--accent-green)";
    card.innerHTML = "<div class=\"shop-card-icon\">" + t.icon + "</div>" +
      "<div class=\"shop-card-name\">" + t.name + "</div>" +
      (active ? "<div class=\"shop-card-price free\">✓ Actif</div>" :
       owned ? "<div class=\"shop-card-price free\">Possédé</div>" :
       t.price === 0 ? "<div class=\"shop-card-price free\">Gratuit</div>" :
       "<div class=\"shop-card-price\">💎 " + t.price + "</div>");
    card.onclick = function() { openThemeModal(t.id, t.name, t.icon, t.price, owned || t.price === 0); };
    grid.appendChild(card);
  });
};
"""

html = html.replace("\n</script>", JS + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"V14 patch applied! {len(html)//1024} KB")
