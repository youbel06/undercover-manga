#!/usr/bin/env python3
"""V6 patch: Shop, gems, profile, bottom nav, mode filtering fix, rewards."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS for shop, profile, gems, bottom nav, rewards
# ═══════════════════════════════════════════════════════════
CSS_V6 = """
/* ===== V6 BOTTOM NAV ===== */
.bottom-nav {
  position: fixed; bottom: 0; left: 0; width: 100%;
  background: var(--bg-secondary); border-top: 1px solid var(--border-glass);
  display: flex; z-index: 350; padding-bottom: env(safe-area-inset-bottom, 0);
  backdrop-filter: blur(15px);
}
.bottom-nav.hidden { display: none; }
.nav-item {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  gap: 2px; padding: 8px 4px; cursor: pointer;
  color: var(--text-dim); font-size: 0.65rem; transition: color 0.2s;
  background: none; border: none;
}
.nav-item.active { color: var(--accent-gold); }
.nav-item:hover { color: var(--text-primary); }
.nav-icon { font-size: 1.2rem; }

/* Pad screens for bottom nav */
.screen { padding-bottom: calc(env(safe-area-inset-bottom, 0px) + 70px) !important; }

/* ===== GEMS DISPLAY ===== */
.gems-display {
  display: inline-flex; align-items: center; gap: 5px;
  background: linear-gradient(135deg, rgba(245,166,35,0.15), rgba(245,166,35,0.05));
  border: 1px solid rgba(245,166,35,0.2);
  border-radius: 20px; padding: 5px 12px;
  font-size: 0.85rem; font-weight: 700; color: var(--accent-gold);
}
.gems-display .gem-icon { font-size: 1rem; }

