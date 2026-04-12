#!/usr/bin/env python3
"""Patch: Add Supabase multiplayer to game_template.html"""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

SUPABASE_URL = "https://frrluakugoabzmkndriv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZycmx1YWt1Z29hYnpta25kcml2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU5MzA2ODEsImV4cCI6MjA5MTUwNjY4MX0.AMVDA104Otfx6LPTxgCUEyk0M5OaG6jszW8G_Nucgmc"

# ═════════════════════��════════════════════════════��════════
# 1. Add Supabase SDK in <head>
# ═══════════════════════════════════════════════════════════
html = html.replace(
    '<title>Undercover Lelox</title>',
    '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>\n'
    '<title>Undercover Lelox</title>'
)

# ═══════════════════════════════════════════════════════════
# 2. CSS for multiplayer screens
# ═══════════════════════════════════════════════════════════
CSS_MP = """
/* ===== MULTIPLAYER ===== */
#screen-mp-menu, #screen-mp-lobby, #screen-mp-game, #screen-mp-leaderboard, #screen-mp-friends {
  padding-top:50px;
}
.mp-code { font-family:var(--font-display); font-size:2.5rem; font-weight:900;
  letter-spacing:8px; color:var(--accent-gold); text-align:center; margin:12px 0;
  user-select:all; cursor:pointer; }
.mp-code-hint { font-size:0.75rem; color:var(--text-muted); text-align:center; }

.mp-player-list { width:100%; max-width:400px; }
.mp-player-row {
  display:flex; align-items:center; gap:10px; padding:10px 14px;
  background:var(--bg-card); border:1px solid var(--border-glass);
  border-radius:var(--radius-md); margin-bottom:6px;
  animation:fadeInUp 0.3s ease both;
}
.mp-player-row .mp-avatar { width:36px; height:36px; border-radius:50%;
  display:flex; align-items:center; justify-content:center; font-size:1.2rem; background:var(--bg-secondary); }
.mp-player-row .mp-info { flex:1; }
.mp-player-row .mp-name { font-weight:600; font-size:0.85rem; color:var(--text-bright); }
.mp-player-row .mp-level { font-size:0.7rem; color:var(--text-muted); }
.mp-ready-badge { font-size:0.7rem; padding:3px 8px; border-radius:8px; font-weight:600; }
.mp-ready-badge.ready { background:rgba(34,197,94,0.15); color:#22c55e; }
.mp-ready-badge.waiting { background:rgba(156,163,175,0.15); color:#9ca3af; }
.mp-host-badge { font-size:0.6rem; background:var(--accent-gold); color:#000;
  padding:2px 6px; border-radius:6px; font-weight:700; margin-left:4px; }

.mp-join-input {
  display:flex; gap:8px; align-items:center; max-width:300px; margin:12px auto;
}
.mp-join-input input {
  flex:1; background:var(--bg-card); border:1px solid var(--border-glass);
  border-radius:var(--radius-sm); padding:12px 16px; color:var(--text-bright);
  font-size:1.2rem; text-align:center; letter-spacing:4px; text-transform:uppercase;
  font-family:var(--font-display);
}

.mp-chat { max-width:400px; width:100%; margin:10px 0; }
.mp-chat-messages {
  max-height:120px; overflow-y:auto; padding:8px;
  background:var(--bg-card); border-radius:var(--radius-sm); margin-bottom:6px;
  font-size:0.8rem;
}
.mp-chat-msg { padding:2px 0; color:var(--text-muted); }
.mp-chat-msg .sender { color:var(--accent-gold); font-weight:600; }
.mp-chat-input {
  display:flex; gap:6px;
}
.mp-chat-input input {
  flex:1; background:var(--bg-card); border:1px solid var(--border-glass);
  border-radius:var(--radius-sm); padding:8px 12px; color:var(--text-primary); font-size:0.8rem;
}

/* Leaderboard */
.lb-podium { display:flex; justify-content:center; align-items:flex-end; gap:8px; margin:16px 0; }
.lb-podium-item { text-align:center; border-radius:var(--radius-md); padding:12px 16px; background:var(--bg-card); }
.lb-podium-item.first { order:2; background:linear-gradient(135deg,rgba(245,166,35,0.15),rgba(245,166,35,0.05)); border:1px solid rgba(245,166,35,0.3); min-height:120px; }
.lb-podium-item.second { order:1; min-height:100px; }
.lb-podium-item.third { order:3; min-height:80px; }
.lb-rank { font-size:1.5rem; }
.lb-name { font-size:0.8rem; font-weight:600; color:var(--text-bright); }
.lb-pts { font-size:0.7rem; color:var(--accent-gold); }

.lb-list { width:100%; max-width:400px; }
.lb-row { display:flex; align-items:center; gap:10px; padding:8px 12px; border-bottom:1px solid var(--border-glass); }
.lb-row .lb-pos { width:24px; font-weight:700; font-size:0.85rem; color:var(--text-muted); }
.lb-row .lb-row-name { flex:1; font-size:0.85rem; color:var(--text-primary); }
.lb-row .lb-row-pts { font-size:0.85rem; color:var(--accent-gold); font-weight:600; }
.lb-row.me { background:rgba(245,166,35,0.05); border-radius:var(--radius-sm); }

/* Connection status */
.mp-status { display:flex; align-items:center; gap:6px; font-size:0.75rem; color:var(--text-muted); margin:8px 0; }
.mp-status .dot { width:8px; height:8px; border-radius:50%; }
.mp-status .dot.online { background:#22c55e; }
.mp-status .dot.offline { background:#ef4444; }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS_MP + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 3. HTML screens for multiplayer
# ═══════════════════════════════════════════════════════════
MP_SCREENS = """
  <!-- ===== MP MENU ===== -->
  <div id="screen-mp-menu" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-splash')" aria-label="Retour">←</button>
    <h2>🌐 Multijoueur</h2>
    <div class="mp-status" id="mp-status"><div class="dot offline"></div><span>Connexion...</span></div>
    <div id="mp-profile-section"></div>
    <div style="display:flex;flex-direction:column;gap:10px;width:100%;max-width:300px;margin-top:16px;">
      <button class="btn btn-primary" onclick="mpCreateRoom()">Créer un salon</button>
      <div class="mp-join-input">
        <input type="text" id="mp-join-code" placeholder="CODE" maxlength="6">
        <button class="btn btn-primary" onclick="mpJoinRoom()">Rejoindre</button>
      </div>
      <button class="btn btn-ghost" onclick="mpQuickMatch()">⚡ Partie rapide</button>
      <button class="btn btn-ghost" onclick="showScreen('screen-mp-leaderboard')">🏆 Classement</button>
      <button class="btn btn-ghost" onclick="showScreen('screen-mp-friends')">👥 Amis</button>
    </div>
  </div>

  <!-- ===== MP LOBBY ===== -->
  <div id="screen-mp-lobby" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="mpLeaveRoom()" aria-label="Retour">←</button>
    <h2>Salon</h2>
    <div class="mp-code" id="mp-room-code" onclick="mpCopyCode()">------</div>
    <div class="mp-code-hint">Partage ce code à tes amis</div>
    <div class="mp-player-list" id="mp-player-list"></div>
    <div id="mp-host-controls" style="display:none;margin-top:12px;">
      <button class="btn btn-primary btn-large" id="mp-start-btn" onclick="mpStartGame()" disabled>LANCER (en attente...)</button>
    </div>
    <div id="mp-guest-controls" style="margin-top:12px;">
      <button class="btn btn-primary" id="mp-ready-btn" onclick="mpToggleReady()">✓ PRÊT</button>
    </div>
    <div class="mp-chat" id="mp-chat">
      <div class="mp-chat-messages" id="mp-chat-messages"></div>
      <div class="mp-chat-input">
        <input type="text" id="mp-chat-input" placeholder="Message..." onkeydown="if(event.key==='Enter')mpSendChat()">
        <button class="btn btn-ghost" onclick="mpSendChat()" style="min-height:36px;">Envoyer</button>
      </div>
    </div>
  </div>

  <!-- ===== MP GAME (per-player view) ===== -->
  <div id="screen-mp-game" class="screen">
    <div id="mp-game-content" style="text-align:center;width:100%;max-width:400px;"></div>
  </div>

  <!-- ===== LEADERBOARD ===== -->
  <div id="screen-mp-leaderboard" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-mp-menu')" aria-label="Retour">←</button>
    <h2>🏆 Classement Global</h2>
    <div class="lb-podium" id="lb-podium"></div>
    <div class="lb-list" id="lb-list"></div>
  </div>

  <!-- ===== FRIENDS ===== -->
  <div id="screen-mp-friends" class="screen">
    <button class="btn btn-icon btn-ghost back-btn" onclick="showScreen('screen-mp-menu')" aria-label="Retour">←</button>
    <h2>👥 Amis</h2>
    <div class="mp-join-input" style="max-width:350px;">
      <input type="text" id="friend-search" placeholder="Rechercher un pseudo..." style="letter-spacing:normal;text-transform:none;">
      <button class="btn btn-primary" onclick="mpSearchFriend()">Ajouter</button>
    </div>
    <div id="friends-list" style="width:100%;max-width:400px;margin-top:10px;"></div>
  </div>

