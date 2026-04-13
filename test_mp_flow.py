#!/usr/bin/env python3
"""Detailed MP flow debug."""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ts = str(int(time.time()))
    host = browser.new_context().new_page()
    guest = browser.new_context().new_page()
    h_console = []
    host.on("console", lambda m: h_console.append(m.text))
    g_console = []
    guest.on("console", lambda m: g_console.append(m.text))

    for pg in [host, guest]:
        pg.goto("https://youbel06.github.io/undercover-manga/")
        pg.wait_for_timeout(3000)
        pg.evaluate('()=>{localStorage.clear();localStorage.setItem("uc_tutorial_done","true");var t=document.getElementById("tutorial-overlay");if(t)t.classList.remove("visible")}')

    host.evaluate('()=>showScreen("screen-mp-menu")'); host.wait_for_timeout(3000)
    host.evaluate('()=>new Promise(async r=>{await mpCreateProfile("H'+ts+'");r()})'); host.wait_for_timeout(1000)
    guest.evaluate('()=>showScreen("screen-mp-menu")'); guest.wait_for_timeout(3000)
    guest.evaluate('()=>new Promise(async r=>{await mpCreateProfile("G'+ts+'");r()})'); guest.wait_for_timeout(1000)

    # Create + join
    host.evaluate('()=>new Promise(async r=>{await mpCreateRoom();r()})'); host.wait_for_timeout(2000)
    code = host.evaluate('()=>mpRoomCode')
    room_id = host.evaluate('()=>mpRoomId')
    print(f"Room: {code}")

    guest.evaluate(f'()=>document.getElementById("mp-join-code").value="{code}"')
    guest.evaluate('()=>new Promise(async r=>{await mpJoinRoom();r()})'); guest.wait_for_timeout(2000)

    # DB verify
    db = host.evaluate("""()=>new Promise(async function(r) {
        var res = await sb.from("room_players").select("username").eq("room_id", mpRoomId);
        r(res.data ? res.data.length : -1);
    })""")
    print(f"DB players: {db}")

    # Force lobby refresh
    host.evaluate("()=>renderMpLobby()")
    host.wait_for_timeout(2000)
    hp = host.evaluate('()=>document.querySelectorAll(".mp-player-row").length')
    print(f"Host lobby rows: {hp}")

    # Ready + start
    guest.evaluate('()=>mpToggleReady()'); guest.wait_for_timeout(1000)

    # Add extensive logging to mpStartGame
    host.evaluate("""()=>{
        var orig = mpStartGame;
        mpStartGame = async function() {
            console.log("=== MPSTART BEGIN ===");
            var res = await sb.from("room_players").select("*").eq("room_id", mpRoomId);
            console.log("Players in DB: " + (res.data ? res.data.length : "null"));
            if (res.data) res.data.forEach(function(p) { console.log("  Player: " + p.username); });
            await orig();
            console.log("=== MPSTART END ===");
            console.log("Screen: " + (document.querySelector(".screen.active") || {}).id);
            var content = document.getElementById("mp-game-content");
            console.log("Content: " + (content ? content.innerHTML.substring(0, 100) : "NULL"));
        };
    }""")

    host.evaluate('()=>new Promise(async r=>{await mpStartGame();r()})'); host.wait_for_timeout(5000)

    # Results
    h_screen = host.evaluate('()=>document.querySelector(".screen.active")?.id')
    h_content = host.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,100) || "EMPTY"')
    g_screen = guest.evaluate('()=>document.querySelector(".screen.active")?.id')
    g_content = guest.evaluate('()=>document.getElementById("mp-game-content")?.innerText?.substring(0,100) || "EMPTY"')

    print(f"\nHost: screen={h_screen}, content={h_content[:60]}")
    print(f"Guest: screen={g_screen}, content={g_content[:60]}")

    print("\nHost console:")
    for c in h_console[-15:]: print(f"  {c[:100]}")

    print("\nGuest console:")
    for c in g_console[-5:]: print(f"  {c[:100]}")

    host.evaluate('()=>mpLeaveRoom().catch(function(){})'); host.wait_for_timeout(500)
    browser.close()
