#!/usr/bin/env python3
"""Clean multiplayer patch - properly handles JS string escaping."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

SUPABASE_URL = "https://frrluakugoabzmkndriv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZycmx1YWt1Z29hYnpta25kcml2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU5MzA2ODEsImV4cCI6MjA5MTUwNjY4MX0.AMVDA104Otfx6LPTxgCUEyk0M5OaG6jszW8G_Nucgmc"

# ═══ 1. CSS for MP screens ═══
CSS = """
/* ===== MULTIPLAYER ===== */
.mp-code{font-family:var(--font-display);font-size:2.5rem;font-weight:900;letter-spacing:8px;color:var(--accent-gold);text-align:center;margin:12px 0;cursor:pointer}
.mp-player-list{width:100%;max-width:400px}
.mp-player-row{display:flex;align-items:center;gap:10px;padding:10px 14px;background:var(--bg-card);border:1px solid var(--border-glass);border-radius:var(--radius-md);margin-bottom:6px}
.mp-player-row .mp-avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;background:var(--bg-secondary)}
.mp-player-row .mp-info{flex:1}
.mp-player-row .mp-name{font-weight:600;font-size:0.85rem;color:var(--text-bright)}
.mp-ready-badge{font-size:0.7rem;padding:3px 8px;border-radius:8px;font-weight:600}
.mp-ready-badge.ready{background:rgba(34,197,94,0.15);color:#22c55e}
.mp-ready-badge.waiting{background:rgba(156,163,175,0.15);color:#9ca3af}
.mp-host-badge{font-size:0.6rem;background:var(--accent-gold);color:#000;padding:2px 6px;border-radius:6px;font-weight:700;margin-left:4px}
.mp-status{display:flex;align-items:center;gap:6px;font-size:0.75rem;color:var(--text-muted);margin:8px 0}
.mp-status .dot{width:8px;height:8px;border-radius:50%}
.mp-status .dot.online{background:#22c55e}
.mp-status .dot.offline{background:#ef4444}
.lb-podium{display:flex;justify-content:center;align-items:flex-end;gap:8px;margin:16px 0}
.lb-podium-item{text-align:center;border-radius:var(--radius-md);padding:12px 16px;background:var(--bg-card)}
.lb-podium-item.first{order:2;background:linear-gradient(135deg,rgba(245,166,35,0.15),rgba(245,166,35,0.05));border:1px solid rgba(245,166,35,0.3);min-height:120px}
.lb-list{width:100%;max-width:400px}
.lb-row{display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid var(--border-glass)}
.lb-row.me{background:rgba(245,166,35,0.05);border-radius:var(--radius-sm)}
"""
html = html.replace("/* ===== APP CONTAINER ===== */", CSS + "\n/* ===== APP CONTAINER ===== */")

# ═══ 2. HTML screens ═══
MP_HTML = '''
  <!-- ===== MP MENU ===== -->
  <div id="screen-mp-menu" class="screen" style="padding-top:50px">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-splash')">←</button>
    <h2>🌐 Multijoueur</h2>
    <div class="mp-status" id="mp-status"><div class="dot offline"></div><span>Connexion...</span></div>
    <div id="mp-profile-section"></div>
    <div style="display:flex;flex-direction:column;gap:10px;width:100%;max-width:300px;margin-top:16px;">
      <button class="btn btn-primary" onclick="mpCreateRoom()">Créer un salon</button>
      <div style="display:flex;gap:8px;max-width:300px;margin:0 auto">
        <input type="text" id="mp-join-code" placeholder="CODE" maxlength="6" style="flex:1;background:var(--bg-card);border:1px solid var(--border-glass);border-radius:var(--radius-sm);padding:12px;color:var(--text-bright);font-size:1.2rem;text-align:center;letter-spacing:4px;text-transform:uppercase">
        <button class="btn btn-primary" onclick="mpJoinRoom()">Rejoindre</button>
      </div>
      <button class="btn btn-ghost" onclick="showScreen('screen-mp-leaderboard')">🏆 Classement</button>
    </div>
  </div>

  <!-- ===== MP LOBBY ===== -->
  <div id="screen-mp-lobby" class="screen" style="padding-top:50px">
    <button class="btn btn-icon btn-ghost back-btn" onclick="mpLeaveRoom()">←</button>
    <h2>Salon</h2>
    <div class="mp-code" id="mp-room-code" onclick="mpCopyCode()">------</div>
    <div style="font-size:0.75rem;color:var(--text-muted);text-align:center">Partage ce code</div>
    <div class="mp-player-list" id="mp-player-list"></div>
    <div id="mp-host-controls" style="display:none;margin-top:12px">
      <button class="btn btn-primary btn-large" id="mp-start-btn" onclick="mpStartGame()" disabled>LANCER</button>
    </div>
    <button class="btn btn-primary" id="mp-ready-btn" onclick="mpToggleReady()" style="margin-top:12px">PRÊT</button>
  </div>

  <!-- ===== MP GAME ===== -->
  <div id="screen-mp-game" class="screen">
    <div id="mp-game-content" style="text-align:center;width:100%;max-width:400px"></div>
  </div>

  <!-- ===== LEADERBOARD ===== -->
  <div id="screen-mp-leaderboard" class="screen" style="padding-top:50px">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-mp-menu')">←</button>
    <h2>🏆 Classement</h2>
    <div class="lb-podium" id="lb-podium"></div>
    <div class="lb-list" id="lb-list"></div>
  </div>

'''
html = html.replace('  <!-- ===== CREDITS SCREEN ===== -->', MP_HTML + '  <!-- ===== CREDITS SCREEN ===== -->')

# Add MP button to splash (avoid quote issues by using double quotes)
html = html.replace(
    """onclick="showScreen('screen-modes')">JOUER</button>""",
    """onclick="showScreen('screen-modes')">JOUER</button>\n    <button class="btn btn-ghost" onclick="showScreen('screen-mp-menu')" style="margin-top:4px">🌐 Multijoueur</button>"""
)

# ═══ 3. JS - using ONLY double quotes inside innerHTML to avoid escaping hell ═══
# All innerHTML strings use double-quoted JS strings with escaped inner double quotes,
# or template literals with backticks.
JS = '''

// ===== SUPABASE MULTIPLAYER =====
const SUPABASE_URL = "''' + SUPABASE_URL + '''";
const SUPABASE_KEY = "''' + SUPABASE_KEY + '''";
let sb = null, mpPlayerId = null, mpRoomId = null, mpRoomCode = null, mpIsHost = false, mpIsReady = false, mpChannel = null;

function initSupabase() {
  return new Promise(function(resolve) {
    if (typeof supabase !== "undefined" && supabase.createClient) {
      sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY); resolve(true); return;
    }
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.49.4/dist/umd/supabase.min.js";
    s.onload = function() { try { sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY); resolve(true); } catch(e) { resolve(false); } };
    s.onerror = function() { resolve(false); };
    document.head.appendChild(s);
  });
}

async function mpEnsurePlayer() {
  if (!sb) { showToast("Serveur non disponible"); return false; }
  var savedId = localStorage.getItem("mp_player_id");
  if (savedId) {
    var res = await sb.from("players").select("*").eq("id", savedId).single();
    if (res.data) { mpPlayerId = res.data.id; return true; }
  }
  return false;
}

function mpCreateProfileFromInput() {
  var el = document.getElementById("mp-username");
  if (el && el.value.trim()) mpCreateProfile(el.value.trim());
}

async function mpCreateProfile(username) {
  if (!sb || !username) return;
  var res = await sb.from("players").insert({username: username, avatar_emoji: "🕵️"}).select().single();
  if (res.error) { showToast("Pseudo pris ou erreur"); return; }
  mpPlayerId = res.data.id;
  localStorage.setItem("mp_player_id", res.data.id);
  showToast("Profil créé !");
  renderMpMenu();
}

function generateRoomCode() {
  var c = "ABCDEFGHJKLMNPQRSTUVWXYZ", code = "";
  for (var i = 0; i < 6; i++) code += c[Math.floor(Math.random() * c.length)];
  return code;
}

async function mpCreateRoom() {
  if (!await mpEnsurePlayer()) { renderMpProfileForm(); return; }
  var code = generateRoomCode();
  var res = await sb.from("rooms").insert({code: code, host_id: mpPlayerId, status: "waiting"}).select().single();
  if (res.error) { showToast("Erreur"); return; }
  mpRoomId = res.data.id; mpRoomCode = code; mpIsHost = true;
  var p = await sb.from("players").select("username,avatar_emoji").eq("id", mpPlayerId).single();
  await sb.from("room_players").insert({room_id: mpRoomId, player_id: mpPlayerId, username: p.data?.username || "Hôte", is_host: true, is_ready: true});
  showScreen("screen-mp-lobby"); renderMpLobby(); mpSubscribe();
}

async function mpJoinRoom() {
  if (!await mpEnsurePlayer()) { renderMpProfileForm(); return; }
  var code = (document.getElementById("mp-join-code")?.value || "").toUpperCase().trim();
  if (code.length < 4) { showToast("Code invalide"); return; }
  var res = await sb.from("rooms").select("*").eq("code", code).eq("status", "waiting").single();
  if (!res.data) { showToast("Salon introuvable"); return; }
  mpRoomId = res.data.id; mpRoomCode = code; mpIsHost = false;
  var p = await sb.from("players").select("username,avatar_emoji").eq("id", mpPlayerId).single();
  await sb.from("room_players").insert({room_id: mpRoomId, player_id: mpPlayerId, username: p.data?.username || "Joueur", is_host: false, is_ready: false});
  showScreen("screen-mp-lobby"); renderMpLobby(); mpSubscribe();
}

function mpSubscribe() {
  if (!sb || !mpRoomId) return;
  mpChannel = sb.channel("room-" + mpRoomId)
    .on("postgres_changes", {event:"*", schema:"public", table:"room_players", filter:"room_id=eq." + mpRoomId}, function() { renderMpLobby(); })
    .on("postgres_changes", {event:"*", schema:"public", table:"game_state", filter:"room_id=eq." + mpRoomId}, function(p) { handleMpGame(p.new); })
    .subscribe();
}

async function renderMpLobby() {
  document.getElementById("mp-room-code").textContent = mpRoomCode || "------";
  var res = await sb.from("room_players").select("*").eq("room_id", mpRoomId);
  var players = res.data || [];
  var list = document.getElementById("mp-player-list");
  if (!list) return;
  list.innerHTML = "";
  var allReady = true;
  players.forEach(function(p) {
    if (!p.is_ready) allReady = false;
    var row = document.createElement("div");
    row.className = "mp-player-row";
    row.innerHTML = "<div class=\\"mp-avatar\\">" + (p.avatar_emoji || "🕵️") + "</div>" +
      "<div class=\\"mp-info\\"><div class=\\"mp-name\\">" + (p.username || "Joueur") +
      (p.is_host ? "<span class=\\"mp-host-badge\\">HÔTE</span>" : "") + "</div></div>" +
      "<span class=\\"mp-ready-badge " + (p.is_ready ? "ready" : "waiting") + "\\">" +
      (p.is_ready ? "✓" : "...") + "</span>";
    list.appendChild(row);
  });
  var hc = document.getElementById("mp-host-controls");
  if (mpIsHost && hc) {
    hc.style.display = "block";
    var btn = document.getElementById("mp-start-btn");
    btn.disabled = !(allReady && players.length >= 3);
    btn.textContent = allReady && players.length >= 3 ? "LANCER (" + players.length + " joueurs)" : "En attente...";
  }
}

async function mpToggleReady() {
  mpIsReady = !mpIsReady;
  await sb.from("room_players").update({is_ready: mpIsReady}).eq("room_id", mpRoomId).eq("player_id", mpPlayerId);
  document.getElementById("mp-ready-btn").textContent = mpIsReady ? "PAS PRÊT" : "PRÊT";
}

async function mpStartGame() {
  if (!mpIsHost) return;
  var pair = PAIRS[Math.floor(Math.random() * PAIRS.length)];
  var res = await sb.from("room_players").select("*").eq("room_id", mpRoomId);
  var players = res.data || [];
  var roles = {};
  var shuffled = players.map(function(_,i){return i}).sort(function(){return Math.random()-0.5});
  players.forEach(function(p,i) { roles[p.player_id] = shuffled.indexOf(i) === 0 ? "undercover" : "civil"; });
  await sb.from("game_state").insert({room_id:mpRoomId, phase:"reveal", current_pair:{civil:pair.civil,undercover:pair.undercover,civilImg:pair.civilImg,undercoverImg:pair.undercoverImg,hint:pair.hint||""}, roles:roles, votes:{}, eliminated:[], round:1, total_rounds:5});
  await sb.from("rooms").update({status:"playing"}).eq("id", mpRoomId);
}

function handleMpGame(state) {
  if (!state) return;
  showScreen("screen-mp-game");
  var content = document.getElementById("mp-game-content");
  if (!content) return;
  var myRole = (state.roles || {})[mpPlayerId] || "civil";
  var pair = state.current_pair || {};
  var myChar = myRole === "undercover" ? pair.undercover : pair.civil;
  var myImg = myRole === "undercover" ? pair.undercoverImg : pair.civilImg;
  var roleColor = myRole === "undercover" ? "var(--accent-undercover)" : "var(--accent-civil)";
  var roleLabel = myRole === "undercover" ? "UNDERCOVER" : "CIVIL";

  if (state.phase === "reveal") {
    content.innerHTML = "<h2>Ton rôle</h2>" +
      "<div style=\\"display:inline-block;padding:24px;border-radius:20px;border:2px solid " + roleColor + ";background:var(--bg-card)\\">" +
      (myImg ? "<img src=\\"" + myImg + "\\" style=\\"width:120px;height:120px;border-radius:16px;object-fit:cover;object-position:top\\" />" : "") +
      "<div style=\\"font-size:1.5rem;font-weight:700;color:var(--text-bright)\\">" + (myChar || "???") + "</div>" +
      "<div style=\\"font-size:0.9rem;color:" + roleColor + ";margin-top:6px\\">" + roleLabel + "</div></div>" +
      "<div style=\\"margin-top:16px\\"><button class=\\"btn btn-primary\\" onclick=\\"mpMarkReady()\\">Mémorisé ✓</button></div>";
  } else if (state.phase === "discuss") {
    content.innerHTML = "<h2>Discussion</h2><p style=\\"color:var(--text-muted)\\">Donnez un indice !</p>" +
      (mpIsHost ? "<button class=\\"btn btn-primary\\" onclick=\\"mpAdvancePhase(&#39;vote&#39;)\\" style=\\"margin-top:14px\\">Passer au vote</button>" : "");
  } else if (state.phase === "vote") {
    mpRenderVote(state);
  } else if (state.phase === "result") {
    var w = state.winner || "civil";
    content.innerHTML = "<h2 style=\\"color:" + (w==="civil"?"var(--accent-civil)":"var(--accent-undercover)") + "\\">" +
      (w==="civil"?"Victoire Civils !":"Undercover gagne !") + "</h2>" +
      (pair.hint ? "<div class=\\"hint-box\\"><div class=\\"hint-label\\">Le saviez-vous ?</div><div class=\\"hint-text\\">" + pair.hint + "</div></div>" : "") +
      "<button class=\\"btn btn-primary\\" onclick=\\"mpLeaveRoom()\\" style=\\"margin-top:16px\\">Quitter</button>";
  }
}

async function mpMarkReady() {
  await sb.from("room_players").update({is_ready:true}).eq("room_id",mpRoomId).eq("player_id",mpPlayerId);
  showToast("Prêt !");
}

async function mpAdvancePhase(phase) {
  if (!mpIsHost) return;
  await sb.from("game_state").update({phase:phase}).eq("room_id",mpRoomId);
}

async function mpRenderVote(state) {
  var content = document.getElementById("mp-game-content");
  var res = await sb.from("room_players").select("*").eq("room_id",mpRoomId);
  var players = res.data || [];
  var eliminated = state.eliminated || [];
  var alive = players.filter(function(p){return eliminated.indexOf(p.player_id)<0});
  var myVote = (state.votes||{})[mpPlayerId];
  var h = "<h2>Vote</h2><div style=\\"display:flex;flex-direction:column;gap:8px;width:100%;max-width:300px\\">";
  alive.forEach(function(p) {
    if (p.player_id === mpPlayerId) return;
    var voted = myVote === p.player_id;
    h += "<button class=\\"btn " + (voted?"btn-primary":"btn-ghost") + "\\" data-vid=\\"" + p.player_id + "\\" onclick=\\"mpVoteFor(this.dataset.vid)\\">" +
      (p.avatar_emoji||"🕵️") + " " + p.username + (voted?" ✓":"") + "</button>";
  });
  h += "</div>";
  if (mpIsHost) h += "<button class=\\"btn btn-primary\\" onclick=\\"mpResolveVote()\\" style=\\"margin-top:14px\\">Résoudre</button>";
  content.innerHTML = h;
}

async function mpVoteFor(targetId) {
  var res = await sb.from("game_state").select("votes").eq("room_id",mpRoomId).single();
  var votes = (res.data||{}).votes || {};
  votes[mpPlayerId] = targetId;
  await sb.from("game_state").update({votes:votes}).eq("room_id",mpRoomId);
}

async function mpResolveVote() {
  if (!mpIsHost) return;
  var res = await sb.from("game_state").select("*").eq("room_id",mpRoomId).single();
  var gs = res.data; if(!gs) return;
  var votes = gs.votes||{}, tally = {};
  Object.values(votes).forEach(function(v){tally[v]=(tally[v]||0)+1});
  var max = Math.max(0,...Object.values(tally));
  var elimId = Object.keys(tally).find(function(k){return tally[k]===max});
  if (!elimId) return;
  var elim = (gs.eliminated||[]).concat([elimId]);
  var roles = gs.roles||{};
  var aliveR = Object.entries(roles).filter(function(e){return elim.indexOf(e[0])<0});
  var ucAlive = aliveR.filter(function(e){return e[1]==="undercover"}).length;
  var civAlive = aliveR.filter(function(e){return e[1]==="civil"}).length;
  var phase = "discuss", winner = null;
  if (ucAlive===0) {phase="result";winner="civil";}
  else if (ucAlive>=civAlive) {phase="result";winner="undercover";}
  await sb.from("game_state").update({eliminated:elim,votes:{},phase:phase,winner:winner}).eq("room_id",mpRoomId);
}

async function mpLeaveRoom() {
  if (sb && mpRoomId) {
    await sb.from("room_players").delete().eq("room_id",mpRoomId).eq("player_id",mpPlayerId);
    if (mpIsHost) await sb.from("rooms").delete().eq("id",mpRoomId);
  }
  if (mpChannel) {sb.removeChannel(mpChannel);mpChannel=null;}
  mpRoomId=null;mpRoomCode=null;mpIsHost=false;mpIsReady=false;
  showScreen("screen-mp-menu");
}

function mpCopyCode() { try{navigator.clipboard.writeText(mpRoomCode||"");showToast("Copié !");}catch(e){} }

function renderMpProfileForm() {
  var s = document.getElementById("mp-profile-section");
  if (!s) return;
  s.innerHTML = "<div style=\\"text-align:center;margin:12px 0\\">" +
    "<p style=\\"color:var(--text-muted);font-size:0.85rem;margin-bottom:10px\\">Crée ton profil en ligne</p>" +
    "<div style=\\"display:flex;gap:8px;max-width:250px;margin:0 auto\\">" +
    "<input type=\\"text\\" id=\\"mp-username\\" placeholder=\\"Pseudo\\" style=\\"flex:1;background:var(--bg-card);border:1px solid var(--border-glass);border-radius:8px;padding:10px;color:var(--text-bright);font-size:1rem\\">" +
    "<button class=\\"btn btn-primary\\" onclick=\\"mpCreateProfileFromInput()\\">Créer</button></div></div>";
}

async function renderMpMenu() {
  var s = document.getElementById("mp-profile-section");
  if (!s) return;
  if (!sb) { s.innerHTML="<div style=\\"color:var(--accent-undercover);text-align:center;font-size:0.85rem\\">Serveur non disponible</div>"; return; }
  var ok = await mpEnsurePlayer();
  if (!ok) { renderMpProfileForm(); return; }
  var res = await sb.from("players").select("*").eq("id",mpPlayerId).single();
  if (res.data) {
    s.innerHTML = "<div style=\\"text-align:center\\"><div style=\\"font-size:2rem\\">" + (res.data.avatar_emoji||"🕵️") + "</div>" +
      "<div style=\\"font-weight:700;color:var(--text-bright)\\">" + res.data.username + "</div></div>";
    document.getElementById("mp-status").innerHTML = "<div class=\\"dot online\\"></div><span>Connecté</span>";
  }
}

async function loadLeaderboard() {
  if (!sb) { document.getElementById("lb-list").innerHTML="<div style=\\"text-align:center;color:var(--text-muted);padding:20px\\">Non disponible</div>"; return; }
  var res = await sb.from("leaderboard").select("*").order("rank_points",{ascending:false}).limit(50);
  var data = res.data || [];
  var list = document.getElementById("lb-list");
  if (!data.length) { list.innerHTML="<div style=\\"text-align:center;color:var(--text-muted);padding:20px\\">Aucun joueur</div>"; return; }
  var podium = document.getElementById("lb-podium");
  podium.innerHTML = "";
  var medals = ["🥇","🥈","🥉"];
  data.slice(0,3).forEach(function(p,i) {
    var d = document.createElement("div");
    d.className = "lb-podium-item " + (i===0?"first":i===1?"second":"third");
    d.innerHTML = "<div>" + medals[i] + "</div><div style=\\"font-size:1.5rem\\">" + (p.avatar_emoji||"🕵️") + "</div><div style=\\"font-weight:600;font-size:0.8rem\\">" + p.username + "</div><div style=\\"color:var(--accent-gold);font-size:0.7rem\\">" + p.rank_points + " pts</div>";
    podium.appendChild(d);
  });
  list.innerHTML = "";
  data.forEach(function(p,i) {
    var row = document.createElement("div");
    row.className = "lb-row" + (p.player_id===mpPlayerId?" me":"");
    row.innerHTML = "<div style=\\"width:24px;font-weight:700;font-size:0.85rem;color:var(--text-muted)\\">#" + (i+1) + "</div><div style=\\"font-size:1.1rem\\">" + (p.avatar_emoji||"🕵️") + "</div><div style=\\"flex:1;font-size:0.85rem\\">" + p.username + "</div><div style=\\"color:var(--accent-gold);font-weight:600\\">" + p.rank_points + " pts</div>";
    list.appendChild(row);
  });
}

// Patch showScreen for MP
var _showScreenMP = showScreen;
showScreen = function(id) {
  _showScreenMP(id);
  if (id === "screen-mp-menu") initSupabase().then(function(){renderMpMenu()});
  if (id === "screen-mp-leaderboard") { initSupabase().then(function(){loadLeaderboard()}); }
};
'''

html = html.replace("\n</script>", JS + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Clean MP patch applied! {len(html)//1024} KB")