"""

html = html.replace(
    '  <!-- ===== CREDITS SCREEN ===== -->',
    MP_SCREENS + '  <!-- ===== CREDITS SCREEN ===== -->'
)

# Add multiplayer button to splash
html = html.replace(
    "onclick=\"showScreen('screen-modes')\">JOUER</button>",
    "onclick=\"showScreen('screen-modes')\">JOUER</button>\n"
    "    <button class=\"btn btn-ghost\" onclick=\"showScreen('screen-mp-menu')\" style=\"margin-top:4px;\">🌐 Multijoueur</button>"
)

# ══════════════════════════════════════════════════���════════
# 4. JavaScript: Supabase client + multiplayer logic
# ═══════════════════════════════════════════════════════════
JS_MP = """

// ===== SUPABASE CLIENT =====
const SUPABASE_URL = '""" + SUPABASE_URL + """';
const SUPABASE_KEY = '""" + SUPABASE_KEY + """';

let sb = null;
let mpPlayerId = null;
let mpRoomId = null;
let mpRoomCode = null;
let mpIsHost = false;
let mpIsReady = false;
let mpChannel = null;

function initSupabase() {
  try {
    if (typeof supabase !== 'undefined' && supabase.createClient) {
      sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
      console.log('Supabase initialized');
      return true;
    }
  } catch(e) { console.warn('Supabase not available:', e); }
  return false;
}

