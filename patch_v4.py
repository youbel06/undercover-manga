#!/usr/bin/env python3
"""V4 patch: burger menu, new modes, streaks, replay, random names, character descriptions."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS for burger menu + sidebar + new mode themes + streak
# ═══════════════════════════════════════════════════════════
CSS_V4 = """
/* ===== BURGER MENU ===== */
.burger-btn {
  position: fixed; top: 12px; left: 12px; z-index: 400;
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--bg-glass); border: 1px solid var(--border-glass);
  backdrop-filter: blur(10px); cursor: pointer;
  display: none; align-items: center; justify-content: center;
  font-size: 1.3rem; color: var(--text-primary);
  transition: all 0.2s;
}
.burger-btn:hover { background: var(--bg-card-hover); }
.burger-btn.game-active { display: flex; }

.sidebar-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.6); z-index: 450;
  opacity: 0; pointer-events: none; transition: opacity 0.3s;
}
.sidebar-overlay.open { opacity: 1; pointer-events: auto; }

.sidebar {
  position: fixed; top: 0; left: -300px; width: 280px; height: 100%;
  background: var(--bg-secondary); border-right: 1px solid var(--border-glass);
  z-index: 451; padding: 20px; transition: left 0.3s ease;
  display: flex; flex-direction: column; gap: 8px;
  overflow-y: auto;
}
.sidebar-overlay.open .sidebar { left: 0; }

.sidebar-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px; padding-bottom: 12px;
  border-bottom: 1px solid var(--border-glass);
}
.sidebar-header h3 { font-size: 1.1rem; color: var(--text-bright); }
.sidebar-close { background: none; border: none; color: var(--text-muted);
  font-size: 1.4rem; cursor: pointer; padding: 4px; }

.sidebar-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 14px; border-radius: var(--radius-sm);
  background: var(--bg-card); cursor: pointer;
  transition: all 0.2s; color: var(--text-primary); font-size: 0.9rem;
  border: none; width: 100%; text-align: left;
}
.sidebar-item:hover { background: var(--bg-card-hover); }
.sidebar-item .si-icon { font-size: 1.2rem; width: 28px; text-align: center; }
.sidebar-item.danger { color: var(--accent-undercover); }

.sidebar-score {
  background: var(--bg-card); border-radius: var(--radius-sm);
  padding: 14px; margin-top: 8px;
}
.sidebar-score h4 { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 8px;
  text-transform: uppercase; letter-spacing: 1px; }
.sidebar-score-row {
  display: flex; justify-content: space-between; padding: 3px 0;
  font-size: 0.85rem;
}
.sidebar-score-row .name { color: var(--text-primary); }
.sidebar-score-row .pts { color: var(--accent-gold); font-weight: 600; }

/* ===== STREAK INDICATOR ===== */
.streak-badge {
  position: fixed; top: 60px; left: 12px; z-index: 399;
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: #000; font-weight: 700; font-size: 0.75rem;
  padding: 4px 10px; border-radius: 12px;
  display: none; align-items: center; gap: 4px;
  animation: pulse 1.5s ease infinite;
  box-shadow: 0 2px 10px rgba(245,158,11,0.4);
}
.streak-badge.visible { display: inline-flex; }
@keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }

/* ===== MODE OR ANIME ===== */
body.mode-or_anime { --accent-civil: #f59e0b; --accent-undercover: #b45309; }
body.mode-or_anime #app {
  background: radial-gradient(ellipse at 50% 30%, #2d1f00 0%, var(--bg-primary) 70%);
}

/* ===== MODE CLASSIQUE PUR ===== */
body.mode-classique_pur { --accent-civil: #06b6d4; --accent-undercover: #ec4899; }

/* ===== MODE SERIES TV ===== */
body.mode-series_netflix { --accent-civil: #e50914; --accent-undercover: #221f1f; }
body.mode-series_disney { --accent-civil: #0070d1; --accent-undercover: #1a1a2e; }
body.mode-cartoons { --accent-civil: #22c55e; --accent-undercover: #f97316; }
body.mode-series_mix { --accent-civil: #8b5cf6; --accent-undercover: #ef4444; }

/* ===== RANDOM NAME BUTTON ===== */
.random-name-btn {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--bg-card); border: 1px solid var(--border-glass);
  cursor: pointer; font-size: 1rem; color: var(--text-muted);
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s; flex-shrink: 0;
}
.random-name-btn:hover { background: var(--bg-card-hover); color: var(--accent-gold); }

/* ===== REPLAY BUTTON ===== */
.replay-btn {
  margin-top: 8px; font-size: 0.8rem; color: var(--text-muted);
}

/* ===== CHAR DESCRIPTION ===== */
.card-description {
  font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;
  line-height: 1.3; max-width: 250px; font-style: italic;
}

/* ===== CONFIRM DIALOG ===== */
.confirm-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.7); z-index: 500;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.2s;
}
.confirm-overlay.open { opacity: 1; pointer-events: auto; }
.confirm-box {
  background: var(--bg-secondary); border: 1px solid var(--border-glass);
  border-radius: var(--radius-lg); padding: 24px; text-align: center;
  max-width: 320px; width: 90%;
}
.confirm-box h3 { margin-bottom: 12px; color: var(--text-bright); }
.confirm-box p { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 18px; }
.confirm-btns { display: flex; gap: 10px; justify-content: center; }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_V4 + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML: Burger menu, sidebar, confirm dialog, streak badge
# ═══════════════════════════════════════════════════════════
BURGER_HTML = """
<!-- ===== BURGER MENU ===== -->
<button class="burger-btn" id="burger-btn" onclick="toggleSidebar()">☰</button>
<div class="streak-badge" id="streak-badge">🔥 <span id="streak-count">0</span></div>

<div class="sidebar-overlay" id="sidebar-overlay" onclick="closeSidebar()">
  <div class="sidebar" onclick="event.stopPropagation()">
    <div class="sidebar-header">
      <h3>Menu</h3>
      <button class="sidebar-close" onclick="closeSidebar()">✕</button>
    </div>
    <button class="sidebar-item" onclick="closeSidebar();toggleAudioPanel()">
      <span class="si-icon">🔊</span> Audio
    </button>
    <button class="sidebar-item" onclick="confirmSkipRound()">
      <span class="si-icon">⏭️</span> Passer la manche
    </button>
    <button class="sidebar-item" onclick="replayCurrentPair()">
      <span class="si-icon">🔄</span> Rejouer cette paire
    </button>
    <div class="sidebar-score" id="sidebar-scores">
      <h4>📊 Scores</h4>
      <div id="sidebar-score-list"></div>
    </div>
    <button class="sidebar-item danger" onclick="confirmQuitGame()">
      <span class="si-icon">🏠</span> Quitter la partie
    </button>
  </div>
</div>

<!-- ===== CONFIRM DIALOG ===== -->
<div class="confirm-overlay" id="confirm-overlay">
  <div class="confirm-box">
    <h3 id="confirm-title">Confirmer</h3>
    <p id="confirm-text"></p>
    <div class="confirm-btns">
      <button class="btn btn-ghost" onclick="closeConfirm()">Annuler</button>
      <button class="btn btn-primary" id="confirm-yes" onclick="closeConfirm()">Oui</button>
    </div>
  </div>
</div>

"""

html = html.replace(
    '<!-- ===== AUDIO CONTROLS (FLOATING) ===== -->',
    BURGER_HTML + '<!-- ===== AUDIO CONTROLS (FLOATING) ===== -->'
)

# Add card-description div to the card overlay
html = html.replace(
    '<div class="card-universe" id="card-universe"></div>',
    '<div class="card-universe" id="card-universe"></div>\n      <div class="card-description" id="card-description"></div>'
)

# ═══════════════════════════════════════════════════════════
# 3. JAVASCRIPT: Burger/sidebar, confirm dialogs, new modes,
#    streaks, replay, random names, char descriptions
# ═══════════════════════════════════════════════════════════
JS_V4 = """

// ===== BURGER MENU / SIDEBAR =====
GameState.civilStreak = 0;

function toggleSidebar() {
  const overlay = document.getElementById('sidebar-overlay');
  overlay.classList.toggle('open');
  updateSidebarScores();
  SoundFX.click();
}

function closeSidebar() {
  document.getElementById('sidebar-overlay').classList.remove('open');
}

function updateSidebarScores() {
  const list = document.getElementById('sidebar-score-list');
  if (!list || !GameState.players.length) return;
  list.innerHTML = '';
  const sorted = [...GameState.playerNames].sort((a, b) => (GameState.scores[b] || 0) - (GameState.scores[a] || 0));
  sorted.forEach(name => {
    const row = document.createElement('div');
    row.className = 'sidebar-score-row';
    row.innerHTML = '<span class="name">' + name + '</span><span class="pts">' + (GameState.scores[name] || 0) + ' pts</span>';
    list.appendChild(row);
  });
}

function updateBurgerVisibility() {
  const btn = document.getElementById('burger-btn');
  if (btn) btn.classList.toggle('game-active', GameState.gameActive);
}

// Patch showScreen to update burger visibility
const _prevShowScreen = showScreen;
showScreen = function(id) {
  _prevShowScreen(id);
  updateBurgerVisibility();
  updateStreakBadge();
};

// ===== CONFIRM DIALOGS =====
let confirmCallback = null;

function showConfirm(title, text, onYes) {
  document.getElementById('confirm-title').textContent = title;
  document.getElementById('confirm-text').textContent = text;
  confirmCallback = onYes;
  document.getElementById('confirm-yes').onclick = () => { closeConfirm(); if (confirmCallback) confirmCallback(); };
  document.getElementById('confirm-overlay').classList.add('open');
}

function closeConfirm() {
  document.getElementById('confirm-overlay').classList.remove('open');
  confirmCallback = null;
}

function confirmQuitGame() {
  closeSidebar();
  showConfirm('Abandonner ?', 'La partie en cours sera perdue.', () => {
    resetToSplash();
  });
}

function confirmSkipRound() {
  closeSidebar();
  showConfirm('Passer la manche ?', 'La manche actuelle sera annulée.', () => {
    // Skip to next round or end
    if (GameState.currentRound >= GameState.totalRounds) {
      showFinalScreen();
    } else {
      nextRound();
    }
  });
}

function replayCurrentPair() {
  closeSidebar();
  if (!GameState.currentPair) return;
  showConfirm('Rejouer cette paire ?', GameState.currentPair.civil + ' vs ' + GameState.currentPair.undercover, () => {
    // Re-setup the round with same pair
    setupRound();
    showScreen('screen-reveal');
  });
}

// ===== STREAK SYSTEM =====
function updateStreakBadge() {
  const badge = document.getElementById('streak-badge');
  const count = document.getElementById('streak-count');
  if (!badge || !count) return;
  if (GameState.civilStreak >= 3) {
    badge.classList.add('visible');
    count.textContent = GameState.civilStreak;
  } else {
    badge.classList.remove('visible');
  }
}

// Patch showRoundResult for streak tracking
const _prevShowRoundResult2 = showRoundResult;
showRoundResult = function(winnerType) {
  if (winnerType === 'civil') {
    GameState.civilStreak = (GameState.civilStreak || 0) + 1;
  } else {
    GameState.civilStreak = 0;
  }
  _prevShowRoundResult2(winnerType);
  updateStreakBadge();
};


// ===== NEW GAME MODES (extend GAME_MODES) =====
GAME_MODES.push(
  { id: 'or_anime', icon: '🥇', name: 'Or Anime', desc: 'Les 50 plus iconiques', theme: 'mode-or_anime' },
  { id: 'classique_pur', icon: '👥', name: 'Classique', desc: 'Concepts du quotidien, pas d\\'anime', theme: 'mode-classique_pur' },
  { id: 'series_netflix', icon: '🎬', name: 'Netflix/HBO', desc: 'Séries TV populaires', theme: 'mode-series_netflix' },
  { id: 'series_disney', icon: '🏰', name: 'Disney+', desc: 'Disney, Marvel, Star Wars', theme: 'mode-series_disney' },
  { id: 'cartoons', icon: '🎨', name: 'Cartoons', desc: 'Dessins animés occidentaux', theme: 'mode-cartoons' },
  { id: 'series_mix', icon: '🌍', name: 'Mixte Total', desc: 'Anime + Séries + Disney + Cartoons', theme: 'mode-series_mix' }
);


// ===== PATCH applyModeFilter for new modes =====
const _origApplyModeFilter = applyModeFilter;
applyModeFilter = function() {
  const mode = GameState.currentMode;
  // For modes that filter by pair.mode field
  const modeFilterModes = ['or_anime', 'classique_pur', 'series_netflix', 'series_disney', 'cartoons', 'series_mix'];
  if (modeFilterModes.includes(mode)) {
    // These modes filter by the pair's mode field, not by universe
    GameState.enabledUniverses = new Set();
    PAIRS.forEach(p => {
      if (p.universe1) GameState.enabledUniverses.add(p.universe1);
      if (p.universe2) GameState.enabledUniverses.add(p.universe2);
    });
    return;
  }
  _origApplyModeFilter();
};

// Override getAvailablePairs to support mode-field filtering
const _origGetAvailablePairs = getAvailablePairs;
getAvailablePairs = function() {
  const mode = GameState.currentMode;
  const modeFilterModes = ['or_anime', 'classique_pur', 'series_netflix', 'series_disney', 'cartoons', 'series_mix'];

  if (modeFilterModes.includes(mode)) {
    let modesToMatch;
    if (mode === 'series_mix') {
      modesToMatch = ['series_netflix', 'series_disney', 'cartoons', 'series_mix', 'or_anime', 'normal'];
    } else {
      modesToMatch = [mode];
    }
    return PAIRS.filter(p => {
      if (!modesToMatch.includes(p.mode || 'normal')) return false;
      const key = pairKey(p);
      if (GameState.recentPairKeys.includes(key)) return false;
      return true;
    });
  }

  return _origGetAvailablePairs();
};


// ===== RANDOM NAME GENERATOR =====
const RANDOM_NAMES = [
  'Ace','Atlas','Blaze','Bolt','Ciel','Cobra','Dash','Echo','Ember','Fang',
  'Frost','Ghost','Hawk','Iris','Jade','Kai','Luna','Mist','Neo','Nyx',
  'Onyx','Phoenix','Raven','Rex','Sage','Shadow','Sky','Storm','Titan','Viper',
  'Wolf','Yuki','Zen','Zero','Aria','Nova','Pixel','Quartz','Ruby','Sora'
];

function randomName() {
  return RANDOM_NAMES[Math.floor(Math.random() * RANDOM_NAMES.length)];
}


// ===== CHARACTER DESCRIPTIONS =====
const CHAR_DESCRIPTIONS = {
  // Major characters - short 2-line descriptions
  'naruto': 'Ninja hyperactif du village de Konoha, porteur du démon renard à neuf queues.',
  'sasuke': 'Dernier survivant du clan Uchiha, obsédé par la vengeance contre son frère.',
  'goku': 'Guerrier Saiyan au cœur pur, toujours en quête de combattants plus forts.',
  'vegeta': 'Prince des Saiyans, rival éternel de Goku, fier et impitoyable.',
  'luffy': 'Capitaine au chapeau de paille, son corps est en caoutchouc. Rêve de devenir le Roi des Pirates.',
  'zoro': 'Épéiste à trois sabres, bras droit de Luffy, rêve de devenir le meilleur escrimeur du monde.',
  'ichigo': 'Lycéen devenu Shinigami, protège les vivants et les morts avec son zanpakutō.',
  'eren': 'Jeune soldat qui découvre qu\\'il peut se transformer en Titan. Prêt à tout pour la liberté.',
  'levi': 'Le soldat le plus fort de l\\'humanité. Froid, efficace, obsédé par la propreté.',
  'gojo': 'Le sorcier le plus puissant. Ses yeux voient l\\'infini. Professeur décontracté mais redoutable.',
  'sukuna': 'Le Roi des Fléaux, entité millénaire d\\'une cruauté absolue.',
  'tanjiro': 'Pourfendeur de démons au cœur pur, cherche à sauver sa sœur transformée en démon.',
  'deku': 'Né sans pouvoir dans un monde de héros, il hérite du One For All et ne recule jamais.',
  'light': 'Génie lycéen qui trouve un carnet de la mort et décide de devenir le dieu du nouveau monde.',
  'l': 'Détective le plus brillant au monde. Excentrique, il résout les affaires impossibles.',
  'gon': 'Garçon de la nature, pur et déterminé, part à la recherche de son père chasseur.',
  'killua': 'Héritier d\\'une famille d\\'assassins, il fuit son destin pour vivre libre avec Gon.',
  'edward': 'Alchimiste d\\'État le plus jeune de l\\'histoire, cherche la Pierre Philosophale pour restaurer son frère.',
  'saitama': 'Héros si puissant qu\\'il bat tout le monde en un coup. Son plus grand ennemi : l\\'ennui.',
  'kakashi': 'Le ninja copieur au Sharingan, sensei cool mais redoutable de l\\'Équipe 7.',
  'itachi': 'Génie du clan Uchiha, a massacré les siens pour protéger son village en secret.',
  'madara': 'Légendaire fondateur du clan Uchiha, son seul nom fait trembler le monde ninja.',
  'jiraiya': 'L\\'Ermite des Crapauds, auteur pervers mais l\\'un des ninjas les plus puissants.',
  'pain': 'Leader de l\\'Akatsuki, veut imposer la paix par la force et la douleur.',
  'kaneki': 'Étudiant timide transformé en goule après une greffe. Déchiré entre deux mondes.',
  'lelouch': 'Prince exilé qui obtient le pouvoir de commander quiconque. Stratège de génie.',
};

function getCharDescription(charName) {
  if (!charName) return '';
  const key = charName.toLowerCase().split(' ')[0];
  return CHAR_DESCRIPTIONS[key] || '';
}


// ===== PATCH revealPlayerRole to show description =====
const _origRevealPlayerRole = revealPlayerRole;
revealPlayerRole = function(playerIndex) {
  _origRevealPlayerRole(playerIndex);
  const player = GameState.players[playerIndex];
  const descEl = document.getElementById('card-description');
  if (descEl && player) {
    const desc = getCharDescription(player.character);
    descEl.textContent = desc;
    descEl.style.display = desc ? 'block' : 'none';
  }
};

// ===== PATCH renderSettings to add random name buttons =====
const _origRenderSettings = renderSettings;
renderSettings = function() {
  _origRenderSettings();
  // Add random name buttons next to each name input
  document.querySelectorAll('.player-name-input').forEach((input, i) => {
    if (input.nextElementSibling && input.nextElementSibling.classList.contains('random-name-btn')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'random-name-btn';
    btn.textContent = '🎲';
    btn.title = 'Nom aléatoire';
    btn.onclick = (e) => {
      e.preventDefault();
      const name = randomName();
      input.value = name;
      input.dispatchEvent(new Event('input', {bubbles: true}));
      SoundFX.click();
    };
    input.parentElement.appendChild(btn);
  });
};
"""

html = html.replace("\n</script>", JS_V4 + "\n</script>")

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print("V4 patch applied!")
print(f"  Template: {len(html)} chars ({len(html)//1024} KB)")
