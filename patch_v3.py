#!/usr/bin/env python3
"""
V3 patch: Apply all new features to game_template.html
- Procedural anime-style music (Web Audio API)
- Audio control panel (floating button + volume sliders)
- Game modes (Normal, Shōnen, Shōjo, Seinen, Isekai, Classique)
- Pair hints revealed at end of round
- Achievements system
- Victory particles (confetti/flames)
- Blind mode
- Easter egg for player names
- Image CSS fix (object-position: top)
"""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS ADDITIONS
# ═══════════════════════════════════════════════════════════

CSS_ADDITIONS = """
/* ===== AUDIO CONTROL FLOAT ===== */
.audio-float {
  position: fixed; top: 12px; right: 12px; z-index: 500;
  display: flex; flex-direction: column; align-items: flex-end; gap: 6px;
}
.audio-float-btn {
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--bg-glass); border: 1px solid var(--border-glass);
  backdrop-filter: blur(10px);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; cursor: pointer; transition: all 0.2s;
  color: var(--text-primary);
}
.audio-float-btn:hover { background: var(--bg-card-hover); transform: scale(1.1); }
.audio-panel {
  background: var(--bg-secondary); border: 1px solid var(--border-glass);
  border-radius: var(--radius-md); padding: 14px 16px;
  backdrop-filter: blur(15px); min-width: 200px;
  display: none; animation: fadeIn 0.2s ease;
}
.audio-panel.show { display: block; }
.audio-panel label {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 0.8rem; color: var(--text-muted); margin-bottom: 4px;
}
.audio-panel input[type=range] {
  width: 100%; height: 6px; -webkit-appearance: none; appearance: none;
  background: rgba(255,255,255,0.1); border-radius: 3px; outline: none;
  margin: 4px 0 12px;
}
.audio-panel input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%;
  background: var(--accent-gold); cursor: pointer;
}

/* ===== GAME MODE SCREEN ===== */
#screen-modes { justify-content: center; gap: 20px; }
.modes-title { font-size: 1.6rem; font-weight: 700; text-align: center; color: var(--text-bright); }
.modes-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px; width: 100%; max-width: 700px;
}
.mode-card {
  background: var(--bg-card); border: 2px solid var(--border-glass);
  border-radius: var(--radius-lg); padding: 20px 12px;
  text-align: center; cursor: pointer; transition: all 0.25s;
}
.mode-card:hover { border-color: var(--accent-gold); transform: translateY(-4px);
  box-shadow: var(--shadow-md); }
.mode-card.selected { border-color: var(--accent-gold);
  background: rgba(245,158,11,0.1); box-shadow: 0 0 20px rgba(245,158,11,0.15); }
.mode-icon { font-size: 2.2rem; margin-bottom: 8px; }
.mode-name { font-size: 0.95rem; font-weight: 600; color: var(--text-bright); }
.mode-desc { font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; line-height: 1.3; }

/* Mode themes */
body.mode-shonen { --accent-civil: #f97316; --accent-undercover: #dc2626; }
body.mode-shojo { --accent-civil: #ec4899; --accent-undercover: #a855f7; --bg-primary: #1a0a1e; }
body.mode-seinen { --accent-civil: #6b7280; --accent-undercover: #991b1b; --bg-primary: #0a0a0a; }
body.mode-isekai { --accent-civil: #8b5cf6; --accent-undercover: #06b6d4; --bg-primary: #0f0a1e; }
body.mode-classic { --accent-civil: #ca8a04; --accent-undercover: #b91c1c; }
body.mode-classic #app { filter: sepia(0.15) contrast(1.05); }

/* Cherry blossoms for shojo */
body.mode-shojo .petal {
  position: fixed; width: 10px; height: 10px; background: #f9a8d4;
  border-radius: 50% 0 50% 0; opacity: 0.4; z-index: 0; pointer-events: none;
  animation: petalFall linear infinite;
}
@keyframes petalFall {
  0% { transform: translateY(-10vh) rotate(0deg) translateX(0); opacity: 0.5; }
  100% { transform: translateY(110vh) rotate(720deg) translateX(80px); opacity: 0; }
}

/* VHS grain for classic */
body.mode-classic::after {
  content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: repeating-linear-gradient(0deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 1px, transparent 2px);
  pointer-events: none; z-index: 999;
}

/* ===== ACHIEVEMENTS ===== */
.achievements-btn {
  position: absolute; top: 12px; left: 12px;
}
.badge-count {
  position: absolute; top: -4px; right: -4px; background: var(--accent-gold);
  color: #000; font-size: 0.65rem; font-weight: 700;
  width: 18px; height: 18px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.achievement-popup {
  position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #000; padding: 12px 24px; border-radius: var(--radius-md);
  font-weight: 600; font-size: 0.9rem; z-index: 600;
  animation: achieveIn 0.5s ease, achieveOut 0.5s ease 2.5s forwards;
  box-shadow: var(--shadow-lg);
}
@keyframes achieveIn { from { opacity: 0; transform: translateX(-50%) translateY(-30px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
@keyframes achieveOut { to { opacity: 0; transform: translateX(-50%) translateY(-30px); } }

.achievements-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 10px; width: 100%; max-width: 600px; margin: 15px 0;
}
.achieve-card {
  background: var(--bg-card); border: 1px solid var(--border-glass);
  border-radius: var(--radius-md); padding: 14px 10px; text-align: center;
  opacity: 0.4; transition: all 0.3s;
}
.achieve-card.unlocked { opacity: 1; border-color: var(--accent-gold); }
.achieve-icon { font-size: 1.8rem; margin-bottom: 6px; }
.achieve-title { font-size: 0.75rem; font-weight: 600; color: var(--text-bright); }
.achieve-desc { font-size: 0.65rem; color: var(--text-muted); margin-top: 3px; }

/* ===== HINT REVEAL ===== */
.hint-box {
  background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2);
  border-radius: var(--radius-md); padding: 14px 18px;
  margin: 12px 0; text-align: center;
  animation: fadeIn 0.5s ease 0.5s both;
}
.hint-label { font-size: 0.75rem; color: var(--accent-gold); text-transform: uppercase;
  letter-spacing: 1px; margin-bottom: 6px; }
.hint-text { font-size: 0.85rem; color: var(--text-primary); line-height: 1.4; font-style: italic; }

/* ===== VICTORY PARTICLES ===== */
.flame-particle {
  position: fixed; width: 8px; height: 12px; border-radius: 50% 50% 50% 0;
  z-index: 50; pointer-events: none;
  animation: flameFall 1.5s ease-out forwards;
}
@keyframes flameFall {
  0% { opacity: 1; transform: translateY(0) scale(1) rotate(0deg); }
  100% { opacity: 0; transform: translateY(-200px) scale(0) rotate(180deg); }
}

/* ===== IMAGE FIX ===== */
.card-image-container img,
.pair-card-image img,
.reveal-player-avatar img,
.player-card img,
.eliminated-avatar img,
.vote-player-avatar img {
  object-fit: cover;
  object-position: top center;
}

/* ===== BLIND MODE ===== */
body.blind-mode .card-character-name { filter: blur(8px); transition: filter 0.3s; }
body.blind-mode .card-character-name:hover { filter: blur(0); }
body.blind-mode .eliminated-player-name { filter: blur(6px); }
body.blind-mode .tally-name { filter: blur(5px); }

/* ===== NAME EASTER EGG ===== */
@keyframes specialReveal {
  0% { filter: brightness(1); }
  25% { filter: brightness(2) hue-rotate(30deg); }
  50% { filter: brightness(1.5) hue-rotate(-30deg); }
  100% { filter: brightness(1); }
}
.special-reveal { animation: specialReveal 1s ease; }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_ADDITIONS + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML ADDITIONS - Audio float, Mode screen, Achievements
# ═══════════════════════════════════════════════════════════

# Add audio float BEFORE the app div
AUDIO_FLOAT_HTML = """
<!-- ===== AUDIO CONTROLS (FLOATING) ===== -->
<div class="audio-float" id="audio-float">
  <button class="audio-float-btn" id="audio-toggle-btn" onclick="toggleAudioPanel()" aria-label="Audio">🔊</button>
  <div class="audio-panel" id="audio-panel">
    <label>🎵 Musique <span id="music-vol-label">70%</span></label>
    <input type="range" id="music-volume" min="0" max="100" value="70" oninput="setMusicVolume(this.value)">
    <label>🔊 Effets <span id="sfx-vol-label">80%</span></label>
    <input type="range" id="sfx-volume" min="0" max="100" value="80" oninput="setSfxVolume(this.value)">
  </div>
