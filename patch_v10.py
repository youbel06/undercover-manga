#!/usr/bin/env python3
"""V10 patch: Shop tabs fix, avatar colors, local profiles, daily challenge, gacha screen, fixes."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS
# ═══════════════════════════════════════════════════════════
CSS_V10 = """
/* ===== V10 SHOP TABS FIX ===== */
.shop-tabs {
  display:flex !important; gap:6px !important; width:100% !important; max-width:600px !important;
  overflow-x:auto !important; -webkit-overflow-scrolling:touch !important;
  padding:8px 0 !important; scroll-snap-type:x proximity; scrollbar-width:none;
}
.shop-tabs::-webkit-scrollbar { display:none; }
.shop-tab {
  flex-shrink:0 !important; min-height:44px !important; padding:10px 18px !important;
  border-radius:22px !important; font-size:0.82rem !important; font-weight:600 !important;
  display:flex !important; align-items:center !important; gap:6px !important;
  scroll-snap-align:start; white-space:nowrap !important;
}
.shop-tab.active {
  background:var(--accent-civil) !important; color:#000 !important;
  border-color:var(--accent-civil) !important;
  box-shadow:0 2px 12px rgba(0,212,255,0.25);
}

/* ===== V10 AVATAR COLOR ===== */
.avatar-color-picker { display:grid; grid-template-columns:repeat(6,1fr); gap:8px; max-width:300px; margin:10px auto; }
.color-swatch {
  width:40px; height:40px; border-radius:50%; cursor:pointer;
  border:3px solid transparent; transition:all 0.2s;
  display:flex; align-items:center; justify-content:center;
  font-size:0.6rem; color:rgba(255,255,255,0.5);
}
.color-swatch:hover { transform:scale(1.15); }
.color-swatch.active { border-color:#fff; box-shadow:0 0 12px rgba(255,255,255,0.3); }
.color-swatch.locked { opacity:0.4; }
.color-swatch.locked::after { content:'🔒'; font-size:0.8rem; }

/* Gradient avatar colors */
.avatar-bg-rainbow { background:conic-gradient(#ef4444,#f59e0b,#22c55e,#3b82f6,#a855f7,#ef4444) !important;
  animation:rainbowSpin 3s linear infinite; }
.avatar-bg-goldblack { background:linear-gradient(135deg,#ffd700,#000,#ffd700) !important;
  background-size:200% 200% !important; animation:gradShift 3s ease infinite; }
.avatar-bg-galaxy { background:radial-gradient(ellipse,#1a0533,#000814,#0a1628) !important;
  position:relative; overflow:hidden; }
@keyframes gradShift { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }

/* ===== V10 LOCAL PROFILES ===== */
.profiles-list { width:100%; max-width:500px; }
.profile-row {
  display:flex; align-items:center; gap:12px; padding:12px 14px;
  background:var(--bg-card); border:1px solid var(--border-glass);
  border-radius:var(--radius-md); margin-bottom:8px; cursor:pointer;
  transition:all 0.2s;
}
.profile-row:hover { border-color:var(--accent-civil); }
.profile-row.active-profile { border-color:var(--accent-gold); background:rgba(245,166,35,0.05); }
.profile-row .pr-avatar { width:40px; height:40px; border-radius:50%;
  display:flex; align-items:center; justify-content:center; font-size:1.3rem; flex-shrink:0; }
.profile-row .pr-info { flex:1; }
.profile-row .pr-name { font-weight:600; font-size:0.9rem; color:var(--text-bright); }
.profile-row .pr-stats { font-size:0.7rem; color:var(--text-muted); }
.profile-row .pr-badge { font-size:0.65rem; background:var(--accent-gold); color:#000;
  padding:2px 6px; border-radius:6px; font-weight:700; }

/* ===== V10 DAILY CHALLENGE ===== */
.daily-challenge {
  background:linear-gradient(135deg,rgba(245,166,35,0.08),rgba(0,212,255,0.05));
  border:1px solid rgba(245,166,35,0.2); border-radius:var(--radius-lg);
  padding:14px 18px; margin:10px 0; width:100%; max-width:400px;
  text-align:center; cursor:pointer; transition:all 0.2s;
}
.daily-challenge:hover { border-color:var(--accent-gold); transform:translateY(-2px); }
.daily-challenge .dc-label { font-size:0.7rem; color:var(--accent-gold);
  text-transform:uppercase; letter-spacing:1px; }
.daily-challenge .dc-title { font-size:1rem; font-weight:700; color:var(--text-bright); margin:4px 0; }
.daily-challenge .dc-reward { font-size:0.8rem; color:var(--text-muted); }

/* ===== V10 THEME TRANSITION ===== */
body { transition:background-color 0.5s ease, color 0.3s ease; }
body * { transition:border-color 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease; }
/* Exclude animations from transition */
body .btn::after, body [class*='animation'], body [class*='pulse'], body [class*='float'] { transition:none; }

/* ===== V10 SOCIAL PROOF FIX ===== */
.social-proof-local { font-size:0.7rem; color:var(--text-dim); margin-top:4px; }

/* ===== V10 GACHA NAV ===== */
.bottom-nav .nav-item { min-width:0; }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_V10 + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML changes
# ═══════════════════════════════════════════════════════════

# Fix bottom nav: replace Succès with Gacha
html = html.replace(
    '<button class="nav-item" onclick="navTo(\'achievements\')" id="nav-achieve"><span class="nav-icon">🏆</span>Succès</button>',
    '<button class="nav-item" onclick="navTo(\'gacha\')" id="nav-gacha"><span class="nav-icon">🎰</span>Gacha</button>\n'
    '  <button class="nav-item" onclick="navTo(\'achievements\')" id="nav-achieve"><span class="nav-icon">🏆</span>Succès</button>'
)

# Fix social proof to show real local stats
html = html.replace(
    '<div class="social-proof"><div class="pulse-dot"></div><span id="social-counter">847 joueurs actifs</span></div>',
    '<div class="social-proof-local" id="local-stats"></div>'
)

# Add daily challenge to splash before JOUER button
html = html.replace(
    "onclick=\"showScreen('screen-modes')\">JOUER</button>",
    "onclick=\"showScreen('screen-modes')\">JOUER</button>\n"
    "    <div class=\"daily-challenge\" id=\"daily-challenge\" onclick=\"playDailyChallenge()\"></div>"
)

# Add profiles screen (before credits)
html = html.replace(
    '  <!-- ===== CREDITS SCREEN ===== -->',
    '  <!-- ===== PROFILES SCREEN ===== -->\n'
    '  <div id="screen-profiles" class="screen">\n'
    '    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen(\'screen-profile\')" aria-label="Retour">←</button>\n'
    '    <h2>👥 Profils locaux</h2>\n'
    '    <div class="profiles-list" id="profiles-list"></div>\n'
    '    <button class="btn btn-primary" onclick="createLocalProfile()">+ Nouveau profil</button>\n'
    '  </div>\n\n'
    '  <!-- ===== CREDITS SCREEN ===== -->'
)

# Add profiles link in profile screen
html = html.replace(
    '<div style="margin-bottom:14px;"><button class="btn btn-ghost" onclick="showScreen(\'screen-cosmetics\')">🎨 Personnalisation</button></div>',
    '<div style="margin-bottom:14px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">'
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-cosmetics\')">🎨 Personnalisation</button>'
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-profiles\')">👥 Profils</button>'
    '</div>'
)

# ═══════════════════════════════════════════════════════════
# 3. JavaScript
# ═══════════════════════════════════════════════════════════
JS_V10 = r"""

// ===== V10 SHOP TABS OVERRIDE =====
// Completely rebuild tabs on each render to ensure they work
const _origRenderShopV10 = renderShop;
renderShop = function() {
  // Remove old tabs first
  const shopScreen = document.getElementById('screen-shop');
  if (shopScreen) {
    shopScreen.querySelectorAll('.shop-tabs').forEach(t => t.remove());
    shopScreen.querySelectorAll('.shop-tab-content').forEach(t => t.remove());
  }
  _origRenderShopV10();
};

// ===== V10 NAV FIX =====
const _origNavTo = navTo;
navTo = function(screen) {
  if (screen === 'gacha') {
    SoundFX.click();
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const el = document.getElementById('nav-gacha');
    if (el) el.classList.add('active');
    showScreen('screen-gacha');
    return;
  }
  _origNavTo(screen);
};


// ===== V10 AVATAR COLORS =====
const AVATAR_COLORS = [
  {id:'black',color:'#1a1a2e',price:0},
  {id:'gray',color:'#4b5563',price:0},
  {id:'navy',color:'#1e3a5f',price:0},
  {id:'darkgreen',color:'#14532d',price:0},
  {id:'white',color:'#e5e7eb',price:0},
  {id:'neon_pink',color:'#FF006E',price:50},
  {id:'neon_cyan',color:'#00F5FF',price:50},
  {id:'neon_green',color:'#39FF14',price:50},
  {id:'neon_orange',color:'#FF6600',price:50},
  {id:'neon_purple',color:'#BF00FF',price:50},
  {id:'gold',color:'#FFD700',price:50},
  {id:'blood',color:'#8B0000',price:50},
  {id:'turquoise',color:'#40E0D0',price:50},
  {id:'rainbow',color:'rainbow',price:0,legendary:true},
  {id:'goldblack',color:'goldblack',price:0,legendary:true},
  {id:'galaxy',color:'galaxy',price:0,legendary:true},
];

function getAvatarBgStyle(colorId) {
  const c = AVATAR_COLORS.find(x => x.id === colorId);
  if (!c) return 'background:#1a1a2e';
  if (c.color === 'rainbow') return '';
  if (c.color === 'goldblack') return '';
  if (c.color === 'galaxy') return '';
  return 'background:' + c.color;
}

function getAvatarBgClass(colorId) {
  if (colorId === 'rainbow') return 'avatar-bg-rainbow';
  if (colorId === 'goldblack') return 'avatar-bg-goldblack';
  if (colorId === 'galaxy') return 'avatar-bg-galaxy';
  return '';
}

// Extend cosmetics screen with color tab
const _origRenderCosmeticsV10 = renderCosmeticsScreen;
renderCosmeticsScreen = function() {
  const eq = getEquipped();
  if (!eq.avatarColor) eq.avatarColor = 'black';

  const preview = document.getElementById('cosm-preview');
  if (preview) {
    const frame = ALL_FRAMES.find(f => f.id === eq.frame);
    preview.className = 'avatar-equipped ' + (frame ? frame.cls : 'frame-rookie') + ' ' + getAvatarBgClass(eq.avatarColor);
    preview.style.cssText = getAvatarBgStyle(eq.avatarColor);
    preview.textContent = eq.avatar;
  }

  const tabs = document.getElementById('cosm-tabs');
  const grid = document.getElementById('cosm-grid');
  if (!tabs || !grid) return;

  const activeTab = tabs.dataset.active || 'avatars';
  tabs.innerHTML = '';
  ['avatars','colors','frames'].forEach(t => {
    const btn = document.createElement('div');
    btn.className = 'cosmetics-tab' + (activeTab === t ? ' active' : '');
    btn.textContent = t === 'avatars' ? '👤 Avatar' : t === 'colors' ? '🎨 Couleur' : '🖼️ Cadre';
    btn.onclick = () => { tabs.dataset.active = t; renderCosmeticsScreen(); SoundFX.click(); };
    tabs.appendChild(btn);
  });

  grid.innerHTML = '';
  if (activeTab === 'avatars') {
    ALL_AVATARS.forEach(av => {
      const owned = ownsCosmetic('avatar', av.id) || av.rarity === 'common';
      const equipped = eq.avatar === av.icon;
      const item = document.createElement('div');
      item.className = 'cosmetic-item' + (equipped ? ' equipped' : '') + (!owned ? ' locked' : '');
      item.innerHTML = '<div class="ci-icon">' + av.icon + '</div><div>' + av.name + '</div>';
      if (owned && !equipped) item.onclick = () => { equipCosmetic('avatar', av.id); SoundFX.click(); };
      grid.appendChild(item);
    });
  } else if (activeTab === 'colors') {
    grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(50px, 1fr))';
    AVATAR_COLORS.forEach(c => {
      const owned = c.price === 0 || Economy._data.ownedColors?.includes(c.id) ||
        (c.legendary && Economy._data.gachaCollection?.some(x => x.name && x.name.includes('Arc-en-ciel')));
      const active = eq.avatarColor === c.id;
      const swatch = document.createElement('div');
      swatch.className = 'color-swatch' + (active ? ' active' : '') + (!owned ? ' locked' : '');
      const bgClass = getAvatarBgClass(c.id);
      if (bgClass) swatch.classList.add(bgClass);
      else swatch.style.background = c.color;
      if (!owned && c.price > 0) swatch.innerHTML = '<span>' + c.price + '💎</span>';
      swatch.onclick = () => {
        if (!owned && c.price > 0) {
          if (Economy.spendGems(c.price)) {
            if (!Economy._data.ownedColors) Economy._data.ownedColors = [];
            Economy._data.ownedColors.push(c.id);
            Economy.save();
            showToast('Couleur débloquée !');
          } else { showToast('Pas assez de gemmes !'); return; }
        }
        if (owned || c.price === 0) {
          if (!Economy._data.equipped) Economy._data.equipped = {};
          Economy._data.equipped.avatarColor = c.id;
          Economy.save();
        }
        renderCosmeticsScreen();
        SoundFX.click();
      };
      grid.appendChild(swatch);
    });
    // Reset grid columns after
    setTimeout(() => { if (grid) grid.style.gridTemplateColumns = ''; }, 0);
  } else if (activeTab === 'frames') {
    ALL_FRAMES.forEach(fr => {
      const owned = ownsCosmetic('frame', fr.id) || fr.rarity === 'common';
      const equipped = eq.frame === fr.id;
      const item = document.createElement('div');
      item.className = 'cosmetic-item' + (equipped ? ' equipped' : '') + (!owned ? ' locked' : '');
      item.innerHTML = '<div class="ci-icon" style="width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem;" class="avatar-equipped ' + fr.cls + '">🕵️</div><div>' + fr.name + '</div>';
      if (owned && !equipped) item.onclick = () => { equipCosmetic('frame', fr.id); SoundFX.click(); };
      grid.appendChild(item);
    });
  }

  const title = document.getElementById('cosm-title');
  if (title) title.textContent = eq.title || Economy.getLevelTitle();
};


// ===== V10 LOCAL PROFILES =====
function getProfiles() {
  try { return JSON.parse(localStorage.getItem('uc_profiles') || '[]'); } catch(e) { return []; }
}
function saveProfiles(profiles) {
  try { localStorage.setItem('uc_profiles', JSON.stringify(profiles)); } catch(e) {}
}
function getActiveProfileId() {
  return localStorage.getItem('uc_active_profile') || null;
}

function createLocalProfile() {
  const name = prompt('Pseudo du nouveau profil :');
  if (!name || !name.trim()) return;
  const profiles = getProfiles();
  const id = 'p_' + Date.now();
  profiles.push({
    id, name: name.trim(), avatar: '🕵️', level: 1, xp: 0,
    gems: 500, wins: 0, games: 0, created: new Date().toISOString().slice(0,10)
  });
  saveProfiles(profiles);
  renderProfilesList();
  SoundFX.click();
  showToast('Profil créé !');
}

function renderProfilesList() {
  const list = document.getElementById('profiles-list');
  if (!list) return;
  list.innerHTML = '';
  const profiles = getProfiles();
  const activeId = getActiveProfileId();

  if (profiles.length === 0) {
    list.innerHTML = '<div style="text-align:center;color:var(--text-muted);padding:20px;">Aucun profil créé. Chaque joueur peut avoir son propre profil !</div>';
    return;
  }

  profiles.forEach(p => {
    const row = document.createElement('div');
    row.className = 'profile-row' + (p.id === activeId ? ' active-profile' : '');
    row.innerHTML = '<div class="pr-avatar" style="background:var(--bg-card);">' + (p.avatar || '🕵️') + '</div>' +
      '<div class="pr-info"><div class="pr-name">' + p.name + '</div>' +
      '<div class="pr-stats">Nv.' + (p.level||1) + ' • ' + (p.games||0) + ' parties • ' + (p.gems||0) + '💎</div></div>' +
      (p.id === activeId ? '<span class="pr-badge">ACTIF</span>' : '');
    row.onclick = () => {
      localStorage.setItem('uc_active_profile', p.id);
      renderProfilesList();
      showToast(p.name + ' activé !');
      SoundFX.click();
    };
    list.appendChild(row);
  });
}


// ===== V10 DAILY CHALLENGE =====
function getDailyPair() {
  const today = new Date().toISOString().slice(0,10);
  // Deterministic selection based on date
  const seed = today.split('-').reduce((a,b) => a + parseInt(b), 0);
  const idx = seed % PAIRS.length;
  return {pair: PAIRS[idx], date: today};
}

function renderDailyChallenge() {
  const el = document.getElementById('daily-challenge');
  if (!el) return;
  const {pair, date} = getDailyPair();
  const done = localStorage.getItem('uc_daily_' + date);
  el.innerHTML = '<div class="dc-label">🗓️ Défi du jour</div>' +
    '<div class="dc-title">' + (done ? '✅ Défi complété !' : 'Paire mystère à découvrir') + '</div>' +
    '<div class="dc-reward">' + (done ? 'Revenez demain !' : 'Récompense : x2 gemmes 💎') + '</div>';
}

function playDailyChallenge() {
  const {pair, date} = getDailyPair();
  const done = localStorage.getItem('uc_daily_' + date);
  if (done) { showToast('Défi déjà complété aujourd\'hui !'); return; }
  // Set up a game with this specific pair
  GameState.currentMode = 'normal';
  showScreen('screen-settings');
  // Pre-select this pair
  GameState.dailyChallengePair = pair;
  showToast('Défi quotidien : trouvez la paire mystère ! 🗓️');
}


// ===== V10 LOCAL STATS ON SPLASH =====
function updateLocalStats() {
  const el = document.getElementById('local-stats');
  if (!el) return;
  const stats = JSON.parse(localStorage.getItem('uc_stats') || '{}');
  const games = stats.games || 0;
  const rounds = stats.rounds || 0;
  el.textContent = games + ' parties jouées sur cet appareil • ' + rounds + ' manches';
}


// ===== V10 SHOWSCREEN PATCHES =====
const _prevShowScreenV10 = showScreen;
showScreen = function(id) {
  _prevShowScreenV10(id);
  if (id === 'screen-profiles') renderProfilesList();
  if (id === 'screen-splash') { renderDailyChallenge(); updateLocalStats(); }
};

// Init on load
document.addEventListener('DOMContentLoaded', () => {
  renderDailyChallenge();
  updateLocalStats();
});
"""

html = html.replace("\n</script>", JS_V10 + "\n</script>")

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V10 patch applied! Template: {len(html)//1024} KB")
