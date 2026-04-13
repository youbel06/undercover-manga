#!/usr/bin/env python3
"""Full multiplayer simulation using broadcast-only approach."""
from playwright.sync_api import sync_playwright
import time

URL = "https://youbel06.github.io/undercover-manga/"
bugs = []

def ok(m): print(f"  [OK] {m}")
def bug(m): print(f"  [BUG] {m}"); bugs.append(m)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ts = str(int(time.time()))
        host = browser.new_context().new_page()
        guest = browser.new_context().new_page()
        h_err, g_err = [], []
        host.on("pageerror", lambda e: h_err.append(str(e)))
        guest.on("pageerror", lambda e: g_err.append(str(e)))

        for pg in [host, guest]:
            pg.goto(URL); pg.wait_for_timeout(3000)
            pg.evaluate('()=>{localStorage.clear();localStorage.setItem("uc_tutorial_done","true");var t=document.getElementById("tutorial-overlay");if(t)t.classList.remove("visible")}')

        print("=== PHASE 1: CONNEXION ===")
        host.evaluate('()=>showScreen("screen-mp-menu")'); host.wait_for_timeout(3000)
        host.evaluate('()=>new Promise(async r=>{await mpCreateProfile("H'+ts+'");r()})'); host.wait_for_timeout(1000)
        ok("Host") if host.evaluate('()=>!!mpPlayerId') else bug("Host profile")
        guest.evaluate('()=>showScreen("screen-mp-menu")'); guest.wait_for_timeout(3000)
        guest.evaluate('()=>new Promise(async r=>{await mpCreateProfile("G'+ts+'");r()})'); guest.wait_for_timeout(1000)
        ok("Guest") if guest.evaluate('()=>!!mpPlayerId') else bug("Guest profile")

        print("\n=== PHASE 2: SALON ===")
        host.evaluate('()=>new Promise(async r=>{await mpCreateRoom();r()})'); host.wait_for_timeout(2000)
        code = host.evaluate('()=>mpRoomCode')
        ok(f"Room: {code}") if code else bug("No room")
        guest.evaluate(f'()=>document.getElementById("mp-join-code").value="{code}"')
        guest.evaluate('()=>new Promise(async r=>{await mpJoinRoom();r()})'); guest.wait_for_timeout(5000)
        host.wait_for_timeout(3000)
        host.evaluate("()=>renderMpLobby()"); host.wait_for_timeout(3000)
        hp = host.evaluate('()=>document.querySelectorAll(".mp-player-row").length')
        gp = guest.evaluate('()=>document.querySelectorAll(".mp-player-row").length')
        ok(f"Lobby: H={hp} G={gp}") if hp >= 2 else bug(f"Lobby: H={hp} G={gp}")

        print("\n=== PHASE 3: LANCER ===")
        guest.evaluate('()=>mpToggleReady()'); guest.wait_for_timeout(2000)
        host.evaluate('()=>new Promise(async r=>{await mpStartGame();r()})'); host.wait_for_timeout(5000)
        hs = host.evaluate('()=>document.querySelector(".screen.active")?.id')
        hc = host.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,80)||""')
        ok(f"Host: {hs}") if "mp-game" in str(hs) else bug(f"Host: {hs}")
        ok("Host role") if "CIVIL" in hc or "UNDERCOVER" in hc else bug(f"No role: {hc[:40]}")
        guest.wait_for_timeout(5000)
        gc = guest.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,80)||""')
        ok("Guest role") if "CIVIL" in gc or "UNDERCOVER" in gc else bug(f"Guest: {gc[:40]}")

        print("\n=== PHASE 4: DISCUSSION ===")
        # Use new broadcast function names
        host.evaluate('()=>mpHA("discuss")'); host.wait_for_timeout(3000)
        hc2 = host.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,60)||""')
        ok("Discussion") if "Discussion" in hc2 or "indice" in hc2 else bug(f"No discuss: {hc2}")

        print("\n=== PHASE 5: VOTE ===")
        host.evaluate('()=>mpHA("vote")'); host.wait_for_timeout(3000)
        hc3 = host.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,60)||""')
        ok("Vote") if "Vote" in hc3 or "vote" in hc3 else bug(f"No vote: {hc3}")

        h_pid = host.evaluate('()=>mpPlayerId')
        g_pid = guest.evaluate('()=>mpPlayerId')
        # Use new vote function
        host.evaluate(f'()=>mpSV("{g_pid}")'); host.wait_for_timeout(1000)
        guest.evaluate(f'()=>mpSV("{h_pid}")'); guest.wait_for_timeout(3000)
        ok("Votes cast")

        print("\n=== PHASE 6: ÉLIMINATION ===")
        host.evaluate('()=>mpHRV()'); host.wait_for_timeout(3000)
        hc4 = host.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,100)||""')
        ok(f"Elim: {hc4[:50]}") if "limin" in hc4 or "CIVIL" in hc4 or "UNDERCOVER" in hc4 else bug(f"No elim: {hc4[:50]}")

        print("\n=== PHASE 7: RÉSULTAT ===")
        host.evaluate('()=>mpHC()'); host.wait_for_timeout(3000)
        hc5 = host.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,100)||""')
        ok(f"Result: {hc5[:50]}") if "Victoire" in hc5 or "gagne" in hc5 or "Discussion" in hc5 else bug(f"No result: {hc5[:50]}")

        print("\n=== JS ERRORS ===")
        for e in h_err[:3]: print(f"  H: {e[:80]}")
        for e in g_err[:3]: print(f"  G: {e[:80]}")
        if not h_err and not g_err: ok("No JS errors")

        host.evaluate('()=>mpLeaveRoom().catch(function(){})'); host.wait_for_timeout(1000)
        print(f"\n{'='*50}\nSIMULATION: {len(bugs)} bugs")
        for b in bugs: print(f"  - {b}")
        browser.close()
        return len(bugs)

if __name__ == "__main__":
    import sys; sys.exit(main())
