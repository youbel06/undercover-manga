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

    host.evaluate('()=>showScreen("screen-mp-menu")'); host.wait_for_timeout(3000)
    host.evaluate('()=>new Promise(async r=>{await mpCreateProfile("H'+ts+'");r()})'); host.wait_for_timeout(1000)
    guest.evaluate('()=>showScreen("screen-mp-menu")'); guest.wait_for_timeout(3000)
    guest.evaluate('()=>new Promise(async r=>{await mpCreateProfile("G'+ts+'");r()})'); guest.wait_for_timeout(1000)
    host.evaluate('()=>new Promise(async r=>{await mpCreateRoom();r()})'); host.wait_for_timeout(2000)
    code = host.evaluate('()=>mpRoomCode')
    guest.evaluate(f'()=>document.getElementById("mp-join-code").value="{code}"')
    guest.evaluate('()=>new Promise(async r=>{await mpJoinRoom();r()})'); guest.wait_for_timeout(5000)

    # Direct query comparison
    q1 = host.evaluate("""()=>new Promise(async function(r) {
        var res = await sb.from("room_players").select("id,room_id,player_id,username,avatar_emoji,is_ready,is_host,joined_at").eq("room_id", mpRoomId).order("joined_at");
        r({count: res.data ? res.data.length : -1, error: res.error ? JSON.stringify(res.error) : null, names: res.data ? res.data.map(function(x){return x.username}) : []});
    })""")
    print(f"Direct query: {q1}")

    # Now call renderMpLobby and check what IT queries
    # First, instrument the original function
    host.evaluate("""()=>{
        window._rlResult = null;
        var origSbFrom = sb.from.bind(sb);
        sb.from = function(table) {
            var builder = origSbFrom(table);
            if (table === "room_players") {
                var origSelect = builder.select.bind(builder);
                builder.select = function(cols) {
                    console.log("INTERCEPTED: sb.from('room_players').select('" + cols + "')");
                    var chain = origSelect(cols);
                    var origEq = chain.eq.bind(chain);
                    chain.eq = function(col, val) {
                        console.log("  .eq('" + col + "', '" + val + "')");
                        return origEq(col, val);
                    };
                    return chain;
                };
            }
            return builder;
        };
    }""")

    h_console = []
    host.on("console", lambda m: h_console.append(m.text))
    host.evaluate("()=>renderMpLobby()")
    host.wait_for_timeout(3000)
    hp = host.evaluate('()=>document.querySelectorAll(".mp-player-row").length')
    print(f"Lobby rows: {hp}")
    for c in h_console:
        if "INTERCEPT" in c or ".eq" in c:
            print(f"  {c}")

    host.evaluate('()=>mpLeaveRoom().catch(function(){})'); host.wait_for_timeout(500)
    browser.close()
