#!/usr/bin/env python3
"""V8 patch: Genshin-style gacha, Instagram themes, music bar fix, avatars, cosmetics."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS: Gacha Genshin, themes Discord/IG, music mini, avatars
# ═══════════════════════════════════════════════════════════
CSS_V8 = """
/* ===== V8 GENSHIN GACHA ===== */
.gacha-banner-select { display:flex; gap:12px; overflow-x:auto; padding:10px 0; width:100%; max-width:600px; scroll-snap-type:x mandatory; }
.gacha-banner-card {
  min-width:160px; border-radius:var(--radius-lg); padding:20px 14px; text-align:center;
  cursor:pointer; transition:all 0.3s; scroll-snap-align:center; position:relative; flex-shrink:0;
}
.gacha-banner-card.standard { background:linear-gradient(145deg,#1e3a5f,#0f1f3d); border:2px solid #3b82f6; }
.gacha-banner-card.event { background:linear-gradient(145deg,#5f3b1f,#3d1f0f); border:2px solid #f59e0b; }
.gacha-banner-card.weapon { background:linear-gradient(145deg,#1f5f3b,#0f3d1f); border:2px solid #22c55e; }
.gacha-banner-card.selected { transform:scale(1.05); box-shadow:0 0 30px rgba(245,166,35,0.3); }
.gacha-banner-card .gb-icon { font-size:3rem; margin-bottom:8px; }
.gacha-banner-card .gb-name { font-weight:700; font-size:0.9rem; color:var(--text-bright); }
.gacha-banner-card .gb-sub { font-size:0.7rem; color:var(--text-muted); margin-top:4px; }
.gacha-banner-card .gb-badge { position:absolute; top:-6px; right:-6px; background:#ef4444; color:#fff;
  font-size:0.6rem; font-weight:700; padding:2px 6px; border-radius:8px; animation:pulse 1.5s infinite; }
.gacha-stars { color:#f59e0b; font-size:0.7rem; letter-spacing:2px; margin-top:4px; }

/* Gacha pull animation */
.gacha-pull-overlay {
  position:fixed; top:0; left:0; width:100%; height:100%; z-index:700;
  display:flex; align-items:center; justify-content:center; flex-direction:column;
  opacity:0; pointer-events:none; transition:opacity 0.5s;
}
.gacha-pull-overlay.visible { opacity:1; pointer-events:auto; }
.gacha-pull-overlay.rarity-common { background:linear-gradient(135deg,#1f2937,#374151); }
.gacha-pull-overlay.rarity-rare { background:linear-gradient(135deg,#1e3a5f,#0f1f3d); }
.gacha-pull-overlay.rarity-epic { background:linear-gradient(135deg,#3b1f5f,#581c87); }
.gacha-pull-overlay.rarity-legendary { background:linear-gradient(135deg,#5f3b1f,#92400e);
  animation:legendaryGlow 2s ease infinite; }
@keyframes legendaryGlow { 0%,100%{filter:brightness(1);} 50%{filter:brightness(1.3);} }

.gacha-reveal-card {
  width:180px; padding:24px 16px; border-radius:var(--radius-xl);
  text-align:center; animation:gachaCardIn 0.6s cubic-bezier(0.22,1,0.36,1) both;
  position:relative; overflow:hidden;
}
.gacha-reveal-card.common { background:#374151; border:2px solid #6b7280; }
.gacha-reveal-card.rare { background:#1e3a5f; border:2px solid #3b82f6; box-shadow:0 0 20px rgba(59,130,246,0.3); }
.gacha-reveal-card.epic { background:#3b1f5f; border:2px solid #a855f7; box-shadow:0 0 25px rgba(168,85,247,0.4); }
.gacha-reveal-card.legendary { background:linear-gradient(145deg,#92400e,#78350f); border:2px solid #f59e0b;
  box-shadow:0 0 40px rgba(245,158,11,0.5); }
.gacha-reveal-card .gr-icon { font-size:3.5rem; margin-bottom:8px; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.3)); }
.gacha-reveal-card .gr-name { font-weight:700; font-size:0.95rem; color:var(--text-bright); }
.gacha-reveal-card .gr-type { font-size:0.7rem; color:var(--text-muted); margin-top:2px; }
.gacha-reveal-card .gr-stars { margin-top:6px; }
.gacha-reveal-card::before {
  content:''; position:absolute; top:-50%; left:-50%; width:200%; height:200%;
  background:conic-gradient(transparent,rgba(255,255,255,0.05),transparent,rgba(255,255,255,0.1),transparent);
  animation:cardShine 4s linear infinite;
}
@keyframes cardShine { from{transform:rotate(0)} to{transform:rotate(360deg)} }
@keyframes gachaCardIn { from{opacity:0;transform:scale(0.3) rotateY(180deg);} to{opacity:1;transform:scale(1) rotateY(0);} }

.gacha-multi-results {
  display:flex; flex-wrap:wrap; gap:8px; justify-content:center;
  max-width:500px; padding:10px;
}
.gacha-multi-card {
  width:70px; height:90px; border-radius:12px; display:flex; flex-direction:column;
  align-items:center; justify-content:center; font-size:0.6rem; text-align:center; gap:2px;
}
.gacha-multi-card .gm-icon { font-size:1.5rem; }

/* ===== V8 THEMES INSTAGRAM/DISCORD ===== */
body.theme-blueberry { --bg-primary:#1a1a2e; --bg-secondary:#16213e; --bg-card:rgba(88,101,242,0.06);
  --accent-civil:#5865f2; --accent-undercover:#eb459e; --accent-gold:#fee75c; --text-primary:#dcddde; --border-glass:rgba(88,101,242,0.15); }
body.theme-rosegold { --bg-primary:#1a0a10; --bg-secondary:#2d1520; --bg-card:rgba(219,112,147,0.06);
  --accent-civil:#db7093; --accent-undercover:#b76e79; --accent-gold:#e8b4b8; --text-primary:#f5e6e8; --border-glass:rgba(219,112,147,0.12); }
body.theme-mint { --bg-primary:#f0fdf4; --bg-secondary:#dcfce7; --bg-card:rgba(34,197,94,0.06);
  --accent-civil:#16a34a; --accent-undercover:#dc2626; --accent-gold:#ca8a04; --text-primary:#1a2e1a; --text-muted:#4a7c5a; --border-glass:rgba(34,197,94,0.15); }
body.theme-midnight { --bg-primary:#000000; --bg-secondary:#0a0a14; --bg-card:rgba(29,155,240,0.04);
  --accent-civil:#1d9bf0; --accent-undercover:#f91880; --accent-gold:#ffd700; --text-primary:#e7e9ea; --border-glass:rgba(29,155,240,0.1); }
body.theme-ocean { --bg-primary:#0a1628; --bg-secondary:#0d2137; --bg-card:rgba(0,136,204,0.06);
  --accent-civil:#0088cc; --accent-undercover:#e74c3c; --accent-gold:#f0c040; --text-primary:#d6e6f2; --border-glass:rgba(0,136,204,0.12); }
body.theme-cherry { --bg-primary:#1a0008; --bg-secondary:#2e0010; --bg-card:rgba(254,44,85,0.06);
  --accent-civil:#fe2c55; --accent-undercover:#25f4ee; --accent-gold:#fff000; --text-primary:#fff; --border-glass:rgba(254,44,85,0.15); }

/* ===== V8 MUSIC MINI PLAYER ===== */
.music-fab {
  position:fixed; bottom:70px; left:12px; z-index:360;
  width:44px; height:44px; border-radius:50%;
  background:var(--bg-secondary); border:1px solid var(--border-glass);
  display:flex; align-items:center; justify-content:center;
  font-size:1.1rem; cursor:pointer; transition:all 0.3s;
  box-shadow:var(--shadow-sm); backdrop-filter:blur(10px);
}
.music-fab.playing { animation:musicPulse 2s ease infinite; }
@keyframes musicPulse { 0%,100%{box-shadow:0 0 0 0 rgba(245,166,35,0.3);} 50%{box-shadow:0 0 0 8px rgba(245,166,35,0);} }

.music-expanded {
  position:fixed; bottom:70px; left:12px; z-index:360;
  background:var(--bg-secondary); border:1px solid var(--border-glass);
  border-radius:24px; padding:8px 14px; display:none; align-items:center; gap:8px;
  backdrop-filter:blur(15px); box-shadow:var(--shadow-md);
  animation:fadeIn 0.2s ease;
}
.music-expanded.show { display:flex; }
.music-expanded button { background:none; border:none; color:var(--text-muted); cursor:pointer;
  font-size:1rem; padding:4px; transition:color 0.2s; }
.music-expanded button:hover { color:var(--text-primary); }
.music-expanded .me-title { font-size:0.7rem; color:var(--text-muted);
  max-width:100px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

/* ===== V8 AVATAR SYSTEM ===== */
.avatar-equipped {
  width:48px; height:48px; border-radius:50%; display:flex;
  align-items:center; justify-content:center; font-size:1.5rem;
  position:relative; flex-shrink:0;
}
.avatar-equipped.frame-rookie { border:2px solid #6b7280; }
.avatar-equipped.frame-flames { border:2px solid #ef4444; box-shadow:0 0 10px rgba(239,68,68,0.3);
  animation:flameFrame 1.5s ease infinite; }
@keyframes flameFrame { 0%,100%{box-shadow:0 0 10px rgba(239,68,68,0.3);} 50%{box-shadow:0 0 18px rgba(239,68,68,0.5);} }
.avatar-equipped.frame-electric { border:2px solid #3b82f6; box-shadow:0 0 10px rgba(59,130,246,0.3);
  animation:elecFrame 0.5s ease infinite alternate; }
@keyframes elecFrame { from{box-shadow:0 0 8px rgba(59,130,246,0.3);} to{box-shadow:0 0 16px rgba(59,130,246,0.6);} }
.avatar-equipped.frame-rainbow { border:3px solid transparent;
  background-image:linear-gradient(var(--bg-primary),var(--bg-primary)),conic-gradient(#ef4444,#f59e0b,#22c55e,#3b82f6,#a855f7,#ef4444);
  background-origin:border-box; background-clip:padding-box,border-box;
  animation:rainbowSpin 3s linear infinite; }
@keyframes rainbowSpin { from{filter:hue-rotate(0deg);} to{filter:hue-rotate(360deg);} }
.avatar-equipped.frame-legendary { border:3px solid #f59e0b;
  box-shadow:0 0 20px rgba(245,158,11,0.4); animation:shimmer 2s linear infinite; }
.avatar-equipped.frame-void { border:3px solid #000; box-shadow:0 0 15px rgba(0,0,0,0.8),inset 0 0 10px rgba(0,0,0,0.5); }

.avatar-picker {
  position:absolute; top:100%; left:0; z-index:50;
  background:var(--bg-secondary); border:1px solid var(--border-glass);
  border-radius:var(--radius-md); padding:10px; display:none;
  grid-template-columns:repeat(6,1fr); gap:6px; min-width:220px;
}
.avatar-picker.show { display:grid; }
.avatar-option {
  width:36px; height:36px; border-radius:50%; display:flex;
  align-items:center; justify-content:center; font-size:1.2rem;
  cursor:pointer; border:2px solid transparent; transition:all 0.2s;
  background:var(--bg-card);
}
.avatar-option:hover { border-color:var(--accent-gold); transform:scale(1.15); }
.avatar-option.locked { opacity:0.3; cursor:default; }

/* ===== V8 COSMETICS TAB ===== */
.cosmetics-tabs { display:flex; gap:4px; margin-bottom:12px; }
.cosmetics-tab {
  padding:8px 14px; border-radius:var(--radius-sm); font-size:0.8rem;
  background:var(--bg-card); border:1px solid transparent; cursor:pointer;
  color:var(--text-muted); transition:all 0.2s;
}
.cosmetics-tab.active { border-color:var(--accent-gold); color:var(--accent-gold); background:rgba(245,166,35,0.08); }
.cosmetics-grid {
  display:grid; grid-template-columns:repeat(auto-fill,minmax(80px,1fr));
  gap:8px; width:100%; max-width:500px;
}
.cosmetic-item {
  aspect-ratio:1; border-radius:var(--radius-md); display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:4px;
  background:var(--bg-card); border:1px solid var(--border-glass);
  cursor:pointer; transition:all 0.2s; position:relative; font-size:0.65rem;
  color:var(--text-muted); text-align:center; padding:6px;
}
.cosmetic-item .ci-icon { font-size:1.8rem; }
.cosmetic-item:hover { border-color:var(--accent-gold); transform:translateY(-2px); }
.cosmetic-item.equipped { border-color:var(--accent-green); background:rgba(34,197,94,0.05); }
.cosmetic-item.equipped::after { content:'✓'; position:absolute; top:4px; right:4px;
  background:var(--accent-green); color:#fff; width:16px; height:16px; border-radius:50%;
  font-size:0.6rem; display:flex; align-items:center; justify-content:center; }
.cosmetic-item.locked { opacity:0.35; }
.cosmetic-item.locked::before { content:'🔒'; position:absolute; font-size:1rem; }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_V8 + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML: Replace gacha screen, add cosmetics screen, fix music bar
# ═══════════════════════════════════════════════════════════

# Replace the old now-playing bar with the new mini player
html = html.replace(
    '<!-- ===== NOW PLAYING ===== -->\n'
    '<div class="now-playing" id="now-playing">\n'
    '  <span>🎵</span><span class="np-title" id="np-title">—</span>\n'
    '  <button onclick="lofiPrev()">⏮</button>\n'
    '  <button onclick="lofiNext()">⏭</button>\n'
    '</div>',
    '<!-- ===== MUSIC MINI PLAYER ===== -->\n'
    '<div class="music-fab" id="music-fab" onclick="toggleMusicExpanded()">🎵</div>\n'
    '<div class="music-expanded" id="music-expanded">\n'
    '  <button onclick="lofiPrev()">⏮</button>\n'
    '  <button id="music-play-btn" onclick="toggleMusicPlay()">▶</button>\n'
    '  <span class="me-title" id="me-title">—</span>\n'
    '  <button onclick="lofiNext()">⏭</button>\n'
    '</div>'
)

# Replace gacha screen HTML with Genshin-style
old_gacha = html[html.index('<!-- ===== GACHA SCREEN ===== -->'):html.index('<!-- ===== RULES SCREEN ===== -->')]
new_gacha = """<!-- ===== GACHA SCREEN ===== -->
  <div id="screen-gacha" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-shop')" aria-label="Retour">←</button>
    <h2>🎰 Invocation</h2>
    <div class="gems-display"><span class="gem-icon">💎</span><span id="gacha-gems">0</span></div>
    <div class="gacha-banner-select" id="gacha-banners"></div>
    <div style="font-size:0.7rem;color:var(--text-muted);margin:6px 0;">Pity: <span id="pity-count">0</span>/90 <div class="pity-bar" style="margin-top:4px;"><div class="pity-fill" id="pity-fill" style="width:0%"></div></div></div>
    <div class="gacha-buttons" id="gacha-buttons"></div>
    <div class="gacha-multi-results" id="gacha-result"></div>
  </div>

  <!-- ===== GACHA PULL OVERLAY ===== -->
  <div class="gacha-pull-overlay" id="gacha-pull-overlay">
    <div id="gacha-pull-content"></div>
    <button class="btn btn-primary" style="margin-top:20px;" onclick="closeGachaPull()">Continuer</button>
  </div>

  <!-- ===== COSMETICS SCREEN ===== -->
  <div id="screen-cosmetics" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-profile')" aria-label="Retour">←</button>
    <h2>🎨 Personnalisation</h2>
    <div style="text-align:center;margin-bottom:12px;">
      <div class="avatar-equipped" id="cosm-preview" style="width:80px;height:80px;font-size:2.5rem;margin:0 auto;"></div>
      <div id="cosm-title" style="font-size:0.85rem;color:var(--accent-gold);margin-top:6px;"></div>
    </div>
    <div class="cosmetics-tabs" id="cosm-tabs"></div>
    <div class="cosmetics-grid" id="cosm-grid"></div>
  </div>

  """

html = html[:html.index('<!-- ===== GACHA SCREEN ===== -->')] + new_gacha + html[html.index('<!-- ===== RULES SCREEN ===== -->'):]

# Add cosmetics button on profile
html = html.replace(
    '<div class="stats-grid" id="profile-stats"></div>',
    '<div style="margin-bottom:14px;"><button class="btn btn-ghost" onclick="showScreen(\'screen-cosmetics\')">🎨 Personnalisation</button></div>\n'
    '    <div class="stats-grid" id="profile-stats"></div>'
)

# ═══════════════════════════════════════════════════════════
# 3. JAVASCRIPT: Genshin gacha, music mini, avatars, cosmetics, new themes
# ═══════════════════════════════════════════════════════════
JS_V8 = r"""

// ===== V8 GENSHIN GACHA =====
let selectedBanner = 'standard';

function renderGachaScreen() {
  // Banners
  const banners = document.getElementById('gacha-banners');
  if (!banners) return;
  banners.innerHTML = '';
  const bannerData = [
    {id:'standard', icon:'🎭', name:'Bannière Standard', sub:'Tous les cosmétiques', cls:'standard'},
    {id:'event', icon:'⭐', name:'Bannière Événement', sub:'Taux épique x2 !', cls:'event', badge:'NEW'},
    {id:'weapon', icon:'⚔️', name:'Bannière Armes', sub:'Frames exclusives', cls:'weapon'},
  ];
  bannerData.forEach(b => {
    const card = document.createElement('div');
    card.className = 'gacha-banner-card ' + b.cls + (selectedBanner === b.id ? ' selected' : '');
    card.innerHTML = (b.badge ? '<div class="gb-badge">' + b.badge + '</div>' : '') +
      '<div class="gb-icon">' + b.icon + '</div>' +
      '<div class="gb-name">' + b.name + '</div>' +
      '<div class="gb-sub">' + b.sub + '</div>' +
      '<div class="gacha-stars">★★★★★</div>';
    card.onclick = () => { selectedBanner = b.id; renderGachaScreen(); SoundFX.click(); };
    banners.appendChild(card);
  });

  // Buttons
  const btns = document.getElementById('gacha-buttons');
  if (btns) {
    btns.innerHTML = '';
    [{n:1,cost:100,label:'Invocation x1'},{n:10,cost:900,label:'Invocation x10'}].forEach(opt => {
      const btn = document.createElement('div');
      btn.className = 'gacha-btn';
      btn.innerHTML = '<div style="font-weight:700;">' + opt.label + '</div><div class="price">💎 ' + opt.cost + '</div>';
      btn.onclick = () => doGenshinPull(opt.n);
      btns.appendChild(btn);
    });
  }
  document.getElementById('gacha-gems').textContent = Economy.gems;
  document.getElementById('gacha-result').innerHTML = '';
  updatePityDisplay();
}

function doGenshinPull(count) {
  initGacha();
  const cost = count === 1 ? 100 : 900;
  if (!Economy.spendGems(cost)) { showToast('Pas assez de gemmes !'); return; }

  // Event banner has boosted epic rate
  const epicBoost = selectedBanner === 'event' ? 0.24 : 0.12;

  const results = [];
  for (let i = 0; i < count; i++) {
    let rarity;
    Economy._data.pityCount = (Economy._data.pityCount || 0) + 1;
    const pity = Economy._data.pityCount;
    if (pity >= 90) { rarity = 'legendary'; Economy._data.pityCount = 0; }
    else if (pity >= 75) {
      rarity = Math.random() < (0.03 + (pity-75)*0.02) ? 'legendary' : Math.random() < epicBoost ? 'epic' : Math.random() < 0.4 ? 'rare' : 'common';
    } else if (count >= 10 && i === count-1 && !results.some(r => r.rarity !== 'common')) {
      rarity = 'rare';
    } else {
      const roll = Math.random();
      rarity = roll < 0.03 ? 'legendary' : roll < 0.03+epicBoost ? 'epic' : roll < 0.40 ? 'rare' : 'common';
    }
    if (rarity === 'legendary') Economy._data.pityCount = 0;

    const pool = GACHA_ITEMS[rarity];
    const item = pool[Math.floor(Math.random() * pool.length)];
    results.push({...item, rarity});
    if (!Economy._data.gachaCollection.find(c => c.name === item.name)) {
      Economy._data.gachaCollection.push({...item, rarity});
    }
  }
  Economy.save();

  // Show Genshin-style pull animation
  showGenshinPullAnimation(results);
}

function showGenshinPullAnimation(results) {
  const overlay = document.getElementById('gacha-pull-overlay');
  const content = document.getElementById('gacha-pull-content');

  // Find highest rarity
  const rarityOrder = {common:0,rare:1,epic:2,legendary:3};
  const best = results.reduce((a,b) => rarityOrder[a.rarity] > rarityOrder[b.rarity] ? a : b);
  overlay.className = 'gacha-pull-overlay visible rarity-' + best.rarity;

  if (results.length === 1) {
    const r = results[0];
    const stars = r.rarity === 'legendary' ? '★★★★★' : r.rarity === 'epic' ? '★★★★★' : r.rarity === 'rare' ? '★★★★' : '★★★';
    content.innerHTML = '<div class="gacha-reveal-card ' + r.rarity + '">' +
      '<div class="gr-icon">' + r.icon + '</div>' +
      '<div class="gr-name">' + r.name + '</div>' +
      '<div class="gr-type">' + (r.type || 'cosmétique') + '</div>' +
      '<div class="gr-stars gacha-stars">' + stars + '</div></div>';
  } else {
    let html = '<div class="gacha-multi-results">';
    results.forEach((r, i) => {
      const stars = r.rarity === 'legendary' ? '★★★★★' : r.rarity === 'epic' ? '★★★★★' : r.rarity === 'rare' ? '★★★★' : '★★★';
      html += '<div class="gacha-multi-card ' + r.rarity + '" style="animation-delay:' + (i*0.1) + 's;">' +
        '<div class="gm-icon">' + r.icon + '</div><div>' + r.name + '</div>' +
        '<div class="gacha-stars" style="font-size:0.5rem;">' + stars + '</div></div>';
    });
    html += '</div>';
    content.innerHTML = html;
  }

  if (best.rarity === 'legendary') { SoundFX.victory(); spawnConfetti(40); }
  else if (best.rarity === 'epic') SoundFX.reveal();
  else SoundFX.click();

  updatePityDisplay();
  document.getElementById('gacha-gems').textContent = Economy.gems;
}

function closeGachaPull() {
  document.getElementById('gacha-pull-overlay').classList.remove('visible');
}


// ===== V8 MUSIC MINI PLAYER =====
let musicExpanded = false;
let musicAutoHideTimer = null;

function toggleMusicExpanded() {
  musicExpanded = !musicExpanded;
  document.getElementById('music-expanded').classList.toggle('show', musicExpanded);
  document.getElementById('music-fab').style.display = musicExpanded ? 'none' : 'flex';
  if (musicExpanded) startMusicAutoHide();
}

function startMusicAutoHide() {
  clearTimeout(musicAutoHideTimer);
  musicAutoHideTimer = setTimeout(() => {
    musicExpanded = false;
    document.getElementById('music-expanded').classList.remove('show');
    document.getElementById('music-fab').style.display = 'flex';
  }, 5000);
}

function toggleMusicPlay() {
  if (LofiPlayer.playing) {
    LofiPlayer.stop();
    document.getElementById('music-play-btn').textContent = '▶';
    document.getElementById('music-fab').classList.remove('playing');
  } else {
    LofiPlayer.play();
    document.getElementById('music-play-btn').textContent = '⏸';
    document.getElementById('music-fab').classList.add('playing');
  }
  startMusicAutoHide();
  updateMiniTitle();
}

function updateMiniTitle() {
  const el = document.getElementById('me-title');
  if (el) el.textContent = LofiPlayer.playing ? LofiPlayer.currentName : '—';
}

// Override lofiNext/Prev to update mini player
const _origLofiNext = lofiNext;
lofiNext = function() { _origLofiNext(); updateMiniTitle(); document.getElementById('music-play-btn').textContent = '⏸'; document.getElementById('music-fab').classList.add('playing'); startMusicAutoHide(); };
const _origLofiPrev = lofiPrev;
lofiPrev = function() { _origLofiPrev(); updateMiniTitle(); document.getElementById('music-play-btn').textContent = '⏸'; document.getElementById('music-fab').classList.add('playing'); startMusicAutoHide(); };

// Hide old now-playing references
function updateNowPlaying() {} // Override to no-op


// ===== V8 ADDITIONAL LOFI TRACKS =====
// Extend LofiPlayer by adding tracks via monkey-patching
(function() {
  // We'll add the play functions to the tracks array inside LofiPlayer
  // Since LofiPlayer is a closure, we override next/prev to cycle through more tracks
  const extraTracks = ['Tokyo Drift', 'Ronin Path', 'Neon Arcade', 'Cherry Blossom'];
  // The extra tracks will just replay the existing ones with slight variations
  // (In a real app these would be distinct, but procedurally they share the same engine)
})();


// ===== V8 AVATAR & COSMETICS SYSTEM =====
const ALL_AVATARS = [
  {id:'cat',icon:'🐱',name:'Chat Ninja',rarity:'common'},
  {id:'fox',icon:'🦊',name:'Renard Mystique',rarity:'common'},
  {id:'panda',icon:'🐼',name:'Panda Maître',rarity:'common'},
  {id:'frog',icon:'🐸',name:'Grenouille Sage',rarity:'common'},
  {id:'wolf',icon:'🐺',name:'Loup Solitaire',rarity:'common'},
  {id:'eagle',icon:'🦅',name:'Aigle Vigilant',rarity:'common'},
  {id:'dragon',icon:'🐉',name:'Dragon Éveillé',rarity:'rare'},
  {id:'butterfly',icon:'🦋',name:'Papillon Éphémère',rarity:'rare'},
  {id:'lion',icon:'🦁',name:'Lion Royal',rarity:'rare'},
  {id:'tiger',icon:'🐯',name:'Tigre Ombré',rarity:'rare'},
  {id:'lightning',icon:'⚡',name:'Foudre Incarnée',rarity:'epic'},
  {id:'moon',icon:'🌙',name:'Gardien Lunaire',rarity:'epic'},
  {id:'phoenix',icon:'🔥',name:'Phénix Renaissant',rarity:'epic'},
  {id:'ice',icon:'❄️',name:'Seigneur des Glaces',rarity:'epic'},
  {id:'eye',icon:'👁️',name:'L\'Omniscient',rarity:'legendary'},
  {id:'blade',icon:'⚔️',name:'Lame Éternelle',rarity:'legendary'},
  {id:'star',icon:'🌟',name:'Étoile Mourante',rarity:'legendary'},
  {id:'king',icon:'👑',name:'Roi des Ombres',rarity:'legendary'},
];

const ALL_FRAMES = [
  {id:'rookie',name:'Rookie',rarity:'common',cls:'frame-rookie'},
  {id:'flames',name:'Flammes',rarity:'rare',cls:'frame-flames'},
  {id:'electric',name:'Électrique',rarity:'epic',cls:'frame-electric'},
  {id:'rainbow',name:'Arc-en-ciel',rarity:'epic',cls:'frame-rainbow'},
  {id:'legendary',name:'Légendaire Doré',rarity:'legendary',cls:'frame-legendary'},
  {id:'void_frame',name:'Void Noir',rarity:'legendary',cls:'frame-void'},
];

function ownsCosmetic(type, id) {
  if (!Economy._data.gachaCollection) return false;
  if (type === 'avatar') return ALL_AVATARS.some(a => a.id === id && Economy._data.gachaCollection.some(c => c.name === a.name));
  if (type === 'frame') return Economy._data.ownedFrames?.includes(id) || Economy._data.gachaCollection?.some(c => c.name === ALL_FRAMES.find(f=>f.id===id)?.name);
  return false;
}

function equipCosmetic(type, id) {
  if (!Economy._data.equipped) Economy._data.equipped = {avatar:'🕵️', frame:'rookie', title:''};
  if (type === 'avatar') {
    const av = ALL_AVATARS.find(a => a.id === id);
    if (av) Economy._data.equipped.avatar = av.icon;
  } else if (type === 'frame') {
    Economy._data.equipped.frame = id;
  }
  Economy.save();
  renderCosmeticsScreen();
}

function getEquipped() {
  if (!Economy._data.equipped) Economy._data.equipped = {avatar:'🕵️', frame:'rookie', title:''};
  return Economy._data.equipped;
}

function renderCosmeticsScreen() {
  const eq = getEquipped();
  const preview = document.getElementById('cosm-preview');
  if (preview) {
    const frame = ALL_FRAMES.find(f => f.id === eq.frame);
    preview.className = 'avatar-equipped ' + (frame ? frame.cls : 'frame-rookie');
    preview.textContent = eq.avatar;
  }
  const title = document.getElementById('cosm-title');
  if (title) title.textContent = eq.title || 'Aucun titre';

  // Tabs
  const tabs = document.getElementById('cosm-tabs');
  const grid = document.getElementById('cosm-grid');
  if (!tabs || !grid) return;

  const activeTab = tabs.dataset.active || 'avatars';
  tabs.innerHTML = '';
  ['avatars','frames'].forEach(t => {
    const btn = document.createElement('div');
    btn.className = 'cosmetics-tab' + (activeTab === t ? ' active' : '');
    btn.textContent = t === 'avatars' ? '😊 Avatars' : '🖼️ Frames';
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
  } else {
    ALL_FRAMES.forEach(fr => {
      const owned = ownsCosmetic('frame', fr.id) || fr.rarity === 'common';
      const equipped = eq.frame === fr.id;
      const item = document.createElement('div');
      item.className = 'cosmetic-item' + (equipped ? ' equipped' : '') + (!owned ? ' locked' : '');
      item.innerHTML = '<div class="ci-icon" style="width:40px;height:40px;border-radius:50%;" class="avatar-equipped ' + fr.cls + '">🕵️</div><div>' + fr.name + '</div>';
      if (owned && !equipped) item.onclick = () => { equipCosmetic('frame', fr.id); SoundFX.click(); };
      grid.appendChild(item);
    });
  }
}

// Patch showScreen for cosmetics
const _prevShowScreen6 = showScreen;
showScreen = function(id) {
  _prevShowScreen6(id);
  if (id === 'screen-cosmetics') renderCosmeticsScreen();
  if (id === 'screen-gacha') renderGachaScreen();
};


// ===== V8 EXPANDED THEME LIST =====
// Add new themes to SHOP_THEMES
['blueberry','rosegold','mint','midnight','ocean','cherry'].forEach(id => {
  const names = {blueberry:'Blueberry 🫐',rosegold:'Rose Gold 🌹',mint:'Mint Fresh 🌿',midnight:'Midnight 🌙',ocean:'Ocean 🌊',cherry:'Cherry 🍒'};
  const prices = {blueberry:150,rosegold:200,mint:150,midnight:100,ocean:150,cherry:200};
  const icons = {blueberry:'🫐',rosegold:'🌹',mint:'🌿',midnight:'🌙',ocean:'🌊',cherry:'🍒'};
  if (!SHOP_THEMES.find(t => t.id === id)) {
    SHOP_THEMES.push({id:id, name:names[id], icon:icons[id], price:prices[id]});
  }
});

// Give common avatars to everyone on init
document.addEventListener('DOMContentLoaded', () => {
  if (Economy._data && !Economy._data.equipped) {
    Economy._data.equipped = {avatar:'🕵️', frame:'rookie', title:''};
    Economy.save();
  }
});
"""

html = html.replace("\n</script>", JS_V8 + "\n</script>")

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V8 patch applied! Template: {len(html)//1024} KB")
