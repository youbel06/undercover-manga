#!/usr/bin/env python3
"""Final music fix: remove old systems, fix mini player, add settings sliders."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. Remove old mini player HTML (music-fab + music-expanded)
# ═══════════════════════════════════════════════════════════
html = html.replace(
    '<!-- ===== MUSIC MINI PLAYER ===== -->\n'
    '<div class="music-fab" id="music-fab" onclick="toggleMusicExpanded()">🎵</div>\n'
    '<div class="music-expanded" id="music-expanded">\n'
    '  <button onclick="lofiPrev()">⏮</button>\n'
    '  <button id="music-play-btn" onclick="toggleMusicPlay()">▶</button>\n'
    '  <span class="me-title" id="me-title">—</span>\n'
    '  <button onclick="lofiNext()">⏭</button>\n'
    '</div>',
    '<!-- mini player removed, using music-modal instead -->'
)
print("1. Removed old mini player HTML")

# ═══════════════════════════════════════════════════════════
# 2. Add audio sliders to settings screen
# ═══════════════════════════════════════════════════════════
# Find the blind mode toggle in settings and add sliders before it
html = html.replace(
    '<div class="settings-group" style="margin-top:12px;">\n'
    '        <label class="settings-label">Mode Aveugle (noms cachés)</label>',
    '<div class="settings-group" style="margin-top:12px;">\n'
    '        <label class="settings-label">🎵 Volume Musique</label>\n'
    '        <input type="range" min="0" max="100" id="slider-music-vol" value="30"\n'
    '          oninput="MusicPlayer.setVolume(this.value/100)" style="width:100%;margin-bottom:10px">\n'
    '        <label class="settings-label">🔊 Volume Effets</label>\n'
    '        <input type="range" min="0" max="100" id="slider-sfx-vol" value="80"\n'
    '          oninput="SfxGlobalVol=this.value/100;localStorage.setItem(\'uc_sfx_vol\',SfxGlobalVol)" style="width:100%;margin-bottom:10px">\n'
    '      </div>\n'
    '      <div class="settings-group" style="margin-top:12px;">\n'
    '        <label class="settings-label">Mode Aveugle (noms cachés)</label>'
)
print("2. Added audio sliders to settings")

# ═══════════════════════════════════════════════════════════
# 3. JS: Initialize settings sliders when settings screen opens
# ═══════════════════════════════════════════════════════════
INIT_SLIDERS_JS = r"""

// ===== INIT AUDIO SLIDERS ON SETTINGS SCREEN =====
var SfxGlobalVol = parseFloat(localStorage.getItem('uc_sfx_vol') || '0.8');

var _origRenderSettingsFinal = renderSettings;
renderSettings = function() {
  _origRenderSettingsFinal();
  // Init sliders
  var ms = document.getElementById('slider-music-vol');
  if (ms) ms.value = Math.round((MusicPlayer.vol || 0.3) * 100);
  var ss = document.getElementById('slider-sfx-vol');
  if (ss) ss.value = Math.round(SfxGlobalVol * 100);
};

// Make SFX respect global volume
var _origSfxClick = SoundFX.click;
SoundFX.click = function() {
  if (SfxGlobalVol <= 0.01) return;
  try { _origSfxClick(); } catch(e) {}
};
var _origSfxReveal = SoundFX.reveal;
SoundFX.reveal = function() { if (SfxGlobalVol <= 0.01) return; try { _origSfxReveal(); } catch(e) {} };
var _origSfxElim = SoundFX.eliminate;
SoundFX.eliminate = function() { if (SfxGlobalVol <= 0.01) return; try { _origSfxElim(); } catch(e) {} };
var _origSfxVict = SoundFX.victory;
SoundFX.victory = function() { if (SfxGlobalVol <= 0.01) return; try { _origSfxVict(); } catch(e) {} };
var _origSfxSusp = SoundFX.suspense;
SoundFX.suspense = function() { if (SfxGlobalVol <= 0.01) return; try { _origSfxSusp(); } catch(e) {} };

// Disable ALL old music systems to prevent interference
MusicEngine.stop = function() {};
MusicEngine.lobby = function() {};
MusicEngine.suspense = function() {};
MusicEngine.victoryCivils = function() {};
MusicEngine.victoryUndercover = function() {};
MusicEngine.reveal = function() {};
if (typeof LofiPlayer !== 'undefined') {
  LofiPlayer.play = function() {};
  LofiPlayer.stop = function() {};
  LofiPlayer.next = function() {};
  LofiPlayer.prev = function() {};
}
if (typeof LofiPlayerV9 !== 'undefined') {
  LofiPlayerV9.play = function() {};
  LofiPlayerV9.stop = function() {};
}
"""

html = html.replace("\n</script>", INIT_SLIDERS_JS + "\n</script>")
print("3. Added slider init + disabled old music systems")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("\nDone!")