/* ===== SHOP SCREEN ===== */
#screen-shop { padding-top: 60px; }
.shop-section { width: 100%; max-width: 600px; margin-bottom: 24px; }
.shop-section-title {
  font-family: var(--font-display); font-size: 1.1rem; font-weight: 700;
  margin-bottom: 10px; color: var(--text-bright);
  display: flex; align-items: center; gap: 8px;
}
.shop-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
}
.shop-card {
  background: var(--bg-card); border: 1px solid var(--border-glass);
  border-radius: var(--radius-lg); padding: 16px 12px;
  text-align: center; position: relative; transition: all 0.2s;
  cursor: pointer;
}
.shop-card:hover { border-color: var(--accent-gold); transform: translateY(-2px); }
.shop-card.owned { border-color: var(--accent-green); opacity: 0.7; }
.shop-card.owned::after {
  content: '✓'; position: absolute; top: 8px; right: 8px;
  background: var(--accent-green); color: #fff; width: 20px; height: 20px;
  border-radius: 50%; font-size: 0.7rem;
  display: flex; align-items: center; justify-content: center;
}
.shop-badge {
  position: absolute; top: -6px; left: 50%; transform: translateX(-50%);
  padding: 2px 8px; border-radius: 8px; font-size: 0.6rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.5px;
}
.shop-badge.popular { background: var(--accent-undercover); color: #fff; }
.shop-badge.new { background: var(--accent-green); color: #fff; }
.shop-card-icon { font-size: 2rem; margin-bottom: 6px; }
.shop-card-name { font-size: 0.85rem; font-weight: 600; color: var(--text-bright); margin-bottom: 4px; }
.shop-card-price {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 0.8rem; font-weight: 700; color: var(--accent-gold);
}
.shop-card-price.free { color: var(--accent-green); }
.shop-card-original {
  font-size: 0.7rem; color: var(--text-dim); text-decoration: line-through;
  margin-right: 4px;
}

/* Daily deal */
.daily-deal {
  background: linear-gradient(135deg, rgba(233,69,96,0.1), rgba(245,166,35,0.1));
  border: 1px solid rgba(233,69,96,0.3);
  border-radius: var(--radius-lg); padding: 16px;
  margin-bottom: 16px; text-align: center;
}
.deal-timer { font-size: 0.75rem; color: var(--accent-undercover); margin-top: 6px; }

/* ===== PROFILE SCREEN ===== */
#screen-profile { padding-top: 60px; }
.profile-header {
  text-align: center; margin-bottom: 20px;
}
.profile-avatar {
  width: 80px; height: 80px; border-radius: 50%;
  margin: 0 auto 10px; display: flex; align-items: center; justify-content: center;
  font-size: 2rem; border: 3px solid var(--accent-gold);
  background: linear-gradient(135deg, var(--accent-civil), var(--accent-undercover));
}
.profile-avatar.frame-champion { border-color: #FFD700; box-shadow: 0 0 20px rgba(255,215,0,0.3); }
.profile-avatar.frame-undercover { border-color: var(--accent-undercover); box-shadow: 0 0 20px rgba(233,69,96,0.3); }

.profile-level {
  font-size: 0.8rem; color: var(--text-muted); margin-bottom: 8px;
}
.xp-bar {
  width: 200px; height: 8px; background: rgba(255,255,255,0.1);
  border-radius: 4px; margin: 0 auto 16px; overflow: hidden;
}
.xp-fill {
  height: 100%; background: linear-gradient(90deg, var(--accent-gold), var(--accent-gold-light));
  border-radius: 4px; transition: width 0.5s ease;
}

.stats-grid {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 8px; max-width: 400px; width: 100%; margin: 0 auto 20px;
}
.stat-card {
  background: var(--bg-card); border-radius: var(--radius-md);
  padding: 12px; text-align: center;
}
.stat-value { font-size: 1.4rem; font-weight: 800; color: var(--text-bright); }
.stat-label { font-size: 0.7rem; color: var(--text-muted); }

/* ===== REWARD OVERLAY ===== */
.reward-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.85); z-index: 550;
  display: flex; align-items: center; justify-content: center;
  flex-direction: column; gap: 16px;
  opacity: 0; pointer-events: none; transition: opacity 0.3s;
}
.reward-overlay.visible { opacity: 1; pointer-events: auto; }
.reward-chest {
  font-size: 4rem; animation: chestBounce 0.6s ease;
}
@keyframes chestBounce {
  0% { transform: scale(0) rotate(-20deg); }
  60% { transform: scale(1.2) rotate(5deg); }
  100% { transform: scale(1) rotate(0); }
}
.reward-gems {
  font-size: 1.8rem; font-weight: 800; color: var(--accent-gold);
  animation: fadeInUp 0.5s ease 0.5s both;
}
.reward-xp {
  font-size: 1rem; color: var(--text-muted);
  animation: fadeInUp 0.5s ease 0.7s both;
}
.reward-level-up {
  font-size: 1.2rem; font-weight: 700; color: var(--accent-green);
  animation: fadeInUp 0.5s ease 0.9s both;
}

/* ===== SOCIAL PROOF BANNER ===== */
.social-proof {
  font-size: 0.7rem; color: var(--text-dim);
  display: flex; align-items: center; gap: 6px;
  animation: fadeIn 1s ease 2s both;
}
.social-proof .pulse-dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--accent-green);
  animation: pulse 1.5s ease infinite;
}
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_V6 + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML: Bottom nav, shop, profile, rewards overlay
# ═══════════════════════════════════════════════════════════

