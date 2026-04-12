#!/usr/bin/env python3
"""Complete music system rewrite."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove old audio panel HTML and replace with simpler one
html = html.replace(
    """<div class="audio-float" id="audio-float">
  <button class="audio-float-btn" id="audio-toggle-btn" onclick="toggleAudioPanel()" aria-label="Audio">🔊</button>
  <div class="audio-panel" id="audio-panel">
    <label>🎵 Musique <span id="music-vol-label">70%</span></label>
    <input type="range" id="music-volume" min="0" max="100" value="70" oninput="setMusicVolume(this.value)">
    <label>🔊 Effets <span id="sfx-vol-label">80%</span></label>
    <input type="range" id="sfx-volume" min="0" max="100" value="80" oninput="setSfxVolume(this.value)">
  </div>
</div>""",
    """<div class="audio-float" id="audio-float">
  <button class="audio-float-btn" id="music-btn" onclick="musicTap()" aria-label="Audio">🔊</button>
</div>
<div class="music-modal" id="music-modal">
  <div class="music-modal-card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <span style="font-weight:700;color:var(--text-bright)">🎵 Musique</span>
      <button onclick="closeMusicModal()" style="background:none;border:none;color:var(--text-muted);font-size:1.2rem;cursor:pointer">✕</button>
    </div>
    <div id="music-track-name" style="font-size:0.9rem;color:var(--accent-gold);margin-bottom:10px;text-align:center">—</div>
    <div style="display:flex;gap:12px;justify-content:center;margin-bottom:14px">
      <button onclick="MusicPlayer.prev()" class="btn btn-ghost" style="min-height:40px;padding:8px 14px">⏮</button>
      <button onclick="MusicPlayer.togglePlay()" class="btn btn-primary" id="music-play-btn" style="min-height:40px;padding:8px 20px">▶</button>
      <button onclick="MusicPlayer.next()" class="btn btn-ghost" style="min-height:40px;padding:8px 14px">⏭</button>
    </div>
    <label style="font-size:0.8rem;color:var(--text-muted);display:flex;justify-content:space-between"><span>🎵 Musique</span><span id="mvol-label">30%</span></label>
    <input type="range" id="mvol-slider" min="0" max="100" value="30" oninput="MusicPlayer.setVolume(this.value/100);document.getElementById('mvol-label').textContent=this.value+'%'" style="width:100%;margin:4px 0 12px">
    <label style="font-size:0.8rem;color:var(--text-muted);display:flex;justify-content:space-between"><span>🔊 Effets</span><span id="svol-label">80%</span></label>
    <input type="range" id="svol-slider" min="0" max="100" value="80" oninput="SfxVolume=this.value/100;localStorage.setItem('uc_sfx_vol',this.value/100);document.getElementById('svol-label').textContent=this.value+'%'" style="width:100%;margin:4px 0">
  </div>
</div>"""
)

# Add CSS for music modal
html = html.replace(
    "/* ===== APP CONTAINER ===== */",
    """/* ===== MUSIC MODAL ===== */
.music-modal{position:fixed;top:0;left:0;width:100%;height:100%;z-index:500;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.2s}
.music-modal.open{opacity:1;pointer-events:auto}
.music-modal-card{background:var(--bg-secondary);border:1px solid var(--border-glass);border-radius:var(--radius-xl);padding:20px;max-width:300px;width:90%}
.music-modal-card input[type=range]{-webkit-appearance:none;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none}
.music-modal-card input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:var(--accent-gold);cursor:pointer}

/* ===== APP CONTAINER ===== */"""
)

# Replace the entire MusicPlayer and related functions at the end of script
MUSIC_JS = r"""

// ===== DEFINITIVE MUSIC PLAYER =====
var SfxVolume = parseFloat(localStorage.getItem('uc_sfx_vol') || '0.8');

