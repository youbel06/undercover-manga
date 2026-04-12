#!/usr/bin/env python3
"""Fix: role reveal logic, mode filtering fallback, lobby min players, music."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# FIX 1: Role reveal — hide CIVIL/UNDERCOVER label
# ═══════════════════════════════════════════════════════════
# In local game: revealPlayerRole shows role label
# Change to only show the character name, not the role

# Local game reveal
html = html.replace(
    "document.getElementById('card-role-label').textContent = 'Civil';",
    "document.getElementById('card-role-label').textContent = '';"
)
html = html.replace(
    "document.getElementById('card-role-label').textContent = 'Undercover';",
    "document.getElementById('card-role-label').textContent = '';"
)
# Keep Mr. White visible (they need to know they have no word)
# html Mr. White label stays

# Multiplayer reveal: remove role labels
html = html.replace(
    """+"<div style='font-size:0.9rem;color:"+rc+";margin-top:6px'>"+rl+"</div></div>"+""",
    """+"</div>"+"""
)

print("FIX 1: Role labels hidden during reveal")

# ═══════════════════════════════════════════════════════════
# FIX 2: Mode filtering fallback — keep mode filter on reset
# ═══════════════════════════════════════════════════════════
html = html.replace(
    """    available = PAIRS.filter(p => {
      if (GameState.enabledUniverses.size === 0) return true;
      return GameState.enabledUniverses.has(p.universe1) || GameState.enabledUniverses.has(p.universe2);
    });""",
    """    // Retry with mode filter (not universe filter)
    var mode = GameState.currentMode;
    if (mode === 'tout_melanger') {
      available = PAIRS.slice();
    } else {
      available = PAIRS.filter(function(p) { return (p.mode || 'normal') === mode; });
    }
    if (available.length === 0) available = PAIRS.slice();"""
)
print("FIX 2: Mode filtering fallback fixed")

# ═══════════════════════════════════════════════════════════
# FIX 3: Lobby — allow 2 players to start
# ═══════════════════════════════════════════════════════════
# Check renderMpLobby for the start button condition
html = html.replace(
    "allReady && players.length >= 3",
    "allReady && players.length >= 2"
)
print("FIX 3: Min 2 players to start (lobby button)")

# ═══════════════════════════════════════════════════════════
# FIX 4: Music — replace proceedural with simple Audio player
# ═══════════════════════════════════════════════════════════
# Add a simple audio system using free music URLs
MUSIC_JS = r"""

// ===== SIMPLE MUSIC PLAYER (replaces procedural) =====
var MusicPlayer = {
  tracks: [
    {name: "Lofi Study", url: "https://cdn.pixabay.com/audio/2024/11/01/audio_ffd7183e41.mp3"},
    {name: "Chill Vibes", url: "https://cdn.pixabay.com/audio/2022/10/25/audio_102b42dae5.mp3"},
    {name: "Aesthetic", url: "https://cdn.pixabay.com/audio/2024/09/10/audio_6e56242e42.mp3"},
  ],
  audio: null,
  currentIndex: 0,
  volume: 0.5,
  muted: false,
  userStopped: false,

  init: function() {
    this.volume = parseFloat(localStorage.getItem("uc_music_vol") || "0.5");
    this.muted = localStorage.getItem("uc_music_muted") === "true";
    this.audio = new Audio();
    this.audio.loop = false;
    this.audio.volume = this.muted ? 0 : this.volume;
    var self = this;
    this.audio.addEventListener("ended", function() { self.next(); });
  },

  play: function() {
    if (this.userStopped) return;
    if (!this.audio) this.init();
    var track = this.tracks[this.currentIndex % this.tracks.length];
    this.audio.src = track.url;
    this.audio.volume = this.muted ? 0 : this.volume;
    this.audio.play().catch(function() {});
    this.updateUI();
  },

  stop: function() {
    if (this.audio) { this.audio.pause(); this.audio.currentTime = 0; }
    this.userStopped = true;
    this.updateUI();
  },

  next: function() {
    this.currentIndex = (this.currentIndex + 1) % this.tracks.length;
    this.userStopped = false;
    this.play();
  },

  prev: function() {
    this.currentIndex = (this.currentIndex - 1 + this.tracks.length) % this.tracks.length;
    this.userStopped = false;
    this.play();
  },

  toggleMute: function() {
    this.muted = !this.muted;
    if (this.audio) this.audio.volume = this.muted ? 0 : this.volume;
    localStorage.setItem("uc_music_muted", this.muted);
    this.updateUI();
  },

  setVolume: function(v) {
    this.volume = v;
    if (this.audio && !this.muted) this.audio.volume = v;
    localStorage.setItem("uc_music_vol", v);
  },

  get currentName() {
    return this.tracks[this.currentIndex % this.tracks.length].name;
  },

  get playing() {
    return this.audio && !this.audio.paused && !this.userStopped;
  },

  updateUI: function() {
    var btn = document.getElementById("audio-toggle-btn");
    if (btn) btn.textContent = this.muted ? "🔇" : (this.playing ? "🔊" : "🔈");
    var title = document.getElementById("me-title");
    if (title) title.textContent = this.playing ? this.currentName : "—";
    var fab = document.getElementById("music-fab");
    if (fab) fab.classList.toggle("playing", this.playing);
  }
};

// Override old music functions
function toggleMusicPlay() {
  if (MusicPlayer.playing) { MusicPlayer.stop(); }
  else { MusicPlayer.userStopped = false; MusicPlayer.play(); }
}
function lofiNext() { SoundFX.click(); MusicPlayer.next(); }
function lofiPrev() { SoundFX.click(); MusicPlayer.prev(); }
function updateMiniTitle() { MusicPlayer.updateUI(); }

// Auto-play on first click (if not muted)
document.addEventListener("click", function() {
  if (!MusicPlayer.muted && !MusicPlayer.userStopped && !MusicPlayer.playing) {
    MusicPlayer.play();
  }
}, { once: true });

// Audio toggle button behavior
var _origToggleAudio = toggleAudioPanel;
toggleAudioPanel = function() {
  MusicPlayer.toggleMute();
};
"""

html = html.replace("\n</script>", MUSIC_JS + "\n</script>")
print("FIX 4: Simple music player with real audio files")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\nAll fixes applied!")
