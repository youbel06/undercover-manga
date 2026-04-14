"""Tests Fibbage : multi 2 joueurs full flow + cas limites"""
from playwright.sync_api import sync_playwright
import time, sys
URL='http://127.0.0.1:8765/fibbage.html'
SUPA_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZycmx1YWt1Z29hYnpta25kcml2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU5MzA2ODEsImV4cCI6MjA5MTUwNjY4MX0.AMVDA104Otfx6LPTxgCUEyk0M5OaG6jszW8G_Nucgmc'
errs=[]

def log_err(tag, page):
    page.on('pageerror', lambda e: errs.append(f'[{tag}] err: {e}'))
    page.on('console', lambda m: errs.append(f'[{tag}] {m.type}: {m.text}') if m.type=='error' else None)

with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    c1=b.new_context(viewport={'width':390,'height':844})
    c2=b.new_context(viewport={'width':390,'height':844})
    host=c1.new_page(); p2=c2.new_page()
    log_err('host',host); log_err('p2',p2)

    # 1. Pages chargent
    host.goto(URL, wait_until='networkidle'); time.sleep(1)
    p2.goto(URL, wait_until='networkidle'); time.sleep(1)
    print('Pages loaded')
    home_state = host.evaluate("""() => ({
      screens: document.querySelectorAll('.screen').length,
      questions: window.QUESTIONS?.length || 0,
      title: document.querySelector('.fb-title')?.textContent
    })""")
    print(f'Home: {home_state}')

    # 2. Host crée
    host.locator('button:has-text("Jouer en ligne")').first.click()
    host.wait_for_selector('#screen-mp-hub.active')
    host.locator('button:has-text("Créer une partie")').first.click()
    host.wait_for_selector('#screen-mp-create.active')
    host.fill('#fb-create-pseudo','Alex')
    host.locator('#fb-create-avatars button').first.click()
    host.locator('button:has-text("CRÉER LA PARTIE")').click()
    host.wait_for_selector('#screen-mp-lobby.active', timeout=15000)
    time.sleep(2)
    code=host.text_content('#fb-lobby-code').strip()
    print(f'Code: {code}')

    # 3. P2 rejoint
    p2.locator('button:has-text("Jouer en ligne")').first.click()
    p2.wait_for_selector('#screen-mp-hub.active')
    p2.locator('button:has-text("Rejoindre une partie")').click()
    p2.wait_for_selector('#screen-mp-join.active')
    p2.fill('#fb-join-code', code)
    p2.fill('#fb-join-pseudo','Lea')
    p2.locator('#fb-join-avatars button').nth(1).click()
    p2.locator('#screen-mp-join button.btn').filter(has_text='REJOINDRE').first.click()
    p2.wait_for_selector('#screen-mp-lobby.active', timeout=15000)
    time.sleep(3)
    n_host = host.text_content('#fb-lobby-count').strip()
    print(f'Players in host lobby: {n_host}')

    # 4. Lance la partie
    host.click('#fb-start-btn')
    host.wait_for_selector('#screen-writing.active', timeout=10000)
    p2.wait_for_selector('#screen-writing.active', timeout=10000)
    time.sleep(1)
    q_host = host.evaluate('() => ({q:document.getElementById("fb-w-question")?.textContent, cat:document.getElementById("fb-w-cat")?.textContent})')
    print(f'Question: {q_host}')

    # 5. Soumettre réponses (host: bonne réponse "trop proche" puis vraie)
    real_ans = host.evaluate('() => FB.room?.current_question?.answer')
    print(f'Real answer: {real_ans!r}')

    # Host: tente de soumettre la vraie → doit rejet
    host.fill('#fb-w-text', real_ans)
    host.click('#fb-w-submit')
    time.sleep(1)
    rejected = host.evaluate('() => !FB.room?.answers?.[FB.me.id]')
    print(f'Vraie réponse rejetée: {rejected}')

    # Soumets une fausse
    host.fill('#fb-w-text', 'Une réponse complètement bidon')
    host.click('#fb-w-submit')
    time.sleep(1)
    p2.fill('#fb-w-text', 'Encore une autre fausse réponse')
    p2.click('#fb-w-submit')

    # 6. Attendre passage à vote
    host.wait_for_selector('#screen-voting.active', timeout=15000)
    p2.wait_for_selector('#screen-voting.active', timeout=15000)
    print('→ vote phase')
    time.sleep(1)
    answers = host.evaluate('() => Array.from(document.querySelectorAll("#fb-v-answers .fb-answer")).map(a => ({text:a.textContent.slice(0,40), disabled:a.disabled, mine:a.classList.contains("disabled")}))')
    print(f'Vote answers count: {len(answers)}')
    own_disabled = sum(1 for a in answers if a['mine'])
    print(f'Own answer disabled: {own_disabled}/expected 1')

    # 7. Voter
    # Host vote pour 'truth' (la vraie)
    host.evaluate("() => FB.submitVote('truth')")
    p2.evaluate("() => { const ids = Object.keys(FB.room.answers||{}).map(p=>'a:'+p).filter(id=>id!=='a:'+FB.me.id); FB.submitVote(ids[0]||'truth'); }")
    time.sleep(2)

    # 8. Reveal
    host.wait_for_selector('#screen-reveal.active', timeout=15000)
    p2.wait_for_selector('#screen-reveal.active', timeout=15000)
    print('→ reveal phase')
    time.sleep(1)
    host.screenshot(path='fb_test_reveal.png')

    # Host avance vers scores
    host.click('button:has-text("SUITE")')
    host.wait_for_selector('#screen-scores.active', timeout=10000)
    p2.wait_for_selector('#screen-scores.active', timeout=10000)
    print('→ scores phase')
    time.sleep(1)
    scores = host.evaluate('() => FB.room?.scores')
    print(f'Scores: {scores}')
    host.screenshot(path='fb_test_scores.png')

    # Cleanup
    host.evaluate(f"async () => {{ const H={{'apikey':'{SUPA_KEY}','Authorization':'Bearer {SUPA_KEY}'}}; await fetch('https://frrluakugoabzmkndriv.supabase.co/rest/v1/fb_rooms?code=eq.{code}',{{method:'DELETE',headers:H}}); }}")

    b.close()

print('\n=== ERRORS ===')
if not errs: print('(none)')
else:
    for e in errs[:10]: print(e)
print('\n=== DONE ===')
