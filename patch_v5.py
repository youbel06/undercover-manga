#!/usr/bin/env python3
"""V5 patch: Premium design, scoring fix, video game mode, tutorial, credits."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. Add Google Fonts import + favicon
# ═══════════════════════════════════════════════════════════
html = html.replace(
    '<title>Undercover Manga</title>',
    '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🕵️</text></svg>">\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">\n'
    '<title>Undercover Manga</title>'
)

# ═══════════════════════════════════════════════════════════
# 2. Replace core CSS variables and base styles for premium feel
# ═══════════════════════════════════════════════════════════
old_vars = """/* ===== CSS CUSTOM PROPERTIES ===== */
:root {
  --bg-primary: #0a0a1a;
  --bg-secondary: #12122a;
  --bg-card: rgba(255,255,255,0.04);
  --bg-card-hover: rgba(255,255,255,0.08);
  --bg-glass: rgba(255,255,255,0.06);
  --border-glass: rgba(255,255,255,0.1);
  --accent-civil: #3b82f6;
  --accent-civil-light: #60a5fa;
  --accent-undercover: #ef4444;
  --accent-undercover-light: #f87171;
  --accent-mrwhite: #9ca3af;
  --accent-mrwhite-light: #d1d5db;
  --accent-gold: #f59e0b;
  --accent-gold-light: #fbbf24;
  --accent-green: #22c55e;
  --text-primary: #e0e0e0;
  --text-bright: #ffffff;
  --text-muted: #888;
  --text-dim: #555;
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.5);
  --shadow-md: 0 8px 30px rgba(0,0,0,0.3);
  --shadow-sm: 0 4px 12px rgba(0,0,0,0.2);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  --font-main: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --transition-fast: 0.2s ease;
  --transition-med: 0.4s ease;
  --transition-slow: 0.6s ease;
}"""

new_vars = """/* ===== CSS CUSTOM PROPERTIES ===== */
:root {
  --bg-primary: #0A0A0F;
  --bg-secondary: #1A1A2E;
  --bg-card: rgba(255,255,255,0.05);
  --bg-card-hover: rgba(255,255,255,0.09);
  --bg-glass: rgba(255,255,255,0.06);
  --border-glass: rgba(255,255,255,0.08);
  --accent-civil: #00D4FF;
  --accent-civil-light: #4DE8FF;
  --accent-undercover: #E94560;
  --accent-undercover-light: #FF6B81;
  --accent-mrwhite: #9ca3af;
  --accent-mrwhite-light: #d1d5db;
  --accent-gold: #F5A623;
  --accent-gold-light: #FFD166;
  --accent-green: #22c55e;
  --text-primary: #E8E8F0;
  --text-bright: #FFFFFF;
  --text-muted: #888;
  --text-dim: #555;
  --shadow-lg: 0 20px 60px rgba(0,0,0,0.6);
  --shadow-md: 0 8px 30px rgba(0,0,0,0.4);
  --shadow-sm: 0 4px 12px rgba(0,0,0,0.2);
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
  --font-main: 'Outfit', 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-display: 'Space Grotesk', 'Outfit', sans-serif;
  --transition-fast: 0.2s ease;
  --transition-med: 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  --transition-slow: 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}"""

html = html.replace(old_vars, new_vars)

# ═══════════════════════════════════════════════════════════
# 3. Add premium CSS enhancements
# ═══════════════════════════════════════════════════════════
PREMIUM_CSS = """
/* ===== V5 PREMIUM STYLES ===== */

/* Display font for titles */
.splash-title, .modes-title, .final-title, .round-result-title,
h2, .settings-header h2, .discuss-title {
  font-family: var(--font-display);
}

/* Screen transitions: slide up with spring */
.screen.entering { transform: translateY(30px); }
.screen.active { transform: translateY(0); transition: opacity 0.4s cubic-bezier(0.22,1,0.36,1), transform 0.4s cubic-bezier(0.22,1,0.36,1); }