</div>

"""

html = html.replace('<div id="app">', AUDIO_FLOAT_HTML + '<div id="app">')

# Add mode screen + achievements screen AFTER splash, BEFORE settings
MODE_SCREEN_HTML = """
  <!-- ===== MODE SELECTION SCREEN ===== -->
  <div id="screen-modes" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-splash')" aria-label="Retour">←</button>
    <div class="modes-title">Choisis ton mode</div>
    <div class="modes-grid" id="modes-grid"></div>
    <button class="btn btn-primary" onclick="confirmMode()">Continuer</button>
  </div>

  <!-- ===== ACHIEVEMENTS SCREEN ===== -->
  <div id="screen-achievements" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-splash')" aria-label="Retour">←</button>
    <h2 style="margin-bottom:5px;">Succès</h2>
    <div class="achievements-grid" id="achievements-grid"></div>
  </div>

"""

html = html.replace(
    '  <!-- ===== SETTINGS SCREEN ===== -->',
    MODE_SCREEN_HTML + '  <!-- ===== SETTINGS SCREEN ===== -->'
)

# Add achievements + blind mode buttons to splash screen
html = html.replace(
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-history\')">Historique</button>\n  </div>',
    '<button class="btn btn-ghost" onclick="showScreen(\'screen-history\')">Historique</button>\n'
    '    <button class="btn btn-ghost" onclick="showScreen(\'screen-achievements\')">🏆 Succès <span class="badge-count" id="achieve-count">0</span></button>\n'
    '  </div>'
)

# Change JOUER to go to mode select first
html = html.replace(
    "onclick=\"startNewGame()\">JOUER</button>",
    "onclick=\"showScreen('screen-modes')\">JOUER</button>"
)

# Add hint box to elimination screen
html = html.replace(
    '  </div>\n\n  <!-- ===== ROUND RESULT SCREEN ===== -->',
    '    <div class="hint-box" id="hint-box" style="display:none">\n'
    '      <div class="hint-label">Le saviez-vous ?</div>\n'
    '      <div class="hint-text" id="hint-text"></div>\n'
    '    </div>\n'
    '  </div>\n\n  <!-- ===== ROUND RESULT SCREEN ===== -->'
)

# Add blind mode toggle in settings - find the universe filter area
html = html.replace(
    '<div class="universe-filter" id="universe-filter"></div>',
    '<div class="universe-filter" id="universe-filter"></div>\n'
    '      <div class="settings-group" style="margin-top:12px;">\n'
    '        <label class="settings-label">Mode Aveugle (noms cachés)</label>\n'
    '        <button class="btn btn-ghost" id="blind-toggle" onclick="toggleBlindMode()">Désactivé</button>\n'
    '      </div>'
)


# ═══════════════════════════════════════════════════════════
# 3. JAVASCRIPT - Music engine, audio controls, modes, etc.
# ═══════════════════════════════════════════════════════════

JS_ADDITIONS = """