var MusicPlayer = {
  audio: null,
  tracks: [
    {name: "Lofi Chill", url: "https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3"},
    {name: "Relaxing", url: "https://cdn.pixabay.com/audio/2024/11/01/audio_ffd7183e41.mp3"},
    {name: "Peaceful", url: "https://cdn.pixabay.com/audio/2022/10/25/audio_102b42dae5.mp3"},
  ],
  idx: 0,
  vol: 0.3,
  stopped: true,

  init: function() {
    if (this.audio) return;
    this.audio = new Audio();
    this.audio.loop = false;
    var self = this;
    this.audio.addEventListener('ended', function() { self.next(); });
    try {
      var s = JSON.parse(localStorage.getItem('uc_mp_settings') || '{}');
      if (s.vol !== undefined) this.vol = s.vol;
      if (s.stopped !== undefined) this.stopped = s.stopped;
    } catch(e) {}
    this.audio.volume = this.vol;
  },

  play: function(i) {
    this.init();
    if (i !== undefined) this.idx = i % this.tracks.length;
    this.audio.src = this.tracks[this.idx].url;
    this.audio.volume = this.vol;
    this.stopped = false;
    this.audio.play().catch(function(){});
    this._save(); this._ui();
  },

  togglePlay: function() {
    this.init();
    if (!this.audio.src || this.stopped) { this.play(); return; }
    if (this.audio.paused) { this.stopped = false; this.audio.play().catch(function(){}); }
    else { this.stopped = true; this.audio.pause(); }
    this._save(); this._ui();
  },

  next: function() { this.play((this.idx + 1) % this.tracks.length); },
  prev: function() { this.play((this.idx - 1 + this.tracks.length) % this.tracks.length); },

  setVolume: function(v) {
    this.vol = v;
    if (this.audio) this.audio.volume = v;
    this._save(); this._ui();
  },

  _save: function() {
    try { localStorage.setItem('uc_mp_settings', JSON.stringify({vol: this.vol, stopped: this.stopped})); } catch(e) {}
  },

  _ui: function() {
    var btn = document.getElementById('music-btn');
    if (btn) btn.textContent = this.stopped ? '🔇' : '🔊';
    var tn = document.getElementById('music-track-name');
    if (tn) tn.textContent = this.tracks[this.idx].name;
    var pb = document.getElementById('music-play-btn');
    if (pb) pb.textContent = (this.audio && !this.audio.paused && !this.stopped) ? '⏸' : '▶';
    var vs = document.getElementById('mvol-slider');
    if (vs) vs.value = Math.round(this.vol * 100);
    var vl = document.getElementById('mvol-label');
    if (vl) vl.textContent = Math.round(this.vol * 100) + '%';
  }
};

// Tap = mute/unmute, Long press = open modal
var _musicTapTimer = null;
function musicTap() {
  // Simple: toggle play/pause on tap
  MusicPlayer.init();
  MusicPlayer.togglePlay();
}

// Open modal on settings icon or long press
function openMusicModal() {
  MusicPlayer.init();
  MusicPlayer._ui();
  document.getElementById('music-modal').classList.add('open');
  var ss = document.getElementById('svol-slider');
  if (ss) { ss.value = Math.round(SfxVolume * 100); document.getElementById('svol-label').textContent = Math.round(SfxVolume * 100) + '%'; }
}
function closeMusicModal() { document.getElementById('music-modal').classList.remove('open'); }

// Close modal on backdrop click
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('music-modal')) closeMusicModal();
});

// Add music button to settings
document.addEventListener('DOMContentLoaded', function() {
  // Override the settings gear to also allow music access
  var settingsBtn = document.querySelector('.splash-settings-btn');
  if (settingsBtn) {
    settingsBtn.addEventListener('long-press', function() { openMusicModal(); });
  }
});

// Auto-play on first interaction (if not stopped)
document.addEventListener('click', function() {
  MusicPlayer.init();
  if (!MusicPlayer.stopped && (!MusicPlayer.audio || MusicPlayer.audio.paused)) {
    MusicPlayer.play();
  }
}, { once: true });

// Override old functions to prevent errors
function toggleAudioPanel() { openMusicModal(); }
function setMusicVolume(v) { MusicPlayer.setVolume(v / 100); }
function setSfxVolume(v) { SfxVolume = v / 100; localStorage.setItem('uc_sfx_vol', v / 100); }
function updateAudioIcon() { MusicPlayer._ui(); }
function toggleMusicPlay() { MusicPlayer.togglePlay(); }
function lofiNext() { MusicPlayer.next(); }
function lofiPrev() { MusicPlayer.prev(); }
function updateMiniTitle() { MusicPlayer._ui(); }
function toggleMusicExpanded() { openMusicModal(); }
"""

html = html.replace("\n</script>", MUSIC_JS + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Music system rewritten!")
