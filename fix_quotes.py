#!/usr/bin/env python3
"""Fix all JS string quoting issues in multiplayer code."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix onclick with inner single quotes inside JS single-quoted strings
html = html.replace(
    """onclick="mpAdvancePhase('vote')" """,
    """onclick="mpAdvancePhase(&apos;vote&apos;)" """
)

html = html.replace(
    """onclick="mpVoteFor('""",
    """onclick="mpVoteFor(&apos;"""
)

html = html.replace(
    """')" style=""",
    """&apos;)" style="""
)

# Fix remaining J'ai in JS strings (in multiplayer section)
# Find the specific line
lines = html.split("\n")
fixed_lines = []
for line in lines:
    # Only fix lines that are clearly inside JS string assignments (content.innerHTML = '...')
    if "content.innerHTML" in line or "innerHTML =" in line or "innerHTML +" in line:
        # Don't touch HTML attributes, only JS string contents
        pass
    # Fix French apostrophes in JS single-quoted strings
    # Heuristic: if line has innerHTML and contains unescaped French words
    if ("innerHTML" in line or "'+'" in line) and "J'ai" in line:
        line = line.replace("J'ai", "J\\'ai")
    if ("innerHTML" in line or "'+'" in line) and "L'Undercover" in line:
        line = line.replace("L'Undercover", "L\\'Undercover")
    if ("innerHTML" in line or "'+'" in line) and "L'hôte" in line:
        line = line.replace("L'hôte", "L\\'hôte")
    if ("innerHTML" in line or "'+'" in line) and "l'hôte" in line:
        line = line.replace("l'hôte", "l\\'hôte")
    if ("innerHTML" in line or "'+'" in line) and "n'a " in line:
        line = line.replace("n'a ", "n\\'a ")
    if ("innerHTML" in line or "'+'" in line) and "d'un" in line:
        line = line.replace("d'un", "d\\'un")
    fixed_lines.append(line)

html = "\n".join(fixed_lines)

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Quotes fixed!")