/* Premium buttons */
.btn {
  min-height: 48px;
  border-radius: var(--radius-md);
  font-weight: 700;
  letter-spacing: 0.3px;
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent-civil), #0098cc);
  box-shadow: 0 4px 20px rgba(0,212,255,0.25);
}
.btn-primary:hover { box-shadow: 0 6px 28px rgba(0,212,255,0.35); }
.btn-primary:active { transform: scale(0.97); }

/* Ripple effect */
.btn::after {
  content: ''; position: absolute; top: 50%; left: 50%;
  width: 0; height: 0; border-radius: 50%;
  background: rgba(255,255,255,0.2);
  transform: translate(-50%, -50%);
  transition: width 0.4s, height 0.4s, opacity 0.4s;
  opacity: 0;
}
.btn:active::after { width: 200px; height: 200px; opacity: 1; transition: 0s; }

/* Premium cards */
.mode-card, .achieve-card, .sidebar-item {
  backdrop-filter: blur(20px);
  border-radius: var(--radius-lg);
}

/* Manche progress bar */
.round-progress {
  position: fixed; top: 0; left: 0; height: 3px; z-index: 300;
  background: linear-gradient(90deg, var(--accent-civil), var(--accent-gold));
  transition: width 0.5s ease;
  box-shadow: 0 0 10px rgba(0,212,255,0.5);
}

/* Splash particles */
.splash-particle {
  position: absolute; width: 2px; height: 2px;
  background: rgba(255,255,255,0.3); border-radius: 50%;
  pointer-events: none; animation: sparkle linear infinite;
}
@keyframes sparkle {
  0% { opacity: 0; transform: translateY(0); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translateY(100vh); }
}

/* Voter indicator glow */
.vote-player-card.is-voter {
  box-shadow: 0 0 15px rgba(0,212,255,0.3);
  border-color: var(--accent-civil);
}
.vote-player-card.is-voter::before {
  content: '🕵️'; position: absolute; top: -8px; right: -8px;
  font-size: 1.2rem; z-index: 2;
}

