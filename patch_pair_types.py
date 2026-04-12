#!/usr/bin/env python3
"""Add pair_type rotation logic + similarity hint display."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add pair_type classification for existing pairs that don't have it
# and the rotation selection logic
JS = r"""

// ===== PAIR TYPE ROTATION (33/33/33) =====
// Classify pairs that don't have pair_type yet
PAIRS.forEach(function(p) {
  if (p.pair_type) return;
  if (p.universe1 === p.universe2) p.pair_type = "intra";
  else p.pair_type = "inter";
});

// Track last pair types for rotation
function getLastPairTypes() {
  try { return JSON.parse(localStorage.getItem("uc_last_pair_types") || "[]"); } catch(e) { return []; }
}
function saveLastPairType(type) {
  var last = getLastPairTypes();
  last.push(type);
  if (last.length > 5) last = last.slice(-5);
  try { localStorage.setItem("uc_last_pair_types", JSON.stringify(last)); } catch(e) {}
}

// Override selectRandomPair to use rotation
var _origSelectRandomPairRot = selectRandomPair;
selectRandomPair = function() {
  var available = getAvailablePairs();
  if (available.length === 0) {
    GameState.recentPairKeys = [];
    localStorage.setItem("uc_recent_pairs", "[]");
    available = getAvailablePairs();
  }
  if (available.length === 0) return _origSelectRandomPairRot();

  // Determine target type based on rotation
  var last = getLastPairTypes();
  var counts = {intra: 0, inter: 0, decale: 0};
  last.forEach(function(t) { if (counts[t] !== undefined) counts[t]++; });

  // Find the least-played type
  var types = ["intra", "inter", "decale"];
  types.sort(function(a, b) { return counts[a] - counts[b]; });
  var targetType = types[0];

  // Don't play same type twice in a row
  if (last.length > 0 && last[last.length - 1] === targetType) {
    targetType = types[1] || types[0];
  }

  // Filter available pairs by target type
  var typed = available.filter(function(p) { return p.pair_type === targetType; });
  if (typed.length === 0) {
    // Fallback: any type except last played
    typed = available.filter(function(p) { return last.length === 0 || p.pair_type !== last[last.length - 1]; });
    if (typed.length === 0) typed = available;
  }

  var pair = typed[Math.floor(Math.random() * typed.length)];

  // Track
  var key = pairKey(pair);
  GameState.recentPairKeys.push(key);
  if (GameState.recentPairKeys.length > 20) GameState.recentPairKeys = GameState.recentPairKeys.slice(-20);
  try { localStorage.setItem("uc_recent_pairs", JSON.stringify(GameState.recentPairKeys)); } catch(e) {}
  saveLastPairType(pair.pair_type || "inter");

  return pair;
};

// Enhanced hint display: show similarity + pair type badge
var _origShowHint = showHintForPair;
showHintForPair = function(pair) {
  var hintBox = document.getElementById("hint-box");
  var hintText = document.getElementById("hint-text");
  if (!hintBox || !hintText || !pair) return;

  var similarity = pair.similarity || pair.hint || "";
  var typeLabel = pair.pair_type === "decale" ? "🎭 Paire décalée" :
                  pair.pair_type === "intra" ? "🔗 Même univers" : "🌐 Cross-univers";

  hintText.innerHTML = "<div style='font-size:0.65rem;color:var(--accent-gold);margin-bottom:4px'>" + typeLabel + "</div>" +
    "<div>💡 " + similarity + "</div>";
  hintBox.style.display = "block";
};
"""

html = html.replace("\n</script>", JS + "\n</script>")

# Also update build.py to include pair_type and similarity in JSON
with open("build.py", "r", encoding="utf-8") as f:
    build = f.read()

build = build.replace(
    '"hint": p.get("hint", ""),',
    '"hint": p.get("hint", ""),\n            "pair_type": p.get("pair_type", "inter"),\n            "similarity": p.get("similarity", p.get("hint", "")),'
)

with open("build.py", "w", encoding="utf-8") as f:
    f.write(build)

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Pair type rotation + hint display added!")