# Add bottom nav AFTER the app div closing
html = html.replace(
    '<!-- ===== TOAST ===== -->',
    '<!-- ===== BOTTOM NAV ===== -->\n'
    '<nav class="bottom-nav" id="bottom-nav">\n'
    '  <button class="nav-item active" onclick="navTo(\'splash\')" id="nav-home"><span class="nav-icon">🏠</span>Accueil</button>\n'
    '  <button class="nav-item" onclick="navTo(\'shop\')" id="nav-shop"><span class="nav-icon">🛍️</span>Boutique</button>\n'
    '  <button class="nav-item" onclick="navTo(\'profile\')" id="nav-profile"><span class="nav-icon">👤</span>Profil</button>\n'
    '  <button class="nav-item" onclick="navTo(\'achievements\')" id="nav-achieve"><span class="nav-icon">🏆</span>Succès</button>\n'
    '</nav>\n\n'
    '<!-- ===== REWARD OVERLAY ===== -->\n'
    '<div class="reward-overlay" id="reward-overlay">\n'
    '  <div class="reward-chest" id="reward-chest">🎁</div>\n'
    '  <div class="reward-gems" id="reward-gems"></div>\n'
    '  <div class="reward-xp" id="reward-xp"></div>\n'
    '  <div class="reward-level-up" id="reward-level-up" style="display:none"></div>\n'
    '  <button class="btn btn-primary" onclick="closeReward()">Continuer</button>\n'
    '</div>\n\n'
    '<!-- ===== TOAST ===== -->'
)

# Add shop + profile screens inside #app (before credits)
SHOP_PROFILE_HTML = """
  <!-- ===== SHOP SCREEN ===== -->
  <div id="screen-shop" class="screen">
    <h2>🛍️ Boutique</h2>
    <div class="gems-display" id="shop-gems"><span class="gem-icon">💎</span><span id="shop-gem-count">0</span></div>
    <div class="daily-deal" id="daily-deal"></div>
    <div class="shop-section"><div class="shop-section-title">🎮 Modes de jeu</div><div class="shop-grid" id="shop-modes"></div></div>
    <div class="shop-section"><div class="shop-section-title">🎨 Thèmes visuels</div><div class="shop-grid" id="shop-themes"></div></div>
    <div class="shop-section"><div class="shop-section-title">🖼️ Cadres de profil</div><div class="shop-grid" id="shop-frames"></div></div>
    <div class="shop-section"><div class="shop-section-title">📦 Packs</div><div class="shop-grid" id="shop-packs"></div></div>
  </div>

  <!-- ===== PROFILE SCREEN ===== -->
  <div id="screen-profile" class="screen">
    <div class="profile-header">
      <div class="profile-avatar" id="profile-avatar">🕵️</div>
      <div style="font-size:1.2rem;font-weight:700;color:var(--text-bright)" id="profile-name">Joueur</div>
      <div class="profile-level" id="profile-level">Niveau 1 — Rookie</div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill" style="width:0%"></div></div>
      <div class="gems-display"><span class="gem-icon">💎</span><span id="profile-gems">0</span></div>
    </div>
    <div class="stats-grid" id="profile-stats"></div>
  </div>

"""

html = html.replace(
    '  <!-- ===== CREDITS SCREEN ===== -->',
    SHOP_PROFILE_HTML + '  <!-- ===== CREDITS SCREEN ===== -->'
)

# Add social proof to splash
html = html.replace(
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-credits\')">Crédits</button>',
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-credits\')">Crédits</button>\n'
    '    <div class="social-proof"><div class="pulse-dot"></div><span id="social-counter">847 joueurs actifs</span></div>'
)