async function mpEnsurePlayer() {
  if (!sb) { showToast('Serveur non disponible'); return false; }
  const savedId = localStorage.getItem('mp_player_id');
  if (savedId) {
    const {data} = await sb.from('players').select('*').eq('id', savedId).single();
    if (data) { mpPlayerId = data.id; return true; }
  }
  return false;
}

async function mpCreateProfile(username) {
  if (!sb || !username.trim()) return;
  const eq = getEquipped();
  const {data, error} = await sb.from('players').insert({
    username: username.trim(),
    avatar_emoji: eq.avatar || '🕵️',
    avatar_color: eq.avatarColor || '#1a1a2e',
  }).select().single();
  if (error) { showToast('Pseudo déjà pris ou erreur'); return; }
  mpPlayerId = data.id;
  localStorage.setItem('mp_player_id', data.id);
  showToast('Profil créé ! 🎉');
  renderMpMenu();
}

function generateRoomCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ';
  let code = '';
  for (let i = 0; i < 6; i++) code += chars[Math.floor(Math.random() * chars.length)];
  return code;
}

async function mpCreateRoom() {
  if (!await mpEnsurePlayer()) {
    renderMpProfileForm(); return;
  }
  const code = generateRoomCode();
  const {data, error} = await sb.from('rooms').insert({
    code: code, host_id: mpPlayerId, status: 'waiting',
    mode: GameState.currentMode || 'normal', max_players: 8,
  }).select().single();
  if (error) { showToast('Erreur création salon'); return; }
  mpRoomId = data.id;
  mpRoomCode = code;
  mpIsHost = true;
  // Add host to room_players
  const pData = await sb.from('players').select('username,avatar_emoji').eq('id', mpPlayerId).single();
  await sb.from('room_players').insert({
    room_id: mpRoomId, player_id: mpPlayerId,
    username: pData.data?.username || 'Hôte',
    avatar_emoji: pData.data?.avatar_emoji || '🕵️',
    is_host: true, is_ready: true,
  });
  showScreen('screen-mp-lobby');
  renderMpLobby();
  mpSubscribeToRoom();
  SoundFX.click();
}

