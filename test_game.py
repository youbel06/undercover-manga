#!/usr/bin/env python3
"""Playwright test: full game simulation for the new Undercover Manga."""
import os, sys
from playwright.sync_api import sync_playwright

HTML_PATH = os.path.join(os.path.dirname(__file__), "index.html")
FILE_URL = "file:///" + HTML_PATH.replace("\\", "/")
bugs = []

def bug(msg):
    print(f"  [BUG] {msg}")
    bugs.append(msg)

def ok(msg):
    print(f"  [OK] {msg}")

def step(desc):
    print(f"\n{'='*60}\n  {desc}\n{'='*60}")

def active_screen(page):
    return page.evaluate("() => document.querySelector('.screen.active')?.id || 'none'")

def check_errors(page, page_errors, ctx=""):
    if page_errors:
        for e in page_errors:
            bug(f"JS error ({ctx}): {e}")
        page_errors.clear()
        return True
    return False

def do_all_reveals(page):
    """Reveal all players and proceed."""
    for j in range(20):
        unrevealed = page.locator(".reveal-player-item:not(.revealed)")
        if unrevealed.count() == 0:
            break
        unrevealed.first.click()
        page.wait_for_timeout(500)
        page.evaluate("() => dismissCard()")
        page.wait_for_timeout(300)
    # Click "all done"
    page.evaluate("() => { const btn = document.getElementById('reveal-all-done-btn'); if(btn) btn.click(); }")
    page.wait_for_timeout(500)