# ═══════════════════════════════════════════════════════════
# 3. JAVASCRIPT: Gems, shop, profile, rewards, nav, mode fix
# ═══════════════════════════════════════════════════════════
JS_V6 = """

// ===== GEMS & ECONOMY SYSTEM =====
const Economy = {
  _data: null,
  load() {
    try {
      this._data = JSON.parse(localStorage.getItem('uc_economy') || 'null');
    } catch(e) {}
    if (!this._data) {
      this._data = {
        gems: 500, // Welcome bonus
        xp: 0, level: 1,
        ownedModes: ['normal','casual'],
        ownedThemes: ['default'],
        ownedFrames: ['rookie'],
        selectedTheme: 'default',
        selectedFrame: 'rookie',
        totalGames: 0, totalWins: 0, totalRounds: 0,
        bestStreak: 0, currentDayStreak: 0,
        lastLoginDate: '', modesPlayed: [],
        dailyDealSeed: 0,
      };
      this.save();
    }
    // Daily login bonus
    const today = new Date().toISOString().slice(0,10);
    if (this._data.lastLoginDate !== today) {
      const wasYesterday = this._data.lastLoginDate === new Date(Date.now()-86400000).toISOString().slice(0,10);
      if (wasYesterday) {
        this._data.currentDayStreak = (this._data.currentDayStreak||0) + 1;
      } else {
        this._data.currentDayStreak = 1;
      }
      this._data.lastLoginDate = today;
      const bonus = this._data.currentDayStreak >= 7 ? 100 : this._data.currentDayStreak >= 3 ? 50 : 10;
      this._data.gems += bonus;
      this.save();
      setTimeout(() => showToast('Connexion jour ' + this._data.currentDayStreak + ' : +' + bonus + '💎', 3000), 1500);
    }
  },
  save() { try { localStorage.setItem('uc_economy', JSON.stringify(this._data)); } catch(e) {} },
  get gems() { return this._data.gems; },
  get xp() { return this._data.xp; },
  get level() { return this._data.level; },
  get data() { return this._data; },
  addGems(n) { this._data.gems += n; this.save(); this.updateUI(); },
  spendGems(n) {
    if (this._data.gems < n) return false;
    this._data.gems -= n; this.save(); this.updateUI(); return true;
  },
  addXP(n) {
    this._data.xp += n;
    const needed = this._data.level * 100;
    if (this._data.xp >= needed) {
      this._data.xp -= needed;
      this._data.level++;
      this.save();
      return true; // leveled up
    }
    this.save(); return false;
  },
  ownsMode(id) { return this._data.ownedModes.includes(id); },
  buyMode(id, price) {
    if (this.ownsMode(id)) return true;
    if (!this.spendGems(price)) { showToast('Pas assez de gemmes !'); return false; }
    this._data.ownedModes.push(id); this.save(); return true;
  },
  ownsTheme(id) { return this._data.ownedThemes.includes(id); },
  buyTheme(id, price) {
    if (this.ownsTheme(id)) return true;
    if (!this.spendGems(price)) { showToast('Pas assez de gemmes !'); return false; }
    this._data.ownedThemes.push(id); this.save(); return true;
  },
  ownsFrame(id) { return this._data.ownedFrames.includes(id); },
  buyFrame(id, price) {
    if (this.ownsFrame(id)) return true;
    if (!this.spendGems(price)) { showToast('Pas assez de gemmes !'); return false; }
    this._data.ownedFrames.push(id); this.save(); return true;
  },
  getLevelTitle() {
    const l = this._data.level;
    if (l >= 20) return 'Légende';
    if (l >= 15) return 'Maître';
    if (l >= 10) return 'Expert';
    if (l >= 5) return 'Amateur';
    return 'Rookie';
  },
  updateUI() {
    ['shop-gem-count','profile-gems'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.textContent = this._data.gems;
    });
  }
};

// ===== BOTTOM NAV =====
function navTo(screen) {
  SoundFX.click();
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const map = {splash:'nav-home',shop:'nav-shop',profile:'nav-profile',achievements:'nav-achieve'};
  const navEl = document.getElementById(map[screen]);
  if (navEl) navEl.classList.add('active');
  showScreen('screen-' + screen);
  if (screen === 'shop') renderShop();
  if (screen === 'profile') renderProfile();
}

function updateNavVisibility() {
  const nav = document.getElementById('bottom-nav');
  if (!nav) return;
  nav.classList.toggle('hidden', GameState.gameActive);
}

// Patch showScreen for nav
const _prevShowScreen4 = showScreen;
showScreen = function(id) {
  _prevShowScreen4(id);
  updateNavVisibility();
};


// ===== SHOP =====
const SHOP_MODES = [
  {id:'normal',icon:'🌀',name:'Anime Mix',price:0,badge:''},
  {id:'casual',icon:'😄',name:'Casual',price:0,badge:''},
  {id:'shonen',icon:'⚔️',name:'Shōnen',price:200,badge:'popular'},
  {id:'shojo',icon:'🌸',name:'Shōjo',price:200,badge:''},
  {id:'seinen',icon:'🖤',name:'Seinen',price:200,badge:''},
  {id:'isekai',icon:'🌀',name:'Isekai',price:200,badge:''},
  {id:'anime_classic',icon:'📼',name:'Anime Classique',price:150,badge:''},
  {id:'anime_gold',icon:'🥇',name:'Anime Gold',price:250,badge:''},
  {id:'series_tv',icon:'📺',name:'Séries TV',price:200,badge:'popular'},
  {id:'disney',icon:'🏰',name:'Disney+',price:200,badge:''},
  {id:'cartoons',icon:'🎨',name:'Cartoons',price:200,badge:'new'},
  {id:'jeux_video',icon:'🎮',name:'Jeux Vidéo',price:200,badge:'new'},
  {id:'tout_melanger',icon:'🌍',name:'Tout Mélanger',price:300,badge:''},
];

const SHOP_THEMES = [
  {id:'default',name:'Dark Default',icon:'🌙',price:0},
  {id:'sakura',name:'Sakura Night',icon:'🌸',price:150},
  {id:'cyber',name:'Cyber Tokyo',icon:'🌃',price:200},
  {id:'gold',name:'Gold Edition',icon:'👑',price:300},
  {id:'void',name:'Void',icon:'⬛',price:100},
];

const SHOP_FRAMES = [
  {id:'rookie',name:'Rookie',icon:'🟢',price:0},
  {id:'champion',name:'Champion',icon:'🏆',price:300},
  {id:'undercover',name:'Undercover',icon:'🔴',price:200},
];

function renderShop() {
  Economy.updateUI();

  // Daily deal
  const deal = document.getElementById('daily-deal');
  if (deal) {
    const hours = 23 - new Date().getHours();
    const mins = 59 - new Date().getMinutes();
    deal.innerHTML = '<div style="font-weight:700;color:var(--accent-gold);font-size:1rem;">🔥 Offre du jour</div>' +
      '<div style="font-size:0.85rem;color:var(--text-primary);margin:6px 0;">Pack Découverte : 3 modes au choix <span class="shop-card-original">600💎</span> <span style="color:var(--accent-gold);font-weight:700;">360💎</span></div>' +
      '<div class="deal-timer">⏰ Expire dans ' + hours + 'h ' + mins + 'min</div>';
  }

  // Modes
  const modesGrid = document.getElementById('shop-modes');
  if (modesGrid) {
    modesGrid.innerHTML = '';
    SHOP_MODES.forEach(m => {
      const owned = Economy.ownsMode(m.id);
      const card = document.createElement('div');
      card.className = 'shop-card' + (owned ? ' owned' : '');
      let badge = '';
      if (m.badge === 'popular') badge = '<div class="shop-badge popular">Populaire</div>';
      if (m.badge === 'new') badge = '<div class="shop-badge new">Nouveau</div>';
      card.innerHTML = badge +
        '<div class="shop-card-icon">' + m.icon + '</div>' +
        '<div class="shop-card-name">' + m.name + '</div>' +
        (owned ? '<div class="shop-card-price free">Possédé</div>' :
         m.price === 0 ? '<div class="shop-card-price free">Gratuit</div>' :
         '<div class="shop-card-price">💎 ' + m.price + '</div>');
      if (!owned && m.price > 0) {
        card.onclick = () => {
          if (Economy.buyMode(m.id, m.price)) {
            showToast(m.name + ' débloqué ! 🎉');
            renderShop();
          }
        };
      }
      modesGrid.appendChild(card);
    });
  }

  // Themes
  const themesGrid = document.getElementById('shop-themes');
  if (themesGrid) {
    themesGrid.innerHTML = '';
    SHOP_THEMES.forEach(t => {
      const owned = Economy.ownsTheme(t.id);
      const card = document.createElement('div');
      card.className = 'shop-card' + (owned ? ' owned' : '');
      card.innerHTML = '<div class="shop-card-icon">' + t.icon + '</div>' +
        '<div class="shop-card-name">' + t.name + '</div>' +
        (owned ? '<div class="shop-card-price free">Possédé</div>' :
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
      themesGrid.appendChild(card);
    });
  }

  // Frames
  const framesGrid = document.getElementById('shop-frames');
  if (framesGrid) {
    framesGrid.innerHTML = '';
    SHOP_FRAMES.forEach(fr => {
      const owned = Economy.ownsFrame(fr.id);
      const card = document.createElement('div');
      card.className = 'shop-card' + (owned ? ' owned' : '');
      card.innerHTML = '<div class="shop-card-icon">' + fr.icon + '</div>' +
        '<div class="shop-card-name">' + fr.name + '</div>' +
        (owned ? '<div class="shop-card-price free">Possédé</div>' :
         fr.price === 0 ? '<div class="shop-card-price free">Gratuit</div>' :
         '<div class="shop-card-price">💎 ' + fr.price + '</div>');
      if (!owned && fr.price > 0) {
        card.onclick = () => {
          if (Economy.buyFrame(fr.id, fr.price)) {
            showToast(fr.name + ' débloqué !');
            renderShop();
          }
        };
      }
      framesGrid.appendChild(card);
    });
  }

  // Packs
  const packsGrid = document.getElementById('shop-packs');
  if (packsGrid) {
    packsGrid.innerHTML = '';
    const packs = [
      {name:'Pack Découverte',icon:'📦',desc:'3 modes + 1 thème',price:480,original:600},
      {name:'Pack Ultimate',icon:'👑',desc:'Tout débloquer',price:1500,original:2500},
      {name:'Pack Streamer',icon:'🎥',desc:'Mode Streamer + Cyber',price:350,original:400},
    ];
    packs.forEach(pk => {
      const card = document.createElement('div');
      card.className = 'shop-card';
      card.innerHTML = '<div class="shop-card-icon">' + pk.icon + '</div>' +
        '<div class="shop-card-name">' + pk.name + '</div>' +
        '<div style="font-size:0.7rem;color:var(--text-muted);margin:4px 0">' + pk.desc + '</div>' +
        '<div class="shop-card-price"><span class="shop-card-original">' + pk.original + '💎</span> 💎 ' + pk.price + '</div>';
      packsGrid.appendChild(card);
    });
  }
}


// ===== PROFILE =====
function renderProfile() {
  Economy.updateUI();
  const d = Economy.data;

  const level = document.getElementById('profile-level');
  if (level) level.textContent = 'Niveau ' + d.level + ' — ' + Economy.getLevelTitle();

  const xpFill = document.getElementById('xp-fill');
  if (xpFill) {
    const needed = d.level * 100;
    xpFill.style.width = Math.min(100, (d.xp / needed) * 100) + '%';
  }

  const stats = document.getElementById('profile-stats');
  if (stats) {
    stats.innerHTML = '';
    const items = [
      {value: d.totalGames, label: 'Parties jouées'},
      {value: d.totalWins, label: 'Victoires'},
      {value: d.totalGames > 0 ? Math.round(d.totalWins / d.totalGames * 100) + '%' : '0%', label: 'Taux victoire'},
      {value: d.bestStreak, label: 'Meilleure streak'},
      {value: d.currentDayStreak + '🔥', label: 'Streak connexion'},
      {value: d.gems + '💎', label: 'Gemmes'},
    ];
    items.forEach(it => {
      const card = document.createElement('div');
      card.className = 'stat-card';
      card.innerHTML = '<div class="stat-value">' + it.value + '</div><div class="stat-label">' + it.label + '</div>';
      stats.appendChild(card);
    });
  }
}


// ===== REWARD SYSTEM =====
function showReward(gemsEarned, xpEarned) {
  const overlay = document.getElementById('reward-overlay');
  document.getElementById('reward-chest').textContent = '🎁';
  document.getElementById('reward-gems').textContent = '+' + gemsEarned + ' 💎';
  document.getElementById('reward-xp').textContent = '+' + xpEarned + ' XP';

  const leveledUp = Economy.addXP(xpEarned);
  Economy.addGems(gemsEarned);

  const lvlEl = document.getElementById('reward-level-up');
  if (leveledUp && lvlEl) {
    lvlEl.textContent = '🎉 Niveau ' + Economy.level + ' !';
    lvlEl.style.display = 'block';
  } else if (lvlEl) {
    lvlEl.style.display = 'none';
  }

  // Variable reward: rare chance of bonus
  if (Math.random() < 0.1) {
    const bonus = Math.floor(Math.random() * 50) + 50;
    Economy.addGems(bonus);
    document.getElementById('reward-gems').textContent += ' + BONUS ' + bonus + '💎 !';
  }

  overlay.classList.add('visible');
  SoundFX.victory();
}

function closeReward() {
  document.getElementById('reward-overlay').classList.remove('visible');
}

// Patch showFinalScreen to show reward first
const _origShowFinal = showFinalScreen;
showFinalScreen = function() {
  // Calculate rewards
  Economy.data.totalGames++;
  Economy.save();
  const gemsBase = 10;
  const xpBase = 25;
  showReward(gemsBase, xpBase);
  // After reward is dismissed, show final screen
  const _origClose = closeReward;
  closeReward = function() {
    document.getElementById('reward-overlay').classList.remove('visible');
    closeReward = _origClose;
    _origShowFinal();
  };
};


// ===== FIX MODE FILTERING =====
// Override GAME_MODES with correct IDs and check ownership
const _origConfirmMode = confirmMode;
confirmMode = function() {
  const mode = GameState.currentMode;
  // Check if mode is owned
  if (!Economy.ownsMode(mode) && mode !== 'normal' && mode !== 'casual') {
    const shopMode = SHOP_MODES.find(m => m.id === mode);
    if (shopMode && shopMode.price > 0) {
      showConfirm('Mode verrouillé 🔒',
        shopMode.name + ' coûte ' + shopMode.price + '💎. Débloquer ?',
        () => {
          if (Economy.buyMode(mode, shopMode.price)) {
            showToast(shopMode.name + ' débloqué ! 🎉');
            _origConfirmMode();
          }
        }
      );
      return;
    }
  }
  _origConfirmMode();
};

// Fix getAvailablePairs to STRICTLY filter by mode
const _origGetAvailablePairs2 = getAvailablePairs;
getAvailablePairs = function() {
  const mode = GameState.currentMode;

  if (mode === 'tout_melanger') {
    // Everything
    return PAIRS.filter(p => {
      const key = pairKey(p);
      return !GameState.recentPairKeys.includes(key);
    });
  }

  // Strict mode filtering
  return PAIRS.filter(p => {
    const pairMode = p.mode || 'normal';
    if (pairMode !== mode) return false;
    const key = pairKey(p);
    return !GameState.recentPairKeys.includes(key);
  });
};


// ===== SOCIAL PROOF (fake but fun) =====
function updateSocialProof() {
  const el = document.getElementById('social-counter');
  if (!el) return;
  const base = 500 + (new Date().getHours() * 37) + (new Date().getMinutes() * 3);
  const variation = Math.floor(Math.random() * 100);
  el.textContent = (base + variation) + ' joueurs actifs';
}
setInterval(updateSocialProof, 30000);


// ===== INIT ECONOMY =====
document.addEventListener('DOMContentLoaded', () => {
  Economy.load();
  Economy.updateUI();
  updateSocialProof();
});
"""

html = html.replace("\n</script>", JS_V6 + "\n</script>")

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V6 patch applied! Template: {len(html)//1024} KB")