async function mpJoinRoom() {
  if (!await mpEnsurePlayer()) { renderMpProfileForm(); return; }
  const code = document.getElementById('mp-join-code')?.value?.toUpperCase().trim();
  if (!code || code.length < 4) { showToast('Code invalide'); return; }
  const {data: room} = await sb.from('rooms').select('*').eq('code', code).eq('status', 'waiting').single();
  if (!room) { showToast('Salon introuvable ou déjà en cours'); return; }
  mpRoomId = room.id;
  mpRoomCode = code;
  mpIsHost = false;
  const pData = await sb.from('players').select('username,avatar_emoji').eq('id', mpPlayerId).single();
  await sb.from('room_players').insert({
    room_id: mpRoomId, player_id: mpPlayerId,
    username: pData.data?.username || 'Joueur',
    avatar_emoji: pData.data?.avatar_emoji || '🕵️',
    is_host: false, is_ready: false,
  });
  showScreen('screen-mp-lobby');
  renderMpLobby();
  mpSubscribeToRoom();
  SoundFX.click();
}

async function mpQuickMatch() {
  if (!await mpEnsurePlayer()) { renderMpProfileForm(); return; }
  const {data: rooms} = await sb.from('rooms').select('*').eq('status', 'waiting').limit(5);
  if (rooms && rooms.length > 0) {
    const room = rooms[Math.floor(Math.random() * rooms.length)];
    document.getElementById('mp-join-code').value = room.code;
    await mpJoinRoom();
  } else {
    await mpCreateRoom();
  }
}

function mpSubscribeToRoom() {
  if (!sb || !mpRoomId) return;
  mpChannel = sb.channel('room-' + mpRoomId)
    .on('postgres_changes', {event:'*', schema:'public', table:'room_players', filter:'room_id=eq.' + mpRoomId}, () => renderMpLobby())
    .on('postgres_changes', {event:'*', schema:'public', table:'game_state', filter:'room_id=eq.' + mpRoomId}, (payload) => handleMpGameState(payload.new))
    .on('postgres_changes', {event:'*', schema:'public', table:'rooms', filter:'id=eq.' + mpRoomId}, (payload) => {
      if (payload.new?.status === 'playing') showScreen('screen-mp-game');
    })
    .subscribe();
}

async function renderMpLobby() {
  document.getElementById('mp-room-code').textContent = mpRoomCode || '------';
  const {data: players} = await sb.from('room_players').select('*').eq('room_id', mpRoomId).order('joined_at');
  const list = document.getElementById('mp-player-list');
  if (!list || !players) return;
  list.innerHTML = '';
  let allReady = true;
  players.forEach(p => {
    if (!p.is_ready) allReady = false;
    const row = document.createElement('div');
    row.className = 'mp-player-row';
    row.innerHTML = '<div class="mp-avatar">' + (p.avatar_emoji || '🕵️') + '</div>' +
      '<div class="mp-info"><div class="mp-name">' + (p.username || 'Joueur') +
      (p.is_host ? '<span class="mp-host-badge">HÔTE</span>' : '') + '</div>' +
      '<div class="mp-level">Nv.1</div></div>' +
      '<span class="mp-ready-badge ' + (p.is_ready ? 'ready' : 'waiting') + '">' +
      (p.is_ready ? '✓ Prêt' : 'En attente') + '</span>';
    list.appendChild(row);
  });
  // Host controls
  const hostCtrl = document.getElementById('mp-host-controls');
  const guestCtrl = document.getElementById('mp-guest-controls');
  if (mpIsHost) {
    hostCtrl.style.display = 'block';
    guestCtrl.style.display = 'none';
    const btn = document.getElementById('mp-start-btn');
    const canStart = allReady && players.length >= 3;
    btn.disabled = !canStart;
    btn.textContent = canStart ? 'LANCER LA PARTIE (' + players.length + ' joueurs)' : 'En attente... (' + players.length + '/3 min)';
  } else {
    hostCtrl.style.display = 'none';
    guestCtrl.style.display = 'block';
  }
}

async function mpToggleReady() {
  mpIsReady = !mpIsReady;
  await sb.from('room_players').update({is_ready: mpIsReady}).eq('room_id', mpRoomId).eq('player_id', mpPlayerId);
  document.getElementById('mp-ready-btn').textContent = mpIsReady ? '✗ Pas prêt' : '✓ PRÊT';
  document.getElementById('mp-ready-btn').classList.toggle('btn-primary', !mpIsReady);
  document.getElementById('mp-ready-btn').classList.toggle('btn-ghost', mpIsReady);
  SoundFX.click();
}

