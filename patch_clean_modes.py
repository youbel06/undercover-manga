#!/usr/bin/env python3
"""CLEAN REWRITE: Remove all getAvailablePairs/selectRandomPair overrides."""

with open("game_template.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find and remove override blocks
remove_ranges = []
i = 0
while i < len(lines):
    line = lines[i]
    # Remove getAvailablePairs overrides (NOT the original function)
    if 'getAvailablePairs = function()' in line and 'const ' in lines[max(0,i-1)]:
        # Find the end of this override block
        start = i - 1  # include the const line
        brace_count = 0
        j = i
        while j < len(lines):
            brace_count += lines[j].count('{') - lines[j].count('}')
            if brace_count <= 0 and j > i:
                remove_ranges.append((start, j + 1))
                break
            j += 1
        i = j + 1
        continue

    # Remove modeFilterModes-related overrides
    if 'const _origApplyModeFilter = applyModeFilter;' in line:
        start = i
        brace_count = 0
        j = i + 1
        while j < len(lines):
            if 'getAvailablePairs = function()' in lines[j]:
                # This is part of the same block, skip to end
                pass
            brace_count += lines[j].count('{') - lines[j].count('}')
            if '};' in lines[j] and brace_count <= 0:
                remove_ranges.append((start, j + 1))
                break
            j += 1
        i = j + 1
        continue

    i += 1

# Sort and remove from bottom to top
remove_ranges.sort(reverse=True)
for start, end in remove_ranges:
    print(f"Removing lines {start+1}-{end}: {lines[start].strip()[:60]}...")
    lines[start:end] = [f"// [REMOVED] override at line {start+1}\n"]

# Now find and replace the ORIGINAL getAvailablePairs
new_func = """function getAvailablePairs() {
  var mode = GameState.currentMode || 'normal';
  var recent = GameState.recentPairKeys || [];

  if (mode === 'tout_melanger' || mode === 'mixte_total') {
    var all = PAIRS.filter(function(p) {
      return recent.indexOf(pairKey(p)) === -1;
    });
    if (all.length < 5) { GameState.recentPairKeys = []; return PAIRS.slice(); }
    return all;
  }

  var filtered = PAIRS.filter(function(p) {
    return (p.mode || 'normal') === mode && recent.indexOf(pairKey(p)) === -1;
  });

  if (filtered.length < 5) {
    GameState.recentPairKeys = [];
    filtered = PAIRS.filter(function(p) { return (p.mode || 'normal') === mode; });
  }

  if (filtered.length === 0) {
    console.error('[MODE] No pairs for mode:', mode);
    return PAIRS.slice();
  }

  return filtered;
}
"""

# Find the original function
for i, line in enumerate(lines):
    if 'function getAvailablePairs()' in line and 'override' not in line.lower() and 'REMOVED' not in line:
        # Find end of function
        brace_count = 0
        j = i
        while j < len(lines):
            brace_count += lines[j].count('{') - lines[j].count('}')
            if brace_count <= 0 and j > i:
                lines[i:j+1] = [new_func + "\n"]
                print(f"Replaced original getAvailablePairs at line {i+1}")
                break
            j += 1
        break

# Also remove the selectRandomPair override (keep original only)
for i, line in enumerate(lines):
    if 'selectRandomPair = function()' in line:
        start = i
        brace_count = 0
        j = i
        while j < len(lines):
            brace_count += lines[j].count('{') - lines[j].count('}')
            if brace_count <= 0 and j > i:
                lines[start:j+1] = [f"// [REMOVED] selectRandomPair override at line {start+1}\n"]
                print(f"Removed selectRandomPair override at line {start+1}")
                break
            j += 1
        break

html = "".join(lines)

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

# Verify
count = html.count("getAvailablePairs")
print(f"\ngetAvailablePairs occurrences remaining: {count}")