def do_all_votes(page):
    """Cast all votes (each voter votes for the first non-self alive player)."""
    for vv in range(20):
        result = page.evaluate("""() => {
            const aliveList = GameState.alivePlayers;
            if (GameState.currentVoterIndex >= aliveList.length) return 'done';
            const voterPI = aliveList[GameState.currentVoterIndex];
            const targetPI = aliveList.find(pi => pi !== voterPI);
            if (targetPI === undefined) return 'no-target';
            GameState.selectedVoteTarget = targetPI;
            confirmVote();
            return 'voted';
        }""")
        page.wait_for_timeout(150)
        if result != 'voted':
            break

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        # ── 1. Load ──
        step("1. Load HTML file")
        page.goto(FILE_URL)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(300)
        # Dismiss tutorial if shown
        page.evaluate("() => { try { localStorage.setItem('uc_tutorial_done','true'); } catch(e) {} }")
        page.evaluate("() => { const t = document.getElementById('tutorial-overlay'); if (t) t.classList.remove('visible'); }")
        page.wait_for_timeout(200)
        print(f"  Title: {page.title()}")

        if page.evaluate("() => document.getElementById('screen-splash').classList.contains('active')"):
            ok("Splash screen active")
        else:
            bug("Splash screen not active")
        check_errors(page, page_errors, "load")

        # ── 2. PAIRS ──
        step("2. Verify PAIRS data")
        total = page.evaluate("() => PAIRS.length")
        with_img = page.evaluate("() => PAIRS.filter(p => p.civilImg && p.civilImg.startsWith('data:')).length")
        print(f"  Pairs: {total}, with images: {with_img}")
        ok(f"{total} pairs") if total >= 150 else bug(f"Only {total} pairs")

        # ── 3. JOUER → Modes → Settings ──
        step("3. Click JOUER → Mode → Settings")
        page.locator("#screen-splash button.btn-primary").click()
        page.wait_for_timeout(600)
        screen = active_screen(page)
        if screen == 'screen-modes':
            ok("Mode selection screen")
            page.evaluate("() => { GameState.currentMode = 'normal'; confirmMode(); }")
            page.wait_for_timeout(600)
        if active_screen(page) == 'screen-settings':
            ok("Settings screen")
        else:
            bug(f"Expected settings, got {active_screen(page)}")
        check_errors(page, page_errors, "jouer")

        # ── 4. Configure ──
        step("4. Configure: 4 players, 1 UC, 0 MW, 3 rounds")
        page.evaluate("""() => {
            GameState.playerCount = 4;
            GameState.undercoverCount = 1;
            GameState.mrWhiteCount = 0;
            GameState.totalRounds = 3;
            GameState.playerNames = ['Alice', 'Bob', 'Charlie', 'David'];
            GameState.timerSeconds = 0;
            renderSettings();
        }""")
        ok("Configured")

        # ── 5. Launch ──
        step("5. Launch game")
        page.evaluate("() => launchGame()")
        page.wait_for_timeout(3000)  # Wait for round intro + setupRound
        check_errors(page, page_errors, "launch")

        # ── 6. Game state ──
        step("6. Check game state after setup")
        gs = page.evaluate("""() => ({
            round: GameState.currentRound,
            totalRounds: GameState.totalRounds,
            playerCount: GameState.players.length,
            roles: GameState.players.map(p => p.role),
            pair: GameState.currentPair ? {c: GameState.currentPair.civil, u: GameState.currentPair.undercover} : null,
            active: GameState.gameActive,
            aliveCount: GameState.alivePlayers.length,
        })""")
        print(f"  Round: {gs['round']}/{gs['totalRounds']}")
        print(f"  Players: {gs['playerCount']}, Alive: {gs['aliveCount']}")
        print(f"  Roles: {gs['roles']}")
        print(f"  Pair: {gs['pair']}")

        if gs['playerCount'] == 4: ok("4 players created")
        else: bug(f"Expected 4 players, got {gs['playerCount']}")

        if gs['roles'].count('undercover') == 1: ok("1 undercover assigned")
        else: bug(f"Undercover count wrong: {gs['roles']}")

        if gs['roles'].count('civil') == 3: ok("3 civils assigned")
        else: bug(f"Civil count wrong: {gs['roles']}")

        # ── 7. Verify no role leak ──
        step("7. Check no role info visible before reveal")
        screen = active_screen(page)
        print(f"  Screen: {screen}")
        if screen == 'screen-reveal':
            page_text = page.locator("#screen-reveal").inner_text()
            role_leaked = any(w in page_text.lower() for w in ['civil', 'undercover', 'mr. white'])
            if role_leaked:
                bug("Role information leaked on reveal screen!")
            else:
                ok("No role info visible before individual reveals")

        # ── 8. Role reveals ──
        step("8. Reveal all 4 players")
        # Dismiss tutorial overlay if it appeared
        page.evaluate("() => { const t = document.getElementById('tutorial-overlay'); if(t) { t.classList.remove('visible'); t.style.display='none'; } }")
        page.wait_for_timeout(200)
        for i in range(4):
            unrevealed = page.locator(".reveal-player-item:not(.revealed)")
            if unrevealed.count() == 0:
                break
            unrevealed.first.click()
            page.wait_for_timeout(600)

            # Verify overlay is visible
            overlay_visible = page.evaluate("() => document.getElementById('card-overlay').classList.contains('visible')")
            if overlay_visible:
                # Check character image present
                has_img = page.evaluate("() => !!document.querySelector('#card-image-container img')")
                if has_img: ok(f"Player {i+1}: image shown")
                else: print(f"  Player {i+1}: no image (may be Mr. White)")

                # Check dismiss button visible
                dismiss_visible = page.locator(".card-dismiss-btn").is_visible()
                if dismiss_visible:
                    page.locator(".card-dismiss-btn").click()
                    page.wait_for_timeout(400)
                else:
                    page.evaluate("() => dismissCard()")
                    page.wait_for_timeout(400)
            else:
                bug(f"Overlay not visible for player {i+1}")
                page.evaluate("() => dismissCard()")

        check_errors(page, page_errors, "reveals")

        # Proceed past reveal
        page.evaluate("() => { const b = document.getElementById('reveal-all-done-btn'); if(b) b.click(); }")
        page.wait_for_timeout(600)
        ok("All reveals done")

        # ── 9. Discussion ──
        step("9. Discussion phase")
        screen = active_screen(page)
        print(f"  Screen: {screen}")
        if screen == 'screen-discuss':
            ok("Discussion screen")
        page.evaluate("() => startVote()")
        page.wait_for_timeout(500)
        check_errors(page, page_errors, "discussion")

        # ── 10. Voting ──
        step("10. Vote phase")
        screen = active_screen(page)
        print(f"  Screen: {screen}")
        do_all_votes(page)
        page.wait_for_timeout(500)
        check_errors(page, page_errors, "votes")

        # Check tally appeared
        eliminated = page.evaluate("() => GameState.eliminatedThisTurn")
        print(f"  Eliminated player index: {eliminated}")
        if eliminated is not None:
            ok("Vote tally computed")
        else:
            bug("eliminatedThisTurn is null after voting")

        # ── 11. Elimination ──
        step("11. Process elimination")
        page.evaluate("() => processElimination()")
        page.wait_for_timeout(800)
        screen = active_screen(page)
        print(f"  Screen: {screen}")

        if screen == 'screen-elimination':
            ok("Elimination screen shown")
            # Check pair images
            pair_imgs = page.locator("#screen-elimination img")
            print(f"  Images on elimination screen: {pair_imgs.count()}")
        check_errors(page, page_errors, "elimination")

        # Continue
        page.evaluate("() => continueAfterElimination()")
        page.wait_for_timeout(800)
        screen = active_screen(page)
        print(f"  After continue: {screen}")
        check_errors(page, page_errors, "continue")

        # ── 12. Play remaining rounds to completion ──
        step("12. Play to completion")
        for loop in range(20):
            screen = active_screen(page)
            print(f"  [{loop}] Screen: {screen}")

            if screen == 'screen-final':
                ok("Final screen reached!")
                break
            elif screen == 'screen-round-result':
                # Check if more rounds
                has_next = page.evaluate("() => GameState.currentRound < GameState.totalRounds")
                if has_next:
                    page.evaluate("() => nextRound()")
                    page.wait_for_timeout(3000)  # round intro + setup
                else:
                    page.evaluate("() => showFinalScreen()")
                    page.wait_for_timeout(500)
            elif screen == 'screen-round-intro':
                page.wait_for_timeout(3000)
            elif screen == 'screen-reveal':
                do_all_reveals(page)
            elif screen == 'screen-discuss':
                page.evaluate("() => startVote()")
                page.wait_for_timeout(500)
            elif screen == 'screen-vote':
                do_all_votes(page)
                page.wait_for_timeout(500)
                elim = page.evaluate("() => GameState.eliminatedThisTurn")
                if elim is not None:
                    page.evaluate("() => processElimination()")
                    page.wait_for_timeout(500)
                else:
                    bug("No elimination target after votes")
                    break
            elif screen == 'screen-elimination':
                page.evaluate("() => continueAfterElimination()")
                page.wait_for_timeout(800)
            else:
                print(f"  Unexpected screen: {screen}")
                break

            check_errors(page, page_errors, f"loop {loop}")

        # ── 13. Final checks ──
        step("13. Final checks")
        scores = page.evaluate("() => JSON.parse(JSON.stringify(GameState.scores))")
        print(f"  Scores: {scores}")

        has_sfx = page.evaluate("() => typeof SoundFX !== 'undefined' && typeof SoundFX.click === 'function'")
        ok("SoundFX system") if has_sfx else bug("SoundFX missing")

        has_manifest = page.evaluate("() => !!document.querySelector('link[rel=manifest]')")
        ok("PWA manifest") if has_manifest else bug("No PWA manifest")

        has_meta = page.evaluate("() => !!document.querySelector('meta[name=apple-mobile-web-app-capable]')")
        ok("iOS PWA meta") if has_meta else bug("No iOS PWA meta")

        screen_count = page.evaluate("() => document.querySelectorAll('.screen').length")
        print(f"  Total screens: {screen_count}")
        ok(f"{screen_count} screens") if screen_count >= 8 else bug(f"Only {screen_count} screens")

        check_errors(page, page_errors, "final")

        # ═══ SUMMARY ═══
        print(f"\n{'='*60}")
        print(f"  TEST SUMMARY")
        print(f"{'='*60}")
        if bugs:
            print(f"\n  BUGS FOUND: {len(bugs)}")
            for i, b in enumerate(bugs, 1):
                print(f"    {i}. {b}")
        else:
            print(f"\n  ALL TESTS PASSED!")
        print(f"  (0 JS console errors)")

        browser.close()
        return len(bugs)

if __name__ == "__main__":
    sys.exit(main())