async function mpStartGame() {
  if (!mpIsHost) return;
  // Pick a random pair
  const pair = PAIRS[Math.floor(Math.random() * PAIRS.length)];
  const {data: players} = await sb.from('room_players').select('*').eq('room_id', mpRoomId);
  if (!players || players.length < 3) return;
  // Assign roles
  const indices = players.map((_, i) => i);
  for (let i = indices.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i+1)); [indices[i],indices[j]] = [indices[j],indices[i]]; }
  const roles = {};
  players.forEach((p, i) => {
    const roleIdx = indices.indexOf(i);
    roles[p.player_id] = roleIdx === 0 ? 'undercover' : 'civil';
  });
  // Create game state
  await sb.from('game_state').insert({
    room_id: mpRoomId, phase: 'reveal',
    current_pair: {civil: pair.civil, undercover: pair.undercover, civilImg: pair.civilImg, undercoverImg: pair.undercoverImg, hint: pair.hint},
    roles: roles, votes: {}, eliminated: [], round: 1, total_rounds: 5,
  });
  await sb.from('rooms').update({status: 'playing'}).eq('id', mpRoomId);
  SoundFX.reveal();
}

function handleMpGameState(state) {
  if (!state) return;
  const content = document.getElementById('mp-game-content');
  if (!content) return;
  const myRole = state.roles?.[mpPlayerId] || 'civil';
  const pair = state.current_pair || {};
  const myChar = myRole === 'undercover' ? pair.undercover : pair.civil;
  const myImg = myRole === 'undercover' ? pair.undercoverImg : pair.civilImg;

  if (state.phase === 'reveal') {
    content.innerHTML = '<h2>Ton rôle</h2>' +
      '<div class="role-card" style="display:inline-block;padding:24px;border-radius:20px;' +
      (myRole === 'undercover' ? 'background:linear-gradient(145deg,#5f1e1e,#3d0f0f);border:2px solid var(--accent-undercover);' : 'background:linear-gradient(145deg,#1e3a5f,#0f1f3d);border:2px solid var(--accent-civil);') + '">' +
      (myImg ? '<img src="' + myImg + '" style="width:120px;height:120px;border-radius:16px;object-fit:cover;object-position:top;margin-bottom:10px;" />' : '') +
      '<div style="font-size:1.5rem;font-weight:700;color:var(--text-bright);">' + (myChar || '???') + '</div>' +
      '<div style="font-size:0.9rem;color:' + (myRole === 'undercover' ? 'var(--accent-undercover)' : 'var(--accent-civil)') + ';margin-top:6px;">' +
      (myRole === 'undercover' ? 'UNDERCOVER' : myRole === 'mrwhite' ? 'MR. WHITE' : 'CIVIL') + '</div></div>' +
      '<div style="margin-top:16px;"><button class="btn btn-primary" onclick="mpMarkReady()">J\'ai mémorisé ✓</button></div>';
  } else if (state.phase === 'discuss') {
    content.innerHTML = '<h2>Phase de discussion</h2>' +
      '<p style="color:var(--text-muted);margin:10px 0;">Donnez un indice sur votre personnage !</p>' +
      '<p style="font-size:0.85rem;color:var(--text-dim);">L\'hôte passera au vote quand tout le monde a parlé.</p>' +
      (mpIsHost ? '<button class="btn btn-primary" onclick="mpAdvancePhase(\'vote\')" style="margin-top:14px;">Passer au vote</button>' : '');
  } else if (state.phase === 'vote') {
    renderMpVote(state);
  } else if (state.phase === 'result') {
    const winner = state.winner || 'civil';
    content.innerHTML = '<h2 style="color:' + (winner === 'civil' ? 'var(--accent-civil)' : 'var(--accent-undercover)') + ';">' +
      (winner === 'civil' ? 'Victoire des Civils !' : 'L\'Undercover gagne !') + '</h2>' +
      '<div style="margin:16px 0;">' +
      (pair.hint ? '<div class="hint-box"><div class="hint-label">Le saviez-vous ?</div><div class="hint-text">' + pair.hint + '</div></div>' : '') +
      '</div>' +
      '<button class="btn btn-primary" onclick="mpLeaveRoom()">Quitter</button>';
  }
}

async function mpMarkReady() {
  await sb.from('room_players').update({is_ready: true}).eq('room_id', mpRoomId).eq('player_id', mpPlayerId);
  showToast('Prêt !');
}

