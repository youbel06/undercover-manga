#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ts = str(int(time.time()))
    host = browser.new_context().new_page()
    guest = browser.new_context().new_page()

    for pg in [host, guest]:
        pg.goto("https://youbel06.github.io/undercover-manga/")
        pg.wait_for_timeout(3000)
        pg.evaluate('()=>{localStorage.clear();localStorage.setItem("uc_tutorial_done","true");var t=document.getElementById("tutorial-overlay");if(t)t.classList.remove("visible")}')

    host.evaluate('()=>showScreen("screen-mp-menu")')
    host.wait_for_timeout(3000)
    host.evaluate('()=>new Promise(async r=>{await mpCreateProfile("H'+ts+'");r()})')
    host.wait_for_timeout(1000)
    guest.evaluate('()=>showScreen("screen-mp-menu")')
    guest.wait_for_timeout(3000)
    guest.evaluate('()=>new Promise(async r=>{await mpCreateProfile("G'+ts+'");r()})')
    guest.wait_for_timeout(1000)

    host.evaluate('()=>new Promise(async r=>{await mpCreateRoom();r()})')
    host.wait_for_timeout(2000)
    code = host.evaluate('()=>mpRoomCode')
    room_id = host.evaluate('()=>mpRoomId')
    print(f"Room: {code} ({room_id})")

    # Guest manual join with error capture
    guest.evaluate(f'()=>document.getElementById("mp-join-code").value="{code}"')
    result = guest.evaluate("""()=>new Promise(async function(resolve) {
        try {
            var code = document.getElementById("mp-join-code").value.toUpperCase().trim();
            var roomRes = await sb.from("rooms").select("*").eq("code", code).eq("status", "waiting").single();
            if (!roomRes.data) { resolve({step:"room", err:"not found"}); return; }
            var pRes = await sb.from("players").select("username,avatar_emoji").eq("id", mpPlayerId).single();
            var insertRes = await sb.from("room_players").insert({
                room_id: roomRes.data.id, player_id: mpPlayerId,
                username: pRes.data ? pRes.data.username : "Guest",
                is_host: false, is_ready: false
            });
            resolve({step:"insert", error: insertRes.error ? JSON.stringify(insertRes.error) : null, ok: !insertRes.error});
        } catch(e) { resolve({step:"catch", err:e.message}); }
    })""")
    print(f"Guest insert: {result}")

    # Check DB directly
    db = host.evaluate("""()=>new Promise(async function(r) {
        var res = await sb.from("room_players").select("player_id,username").eq("room_id", mpRoomId);
        r({count: res.data ? res.data.length : 0, players: res.data, error: res.error ? JSON.stringify(res.error) : null});
    })""")
    print(f"DB players: {db}")

    host.evaluate('()=>mpLeaveRoom().catch(function(){})')
    host.wait_for_timeout(500)
    browser.close()