/* Player avatar with unique colors */
.player-avatar-color-0 { background: linear-gradient(135deg, #E94560, #c23152) !important; }
.player-avatar-color-1 { background: linear-gradient(135deg, #00D4FF, #0098cc) !important; }
.player-avatar-color-2 { background: linear-gradient(135deg, #F5A623, #d4891a) !important; }
.player-avatar-color-3 { background: linear-gradient(135deg, #22c55e, #16a34a) !important; }
.player-avatar-color-4 { background: linear-gradient(135deg, #a855f7, #7c3aed) !important; }
.player-avatar-color-5 { background: linear-gradient(135deg, #ec4899, #be185d) !important; }
.player-avatar-color-6 { background: linear-gradient(135deg, #14b8a6, #0d9488) !important; }
.player-avatar-color-7 { background: linear-gradient(135deg, #f97316, #c2410c) !important; }
.player-avatar-color-8 { background: linear-gradient(135deg, #6366f1, #4338ca) !important; }
.player-avatar-color-9 { background: linear-gradient(135deg, #84cc16, #65a30d) !important; }
.player-avatar-color-10 { background: linear-gradient(135deg, #06b6d4, #0891b2) !important; }
.player-avatar-color-11 { background: linear-gradient(135deg, #f43f5e, #e11d48) !important; }

/* Toast at bottom */
.toast {
  bottom: 30px !important; top: auto !important;
  border-radius: var(--radius-md) !important;
}

/* Mode jeux_video theme */
body.mode-jeux_video { --accent-civil: #22c55e; --accent-undercover: #a855f7; }

/* Credits screen */
#screen-credits { justify-content: center; gap: 20px; text-align: center; }
#screen-credits .credit-line { font-size: 0.85rem; color: var(--text-muted); }
#screen-credits .credit-name { color: var(--accent-gold); font-weight: 600; }
#screen-credits .credit-version { font-size: 0.75rem; color: var(--text-dim); margin-top: 10px; }

/* Tutorial overlay */
.tutorial-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.9); z-index: 600;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.3s;
}
.tutorial-overlay.visible { opacity: 1; pointer-events: auto; }
.tutorial-card {
  background: var(--bg-secondary); border-radius: var(--radius-xl);
  padding: 30px 24px; max-width: 380px; width: 90%; text-align: center;
}
.tutorial-step { font-size: 3rem; margin-bottom: 12px; }
.tutorial-title { font-family: var(--font-display); font-size: 1.3rem; font-weight: 700; margin-bottom: 8px; color: var(--text-bright); }
.tutorial-text { font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 20px; }
.tutorial-dots { display: flex; justify-content: center; gap: 8px; margin-bottom: 16px; }
.tutorial-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--text-dim); }
.tutorial-dot.active { background: var(--accent-gold); }

/* Game timer display */
.game-timer-display {
  position: fixed; top: 12px; left: 50%; transform: translateX(-50%);
  background: var(--bg-glass); backdrop-filter: blur(10px);
  border: 1px solid var(--border-glass); border-radius: 20px;
  padding: 4px 14px; font-size: 0.75rem; color: var(--text-muted);
  z-index: 300; display: none;
}
.game-timer-display.visible { display: block; }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", PREMIUM_CSS + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 4. HTML additions: progress bar, credits, tutorial, game timer
# ═══════════════════════════════════════════════════════════

# Add progress bar + game timer before burger
html = html.replace(
    '<!-- ===== BURGER MENU ===== -->',
    '<!-- ===== ROUND PROGRESS BAR ===== -->\n'
    '<div class="round-progress" id="round-progress" style="width:0%"></div>\n'
    '<div class="game-timer-display" id="game-timer-display">00:00</div>\n\n'
    '<!-- ===== BURGER MENU ===== -->'
)

# Add credits screen + tutorial after history screen
html = html.replace(
    '</div>\n\n<!-- ===== TOAST ===== -->',
    '</div>\n\n'
    '  <!-- ===== CREDITS SCREEN ===== -->\n'
    '  <div id="screen-credits" class="screen">\n'
    '    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen(\'screen-splash\')" aria-label="Retour">←</button>\n'
    '    <h2>Crédits</h2>\n'
    '    <div class="credit-line">Développé avec <span class="credit-name">Claude Code</span></div>\n'
    '    <div class="credit-line">Images via <span class="credit-name">Fandom Wikis</span></div>\n'
    '    <div class="credit-line">Musique procédurale <span class="credit-name">Web Audio API</span></div>\n'
    '    <div class="credit-line"><span class="credit-name">371+ paires</span> de personnages</div>\n'
    '    <div class="credit-line"><span class="credit-name">12+ modes</span> de jeu</div>\n'
    '    <div class="credit-version">Undercover Manga v5.0</div>\n'
    '  </div>\n\n'
    '  <!-- ===== TUTORIAL OVERLAY ===== -->\n'
    '  <div class="tutorial-overlay" id="tutorial-overlay">\n'
    '    <div class="tutorial-card">\n'
    '      <div class="tutorial-step" id="tutorial-icon">🕵️</div>\n'
    '      <div class="tutorial-title" id="tutorial-title"></div>\n'
    '      <div class="tutorial-text" id="tutorial-text"></div>\n'
    '      <div class="tutorial-dots" id="tutorial-dots"></div>\n'
    '      <button class="btn btn-primary" id="tutorial-btn" onclick="nextTutorialStep()">Suivant</button>\n'
    '    </div>\n'
    '  </div>\n\n'
    '</div>\n\n<!-- ===== TOAST ===== -->'
)

# Add credits button to splash screen
html = html.replace(
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-achievements\')">',
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-credits\')">Crédits</button>\n'
    '    <button class="btn btn-ghost" onclick="showScreen(\'screen-achievements\')">'
)

# ═══════════════════════════════════════════════════════════
# 5. JavaScript additions
# ═══════════════════════════════════════════════════════════
JS_V5 = """

// ===== JEUX VIDEO MODE =====
GAME_MODES.push(
  { id: 'jeux_video', icon: '🎮', name: 'Jeux Vidéo', desc: 'Mario, Zelda, FF, GoW...', theme: 'mode-jeux_video' }
);

// ===== ENHANCED SCORING SYSTEM =====
const _origCalculateRoundScores = calculateRoundScores;
calculateRoundScores = function(winnerType) {
  // Reset round scores
  GameState.players.forEach(p => { p.roundScore = 0; });

  const aliveCivils = GameState.players.filter(p => p.alive && p.role === 'civil');
  const aliveUC = GameState.players.filter(p => p.alive && p.role === 'undercover');
  const aliveMW = GameState.players.filter(p => p.alive && p.role === 'mrwhite');
  const eliminated = GameState.players.filter(p => !p.alive);

  if (winnerType === 'civil') {
    // Civils win
    aliveCivils.forEach(p => {
      p.roundScore += 3; // survive bonus
      // Bonus for voting for undercover
      const votedFor = p.votedFor;
      if (votedFor !== null) {
        const target = GameState.players[votedFor];
        if (target && target.role === 'undercover') p.roundScore += 2;
      }
    });
    // Streak bonus
    if (GameState.civilStreak >= 2) {
      aliveCivils.forEach(p => { p.roundScore += 2; });
    }
  } else if (winnerType === 'undercover') {
    aliveUC.forEach(p => { p.roundScore += 5; }); // UC survives
    aliveMW.forEach(p => { p.roundScore += 3; }); // MW also on winning team
  } else if (winnerType === 'mrwhite') {
    aliveMW.forEach(p => { p.roundScore += 10; }); // MW guessed correctly
  }

  // Civils who voted wrong (eliminated a civil) get -1
  GameState.players.forEach(p => {
    if (p.role === 'civil' && p.votedFor !== null) {
      const target = GameState.players[p.votedFor];
      if (target && target.role === 'civil' && !target.alive) {
        p.roundScore -= 1;
      }
    }
  });

  // Apply scores
  GameState.players.forEach(p => {
    GameState.scores[p.name] = (GameState.scores[p.name] || 0) + p.roundScore;
  });
};

// ===== ROUND PROGRESS BAR =====
function updateRoundProgress() {
  const bar = document.getElementById('round-progress');
  if (!bar || !GameState.totalRounds) return;
  const pct = (GameState.currentRound / GameState.totalRounds) * 100;
  bar.style.width = pct + '%';
}

// Patch showScreen for progress bar
const _prevShowScreen3 = showScreen;
showScreen = function(id) {
  _prevShowScreen3(id);
  updateRoundProgress();
  // Show/hide game timer
  const timer = document.getElementById('game-timer-display');
  if (timer) timer.classList.toggle('visible', GameState.gameActive);
};

// ===== GAME TIMER =====
GameState.gameStartTime = 0;
GameState.gameTimerInterval = null;

function startGameTimer() {
  GameState.gameStartTime = Date.now();
  if (GameState.gameTimerInterval) clearInterval(GameState.gameTimerInterval);
  GameState.gameTimerInterval = setInterval(() => {
    const elapsed = Math.floor((Date.now() - GameState.gameStartTime) / 1000);
    const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
    const secs = String(elapsed % 60).padStart(2, '0');
    const el = document.getElementById('game-timer-display');
    if (el) el.textContent = mins + ':' + secs;
  }, 1000);
}

function stopGameTimer() {
  if (GameState.gameTimerInterval) clearInterval(GameState.gameTimerInterval);
  GameState.gameTimerInterval = null;
}

// Patch launchGame to start timer
const _origLaunchGame = launchGame;
launchGame = function() {
  _origLaunchGame();
  startGameTimer();
};

// Patch resetToSplash to stop timer
const _origResetToSplash = resetToSplash;
resetToSplash = function() {
  stopGameTimer();
  const timer = document.getElementById('game-timer-display');
  if (timer) timer.classList.remove('visible');
  document.getElementById('round-progress').style.width = '0%';
  _origResetToSplash();
};


// ===== SPLASH PARTICLES =====
function initSplashParticles() {
  const splash = document.getElementById('screen-splash');
  if (!splash) return;
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div');
    p.className = 'splash-particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.top = Math.random() * 100 + '%';
    p.style.animationDuration = (5 + Math.random() * 10) + 's';
    p.style.animationDelay = Math.random() * 5 + 's';
    p.style.width = (1 + Math.random() * 2) + 'px';
    p.style.height = p.style.width;
    splash.appendChild(p);
  }
}

// ===== TUTORIAL =====
const TUTORIAL_STEPS = [
  { icon: '🕵️', title: 'Bienvenue !', text: 'Undercover Manga est un jeu social où vous devez identifier l\\'imposteur parmi vos amis.' },
  { icon: '🃏', title: 'Les rôles', text: 'Les Civils reçoivent le même personnage. L\\'Undercover reçoit un personnage similaire mais différent. Le Mr. White ne sait rien !' },
  { icon: '💬', title: 'Comment jouer', text: 'Donnez un indice sur votre personnage sans le nommer. Votez pour éliminer celui que vous soupçonnez. Les Civils gagnent en éliminant l\\'Undercover !' },
];
let tutorialStep = 0;

function showTutorial() {
  tutorialStep = 0;
  renderTutorialStep();
  document.getElementById('tutorial-overlay').classList.add('visible');
}

function renderTutorialStep() {
  const s = TUTORIAL_STEPS[tutorialStep];
  document.getElementById('tutorial-icon').textContent = s.icon;
  document.getElementById('tutorial-title').textContent = s.title;
  document.getElementById('tutorial-text').textContent = s.text;
  const dots = document.getElementById('tutorial-dots');
  dots.innerHTML = '';
  TUTORIAL_STEPS.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'tutorial-dot' + (i === tutorialStep ? ' active' : '');
    dots.appendChild(d);
  });
  document.getElementById('tutorial-btn').textContent =
    tutorialStep >= TUTORIAL_STEPS.length - 1 ? 'C\\'est parti !' : 'Suivant';
}

function nextTutorialStep() {
  SoundFX.click();
  tutorialStep++;
  if (tutorialStep >= TUTORIAL_STEPS.length) {
    document.getElementById('tutorial-overlay').classList.remove('visible');
    try { localStorage.setItem('uc_tutorial_done', 'true'); } catch(e) {}
    return;
  }
  renderTutorialStep();
}

// Show tutorial on first launch
document.addEventListener('DOMContentLoaded', () => {
  try {
    if (!localStorage.getItem('uc_tutorial_done')) {
      setTimeout(showTutorial, 800);
    }
  } catch(e) {}
  initSplashParticles();
});


// ===== HAPTIC FEEDBACK =====
function haptic(style) {
  try {
    if (navigator.vibrate) {
      if (style === 'light') navigator.vibrate(10);
      else if (style === 'medium') navigator.vibrate(25);
      else if (style === 'heavy') navigator.vibrate([30, 20, 50]);
    }
  } catch(e) {}
}

// Add haptic to key actions
const _origSFXClick = SoundFX.click;
SoundFX.click = function() { haptic('light'); _origSFXClick(); };
const _origSFXEliminate = SoundFX.eliminate;
SoundFX.eliminate = function() { haptic('heavy'); _origSFXEliminate(); };
const _origSFXVictory = SoundFX.victory;
SoundFX.victory = function() { haptic('medium'); _origSFXVictory(); };
"""

html = html.replace("\n</script>", JS_V5 + "\n</script>")

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V5 patch applied! Template: {len(html)//1024} KB")
