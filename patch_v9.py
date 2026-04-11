#!/usr/bin/env python3
"""V9 patch: Interactive gacha cards, looping music, shop tabs, new roles, levels, admin toggle."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS
# ═══════════════════════════════════════════════════════════
CSS_V9 = """
/* ===== V9 INTERACTIVE GACHA CARDS ===== */
.gacha-card-back {
  width:120px; height:170px; border-radius:16px; cursor:pointer;
  position:relative; perspective:800px; display:inline-flex;
  align-items:center; justify-content:center;
}
.gacha-card-inner {
  width:100%; height:100%; position:relative;
  transform-style:preserve-3d; transition:transform 0.6s cubic-bezier(0.22,1,0.36,1);
}
.gacha-card-back.flipped .gacha-card-inner { transform:rotateY(180deg); }
.gacha-card-front, .gacha-card-rear {
  position:absolute; top:0; left:0; width:100%; height:100%;
  backface-visibility:hidden; border-radius:16px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
}
.gacha-card-rear {
  background:linear-gradient(145deg,#1a1a2e,#0f0f1e);
  border:2px solid rgba(255,255,255,0.1);
  overflow:hidden;
}
.gacha-card-rear::before {
  content:''; position:absolute; width:200%; height:200%;
  background:repeating-conic-gradient(rgba(255,255,255,0.02) 0deg,transparent 15deg,rgba(255,255,255,0.01) 30deg);
  animation:cardShine 8s linear infinite;
}
.gacha-card-rear .card-logo { font-size:2.5rem; z-index:1; opacity:0.4; }
.gacha-card-front { transform:rotateY(180deg); padding:12px 8px; text-align:center; gap:4px; }
.gacha-card-front.common { background:linear-gradient(145deg,#374151,#1f2937); border:2px solid #6b7280; }
.gacha-card-front.rare { background:linear-gradient(145deg,#1e3a5f,#0f1f3d); border:2px solid #3b82f6; box-shadow:0 0 15px rgba(59,130,246,0.3); }
.gacha-card-front.epic { background:linear-gradient(145deg,#3b1f5f,#581c87); border:2px solid #a855f7; box-shadow:0 0 20px rgba(168,85,247,0.4); }
.gacha-card-front.legendary { background:linear-gradient(145deg,#92400e,#78350f); border:2px solid #f59e0b;
  box-shadow:0 0 30px rgba(245,158,11,0.5); }
.gacha-card-front .gcf-icon { font-size:2.8rem; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.4)); }
.gacha-card-front .gcf-name { font-size:0.7rem; font-weight:600; color:var(--text-bright); margin-top:4px; }
.gacha-card-front .gcf-stars { color:#f59e0b; font-size:0.55rem; letter-spacing:1px; }
.gacha-card-front.legendary .gcf-tag {
  position:absolute; top:6px; font-size:0.5rem; font-weight:800; color:#ffd700;
  text-transform:uppercase; letter-spacing:2px; text-shadow:0 0 10px rgba(255,215,0,0.5);
}
.gacha-card-back.float { animation:cardFloat 2s ease-in-out infinite; }
@keyframes cardFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }

.gacha-tap-hint {
  font-size:0.8rem; color:var(--accent-gold); animation:blink 1.2s ease infinite; margin-top:12px;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.gacha-cards-grid {
  display:flex; flex-wrap:wrap; gap:8px; justify-content:center; max-width:500px;
}
.gacha-reveal-all { margin-top:10px; }

/* Particle burst */
.gacha-burst { position:absolute; pointer-events:none; }
.gacha-particle {
  position:absolute; width:6px; height:6px; border-radius:50%;
  animation:burstOut 0.8s ease-out forwards;
}
@keyframes burstOut { 0%{transform:translate(0,0) scale(1);opacity:1} 100%{transform:translate(var(--dx),var(--dy)) scale(0);opacity:0} }

/* ===== V9 SHOP TABS ===== */
.shop-tabs {
  display:flex; gap:2px; width:100%; max-width:600px;
  overflow-x:auto; -webkit-overflow-scrolling:touch;
  margin-bottom:14px; padding:2px 0;
}
.shop-tab {
  flex-shrink:0; padding:8px 14px; border-radius:var(--radius-sm);
  font-size:0.75rem; font-weight:600; background:var(--bg-card);
  border:1px solid transparent; cursor:pointer; color:var(--text-muted);
  transition:all 0.2s; white-space:nowrap;
}
.shop-tab.active { border-color:var(--accent-gold); color:var(--accent-gold); background:rgba(245,166,35,0.08); }
.shop-tab-content { display:none; width:100%; max-width:600px; }
.shop-tab-content.active { display:block; }

/* ===== V9 NEW ROLES ===== */
.role-card-ghost { background:linear-gradient(145deg,#1f1f3d,#0f0f2e) !important; border-color:#9ca3af !important; }
.role-card-detective { background:linear-gradient(145deg,#1f3d1f,#0f2e0f) !important; border-color:#22c55e !important; }
.role-card-traitor { background:linear-gradient(145deg,#3d1f1f,#2e0f0f) !important; border-color:#dc2626 !important; }
.role-card-oracle { background:linear-gradient(145deg,#3d3d1f,#2e2e0f) !important; border-color:#f59e0b !important; }

.role-toggle { display:flex; align-items:center; gap:10px; padding:10px; border-radius:var(--radius-sm);
  background:var(--bg-card); margin-bottom:6px; }
.role-toggle .rt-icon { font-size:1.5rem; }
.role-toggle .rt-info { flex:1; }
.role-toggle .rt-name { font-weight:600; font-size:0.85rem; color:var(--text-bright); }
.role-toggle .rt-desc { font-size:0.7rem; color:var(--text-muted); }
.role-toggle .rt-level { font-size:0.65rem; color:var(--accent-gold); }
.role-toggle-btn {
  width:44px; height:24px; border-radius:12px; border:none; cursor:pointer;
  background:#374151; position:relative; transition:background 0.2s;
}
.role-toggle-btn.on { background:var(--accent-green); }
.role-toggle-btn::after {
  content:''; position:absolute; top:2px; left:2px; width:20px; height:20px;
  border-radius:50%; background:#fff; transition:left 0.2s;
}
.role-toggle-btn.on::after { left:22px; }
.role-toggle.locked { opacity:0.4; }

/* ===== V9 LEVEL UP ANIMATION ===== */
.level-up-overlay {
  position:fixed; top:0; left:0; width:100%; height:100%; z-index:650;
  background:rgba(0,0,0,0.85); display:flex; align-items:center; justify-content:center;
  flex-direction:column; gap:12px; opacity:0; pointer-events:none; transition:opacity 0.3s;
}
.level-up-overlay.visible { opacity:1; pointer-events:auto; }
.level-up-number { font-family:var(--font-display); font-size:5rem; font-weight:900;
  background:linear-gradient(135deg,#f59e0b,#fbbf24); -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; animation:levelBounce 0.6s cubic-bezier(0.22,1,0.36,1); }
@keyframes levelBounce { 0%{transform:scale(0);} 60%{transform:scale(1.2);} 100%{transform:scale(1);} }
.level-up-label { font-size:1.2rem; color:var(--accent-gold); font-weight:700; }
.level-up-reward { font-size:0.85rem; color:var(--text-muted); }

/* ===== V9 ADMIN PANEL ===== */
.admin-panel { background:rgba(245,166,35,0.05); border:1px solid rgba(245,166,35,0.15);
  border-radius:var(--radius-md); padding:14px; margin-top:12px; }
.admin-panel h4 { font-size:0.85rem; color:var(--accent-gold); margin-bottom:8px; display:flex; align-items:center; gap:6px; }
.admin-actions { display:flex; flex-wrap:wrap; gap:6px; }
.admin-btn { padding:6px 12px; border-radius:var(--radius-sm); font-size:0.75rem; font-weight:600;
  background:var(--bg-card); border:1px solid var(--border-glass); cursor:pointer;
  color:var(--text-primary); transition:all 0.2s; }
.admin-btn:hover { border-color:var(--accent-gold); }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_V9 + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML: Level up overlay, role settings, admin panel
# ═══════════════════════════════════════════════════════════

# Add level-up overlay before toast
html = html.replace(
    '<!-- ===== TOAST ===== -->',
    '<!-- ===== LEVEL UP OVERLAY ===== -->\n'
    '<div class="level-up-overlay" id="level-up-overlay">\n'
    '  <div class="level-up-label">NIVEAU SUPÉRIEUR</div>\n'
    '  <div class="level-up-number" id="level-up-number">0</div>\n'
    '  <div class="level-up-reward" id="level-up-reward"></div>\n'
    '  <button class="btn btn-primary" onclick="closeLevelUp()">Continuer</button>\n'
    '</div>\n\n'
    '<!-- ===== TOAST ===== -->'
)

# Add roles section + admin panel to settings (find blind toggle area)
html = html.replace(
    '<div class="settings-group" style="margin-top:14px;">\n'
    '        <label class="settings-label">🔑 Code Admin</label>',
    '<div class="settings-group" style="margin-top:14px;">\n'
    '        <label class="settings-label">🎭 Rôles additionnels</label>\n'
    '        <div id="roles-toggles"></div>\n'
    '      </div>\n'
    '      <div class="settings-group" style="margin-top:14px;">\n'
    '        <label class="settings-label">🔑 Code Admin</label>'
)

# Add admin panel after admin code input
html = html.replace(
    '<button class="btn btn-ghost" onclick="checkAdminCode()" style="min-height:36px;padding:6px 12px;">Valider</button>\n'
    '        </div>\n'
    '      </div>',
    '<button class="btn btn-ghost" onclick="checkAdminCode()" style="min-height:36px;padding:6px 12px;">Valider</button>\n'
    '        </div>\n'
    '        <div class="admin-panel" id="admin-panel" style="display:none;">\n'
    '          <h4>👑 Admin actif</h4>\n'
    '          <div class="admin-actions">\n'
    '            <button class="admin-btn" onclick="adminResetData()">Reset données</button>\n'
    '            <button class="admin-btn" onclick="adminForceGold()">Prochain = Légendaire</button>\n'
    '            <button class="admin-btn" onclick="Economy.addGems(1000);showToast(\'+1000💎\')">+1000💎</button>\n'
    '            <button class="admin-btn" onclick="adminToggle()">Désactiver Admin</button>\n'
    '          </div>\n'
    '        </div>\n'
    '      </div>'
)

# ═══════════════════════════════════════════════════════════
# 3. JAVASCRIPT
# ═══════════════════════════════════════════════════════════
JS_V9 = r"""

// ===== V9 INTERACTIVE GACHA =====
let gachaResults = [];
let gachaRevealed = new Set();

function doGenshinPull(count) {
  initGacha();
  const isAdmin = Economy._data.isAdmin;
  const cost = isAdmin ? 0 : (count === 1 ? 100 : 900);
  if (!isAdmin && !Economy.spendGems(cost)) { showToast('Pas assez de gemmes !'); return; }

  const epicBoost = selectedBanner === 'event' ? 0.24 : 0.12;
  const forceGold = Economy._data.forceNextLegendary;

  gachaResults = [];
  gachaRevealed = new Set();

  for (let i = 0; i < count; i++) {
    let rarity;
    Economy._data.pityCount = (Economy._data.pityCount || 0) + 1;
    const pity = Economy._data.pityCount;

    if (forceGold && i === 0) {
      rarity = 'legendary'; Economy._data.pityCount = 0; Economy._data.forceNextLegendary = false;
    } else if (pity >= 90) { rarity = 'legendary'; Economy._data.pityCount = 0; }
    else if (pity >= 75) {
      rarity = Math.random() < (0.03 + (pity-75)*0.02) ? 'legendary' : Math.random() < epicBoost ? 'epic' : Math.random() < 0.4 ? 'rare' : 'common';
    } else if (count >= 10 && i === count-1 && !gachaResults.some(r => r.rarity !== 'common')) {
      rarity = 'rare';
    } else {
      const roll = Math.random();
      rarity = roll < 0.03 ? 'legendary' : roll < 0.03+epicBoost ? 'epic' : roll < 0.40 ? 'rare' : 'common';
    }
    if (rarity === 'legendary') Economy._data.pityCount = 0;

    const pool = GACHA_ITEMS[rarity];
    const item = pool[Math.floor(Math.random() * pool.length)];
    gachaResults.push({...item, rarity});
    if (!Economy._data.gachaCollection.find(c => c.name === item.name)) {
      Economy._data.gachaCollection.push({...item, rarity});
    }
  }
  Economy.save();
  showInteractiveCards();
}

function showInteractiveCards() {
  const overlay = document.getElementById('gacha-pull-overlay');
  const content = document.getElementById('gacha-pull-content');
  const best = gachaResults.reduce((a,b) => ({common:0,rare:1,epic:2,legendary:3})[a.rarity] > ({common:0,rare:1,epic:2,legendary:3})[b.rarity] ? a : b);
  overlay.className = 'gacha-pull-overlay visible rarity-' + best.rarity;

  let cardsHtml = '<div class="gacha-cards-grid">';
  gachaResults.forEach((r, i) => {
    const stars = r.rarity === 'legendary' ? '★★★★★' : r.rarity === 'epic' ? '★★★★★' : r.rarity === 'rare' ? '★★★★' : '★★★';
    cardsHtml += '<div class="gacha-card-back float" id="gcard-' + i + '" onclick="revealGachaCard(' + i + ')">' +
      '<div class="gacha-card-inner">' +
      '<div class="gacha-card-rear"><span class="card-logo">🎴</span></div>' +
      '<div class="gacha-card-front ' + r.rarity + '">' +
      (r.rarity === 'legendary' ? '<div class="gcf-tag">LÉGENDAIRE</div>' : '') +
      '<div class="gcf-icon">' + r.icon + '</div>' +
      '<div class="gcf-name">' + r.name + '</div>' +
      '<div class="gcf-stars">' + stars + '</div>' +
      '</div></div></div>';
  });
  cardsHtml += '</div>';
  cardsHtml += '<div class="gacha-tap-hint" id="gacha-tap-hint">' + (gachaResults.length === 1 ? 'APPUYEZ POUR RÉVÉLER' : 'APPUYEZ SUR CHAQUE CARTE') + '</div>';
  if (gachaResults.length > 1) {
    cardsHtml += '<button class="btn btn-ghost gacha-reveal-all" onclick="revealAllGachaCards()">Tout révéler</button>';
  }

  content.innerHTML = cardsHtml;
  // Remove the default continue button - we'll show it after all revealed
  const continueBtn = overlay.querySelector('.btn-primary');
  if (continueBtn) continueBtn.style.display = 'none';

  SoundFX.suspense();
}

function revealGachaCard(index) {
  if (gachaRevealed.has(index)) return;
  gachaRevealed.add(index);
  const card = document.getElementById('gcard-' + index);
  if (!card) return;
  card.classList.remove('float');
  card.classList.add('flipped');

  // Particle burst
  const r = gachaResults[index];
  spawnCardBurst(card, r.rarity);

  if (r.rarity === 'legendary') { SoundFX.victory(); haptic('heavy'); }
  else if (r.rarity === 'epic') { SoundFX.reveal(); haptic('medium'); }
  else { SoundFX.click(); haptic('light'); }

  // Check if all revealed
  if (gachaRevealed.size >= gachaResults.length) {
    document.getElementById('gacha-tap-hint').style.display = 'none';
    const overlay = document.getElementById('gacha-pull-overlay');
    const btn = overlay.querySelector('.btn-primary');
    if (btn) { btn.style.display = 'inline-flex'; btn.style.marginTop = '12px'; }
    updatePityDisplay();
    document.getElementById('gacha-gems').textContent = Economy.gems;
  }
}

function revealAllGachaCards() {
  gachaResults.forEach((_, i) => {
    setTimeout(() => revealGachaCard(i), i * 150);
  });
}

function spawnCardBurst(el, rarity) {
  const colors = {common:'#9ca3af',rare:'#3b82f6',epic:'#a855f7',legendary:'#f59e0b'};
  const color = colors[rarity] || '#fff';
  const rect = el.getBoundingClientRect();
  const cx = rect.left + rect.width/2;
  const cy = rect.top + rect.height/2;
  for (let i = 0; i < (rarity === 'legendary' ? 20 : 10); i++) {
    const p = document.createElement('div');
    p.className = 'gacha-particle';
    p.style.position = 'fixed';
    p.style.left = cx + 'px';
    p.style.top = cy + 'px';
    p.style.background = color;
    p.style.zIndex = '800';
    const angle = (Math.PI * 2 / (rarity === 'legendary' ? 20 : 10)) * i;
    const dist = 40 + Math.random() * 60;
    p.style.setProperty('--dx', Math.cos(angle) * dist + 'px');
    p.style.setProperty('--dy', Math.sin(angle) * dist + 'px');
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 900);
  }
}


// ===== V9 SHOP WITH TABS =====
const _origRenderShopV9 = renderShop;
renderShop = function() {
  _origRenderShopV9();

  // Wrap existing sections in tab system
  const shopScreen = document.getElementById('screen-shop');
  if (!shopScreen || shopScreen.querySelector('.shop-tabs')) return;

  // Collect all shop sections
  const sections = shopScreen.querySelectorAll('.shop-section');
  const dailyDeal = shopScreen.querySelector('.daily-deal');

  // Create tabs
  const tabBar = document.createElement('div');
  tabBar.className = 'shop-tabs';
  const tabNames = ['🎮 Modes','🎨 Thèmes','👤 Avatars','🖼️ Cadres','🎰 Gacha','📦 Packs'];

  tabNames.forEach((name, i) => {
    const tab = document.createElement('div');
    tab.className = 'shop-tab' + (i === 0 ? ' active' : '');
    tab.textContent = name;
    tab.dataset.tab = i;
    tab.onclick = () => {
      tabBar.querySelectorAll('.shop-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      sections.forEach((s, j) => s.style.display = j === i ? 'block' : 'none');
      if (dailyDeal) dailyDeal.style.display = i === 0 ? 'block' : 'none';
      SoundFX.click();
    };
    tabBar.appendChild(tab);
  });

  // Insert tabs after gems display
  const gemsDisplay = shopScreen.querySelector('.gems-display');
  if (gemsDisplay && gemsDisplay.nextSibling) {
    gemsDisplay.parentNode.insertBefore(tabBar, gemsDisplay.nextSibling);
  }

  // Hide all sections except first
  sections.forEach((s, i) => { if (i > 0) s.style.display = 'none'; });
};


// ===== V9 NEW ROLES =====
const EXTRA_ROLES = [
  {id:'ghost', icon:'👻', name:'Fantôme', desc:'Connaît les deux mots, aide les civils discrètement', level:21, color:'#9ca3af'},
  {id:'detective', icon:'🕵️', name:'Détective', desc:'Peut poser une question oui/non par manche', level:31, color:'#22c55e'},
  {id:'traitor', icon:'🗡️', name:'Traître', desc:'Civil qui gagne avec les Undercovers', level:1, color:'#dc2626'},
  {id:'oracle', icon:'🔮', name:'Oracle', desc:'Peut voir le rôle d\'un joueur avant le jeu', level:1, color:'#f59e0b'},
];

GameState.enabledRoles = {ghost:false, detective:false, traitor:false, oracle:false};

function renderRoleToggles() {
  const container = document.getElementById('roles-toggles');
  if (!container) return;
  container.innerHTML = '';
  const playerLevel = Economy?.data?.level || 1;

  EXTRA_ROLES.forEach(role => {
    const locked = playerLevel < role.level;
    const enabled = GameState.enabledRoles[role.id] && !locked;
    const div = document.createElement('div');
    div.className = 'role-toggle' + (locked ? ' locked' : '');
    div.innerHTML = '<div class="rt-icon">' + role.icon + '</div>' +
      '<div class="rt-info"><div class="rt-name">' + role.name + '</div>' +
      '<div class="rt-desc">' + role.desc + '</div>' +
      (locked ? '<div class="rt-level">🔒 Niveau ' + role.level + ' requis</div>' : '') +
      '</div>' +
      '<button class="role-toggle-btn' + (enabled ? ' on' : '') + '"' +
      (locked ? ' disabled' : '') +
      ' onclick="toggleRole(\'' + role.id + '\',this)"></button>';
    container.appendChild(div);
  });
}

function toggleRole(id, btn) {
  GameState.enabledRoles[id] = !GameState.enabledRoles[id];
  btn.classList.toggle('on', GameState.enabledRoles[id]);
  SoundFX.click();
}

// Render roles on settings screen
const _origRenderSettings2 = renderSettings;
renderSettings = function() {
  _origRenderSettings2();
  renderRoleToggles();
  // Show/hide admin panel
  const panel = document.getElementById('admin-panel');
  if (panel) panel.style.display = Economy?._data?.isAdmin ? 'block' : 'none';
};


// ===== V9 LEVEL UP SYSTEM =====
const LEVEL_TITLES = {
  1:'Rookie', 6:'Initié', 11:'Chasseur', 21:'Expert', 31:'Maître', 51:'Légende'
};

function getLevelTitle(level) {
  let title = 'Rookie';
  Object.entries(LEVEL_TITLES).forEach(([lv, t]) => { if (level >= parseInt(lv)) title = t; });
  return title;
}

function showLevelUpAnimation(newLevel) {
  const overlay = document.getElementById('level-up-overlay');
  document.getElementById('level-up-number').textContent = newLevel;
  const title = getLevelTitle(newLevel);
  let reward = title;
  if (newLevel === 6) reward += ' — +5% gemmes/partie';
  if (newLevel === 11) reward += ' — Mode Tournoi débloqué';
  if (newLevel === 21) reward += ' — Rôle Fantôme débloqué';
  if (newLevel === 31) reward += ' — Rôle Détective débloqué';
  if (newLevel === 51) reward += ' — Avatar Légendaire offert !';
  document.getElementById('level-up-reward').textContent = reward;
  overlay.classList.add('visible');
  SoundFX.victory();
  spawnConfetti(40);
}

function closeLevelUp() {
  document.getElementById('level-up-overlay').classList.remove('visible');
}

// Override Economy.addXP to trigger level-up animation
const _origAddXP = Economy.addXP.bind(Economy);
Economy.addXP = function(n) {
  const oldLevel = this._data.level;
  this._data.xp += n;
  const needed = this._data.level * 100;
  let leveledUp = false;
  while (this._data.xp >= this._data.level * 100) {
    this._data.xp -= this._data.level * 100;
    this._data.level++;
    leveledUp = true;
  }
  this.save();
  if (leveledUp && this._data.level > oldLevel) {
    setTimeout(() => showLevelUpAnimation(this._data.level), 500);
  }
  return leveledUp;
};


// ===== V9 ADMIN TOGGLE & PANEL =====
function adminToggle() {
  Economy._data.isAdmin = false;
  Economy.save();
  showToast('Admin désactivé');
  renderSettings();
}

function adminResetData() {
  showConfirm('Reset complet ?', 'Toutes les données seront effacées.', () => {
    localStorage.clear();
    localStorage.setItem('uc_tutorial_done', 'true');
    location.reload();
  });
}

function adminForceGold() {
  Economy._data.forceNextLegendary = true;
  Economy.save();
  showToast('Prochain tirage = Légendaire garanti ⭐');
}


// ===== V9 IMPROVED LOOPING MUSIC =====
// Override LofiPlayer to implement proper looping with longer compositions
const LofiPlayerV9 = (() => {
  let ctx = null, masterGain = null, currentOscs = [], trackIndex = 0, isPlaying = false;
  let loopTimer = null;

  const TRACKS = [
    {name:'Shibuya Nights', emoji:'🌃'},
    {name:'Ninja Village', emoji:'🏯'},
    {name:'Sakura Rain', emoji:'🌸'},
    {name:'Cyber Lounge', emoji:'⚡'},
    {name:'Tokyo Drift', emoji:'🚗'},
    {name:'Ronin Path', emoji:'⚔️'},
    {name:'Neon Arcade', emoji:'🕹️'},
    {name:'Cherry Blossom', emoji:'🌺'},
  ];

  function getCtx() {
    if (!ctx) { ctx = new (window.AudioContext || window.webkitAudioContext)(); masterGain = ctx.createGain(); masterGain.gain.value = MusicEngine.musicVolume; masterGain.connect(ctx.destination); }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function stopAll() {
    currentOscs.forEach(o => { try{o.stop()}catch(e){} }); currentOscs = [];
    if (loopTimer) { clearTimeout(loopTimer); loopTimer = null; }
    isPlaying = false;
  }

  function n(freq, type, start, dur, vol) {
    const c = getCtx(); const osc = c.createOscillator(); const gain = c.createGain();
    osc.type = type; osc.frequency.value = freq;
    gain.gain.setValueAtTime(0, start); gain.gain.linearRampToValueAtTime(vol, start+0.02);
    gain.gain.setValueAtTime(vol, start+dur*0.7); gain.gain.exponentialRampToValueAtTime(0.001, start+dur);
    osc.connect(gain); gain.connect(masterGain); osc.start(start); osc.stop(start+dur+0.05);
    currentOscs.push(osc);
  }

  // Generate a pentatonic melody phrase (8 notes, varied each time)
  function genMelody(root, scale, count) {
    const notes = [];
    let prev = Math.floor(scale.length / 2);
    for (let i = 0; i < count; i++) {
      const step = Math.floor(Math.random() * 3) - 1; // -1, 0, +1
      prev = Math.max(0, Math.min(scale.length - 1, prev + step));
      notes.push(root * scale[prev]);
    }
    return notes;
  }

  function playTrack(idx) {
    stopAll();
    const c = getCtx(); const t = c.currentTime + 0.1;
    const penta = [1, 9/8, 5/4, 3/2, 5/3]; // major pentatonic ratios
    const minor = [1, 9/8, 6/5, 3/2, 8/5]; // minor pentatonic
    const roots = [131, 147, 165, 175, 196, 220, 247, 262];
    const root = roots[idx % roots.length];
    const scale = idx % 2 === 0 ? penta : minor;
    const beatDur = 0.45 + (idx % 3) * 0.05;
    const totalBars = 4; // 4 bars of 8 notes = 32 notes
    const totalNotes = totalBars * 8;
    const totalDuration = totalNotes * beatDur;

    // Pad chord (sustained)
    [1, 5/4, 3/2].forEach(r => { n(root * r * 0.5, 'sine', t, totalDuration, 0.015); });

    // Bass
    for (let bar = 0; bar < totalBars; bar++) {
      const bassNote = root * 0.5 * scale[Math.floor(Math.random() * 3)];
      n(bassNote, 'sine', t + bar * 8 * beatDur, 8 * beatDur * 0.9, 0.02);
    }

    // Melody (varied each loop)
    const melody = genMelody(root, scale, totalNotes);
    melody.forEach((freq, i) => {
      const type = idx < 4 ? 'triangle' : 'sine';
      n(freq, type, t + i * beatDur, beatDur * 0.8, 0.05);
    });

    // Schedule loop with variation
    isPlaying = true;
    loopTimer = setTimeout(() => {
      if (isPlaying) playTrack(idx);
    }, totalDuration * 1000);
  }

  return {
    play() { playTrack(trackIndex); updateMiniTitle(); },
    stop() { stopAll(); updateMiniTitle(); },
    next() { trackIndex = (trackIndex + 1) % TRACKS.length; if (isPlaying) this.play(); else { trackIndex = (trackIndex) % TRACKS.length; } updateMiniTitle(); },
    prev() { trackIndex = (trackIndex - 1 + TRACKS.length) % TRACKS.length; if (isPlaying) this.play(); updateMiniTitle(); },
    get currentName() { return TRACKS[trackIndex].name; },
    get currentEmoji() { return TRACKS[trackIndex].emoji; },
    get playing() { return isPlaying; },
  };
})();

// Replace old LofiPlayer
Object.keys(LofiPlayerV9).forEach(k => { LofiPlayer[k] = LofiPlayerV9[k]; });
if (typeof LofiPlayer.play !== 'function') {
  // Fallback: assign methods
  LofiPlayer.play = LofiPlayerV9.play;
  LofiPlayer.stop = LofiPlayerV9.stop;
  LofiPlayer.next = LofiPlayerV9.next;
  LofiPlayer.prev = LofiPlayerV9.prev;
}


// ===== V9 PSEUDO CHANGE IN PROFILE =====
function renderProfileV9() {
  renderProfile();
  const nameEl = document.getElementById('profile-name');
  if (nameEl && !nameEl.dataset.editable) {
    nameEl.dataset.editable = 'true';
    nameEl.style.cursor = 'pointer';
    nameEl.title = 'Cliquer pour changer';
    nameEl.onclick = () => {
      const current = Economy._data.pseudo || 'Joueur';
      const input = document.createElement('input');
      input.type = 'text'; input.value = current;
      input.style.cssText = 'background:var(--bg-card);border:1px solid var(--border-glass);border-radius:8px;padding:6px 10px;color:var(--text-bright);font-size:1.1rem;text-align:center;width:150px;';
      input.onblur = () => {
        Economy._data.pseudo = input.value || 'Joueur';
        Economy.save();
        nameEl.textContent = Economy._data.pseudo;
      };
      input.onkeydown = (e) => { if (e.key === 'Enter') input.blur(); };
      nameEl.textContent = '';
      nameEl.appendChild(input);
      input.focus();
    };
    nameEl.textContent = Economy._data?.pseudo || 'Joueur';
  }

  // Show avatar
  const avatarEl = document.getElementById('profile-avatar');
  if (avatarEl) {
    const eq = getEquipped();
    avatarEl.textContent = eq.avatar;
    const frame = ALL_FRAMES.find(f => f.id === eq.frame);
    avatarEl.className = 'profile-avatar ' + (frame ? frame.cls : '');
  }
}

// Patch profile render
const _prevShowScreen7 = showScreen;
showScreen = function(id) {
  _prevShowScreen7(id);
  if (id === 'screen-profile') renderProfileV9();
};
"""

html = html.replace("\n</script>", JS_V9 + "\n</script>")

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V9 patch applied! Template: {len(html)//1024} KB")