// ===== PROCEDURAL MUSIC ENGINE (Anime-style) =====
const MusicEngine = (() => {
  let ctx = null;
  let masterGain = null;
  let currentTrack = null;
  let musicVolume = 0.7;
  let sfxVolume = 0.8;

  // Load saved volumes
  try {
    const saved = JSON.parse(localStorage.getItem('uc_audio'));
    if (saved) { musicVolume = saved.music ?? 0.7; sfxVolume = saved.sfx ?? 0.8; }
  } catch(e) {}

  function getCtx() {
    if (!ctx) {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      masterGain = ctx.createGain();
      masterGain.gain.value = musicVolume;
      masterGain.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function saveVolumes() {
    try { localStorage.setItem('uc_audio', JSON.stringify({music: musicVolume, sfx: sfxVolume})); } catch(e) {}
  }

  function note(freq, type, start, dur, vol, vibrato) {
    const c = getCtx();
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    if (vibrato) {
      const lfo = c.createOscillator();
      const lfoGain = c.createGain();
      lfo.frequency.value = vibrato.rate || 5;
      lfoGain.gain.value = vibrato.depth || 3;
      lfo.connect(lfoGain);
      lfoGain.connect(osc.frequency);
      lfo.start(start);
      lfo.stop(start + dur);
    }
    gain.gain.setValueAtTime(0, start);
    gain.gain.linearRampToValueAtTime(vol, start + 0.02);
    gain.gain.setValueAtTime(vol, start + dur * 0.7);
    gain.gain.exponentialRampToValueAtTime(0.001, start + dur);
    osc.connect(gain);
    gain.connect(masterGain);
    osc.start(start);
    osc.stop(start + dur + 0.05);
    return osc;
  }

  function playDrumHit(start, freq, dur) {
    const c = getCtx();
    const osc = c.createOscillator();
    const gain = c.createGain();
    const noise = c.createBufferSource();
    const noiseGain = c.createGain();
    // Drum body
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, start);
    osc.frequency.exponentialRampToValueAtTime(freq * 0.3, start + dur);
    gain.gain.setValueAtTime(0.3, start);
    gain.gain.exponentialRampToValueAtTime(0.001, start + dur);
    osc.connect(gain);
    gain.connect(masterGain);
    osc.start(start);
    osc.stop(start + dur + 0.05);
    // Noise layer
    const bufSize = c.sampleRate * dur;
    const buf = c.createBuffer(1, Math.max(1, Math.floor(bufSize)), c.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1) * 0.3;
    noise.buffer = buf;
    noiseGain.gain.setValueAtTime(0.08, start);
    noiseGain.gain.exponentialRampToValueAtTime(0.001, start + dur * 0.5);
    noise.connect(noiseGain);
    noiseGain.connect(masterGain);
    noise.start(start);
    noise.stop(start + dur + 0.05);
  }

  function stopCurrent() {
    if (currentTrack) {
      currentTrack.forEach(osc => { try { osc.stop(); } catch(e) {} });
      currentTrack = null;
    }
  }

  // ── LOBBY: Calm epic melody (pentatonic, strings + flute feel) ──
  function playLobby() {
    stopCurrent();
    const c = getCtx();
    const t = c.currentTime + 0.1;
    const oscs = [];
    // Pentatonic scale melody: C D E G A
    const melody = [262, 294, 330, 392, 440, 392, 330, 294, 262, 294, 330, 392, 523, 440, 392, 330];
    const beatDur = 0.6;
    // Pad chord
    [130.8, 164.8, 196].forEach(f => {
      const o = note(f, 'sine', t, melody.length * beatDur, 0.04, {rate: 4, depth: 2});
      oscs.push(o);
    });
    // Melody (flute-like triangle)
    melody.forEach((freq, i) => {
      const o = note(freq, 'triangle', t + i * beatDur, beatDur * 0.85, 0.08, {rate: 5, depth: 4});
      oscs.push(o);
    });
    // Soft percussion
    for (let i = 0; i < melody.length; i += 2) {
      playDrumHit(t + i * beatDur, 80, 0.2);
    }
    currentTrack = oscs;
  }

  // ── SUSPENSE: Tense strings + heartbeat ──
  function playSuspense() {
    stopCurrent();
    const c = getCtx();
    const t = c.currentTime + 0.1;
    const oscs = [];
    const dur = 12;
    // Low drone
    oscs.push(note(55, 'sawtooth', t, dur, 0.04));
    oscs.push(note(82.4, 'sawtooth', t, dur, 0.03));
    // Dissonant intervals
    const tensions = [117, 123.5, 117, 110, 123.5, 130.8, 123.5, 117];
    tensions.forEach((f, i) => {
      oscs.push(note(f, 'sine', t + i * 1.4, 1.3, 0.05, {rate: 6, depth: 5}));
    });
    // Heartbeat drums
    for (let i = 0; i < 10; i++) {
      playDrumHit(t + i * 1.1, 50, 0.15);
      playDrumHit(t + i * 1.1 + 0.25, 45, 0.12);
    }
    currentTrack = oscs;
  }

  // ── VICTORY CIVILS: Triumphant fanfare ──
  function playVictoryCivils() {
    stopCurrent();
    const c = getCtx();
    const t = c.currentTime + 0.1;
    const oscs = [];
    // Fanfare melody (major scale ascending)
    const fanfare = [262, 330, 392, 523, 523, 659, 784, 1047];
    const durations = [0.2, 0.2, 0.2, 0.4, 0.15, 0.2, 0.3, 0.8];
    let offset = 0;
    fanfare.forEach((f, i) => {
      oscs.push(note(f, 'triangle', t + offset, durations[i] * 0.9, 0.1));
      oscs.push(note(f * 1.5, 'sine', t + offset, durations[i] * 0.7, 0.03));
      offset += durations[i];
    });
    // Chord stab
    [523, 659, 784].forEach(f => {
      oscs.push(note(f, 'sine', t + offset, 1.5, 0.06, {rate: 4, depth: 3}));
    });
    // Taiko hits
    playDrumHit(t, 100, 0.3);
    playDrumHit(t + 0.6, 100, 0.3);
    playDrumHit(t + offset, 80, 0.5);
    currentTrack = oscs;
  }

  // ── VICTORY UNDERCOVER: Dark triumphant ──
  function playVictoryUndercover() {
    stopCurrent();
    const c = getCtx();
    const t = c.currentTime + 0.1;
    const oscs = [];
    // Minor key descending
    const melody = [659, 622, 587, 523, 466, 440, 392, 349];
    melody.forEach((f, i) => {
      oscs.push(note(f, 'sawtooth', t + i * 0.25, 0.35, 0.06));
      oscs.push(note(f * 0.5, 'sine', t + i * 0.25, 0.4, 0.04));
    });
    // Power chord
    [220, 261.6, 329.6].forEach(f => {
      oscs.push(note(f, 'sawtooth', t + 2.2, 2, 0.05));
    });
    for (let i = 0; i < 4; i++) playDrumHit(t + i * 0.5, 60, 0.25);
    currentTrack = oscs;
  }

  // ── REVEAL: Mysterious sweep ──
  function playReveal() {
    stopCurrent();
    const c = getCtx();
    const t = c.currentTime + 0.1;
    const oscs = [];
    const sweep = [220, 277, 330, 415, 523, 659];
    sweep.forEach((f, i) => {
      oscs.push(note(f, 'sine', t + i * 0.15, 0.8 - i * 0.05, 0.07, {rate: 6, depth: 4}));
    });
    playDrumHit(t + 0.8, 100, 0.4);
    currentTrack = oscs;
  }

  return {
    get musicVolume() { return musicVolume; },
    get sfxVolume() { return sfxVolume; },
    setMusicVolume(v) {
      musicVolume = v;
      if (masterGain) masterGain.gain.value = v;
      saveVolumes();
    },
    setSfxVolume(v) { sfxVolume = v; saveVolumes(); },
    lobby: playLobby,
    suspense: playSuspense,
    victoryCivils: playVictoryCivils,
    victoryUndercover: playVictoryUndercover,
    reveal: playReveal,
    stop: stopCurrent,
  };
})();

// ===== AUDIO CONTROL UI =====
function toggleAudioPanel() {
  document.getElementById('audio-panel').classList.toggle('show');
}
function setMusicVolume(val) {
  MusicEngine.setMusicVolume(val / 100);
  document.getElementById('music-vol-label').textContent = val + '%';
  updateAudioIcon();
}
function setSfxVolume(val) {
  MusicEngine.setSfxVolume(val / 100);
  document.getElementById('sfx-vol-label').textContent = val + '%';
  updateAudioIcon();
}
function updateAudioIcon() {
  const m = MusicEngine.musicVolume > 0.01;
  const s = MusicEngine.sfxVolume > 0.01;
  const btn = document.getElementById('audio-toggle-btn');
  if (m && s) btn.textContent = '🔊';
  else if (m) btn.textContent = '🎵';
  else if (s) btn.textContent = '🔔';
  else btn.textContent = '🔇';
}
// Init audio UI
document.addEventListener('DOMContentLoaded', () => {
  const mv = Math.round(MusicEngine.musicVolume * 100);
  const sv = Math.round(MusicEngine.sfxVolume * 100);
  const mSlider = document.getElementById('music-volume');
  const sSlider = document.getElementById('sfx-volume');
  if (mSlider) { mSlider.value = mv; document.getElementById('music-vol-label').textContent = mv + '%'; }
  if (sSlider) { sSlider.value = sv; document.getElementById('sfx-vol-label').textContent = sv + '%'; }
  updateAudioIcon();
});
// Close panel on outside click
document.addEventListener('click', (e) => {
  if (!e.target.closest('.audio-float')) {
    const panel = document.getElementById('audio-panel');
    if (panel) panel.classList.remove('show');
  }
});


// ===== GAME MODES =====
const GAME_MODES = [
  { id: 'normal', icon: '🎮', name: 'Normal', desc: 'Tous les univers mélangés', theme: '' },
  { id: 'shonen', icon: '⚔️', name: 'Shōnen', desc: 'Héros, combats, amitié', theme: 'mode-shonen' },
  { id: 'shojo', icon: '🌸', name: 'Shōjo', desc: 'Émotions, relations, magie', theme: 'mode-shojo' },
  { id: 'seinen', icon: '🖤', name: 'Seinen', desc: 'Sombre, psychologique, mature', theme: 'mode-seinen' },
  { id: 'isekai', icon: '🌀', name: 'Isekai', desc: 'Autre monde, réincarnation', theme: 'mode-isekai' },
  { id: 'classic', icon: '👴', name: 'Classique', desc: 'Animes rétro, avant 2010', theme: 'mode-classic' },
];

GameState.currentMode = 'normal';
GameState.blindMode = false;

function renderModeScreen() {
  const grid = document.getElementById('modes-grid');
  if (!grid) return;
  grid.innerHTML = '';
  GAME_MODES.forEach(m => {
    const card = document.createElement('div');
    card.className = 'mode-card' + (GameState.currentMode === m.id ? ' selected' : '');
    card.innerHTML = '<div class="mode-icon">' + m.icon + '</div>' +
      '<div class="mode-name">' + m.name + '</div>' +
      '<div class="mode-desc">' + m.desc + '</div>';
    card.onclick = () => {
      GameState.currentMode = m.id;
      renderModeScreen();
      SoundFX.click();
    };
    grid.appendChild(card);
  });
}

function confirmMode() {
  SoundFX.click();
  // Apply theme
  document.body.className = document.body.className.replace(/mode-\\S+/g, '');
  const mode = GAME_MODES.find(m => m.id === GameState.currentMode);
  if (mode && mode.theme) document.body.classList.add(mode.theme);
  // Shojo petals
  document.querySelectorAll('.petal').forEach(p => p.remove());
  if (GameState.currentMode === 'shojo') {
    for (let i = 0; i < 15; i++) {
      const p = document.createElement('div');
      p.className = 'petal';
      p.style.left = Math.random() * 100 + 'vw';
      p.style.animationDuration = (4 + Math.random() * 6) + 's';
      p.style.animationDelay = Math.random() * 5 + 's';
      document.body.appendChild(p);
    }
  }
  // Filter pairs by mode
  applyModeFilter();
  startNewGame();
}

function applyModeFilter() {
  const mode = GameState.currentMode;
  if (mode === 'normal') {
    GameState.enabledUniverses = new Set();
    PAIRS.forEach(p => {
      if (p.universe1) GameState.enabledUniverses.add(p.universe1);
      if (p.universe2) GameState.enabledUniverses.add(p.universe2);
    });
    return;
  }
  // Filter by mode field or universe
  const modeUniverses = {
    shonen: ['Naruto','Dragon Ball','One Piece','Bleach','My Hero Academia','Demon Slayer','Jujutsu Kaisen','Black Clover','Fairy Tail','Hunter x Hunter'],
    shojo: ['Sailor Moon','Fruits Basket','Ouran','Kimi ni Todoke','Clannad','Violet Evergarden','Your Lie in April','Toradora','Cardcaptor Sakura','Madoka Magica','Maid Sama'],
    seinen: ['Attack on Titan','Berserk','Tokyo Ghoul','Death Note','Vinland Saga','Chainsaw Man','Evangelion','Code Geass','Parasyte','Psycho-Pass','Ghost in the Shell','Monster','Black Lagoon'],
    isekai: ['Re:Zero','Sword Art Online','Overlord','Tensura','KonoSuba','Mushoku Tensei','Shield Hero','No Game No Life'],
    classic: ['Dragon Ball','Saint Seiya','Slam Dunk','Inuyasha','Hokuto no Ken','Ranma ½','Yu-Gi-Oh','Captain Tsubasa','Gintama','Rurouni Kenshin','Trigun','Cowboy Bebop','Gundam','Yu Yu Hakusho','Sailor Moon'],
  };
  const universes = new Set(modeUniverses[mode] || []);
  GameState.enabledUniverses = universes;
}

// Patch showScreen to render mode screen and play music
const _origShowScreen = showScreen;
showScreen = function(screenId) {
  _origShowScreen(screenId);
  if (screenId === 'screen-modes') renderModeScreen();
  if (screenId === 'screen-achievements') renderAchievements();
  // Music triggers
  if (screenId === 'screen-splash') { try { MusicEngine.lobby(); } catch(e) {} }
  if (screenId === 'screen-vote') { try { MusicEngine.suspense(); } catch(e) {} }
  if (screenId === 'screen-reveal') { try { MusicEngine.reveal(); } catch(e) {} }
};


// ===== BLIND MODE =====
function toggleBlindMode() {
  GameState.blindMode = !GameState.blindMode;
  document.body.classList.toggle('blind-mode', GameState.blindMode);
  const btn = document.getElementById('blind-toggle');
  if (btn) btn.textContent = GameState.blindMode ? 'Activé 👁️' : 'Désactivé';
  SoundFX.click();
}


// ===== ACHIEVEMENTS SYSTEM =====
const ACHIEVEMENTS = [
  { id: 'first_win', icon: '🏆', title: 'Première victoire', desc: 'Gagne une manche' },
  { id: 'ten_games', icon: '🎮', title: 'Vétéran', desc: 'Joue 10 parties' },
  { id: 'mrwhite_guess', icon: '👻', title: 'Mentaliste', desc: 'Devine en Mr. White' },
  { id: 'perfect_civil', icon: '🎯', title: 'Détective parfait', desc: 'Vote toujours pour l\\'Undercover' },
  { id: 'undercover_win', icon: '🕵️', title: 'Infiltré', desc: 'Gagne en Undercover' },
  { id: 'five_streak', icon: '🔥', title: 'Inarrêtable', desc: '5 manches gagnées d\\'affilée' },
  { id: 'all_modes', icon: '🌈', title: 'Explorateur', desc: 'Joue chaque mode de jeu' },
  { id: 'konami', icon: '🕹️', title: 'Old School', desc: 'Active le code Konami' },
  { id: 'blind_win', icon: '👁️', title: 'Aveugle', desc: 'Gagne en mode Aveugle' },
  { id: 'hundred_rounds', icon: '💯', title: 'Centenaire', desc: 'Joue 100 manches' },
];

function getUnlockedAchievements() {
  try { return JSON.parse(localStorage.getItem('uc_achievements') || '[]'); } catch(e) { return []; }
}

function unlockAchievement(id) {
  const unlocked = getUnlockedAchievements();
  if (unlocked.includes(id)) return;
  unlocked.push(id);
  try { localStorage.setItem('uc_achievements', JSON.stringify(unlocked)); } catch(e) {}
  const achieve = ACHIEVEMENTS.find(a => a.id === id);
  if (!achieve) return;
  // Show popup
  const popup = document.createElement('div');
  popup.className = 'achievement-popup';
  popup.textContent = '🏆 ' + achieve.title + ' débloqué !';
  document.body.appendChild(popup);
  SoundFX.victory();
  setTimeout(() => popup.remove(), 3000);
  updateAchieveCount();
}

function updateAchieveCount() {
  const el = document.getElementById('achieve-count');
  if (el) el.textContent = getUnlockedAchievements().length;
}

function renderAchievements() {
  const grid = document.getElementById('achievements-grid');
  if (!grid) return;
  grid.innerHTML = '';
  const unlocked = getUnlockedAchievements();
  ACHIEVEMENTS.forEach(a => {
    const card = document.createElement('div');
    card.className = 'achieve-card' + (unlocked.includes(a.id) ? ' unlocked' : '');
    card.innerHTML = '<div class="achieve-icon">' + a.icon + '</div>' +
      '<div class="achieve-title">' + a.title + '</div>' +
      '<div class="achieve-desc">' + a.desc + '</div>';
    grid.appendChild(card);
  });
}


// ===== PAIR HINTS =====
const PAIR_HINTS = {
  'sensei protecteur': 'Ces deux personnages sont des mentors légendaires qui protègent leurs élèves au péril de leur vie.',
  'génie maudit': 'Deux génies tourmentés par leur héritage familial, forcés de porter un fardeau qu\\'ils n\\'ont pas choisi.',
  'villain charismatique': 'Des antagonistes si charismatiques qu\\'on finit presque par les comprendre. Leur vision du monde est terrifiante... mais cohérente.',
  'héros solaire': 'Le même archétype du héros solaire : courageux, naïf, et capable de changer le cœur de ses ennemis par sa seule volonté.',
  'rival / double inversé': 'Deux faces d\\'une même pièce. L\\'un est la lumière, l\\'autre l\\'ombre — mais ils se comprennent mieux que quiconque.',
  'puissance incontrôlable': 'Des êtres dont la puissance les isole du reste de l\\'humanité. Le pouvoir est autant une malédiction qu\\'un don.',
  'sacrifié par son système': 'Des soldats loyaux qui ont sacrifié tout — honneur, bonheur, parfois leur vie — pour un système qui ne le méritait peut-être pas.',
  'miroir historique': 'Un miroir des drames réels de l\\'Histoire. La fiction manga s\\'inspire des tragédies humaines pour raconter des vérités universelles.',
  'entité non-humaine': 'Des êtres au-delà de l\\'humanité qui observent, jugent, et parfois interviennent dans le destin des mortels.',
  'duo inséparable': 'Un duo iconique dont la force vient de leur complémentarité. Séparés, ils sont forts. Ensemble, ils sont invincibles.',
  'femme guerrière badass': 'Des guerrières qui n\\'ont besoin de personne pour se sauver. Leur force inspire et brise les clichés.',
  'miroir père-fils': 'Le poids de l\\'héritage paternel : ces personnages vivent dans l\\'ombre de leur père, cherchant à le surpasser ou le comprendre.',
  'miroir frères': 'Frères de sang ou de cœur, leur lien est aussi fort que leur rivalité.',
  'miroir familial': 'La famille comme source de force et de douleur. Ces personnages portent les cicatrices de leur lignée.',
  'sensei et élève': 'La transmission du savoir, du maître à l\\'élève. Un lien sacré dans le monde du manga.',
};

function showHintForPair(pair) {
  const hintBox = document.getElementById('hint-box');
  const hintText = document.getElementById('hint-text');
  if (!hintBox || !hintText || !pair) return;
  const archetype = (pair.archetype || '').toLowerCase();
  let hint = PAIR_HINTS[archetype];
  if (!hint) {
    // Generic hint
    hint = 'Ces deux personnages partagent un archétype commun qui transcende les frontières de leurs univers respectifs.';
  }
  hintText.textContent = hint;
  hintBox.style.display = 'block';
}


// ===== VICTORY PARTICLES =====
function spawnFlames(count) {
  for (let i = 0; i < count; i++) {
    const el = document.createElement('div');
    el.className = 'flame-particle';
    const hue = Math.random() * 40;  // red-orange range
    el.style.background = 'hsl(' + hue + ', 100%, ' + (50 + Math.random() * 20) + '%)';
    el.style.left = (10 + Math.random() * 80) + 'vw';
    el.style.bottom = '0';
    el.style.animationDuration = (1 + Math.random() * 1) + 's';
    el.style.animationDelay = Math.random() * 0.5 + 's';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2500);
  }
}


// ===== NAME EASTER EGGS =====
const SPECIAL_NAMES = ['gojo', 'naruto', 'luffy', 'goku', 'sasuke', 'levi', 'eren', 'itachi', 'zoro'];

function checkNameEasterEgg(playerName) {
  return SPECIAL_NAMES.includes(playerName.toLowerCase().trim());
}


// ===== PATCH: Music on victory, hints, achievements, particles =====
const _origShowResult = typeof showRoundResult === 'function' ? showRoundResult : null;
const _origProcessElim = typeof processElimination === 'function' ? processElimination : null;
const _origDismissCard = typeof dismissCard === 'function' ? dismissCard : null;
const _origContinueAfterElim = typeof continueAfterElimination === 'function' ? continueAfterElimination : null;

// Wrap showRoundResult to add music + particles
if (_origShowResult) {
  const _saved_showRoundResult = showRoundResult;
  showRoundResult = function(winnerType) {
    _saved_showRoundResult(winnerType);
    if (winnerType === 'civil') {
      try { MusicEngine.victoryCivils(); } catch(e) {}
      spawnConfetti(40);
    } else {
      try { MusicEngine.victoryUndercover(); } catch(e) {}
      spawnFlames(30);
    }
    // Track achievements
    const stats = JSON.parse(localStorage.getItem('uc_stats') || '{"games":0,"rounds":0,"modes":[]}');
    stats.rounds = (stats.rounds || 0) + 1;
    if (stats.rounds >= 100) unlockAchievement('hundred_rounds');
    if (!stats.modes) stats.modes = [];
    if (!stats.modes.includes(GameState.currentMode)) stats.modes.push(GameState.currentMode);
    if (stats.modes.length >= GAME_MODES.length) unlockAchievement('all_modes');
    localStorage.setItem('uc_stats', JSON.stringify(stats));
    if (winnerType === 'civil') unlockAchievement('first_win');
    if (winnerType === 'undercover') {
      // Check if any undercover player is still alive
      unlockAchievement('undercover_win');
    }
    if (GameState.blindMode && winnerType === 'civil') unlockAchievement('blind_win');
  };
}

// Wrap processElimination to show hint
if (_origProcessElim) {
  const _saved_processElim = processElimination;
  processElimination = function() {
    _saved_processElim();
    showHintForPair(GameState.currentPair);
  };
}

// Wrap dismissCard for name easter egg
if (_origDismissCard) {
  const _saved_dismissCard = dismissCard;
  dismissCard = function() {
    // Check easter egg before dismiss
    const overlay = document.getElementById('card-overlay');
    const pi = parseInt(overlay.dataset.playerIndex);
    const player = GameState.players[pi];
    if (player && checkNameEasterEgg(player.name)) {
      const card = document.getElementById('role-card');
      if (card) card.classList.add('special-reveal');
      setTimeout(() => { if (card) card.classList.remove('special-reveal'); }, 1000);
    }
    _saved_dismissCard();
  };
}

// Konami achievement
const _origKonami = document.body.classList;
const konamiObserver = new MutationObserver(() => {
  if (document.body.classList.contains('rainbow-mode')) {
    unlockAchievement('konami');
  }
});
konamiObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });

// Init achieve count on load
document.addEventListener('DOMContentLoaded', () => {
  updateAchieveCount();
  // Track game count
  const stats = JSON.parse(localStorage.getItem('uc_stats') || '{"games":0,"rounds":0,"modes":[]}');
  stats.games = (stats.games || 0) + 1;
  if (stats.games >= 10) unlockAchievement('ten_games');
  localStorage.setItem('uc_stats', JSON.stringify(stats));
});
"""

# Insert JS additions BEFORE the closing </script>
html = html.replace("</script>", JS_ADDITIONS + "\n</script>")

# ═══════════════════════════════════════════════════════════
# 4. ALSO PATCH: existing SFX to use sfxVolume
# ═══════════════════════════════════════════════════════════
# Wrap the SFX gain to respect sfxVolume
html = html.replace(
    "gain.connect(c.destination);",
    "gain.gain.value *= (typeof MusicEngine !== 'undefined' ? MusicEngine.sfxVolume : 0.8); gain.connect(c.destination);",
    10  # only first 10 occurrences in SFX section
)

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print("V3 patch applied successfully!")
print(f"  Template size: {len(html)} chars ({len(html)//1024} KB)")
