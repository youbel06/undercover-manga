#!/usr/bin/env python3
"""V7 patch: Admin mode, real themes, gacha, lofi music, rules, enhanced profile."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS for themes, gacha, rules, admin, enhanced profile
# ═══════════════════════════════════════════════════════════
CSS_V7 = """
/* ===== V7 THEME SYSTEM ===== */
body.theme-sakura { --bg-primary:#1a0a1a; --bg-secondary:#2d1b2d; --bg-card:rgba(255,107,157,0.06);
  --accent-civil:#ff6b9d; --accent-undercover:#c850c0; --accent-gold:#ff9a9e; --text-primary:#ffd6e8; --border-glass:rgba(255,107,157,0.15); }
body.theme-cyber { --bg-primary:#000814; --bg-secondary:#001d3d; --bg-card:rgba(0,212,255,0.05);
  --accent-civil:#00d4ff; --accent-undercover:#ff006e; --accent-gold:#00ffcc; --text-primary:#caf0f8; --border-glass:rgba(0,212,255,0.15); }
body.theme-cyber .splash-title, body.theme-cyber h2 { animation: glitch 3s infinite; }
@keyframes glitch { 0%,95%,100%{transform:none;} 96%{transform:translateX(-2px);} 97%{transform:translateX(2px);} 98%{transform:translateX(-1px);} }
body.theme-cyber::after { content:''; position:fixed; top:0;left:0;width:100%;height:100%;
  background:repeating-linear-gradient(0deg,rgba(0,0,0,0.1) 0px,transparent 1px,transparent 2px); pointer-events:none; z-index:998; opacity:0.3; }
body.theme-gold { --bg-primary:#0d0900; --bg-secondary:#1a1000; --bg-card:rgba(245,166,35,0.06);
  --accent-civil:#f5a623; --accent-undercover:#b45309; --accent-gold:#ffd700; --text-primary:#ffd700; --border-glass:rgba(245,166,35,0.2); }
body.theme-gold .btn-primary { background:linear-gradient(135deg,#f5a623,#d4891a); }
body.theme-gold .shop-card, body.theme-gold .mode-card { border-color:rgba(245,166,35,0.2); }
body.theme-void { --bg-primary:#000; --bg-secondary:#0a0a0a; --bg-card:rgba(255,255,255,0.03);
  --accent-civil:#fff; --accent-undercover:#666; --accent-gold:#aaa; --text-primary:#ccc; --border-glass:rgba(255,255,255,0.06); }
body.theme-forest { --bg-primary:#0a1a0a; --bg-secondary:#1a2e1a; --bg-card:rgba(74,222,128,0.05);
  --accent-civil:#4ade80; --accent-undercover:#166534; --accent-gold:#86efac; --text-primary:#d4edda; --border-glass:rgba(74,222,128,0.12); }
body.theme-sunset { --bg-primary:#1a0a00; --bg-secondary:#2e1a00; --bg-card:rgba(255,107,53,0.06);
  --accent-civil:#ff6b35; --accent-undercover:#c2410c; --accent-gold:#fb923c; --text-primary:#ffd6b0; --border-glass:rgba(255,107,53,0.15); }
body.theme-ice { --bg-primary:#0a0f1a; --bg-secondary:#0f1a2e; --bg-card:rgba(125,211,252,0.05);
  --accent-civil:#7dd3fc; --accent-undercover:#0284c7; --accent-gold:#bae6fd; --text-primary:#e0f2fe; --border-glass:rgba(125,211,252,0.12); }
body.theme-blood { --bg-primary:#1a0000; --bg-secondary:#2e0000; --bg-card:rgba(220,38,38,0.06);
  --accent-civil:#dc2626; --accent-undercover:#7f1d1d; --accent-gold:#fca5a5; --text-primary:#fecaca; --border-glass:rgba(220,38,38,0.15); }

/* ===== ADMIN BADGE ===== */
.admin-badge { display:inline-flex; align-items:center; gap:4px; background:linear-gradient(135deg,#f5a623,#d4891a);
  color:#000; font-size:0.65rem; font-weight:800; padding:3px 8px; border-radius:8px; margin-left:6px; }
.admin-lock { cursor:pointer; font-size:1.2rem; transition:transform 0.3s; }
.admin-lock:hover { transform:scale(1.2); }

/* ===== GACHA ===== */
#screen-gacha { justify-content:center; gap:16px; }
.gacha-banner { font-size:2.5rem; text-align:center; animation:titleFloat 3s ease-in-out infinite; }
.gacha-buttons { display:flex; gap:10px; flex-wrap:wrap; justify-content:center; }
.gacha-btn { padding:14px 20px; border-radius:var(--radius-lg); background:var(--bg-card);
  border:1px solid var(--border-glass); cursor:pointer; text-align:center; transition:all 0.2s; color:var(--text-primary); }
.gacha-btn:hover { border-color:var(--accent-gold); transform:translateY(-2px); }
.gacha-btn .price { color:var(--accent-gold); font-weight:700; font-size:0.9rem; }
.gacha-btn .desc { font-size:0.7rem; color:var(--text-muted); }
.gacha-result { display:flex; flex-wrap:wrap; gap:10px; justify-content:center; max-width:400px; }
.gacha-card { width:80px; height:100px; border-radius:var(--radius-md); display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:4px; animation:flipCard 0.6s ease both;
  font-size:0.7rem; text-align:center; }
.gacha-card.common { background:linear-gradient(135deg,#374151,#1f2937); border:2px solid #6b7280; }
.gacha-card.rare { background:linear-gradient(135deg,#1e3a5f,#0f1f3d); border:2px solid #3b82f6; box-shadow:0 0 10px rgba(59,130,246,0.3); }
.gacha-card.epic { background:linear-gradient(135deg,#3b1f5f,#1f0f3d); border:2px solid #a855f7; box-shadow:0 0 15px rgba(168,85,247,0.3); }
.gacha-card.legendary { background:linear-gradient(135deg,#5f3b1f,#3d1f0f); border:2px solid #f59e0b;
  box-shadow:0 0 20px rgba(245,158,11,0.4); animation:flipCard 0.6s ease both, shimmer 2s linear infinite; }
@keyframes shimmer { 0%{filter:brightness(1);} 50%{filter:brightness(1.3);} 100%{filter:brightness(1);} }
.gacha-card .gi { font-size:1.8rem; }
.pity-bar { width:100%; max-width:300px; height:6px; background:rgba(255,255,255,0.1); border-radius:3px; overflow:hidden; }
.pity-fill { height:100%; background:linear-gradient(90deg,var(--accent-gold),#f59e0b); border-radius:3px; transition:width 0.3s; }

/* ===== RULES ===== */
#screen-rules { padding-top:60px; }
.rules-list { max-width:500px; width:100%; }
.rule-item { display:flex; gap:14px; align-items:flex-start; padding:14px 0;
  border-bottom:1px solid var(--border-glass); animation:fadeInUp 0.4s ease both; }
.rule-num { width:32px; height:32px; border-radius:50%; background:var(--accent-civil);
  color:#000; font-weight:800; font-size:0.85rem; flex-shrink:0;
  display:flex; align-items:center; justify-content:center; }
.rule-text { font-size:0.9rem; color:var(--text-primary); line-height:1.5; }
.rule-text em { color:var(--accent-gold); font-style:normal; font-weight:600; }

/* ===== NOW PLAYING BAR ===== */
.now-playing { position:fixed; bottom:60px; left:0; width:100%; z-index:340;
  background:var(--bg-secondary); border-top:1px solid var(--border-glass);
  padding:6px 16px; display:flex; align-items:center; gap:10px; font-size:0.75rem;
  color:var(--text-muted); opacity:0; pointer-events:none; transition:opacity 0.3s; }
.now-playing.visible { opacity:1; pointer-events:auto; }
.now-playing .np-title { flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.now-playing button { background:none; border:none; color:var(--text-muted); cursor:pointer; font-size:1rem; padding:2px 6px; }
.now-playing button:hover { color:var(--text-primary); }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_V7 + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML: Gacha screen, Rules screen, admin section, now-playing bar
# ═══════════════════════════════════════════════════════════

# Add gacha + rules screens before credits
html = html.replace(
    '  <!-- ===== CREDITS SCREEN ===== -->',
    '  <!-- ===== GACHA SCREEN ===== -->\n'
    '  <div id="screen-gacha" class="screen">\n'
    '    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen(\'screen-shop\')" aria-label="Retour">←</button>\n'
    '    <div class="gacha-banner">🎰</div>\n'
    '    <h2>Tirage Gacha</h2>\n'
    '    <div class="gems-display"><span class="gem-icon">💎</span><span id="gacha-gems">0</span></div>\n'
    '    <div class="gacha-buttons" id="gacha-buttons"></div>\n'
    '    <div style="font-size:0.75rem;color:var(--text-muted)">Pity: <span id="pity-count">0</span>/90 — Prochain légendaire garanti</div>\n'
    '    <div class="pity-bar"><div class="pity-fill" id="pity-fill" style="width:0%"></div></div>\n'
    '    <div class="gacha-result" id="gacha-result"></div>\n'
    '  </div>\n\n'
    '  <!-- ===== RULES SCREEN ===== -->\n'
    '  <div id="screen-rules" class="screen">\n'
    '    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen(\'screen-splash\')" aria-label="Retour">←</button>\n'
    '    <h2>📖 Règles du jeu</h2>\n'
    '    <div class="rules-list" id="rules-list"></div>\n'
    '  </div>\n\n'
    '  <!-- ===== CREDITS SCREEN ===== -->'
)

# Add admin input to settings screen (find the blind toggle area)
html = html.replace(
    '<div class="universe-filter" id="universe-filter"></div>',
    '<div class="universe-filter" id="universe-filter"></div>\n'
    '      <div class="settings-group" style="margin-top:14px;">\n'
    '        <label class="settings-label">🔑 Code Admin</label>\n'
    '        <div style="display:flex;gap:8px;align-items:center;">\n'
    '          <input type="password" id="admin-code" placeholder="••••" maxlength="4" style="width:80px;background:var(--bg-card);border:1px solid var(--border-glass);border-radius:var(--radius-sm);padding:8px;color:var(--text-primary);font-size:1rem;text-align:center;">\n'
    '          <button class="btn btn-ghost" onclick="checkAdminCode()" style="min-height:36px;padding:6px 12px;">Valider</button>\n'
    '        </div>\n'
    '      </div>'
)

# Add rules + gacha buttons to splash
html = html.replace(
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-credits\')">Crédits</button>',
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-rules\')">📖 Règles</button>\n'
    '    <button class="btn btn-ghost" onclick="showScreen(\'screen-credits\')">Crédits</button>'
)

# Add gacha button in shop
html = html.replace(
    '<div class="shop-section"><div class="shop-section-title">📦 Packs</div>',
    '<div class="shop-section"><div class="shop-section-title">🎰 Gacha <button class="btn btn-ghost" onclick="showScreen(\'screen-gacha\')" style="min-height:32px;padding:4px 12px;font-size:0.8rem;">Ouvrir le Gacha</button></div></div>\n'
    '    <div class="shop-section"><div class="shop-section-title">📦 Packs</div>'
)

# Add now-playing bar before bottom nav
html = html.replace(
    '<!-- ===== BOTTOM NAV ===== -->',
    '<!-- ===== NOW PLAYING ===== -->\n'
    '<div class="now-playing" id="now-playing">\n'
    '  <span>🎵</span><span class="np-title" id="np-title">—</span>\n'
    '  <button onclick="lofiPrev()">⏮</button>\n'
    '  <button onclick="lofiNext()">⏭</button>\n'
    '</div>\n\n'
    '<!-- ===== BOTTOM NAV ===== -->'
)

# ═══════════════════════════════════════════════════════════
# 3. JAVASCRIPT
# ═══════════════════════════════════════════════════════════
JS_V7 = r"""

// ===== ADMIN MODE =====
function checkAdminCode() {
  const code = document.getElementById('admin-code')?.value;
  if (code === '4437') {
    // Unlock everything
    const allModes = SHOP_MODES.map(m => m.id);
    const allThemes = SHOP_THEMES.map(t => t.id);
    const allFrames = SHOP_FRAMES.map(f => f.id);
    Economy._data.ownedModes = [...new Set([...Economy._data.ownedModes, ...allModes])];
    Economy._data.ownedThemes = [...new Set([...Economy._data.ownedThemes, ...allThemes])];
    Economy._data.ownedFrames = [...new Set([...Economy._data.ownedFrames, ...allFrames])];
    Economy._data.isAdmin = true;
    Economy._data.gems += 10000;
    Economy.save();
    SoundFX.victory();
    showToast('👑 Accès Admin activé — tout est débloqué !', 4000);
    spawnConfetti(50);
    document.getElementById('admin-code').value = '';
    renderSettings();
  } else {
    showToast('Code incorrect');
    SoundFX.click();
  }
}


// ===== REAL THEME APPLICATION =====
function applyTheme(themeId) {
  // Remove all theme classes
  document.body.className = document.body.className.replace(/theme-\S+/g, '').trim();
  if (themeId && themeId !== 'default') {
    document.body.classList.add('theme-' + themeId);
  }
  Economy._data.selectedTheme = themeId;
  Economy.save();
}

// Apply saved theme on load
document.addEventListener('DOMContentLoaded', () => {
  const saved = Economy?.data?.selectedTheme;
  if (saved && saved !== 'default') {
    document.body.classList.add('theme-' + saved);
  }
});

// Patch SHOP_THEMES rendering to add Aperçu + Activer
const _origRenderShop = renderShop;
renderShop = function() {
  _origRenderShop();
  // Re-render themes with preview/activate buttons
  const grid = document.getElementById('shop-themes');
  if (!grid) return;
  grid.innerHTML = '';
  SHOP_THEMES.forEach(t => {
    const owned = Economy.ownsTheme(t.id);
    const active = Economy.data.selectedTheme === t.id;
    const card = document.createElement('div');
    card.className = 'shop-card' + (owned ? ' owned' : '');
    if (active) card.style.borderColor = 'var(--accent-green)';
    card.innerHTML = '<div class="shop-card-icon">' + t.icon + '</div>' +
      '<div class="shop-card-name">' + t.name + '</div>' +
      (active ? '<div class="shop-card-price free">✓ Actif</div>' :
       owned ? '<div style="display:flex;gap:4px;justify-content:center;margin-top:4px;">' +
         '<button class="btn btn-ghost" style="min-height:28px;padding:2px 8px;font-size:0.7rem;" onclick="event.stopPropagation();previewTheme(\'' + t.id + '\')">Aperçu</button>' +
         '<button class="btn btn-primary" style="min-height:28px;padding:2px 8px;font-size:0.7rem;" onclick="event.stopPropagation();applyTheme(\'' + t.id + '\');renderShop()">Activer</button></div>' :
       t.price === 0 ? '<div class="shop-card-price free">Gratuit</div>' :
       '<div class="shop-card-price">💎 ' + t.price + '</div>');
    if (!owned && t.price > 0) {
      card.onclick = () => {
        if (Economy.buyTheme(t.id, t.price)) {
          showToast(t.name + ' débloqué ! 🎨');
          renderShop();
        }
      };
    }
    grid.appendChild(card);
  });

  // Add more themes
  ['forest','sunset','ice','blood'].forEach(id => {
    const names = {forest:'Forest Spirit 🌿',sunset:'Sunset Duel 🌅',ice:'Ice Realm ❄️',blood:'Blood Moon 🔴'};
    const prices = {forest:150,sunset:200,ice:150,blood:250};
    const icons = {forest:'🌿',sunset:'🌅',ice:'❄️',blood:'🔴'};
    if (grid.querySelector('[data-theme="'+id+'"]')) return;
    const owned = Economy.ownsTheme(id);
    const active = Economy.data.selectedTheme === id;
    const card = document.createElement('div');
    card.className = 'shop-card' + (owned ? ' owned' : '');
    card.dataset.theme = id;
    card.innerHTML = '<div class="shop-card-icon">' + icons[id] + '</div>' +
      '<div class="shop-card-name">' + names[id] + '</div>' +
      (active ? '<div class="shop-card-price free">✓ Actif</div>' :
       owned ? '<div style="display:flex;gap:4px;justify-content:center;margin-top:4px;">' +
         '<button class="btn btn-ghost" style="min-height:28px;padding:2px 8px;font-size:0.7rem;" onclick="event.stopPropagation();previewTheme(\'' + id + '\')">Aperçu</button>' +
         '<button class="btn btn-primary" style="min-height:28px;padding:2px 8px;font-size:0.7rem;" onclick="event.stopPropagation();applyTheme(\'' + id + '\');renderShop()">Activer</button></div>' :
       '<div class="shop-card-price">💎 ' + prices[id] + '</div>');
    if (!owned) {
      card.onclick = () => {
        if (Economy.buyTheme(id, prices[id])) {
          showToast(names[id] + ' débloqué !');
          renderShop();
        }
      };
    }
    grid.appendChild(card);
  });
};

function previewTheme(id) {
  applyTheme(id);
  showToast('Aperçu : ' + id + ' — Retournez en boutique pour changer', 2000);
}


// ===== GACHA SYSTEM =====
const GACHA_ITEMS = {
  common: [
    {icon:'🐱',name:'Chat Ninja',type:'avatar'},{icon:'🦊',name:'Renard Mystique',type:'avatar'},
    {icon:'🐼',name:'Panda Sensei',type:'avatar'},{icon:'🐸',name:'Crapaud Sage',type:'avatar'},
    {icon:'🦉',name:'Hibou Oracle',type:'avatar'},{icon:'🐍',name:'Serpent Rusé',type:'avatar'},
    {icon:'⭐',name:'Cadre Étoiles',type:'frame'},{icon:'🔵',name:'Cadre Simple',type:'frame'},
  ],
  rare: [
    {icon:'🦅',name:'Aigle Doré',type:'avatar'},{icon:'🐉',name:'Dragon Éveillé',type:'avatar'},
    {icon:'🔥',name:'Cadre Flammes',type:'frame'},{icon:'⚡',name:'Cadre Électrique',type:'frame'},
    {icon:'🌸',name:'Cadre Fleurs',type:'frame'},{icon:'🏆',name:'Badge Champion',type:'badge'},
  ],
  epic: [
    {icon:'💀',name:'Avatar Shinigami',type:'avatar'},{icon:'🧙',name:'Avatar Sorcier',type:'avatar'},
    {icon:'🌈',name:'Cadre Arc-en-ciel',type:'frame'},{icon:'💎',name:'Cadre Cristaux',type:'frame'},
    {icon:'⚔️',name:'Titre: Le Guerrier',type:'title'},{icon:'🕵️',name:'Titre: L\'Infiltré',type:'title'},
  ],
  legendary: [
    {icon:'👑',name:'Avatar Le Dernier',type:'avatar'},{icon:'🌟',name:'Avatar Dieu Caché',type:'avatar'},
    {icon:'🖤',name:'Cadre Roi des Ombres',type:'frame'},{icon:'✨',name:'Cadre Céleste',type:'frame'},
    {icon:'🏅',name:'Titre: L\'Invincible',type:'title'},{icon:'💫',name:'Titre: Le Légendaire',type:'title'},
  ],
};

function initGacha() {
  if (!Economy._data.pityCount) Economy._data.pityCount = 0;
  if (!Economy._data.gachaCollection) Economy._data.gachaCollection = [];
  Economy.save();
}

function doGachaPull(count) {
  initGacha();
  const cost = count === 1 ? 100 : count === 10 ? 900 : 2500;
  if (!Economy.spendGems(cost)) { showToast('Pas assez de gemmes !'); return; }

  const results = [];
  for (let i = 0; i < count; i++) {
    let rarity;
    Economy._data.pityCount++;
    if (Economy._data.pityCount >= 90) {
      rarity = 'legendary'; Economy._data.pityCount = 0;
    } else if (Economy._data.pityCount >= 75) {
      // Soft pity
      const bonus = (Economy._data.pityCount - 75) * 0.02;
      rarity = Math.random() < (0.03 + bonus) ? 'legendary' : Math.random() < 0.12 ? 'epic' : Math.random() < 0.25 ? 'rare' : 'common';
    } else if (count >= 10 && i === count - 1 && !results.some(r => r.rarity === 'rare' || r.rarity === 'epic' || r.rarity === 'legendary')) {
      rarity = 'rare'; // Guaranteed rare on 10-pull
    } else if (count >= 30 && i === count - 1 && !results.some(r => r.rarity === 'legendary')) {
      rarity = 'legendary'; // Guaranteed legendary on 30-pull
    } else {
      const roll = Math.random();
      rarity = roll < 0.03 ? 'legendary' : roll < 0.15 ? 'epic' : roll < 0.40 ? 'rare' : 'common';
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
  renderGachaResults(results);
}

function renderGachaResults(results) {
  const container = document.getElementById('gacha-result');
  container.innerHTML = '';
  results.forEach((item, i) => {
    const card = document.createElement('div');
    card.className = 'gacha-card ' + item.rarity;
    card.style.animationDelay = (i * 0.1) + 's';
    card.innerHTML = '<div class="gi">' + item.icon + '</div><div>' + item.name + '</div>';
    container.appendChild(card);
  });
  updatePityDisplay();
  document.getElementById('gacha-gems').textContent = Economy.gems;
  SoundFX.reveal();
  if (results.some(r => r.rarity === 'legendary')) { SoundFX.victory(); spawnConfetti(40); }
}

function updatePityDisplay() {
  initGacha();
  const count = Economy._data.pityCount || 0;
  document.getElementById('pity-count').textContent = count;
  document.getElementById('pity-fill').style.width = (count / 90 * 100) + '%';
}

function renderGachaScreen() {
  const btns = document.getElementById('gacha-buttons');
  if (!btns) return;
  btns.innerHTML = '';
  [{n:1,cost:100,desc:'1 tirage'},{n:10,cost:900,desc:'10 tirages (1 rare garanti)'},{n:30,cost:2500,desc:'30 tirages (1 légendaire garanti)'}].forEach(opt => {
    const btn = document.createElement('div');
    btn.className = 'gacha-btn';
    btn.innerHTML = '<div class="price">💎 ' + opt.cost + '</div><div class="desc">' + opt.desc + '</div>';
    btn.onclick = () => doGachaPull(opt.n);
    btns.appendChild(btn);
  });
  document.getElementById('gacha-gems').textContent = Economy.gems;
  document.getElementById('gacha-result').innerHTML = '';
  updatePityDisplay();
}

// Patch showScreen for gacha
const _prevShowScreen5 = showScreen;
showScreen = function(id) {
  _prevShowScreen5(id);
  if (id === 'screen-gacha') renderGachaScreen();
  if (id === 'screen-rules') renderRules();
};


// ===== RULES =====
const RULES = [
  {emoji:'🃏', text:'Chaque joueur reçoit un <em>personnage secret</em>.'},
  {emoji:'🟦', text:'Les <em>Civils</em> ont tous le même personnage.'},
  {emoji:'🟥', text:'L\'<em>Undercover</em> a un personnage similaire mais différent.'},
  {emoji:'⬜', text:'<em>Mr. White</em> ne connaît pas son personnage.'},
  {emoji:'💬', text:'Tour par tour, donnez un <em>indice</em> sur votre personnage sans le nommer.'},
  {emoji:'🗳️', text:'<em>Votez</em> pour éliminer le joueur le plus suspect.'},
  {emoji:'🏆', text:'Les Civils gagnent en éliminant <em>tous les imposteurs</em>.'},
  {emoji:'🕵️', text:'L\'Undercover gagne en <em>restant caché</em> jusqu\'à la fin.'},
  {emoji:'👻', text:'Mr. White peut gagner en <em>devinant le mot civil</em> après élimination.'},
];

function renderRules() {
  const list = document.getElementById('rules-list');
  if (!list) return;
  list.innerHTML = '';
  RULES.forEach((r, i) => {
    const item = document.createElement('div');
    item.className = 'rule-item';
    item.style.animationDelay = (i * 0.08) + 's';
    item.innerHTML = '<div class="rule-num">' + r.emoji + '</div><div class="rule-text">' + r.text + '</div>';
    list.appendChild(item);
  });
}


// ===== LOFI MUSIC PLAYER =====
const LofiPlayer = (() => {
  let ctx = null, masterGain = null, currentOscs = [], trackIndex = 0, isPlaying = false;

  const tracks = [
    {name: 'Shibuya Nights', play: playShibuya},
    {name: 'Ninja Village', play: playNinja},
    {name: 'Sakura Rain', play: playSakuraRain},
    {name: 'Cyber Lounge', play: playCyber},
  ];

  function getCtx() {
    if (!ctx) { ctx = new (window.AudioContext || window.webkitAudioContext)(); masterGain = ctx.createGain(); masterGain.gain.value = MusicEngine.musicVolume; masterGain.connect(ctx.destination); }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function stopAll() { currentOscs.forEach(o => { try { o.stop(); } catch(e) {} }); currentOscs = []; isPlaying = false; }

  function note(freq, type, start, dur, vol, vibRate, vibDepth) {
    const c = getCtx();
    const osc = c.createOscillator(); const gain = c.createGain();
    osc.type = type; osc.frequency.value = freq;
    if (vibRate) { const lfo = c.createOscillator(); const lg = c.createGain(); lfo.frequency.value = vibRate; lg.gain.value = vibDepth||3; lfo.connect(lg); lg.connect(osc.frequency); lfo.start(start); lfo.stop(start+dur); }
    gain.gain.setValueAtTime(0,start); gain.gain.linearRampToValueAtTime(vol,start+0.03);
    gain.gain.setValueAtTime(vol,start+dur*0.6); gain.gain.exponentialRampToValueAtTime(0.001,start+dur);
    osc.connect(gain); gain.connect(masterGain); osc.start(start); osc.stop(start+dur+0.05);
    currentOscs.push(osc); return osc;
  }

  function playShibuya() {
    stopAll(); const c = getCtx(); const t = c.currentTime + 0.1;
    const melody = [330,392,440,523,440,392,330,294,330,392,440,523,587,523,440,392];
    melody.forEach((f,i) => { note(f,'triangle',t+i*0.5,0.45,0.06,5,3); note(f*0.5,'sine',t+i*0.5,0.5,0.02); });
    [131,165,196].forEach(f => note(f,'sine',t,melody.length*0.5,0.02));
    isPlaying = true;
  }

  function playNinja() {
    stopAll(); const c = getCtx(); const t = c.currentTime + 0.1;
    const penta = [294,330,392,440,523,440,392,330,294,262,294,330,392,523,440,330];
    penta.forEach((f,i) => { note(f,'triangle',t+i*0.55,0.5,0.05,6,5); });
    [147,175].forEach(f => note(f,'sine',t,penta.length*0.55,0.02,4,2));
    isPlaying = true;
  }

  function playSakuraRain() {
    stopAll(); const c = getCtx(); const t = c.currentTime + 0.1;
    const harp = [523,659,784,880,1047,880,784,659,523,440,523,659,784,1047,880,659];
    harp.forEach((f,i) => { note(f,'sine',t+i*0.45,0.6,0.04,0,0); });
    note(131,'sine',t,harp.length*0.45,0.02);
    isPlaying = true;
  }

  function playCyber() {
    stopAll(); const c = getCtx(); const t = c.currentTime + 0.1;
    const synth = [220,262,330,392,440,392,330,262,220,196,220,262,330,440,392,262];
    synth.forEach((f,i) => { note(f,'sawtooth',t+i*0.5,0.4,0.03); note(f*2,'sine',t+i*0.5,0.35,0.01); });
    note(55,'sawtooth',t,synth.length*0.5,0.02);
    isPlaying = true;
  }

  return {
    play() { tracks[trackIndex].play(); updateNowPlaying(); },
    stop() { stopAll(); updateNowPlaying(); },
    next() { trackIndex = (trackIndex + 1) % tracks.length; this.play(); },
    prev() { trackIndex = (trackIndex - 1 + tracks.length) % tracks.length; this.play(); },
    get currentName() { return tracks[trackIndex].name; },
    get playing() { return isPlaying; },
  };
})();

function updateNowPlaying() {
  const bar = document.getElementById('now-playing');
  const title = document.getElementById('np-title');
  if (!bar) return;
  if (LofiPlayer.playing && !GameState.gameActive) {
    bar.classList.add('visible');
    if (title) title.textContent = LofiPlayer.currentName;
  } else {
    bar.classList.remove('visible');
  }
}

function lofiNext() { SoundFX.click(); LofiPlayer.next(); }
function lofiPrev() { SoundFX.click(); LofiPlayer.prev(); }

// Auto-play lofi on splash (after first interaction)
document.addEventListener('click', () => {
  if (!LofiPlayer.playing && !GameState.gameActive) {
    try { LofiPlayer.play(); } catch(e) {}
  }
}, { once: true });
"""

html = html.replace("\n</script>", JS_V7 + "\n</script>")

# ═══════════════════════════════════════════════════════════
# 4. Update hint display to use pair.hint field from data
# ═══════════════════════════════════════════════════════════
html = html.replace(
    "function showHintForPair(pair) {\n  const hintBox = document.getElementById('hint-box');\n  const hintText = document.getElementById('hint-text');\n  if (!hintBox || !hintText || !pair) return;\n  const archetype = (pair.archetype || '').toLowerCase();\n  let hint = PAIR_HINTS[archetype];",
    "function showHintForPair(pair) {\n  const hintBox = document.getElementById('hint-box');\n  const hintText = document.getElementById('hint-text');\n  if (!hintBox || !hintText || !pair) return;\n  // Use pair's own hint if available\n  let hint = pair.hint;\n  if (!hint) { const archetype = (pair.archetype || '').toLowerCase(); hint = PAIR_HINTS[archetype]; }"
)

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V7 patch applied! Template: {len(html)//1024} KB")