async function mpAdvancePhase(phase) {
  if (!mpIsHost) return;
  await sb.from('game_state').update({phase: phase, updated_at: new Date().toISOString()}).eq('room_id', mpRoomId);
}

async function renderMpVote(state) {
  const content = document.getElementById('mp-game-content');
  const {data: players} = await sb.from('room_players').select('*').eq('room_id', mpRoomId);
  const eliminated = state.eliminated || [];
  const alive = players?.filter(p => !eliminated.includes(p.player_id)) || [];
  const myVote = state.votes?.[mpPlayerId];

  let html = '<h2>Vote</h2><p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:12px;">Qui est suspect ?</p>';
  html += '<div style="display:flex;flex-direction:column;gap:8px;width:100%;max-width:300px;">';
  alive.forEach(p => {
    if (p.player_id === mpPlayerId) return;
    const voted = myVote === p.player_id;
    html += '<button class="btn ' + (voted ? 'btn-primary' : 'btn-ghost') + '" onclick="mpVoteFor(\'' + p.player_id + '\')" style="justify-content:flex-start;gap:10px;">' +
      '<span style="font-size:1.2rem;">' + (p.avatar_emoji || '🕵️') + '</span> ' + p.username +
      (voted ? ' ✓' : '') + '</button>';
  });
  html += '</div>';
  if (mpIsHost) {
    html += '<button class="btn btn-primary" onclick="mpResolveVote()" style="margin-top:14px;">Résoudre le vote</button>';
  }
  content.innerHTML = html;
}

async function mpVoteFor(targetId) {
  const {data: gs} = await sb.from('game_state').select('votes').eq('room_id', mpRoomId).single();
  const votes = gs?.votes || {};
  votes[mpPlayerId] = targetId;
  await sb.from('game_state').update({votes: votes, updated_at: new Date().toISOString()}).eq('room_id', mpRoomId);
  SoundFX.click();
}

async function mpResolveVote() {
  if (!mpIsHost) return;
  const {data: gs} = await sb.from('game_state').select('*').eq('room_id', mpRoomId).single();
  const votes = gs?.votes || {};
  // Tally
  const tally = {};
  Object.values(votes).forEach(v => { tally[v] = (tally[v] || 0) + 1; });
  const maxVotes = Math.max(0, ...Object.values(tally));
  const eliminated_id = Object.entries(tally).find(([_, v]) => v === maxVotes)?.[0];
  if (!eliminated_id) return;
  const elim = [...(gs.eliminated || []), eliminated_id];
  // Check win condition
  const roles = gs.roles || {};
  const aliveRoles = Object.entries(roles).filter(([id]) => !elim.includes(id));
  const ucAlive = aliveRoles.filter(([_, r]) => r === 'undercover').length;
  const civAlive = aliveRoles.filter(([_, r]) => r === 'civil').length;
  let phase = 'discuss';
  let winner = null;
  if (ucAlive === 0) { phase = 'result'; winner = 'civil'; }
  else if (ucAlive >= civAlive) { phase = 'result'; winner = 'undercover'; }
  await sb.from('game_state').update({eliminated: elim, votes: {}, phase, winner, updated_at: new Date().toISOString()}).eq('room_id', mpRoomId);
}

async function mpLeaveRoom() {
  if (sb && mpRoomId && mpPlayerId) {
    await sb.from('room_players').delete().eq('room_id', mpRoomId).eq('player_id', mpPlayerId);
    if (mpIsHost) await sb.from('rooms').delete().eq('id', mpRoomId);
  }
  if (mpChannel) { sb.removeChannel(mpChannel); mpChannel = null; }
  mpRoomId = null; mpRoomCode = null; mpIsHost = false; mpIsReady = false;
  showScreen('screen-mp-menu');
}

function mpCopyCode() {
  try { navigator.clipboard.writeText(mpRoomCode || ''); showToast('Code copié !'); } catch(e) {}
}

async function mpSendChat() {
  // Simple broadcast via channel (not persisted)
  const input = document.getElementById('mp-chat-input');
  const msg = input?.value?.trim();
  if (!msg || !mpChannel) return;
  const pData = await sb.from('players').select('username').eq('id', mpPlayerId).single();
  mpChannel.send({type:'broadcast', event:'chat', payload:{sender: pData.data?.username || 'Joueur', msg}});
  input.value = '';
  appendChatMsg(pData.data?.username || 'Moi', msg);
}

function appendChatMsg(sender, msg) {
  const container = document.getElementById('mp-chat-messages');
  if (!container) return;
  const div = document.createElement('div');
  div.className = 'mp-chat-msg';
  div.innerHTML = '<span class="sender">' + sender + ':</span> ' + msg;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function renderMpProfileForm() {
  const section = document.getElementById('mp-profile-section');
  if (!section) return;
  section.innerHTML = '<div style="text-align:center;margin:12px 0;">' +
    '<p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:10px;">Crée ton profil en ligne</p>' +
    '<div class="mp-join-input" style="max-width:250px;">' +
    '<input type="text" id="mp-username" placeholder="Pseudo" style="letter-spacing:normal;text-transform:none;">' +
    '<button class="btn btn-primary" onclick="mpCreateProfile(document.getElementById(\'mp-username\').value)">Créer</button>' +
    '</div></div>';
}

async function renderMpMenu() {
  const section = document.getElementById('mp-profile-section');
  if (!section) return;
  if (!sb) {
    section.innerHTML = '<div style="color:var(--accent-undercover);text-align:center;font-size:0.85rem;">Serveur non disponible — Mode hors-ligne uniquement</div>';
    document.getElementById('mp-status').innerHTML = '<div class="dot offline"></div><span>Hors ligne</span>';
    return;
  }
  const ok = await mpEnsurePlayer();
  if (!ok) { renderMpProfileForm(); return; }
  const {data} = await sb.from('players').select('*').eq('id', mpPlayerId).single();
  if (data) {
    section.innerHTML = '<div style="text-align:center;">' +
      '<div style="font-size:2rem;">' + (data.avatar_emoji || '🕵️') + '</div>' +
      '<div style="font-weight:700;color:var(--text-bright);font-size:1rem;">' + data.username + '</div>' +
      '<div style="font-size:0.75rem;color:var(--text-muted);">Nv.' + data.level + ' • ' + data.rank_tier + ' • ' + data.rank_points + ' pts</div></div>';
    document.getElementById('mp-status').innerHTML = '<div class="dot online"></div><span>Connecté</span>';
  }
}

async function loadLeaderboard() {
  if (!sb) return;
  const {data} = await sb.from('leaderboard').select('*').order('rank_points', {ascending:false}).limit(50);
  if (!data || !data.length) {
    document.getElementById('lb-list').innerHTML = '<div style="text-align:center;color:var(--text-muted);padding:20px;">Aucun joueur classé</div>';
    return;
  }
  // Podium
  const podium = document.getElementById('lb-podium');
  podium.innerHTML = '';
  const medals = ['🥇','🥈','🥉'];
  data.slice(0, 3).forEach((p, i) => {
    const cls = i === 0 ? 'first' : i === 1 ? 'second' : 'third';
    const div = document.createElement('div');
    div.className = 'lb-podium-item ' + cls;
    div.innerHTML = '<div class="lb-rank">' + medals[i] + '</div>' +
      '<div style="font-size:1.5rem;">' + (p.avatar_emoji || '🕵️') + '</div>' +
      '<div class="lb-name">' + p.username + '</div>' +
      '<div class="lb-pts">' + p.rank_points + ' pts</div>';
    podium.appendChild(div);
  });
  // List
  const list = document.getElementById('lb-list');
  list.innerHTML = '';
  data.forEach((p, i) => {
    const row = document.createElement('div');
    row.className = 'lb-row' + (p.player_id === mpPlayerId ? ' me' : '');
    row.innerHTML = '<div class="lb-pos">#' + (i+1) + '</div>' +
      '<div style="font-size:1.1rem;">' + (p.avatar_emoji || '🕵️') + '</div>' +
      '<div class="lb-row-name">' + p.username + '</div>' +
      '<div class="lb-row-pts">' + p.rank_points + ' pts</div>';
    list.appendChild(row);
  });
}

// Patch showScreen for MP screens
const _prevShowScreenMP = showScreen;
showScreen = function(id) {
  _prevShowScreenMP(id);
  if (id === 'screen-mp-menu') { initSupabase(); renderMpMenu(); }
  if (id === 'screen-mp-leaderboard') loadLeaderboard();
};

// Init Supabase when page loads
document.addEventListener('DOMContentLoaded', () => { initSupabase(); });
"""

html = html.replace("\n</script>", JS_MP + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Multiplayer patch applied! Template: {len(html)//1024} KB")
