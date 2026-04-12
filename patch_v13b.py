#!/usr/bin/env python3
"""V13b: Complete multiplayer sync, WebRTC voice, visual polish."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. CSS for voice chat, polish
# ═══════════════════════════════════════════════════════════
CSS = """
/* ===== VOICE CHAT ===== */
.voice-fab {
  position:fixed; bottom:130px; left:12px; z-index:360;
  width:44px; height:44px; border-radius:50%;
  background:var(--bg-secondary); border:1px solid var(--border-glass);
  display:none; align-items:center; justify-content:center;
  font-size:1.1rem; cursor:pointer; backdrop-filter:blur(10px);
  box-shadow:var(--shadow-sm); transition:all 0.2s;
}
.voice-fab.active { display:flex; }
.voice-fab.speaking { background:var(--accent-green); border-color:var(--accent-green);
  animation:voicePulse 1s ease infinite; }
@keyframes voicePulse { 0%,100%{box-shadow:0 0 0 0 rgba(34,197,94,0.3)} 50%{box-shadow:0 0 0 12px rgba(34,197,94,0)} }
.voice-fab.muted { opacity:0.5; }

.voice-indicator {
  position:absolute; top:-4px; right:-4px; width:12px; height:12px;
  border-radius:50%; border:2px solid var(--bg-secondary);
}
.voice-indicator.connected { background:var(--accent-green); }
.voice-indicator.disconnected { background:var(--accent-undercover); }

/* ===== VOTE PROGRESS BARS ===== */
.mp-vote-progress {
  width:100%; max-width:350px; margin:10px auto;
}
.mp-vote-bar {
  display:flex; align-items:center; gap:8px; padding:6px 0;
}
.mp-vote-bar .vb-name { min-width:70px; font-size:0.8rem; color:var(--text-primary); }
.mp-vote-bar .vb-track {
  flex:1; height:12px; background:rgba(255,255,255,0.06);
  border-radius:6px; overflow:hidden;
}
.mp-vote-bar .vb-fill {
  height:100%; background:linear-gradient(90deg,var(--accent-undercover),#ff6b81);
  border-radius:6px; transition:width 0.4s ease;
}
.mp-vote-bar .vb-count { min-width:24px; font-size:0.75rem; color:var(--text-muted); text-align:right; }

/* ===== SCREEN TRANSITIONS ===== */
.screen { transition:opacity 0.35s ease, transform 0.35s cubic-bezier(0.22,1,0.36,1) !important; }
.screen:not(.active) { transform:translateY(20px); }
.screen.active { transform:translateY(0); }

/* ===== MP TIMER ===== */
.mp-timer {
  font-family:var(--font-display); font-size:2.5rem; font-weight:900;
  color:var(--accent-gold); text-align:center; margin:10px 0;
}
.mp-timer.warning { color:var(--accent-undercover); animation:pulse 0.5s ease infinite; }

/* ===== MP ELIMINATION SCREEN ===== */
.mp-elim-card {
  background:var(--bg-card); border:2px solid var(--accent-undercover);
  border-radius:var(--radius-xl); padding:24px; text-align:center;
  max-width:320px; width:90%; margin:0 auto;
  animation:slideInUp 0.5s cubic-bezier(0.22,1,0.36,1);
}
@keyframes slideInUp { from{opacity:0;transform:translateY(40px)} to{opacity:1;transform:translateY(0)} }
.mp-elim-name { font-size:1.5rem; font-weight:700; color:var(--accent-undercover); margin:8px 0; }
.mp-elim-role { font-size:1rem; margin:6px 0; }

/* ===== REVANCHE ===== */
.mp-result-actions { display:flex; gap:10px; justify-content:center; margin-top:16px; flex-wrap:wrap; }
"""

html = html.replace("/* ===== APP CONTAINER ===== */", CSS + "\n/* ===== APP CONTAINER ===== */")

# ═══════════════════════════════════════════════════════════
# 2. HTML: Voice FAB
# ═══════════════════════════════════════════════════════════
html = html.replace(
    '<!-- ===== BOTTOM NAV ===== -->',
    '<!-- ===== VOICE CHAT FAB ===== -->\n'
    '<div class="voice-fab" id="voice-fab" onclick="toggleVoice()">\n'
    '  🎙️\n'
    '  <div class="voice-indicator disconnected" id="voice-indicator"></div>\n'
    '</div>\n\n'
    '<!-- ===== BOTTOM NAV ===== -->'
)

# ═══════════════════════════════════════════════════════════
# 3. JAVASCRIPT: Complete multiplayer + WebRTC + polish
# ═══════════════════════════════════════════════════════════
JS = r"""

// ===== V13b: COMPLETE MULTIPLAYER SYNC =====

// Override handleMpGame for full phase support
var _origHandleMpGame = handleMpGame;
handleMpGame = function(state) {
  if (!state) return;
  showScreen("screen-mp-game");
  var content = document.getElementById("mp-game-content");
  if (!content) return;
  var myRole = (state.roles || {})[mpPlayerId];
  var roleData = typeof myRole === "object" ? myRole : {role: myRole || "civil"};
  var role = roleData.role || myRole || "civil";
  var pair = state.current_pair || {};
  var myChar = role === "undercover" ? (pair.undercover || "???") : role === "mrwhite" ? "???" : (pair.civil || "???");
  var myImg = role === "undercover" ? ImageLoader.resolve(pair.undercoverImg) : role === "mrwhite" ? "" : ImageLoader.resolve(pair.civilImg);
  var roleColor = role === "undercover" ? "var(--accent-undercover)" : role === "mrwhite" ? "var(--accent-mrwhite)" : "var(--accent-civil)";
  var roleLabel = role === "undercover" ? "UNDERCOVER" : role === "mrwhite" ? "MR. WHITE" : "CIVIL";

  // Show voice FAB during game
  var vfab = document.getElementById("voice-fab");
  if (vfab) vfab.classList.add("active");

  if (state.phase === "reveal") {
    content.innerHTML = "<h2>Ton rôle</h2>" +
      "<div class=\"mp-elim-card\" style=\"border-color:" + roleColor + "\">" +
      (myImg ? "<img src=\"" + myImg + "\" style=\"width:120px;height:120px;border-radius:16px;object-fit:cover;object-position:top;margin-bottom:10px\" />" : "") +
      "<div style=\"font-size:1.5rem;font-weight:700;color:var(--text-bright)\">" + myChar + "</div>" +
      "<div style=\"font-size:0.9rem;color:" + roleColor + ";margin-top:6px\">" + roleLabel + "</div>" +
      (role === "mrwhite" ? "<div style=\"font-size:0.8rem;color:var(--text-muted);margin-top:6px\">Tu ne connais pas le personnage...</div>" : "") +
      "</div>" +
      "<div style=\"margin-top:16px\"><button class=\"btn btn-primary\" onclick=\"mpMarkReady()\">Mémorisé ✓</button></div>";
  }

  else if (state.phase === "discuss") {
    var endTime = state.discuss_end_time || 0;
    var remaining = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
    content.innerHTML = "<h2>💬 Discussion</h2>" +
      "<div class=\"mp-timer\" id=\"mp-discuss-timer\">" + remaining + "s</div>" +
      "<p style=\"color:var(--text-muted);font-size:0.85rem\">Donnez un indice sur votre personnage sans le nommer !</p>" +
      (mpIsHost ? "<button class=\"btn btn-primary\" onclick=\"mpAdvancePhase('vote')\" style=\"margin-top:14px\">Passer au vote</button>" : "");
    // Start timer countdown
    if (endTime > Date.now()) {
      clearInterval(window._mpTimerInterval);
      window._mpTimerInterval = setInterval(function() {
        var rem = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
        var el = document.getElementById("mp-discuss-timer");
        if (el) {
          el.textContent = rem + "s";
          if (rem <= 10) el.classList.add("warning");
        }
        if (rem <= 0) {
          clearInterval(window._mpTimerInterval);
          if (mpIsHost) mpAdvancePhase("vote");
        }
      }, 1000);
    }
  }

  else if (state.phase === "vote") {
    clearInterval(window._mpTimerInterval);
    mpRenderVoteSync(state);
  }

  else if (state.phase === "elimination") {
    clearInterval(window._mpTimerInterval);
    var elimId = state.eliminated_player;
    var elimRole = (state.roles || {})[elimId];
    var elimRoleStr = typeof elimRole === "object" ? elimRole.role : elimRole;
    var elimName = state.eliminated_name || "Joueur";
    content.innerHTML = "<h2>Éliminé !</h2>" +
      "<div class=\"mp-elim-card\">" +
      "<div class=\"mp-elim-name\">" + elimName + "</div>" +
      "<div class=\"mp-elim-role\" style=\"color:" + (elimRoleStr==="undercover"?"var(--accent-undercover)":elimRoleStr==="mrwhite"?"var(--accent-mrwhite)":"var(--accent-civil)") + "\">" +
      (elimRoleStr==="undercover"?"UNDERCOVER":elimRoleStr==="mrwhite"?"MR. WHITE":"CIVIL") + "</div>" +
      "</div>" +
      (pair.hint ? "<div class=\"hint-box\" style=\"margin-top:12px\"><div class=\"hint-label\">Le saviez-vous ?</div><div class=\"hint-text\">" + (pair.hint||"") + "</div></div>" : "") +
      (elimRoleStr === "mrwhite" && elimId === mpPlayerId ?
        "<div style=\"margin-top:12px\"><p style=\"color:var(--accent-gold)\">Tu peux deviner le personnage civil !</p>" +
        "<input type=\"text\" id=\"mw-guess-input\" placeholder=\"Ton guess...\" style=\"background:var(--bg-card);border:1px solid var(--border-glass);border-radius:8px;padding:10px;color:var(--text-bright);font-size:1rem;width:200px;margin:8px 0\">" +
        "<button class=\"btn btn-primary\" onclick=\"mpMrWhiteGuess()\">Deviner</button></div>" : "") +
      (mpIsHost ? "<button class=\"btn btn-primary\" onclick=\"mpContinueAfterElim()\" style=\"margin-top:14px\">Continuer</button>" : "");
    SoundFX.eliminate();
  }

  else if (state.phase === "finished") {
    clearInterval(window._mpTimerInterval);
    var winner = state.winner || "civil";
    content.innerHTML = "<h2 style=\"color:" + (winner==="civil"?"var(--accent-civil)":"var(--accent-undercover)") + "\">" +
      (winner==="civil"?"Victoire des Civils !":"Undercover gagne !") + "</h2>" +
      "<div style=\"display:flex;gap:16px;justify-content:center;margin:16px 0\">" +
      "<div style=\"text-align:center\">" +
      (ImageLoader.resolve(pair.civilImg) ? "<img src=\"" + ImageLoader.resolve(pair.civilImg) + "\" style=\"width:80px;height:80px;border-radius:12px;object-fit:cover;object-position:top\" />" : "") +
      "<div style=\"font-size:0.85rem;font-weight:600;color:var(--text-bright);margin-top:4px\">" + (pair.civil||"") + "</div>" +
      "<div style=\"font-size:0.7rem;color:var(--accent-civil)\">Civil</div></div>" +
      "<div style=\"display:flex;align-items:center;color:var(--text-dim)\">VS</div>" +
      "<div style=\"text-align:center\">" +
      (ImageLoader.resolve(pair.undercoverImg) ? "<img src=\"" + ImageLoader.resolve(pair.undercoverImg) + "\" style=\"width:80px;height:80px;border-radius:12px;object-fit:cover;object-position:top\" />" : "") +
      "<div style=\"font-size:0.85rem;font-weight:600;color:var(--text-bright);margin-top:4px\">" + (pair.undercover||"") + "</div>" +
      "<div style=\"font-size:0.7rem;color:var(--accent-undercover)\">Undercover</div></div></div>" +
      (pair.hint ? "<div class=\"hint-box\"><div class=\"hint-label\">Le saviez-vous ?</div><div class=\"hint-text\">" + (pair.hint||"") + "</div></div>" : "") +
      "<div class=\"mp-result-actions\">" +
      (mpIsHost ? "<button class=\"btn btn-primary\" onclick=\"mpRevanche()\">Revanche</button>" : "") +
      "<button class=\"btn btn-ghost\" onclick=\"mpLeaveRoom()\">Quitter</button></div>";
    SoundFX.victory();
    spawnConfetti(30);
    // Hide voice FAB
    var vf = document.getElementById("voice-fab"); if (vf) vf.classList.remove("active");
  }
};

// Synced vote rendering with live progress bars
async function mpRenderVoteSync(state) {
  var content = document.getElementById("mp-game-content");
  var res = await sb.from("room_players").select("*").eq("room_id", mpRoomId);
  var players = res.data || [];
  var eliminated = state.eliminated || [];
  var alive = players.filter(function(p) { return eliminated.indexOf(p.player_id) < 0; });
  var votes = state.votes || {};
  var myVote = votes[mpPlayerId];
  var totalVoters = alive.length;
  var votesIn = Object.keys(votes).length;

  // Tally for progress bars (don't reveal WHO voted for whom)
  var tally = {};
  alive.forEach(function(p) { tally[p.player_id] = 0; });
  Object.values(votes).forEach(function(t) { if (tally[t] !== undefined) tally[t]++; });
  var maxVotes = Math.max(1, Math.max.apply(null, Object.values(tally)));

  var h = "<h2>🗳️ Vote</h2>";
  h += "<div style=\"font-size:0.8rem;color:var(--text-muted);margin-bottom:10px\">" + votesIn + "/" + totalVoters + " votes</div>";

  if (!myVote) {
    // Player hasn't voted yet - show vote buttons
    h += "<div style=\"display:flex;flex-direction:column;gap:8px;width:100%;max-width:300px\">";
    alive.forEach(function(p) {
      if (p.player_id === mpPlayerId) return;
      h += "<button class=\"btn btn-ghost\" data-vid=\"" + p.player_id + "\" onclick=\"mpVoteFor(this.dataset.vid)\" style=\"justify-content:flex-start;gap:10px\">" +
        "<span style=\"font-size:1.2rem\">" + (p.avatar_emoji || "🕵️") + "</span> " + p.username + "</button>";
    });
    h += "</div>";
  } else {
    h += "<div style=\"color:var(--accent-green);margin-bottom:10px\">✓ Vote enregistré</div>";
  }

  // Progress bars (visible to all)
  h += "<div class=\"mp-vote-progress\">";
  alive.forEach(function(p) {
    var count = tally[p.player_id] || 0;
    var pct = (count / maxVotes) * 100;
    h += "<div class=\"mp-vote-bar\">" +
      "<span class=\"vb-name\">" + (p.avatar_emoji || "🕵️") + " " + (p.username || "").substring(0,8) + "</span>" +
      "<div class=\"vb-track\"><div class=\"vb-fill\" style=\"width:" + pct + "%\"></div></div>" +
      "<span class=\"vb-count\">" + count + "</span></div>";
  });
  h += "</div>";

  // Auto-resolve when all voted
  if (votesIn >= totalVoters && mpIsHost) {
    h += "<button class=\"btn btn-primary\" onclick=\"mpResolveVote()\" style=\"margin-top:12px\">Résoudre le vote</button>";
  }

  content.innerHTML = h;
}

// Mr. White guess
async function mpMrWhiteGuess() {
  var input = document.getElementById("mw-guess-input");
  var guess = input ? input.value.trim().toLowerCase() : "";
  var gs = (await sb.from("game_state").select("current_pair").eq("room_id", mpRoomId).single()).data;
  var civilWord = (gs?.current_pair?.civil || "").toLowerCase();
  if (guess === civilWord) {
    showToast("Mr. White a deviné ! 👻");
    await sb.from("game_state").update({phase: "finished", winner: "undercover"}).eq("room_id", mpRoomId);
  } else {
    showToast("Mauvaise réponse !");
  }
}

// Host starts discussion with timer
var _origMpAdvancePhase = mpAdvancePhase;
mpAdvancePhase = async function(phase) {
  if (!mpIsHost) return;
  var update = {phase: phase};
  if (phase === "discuss") {
    update.discuss_end_time = Date.now() + 60000; // 60s timer
    update.votes = {};
  }
  if (phase === "vote") {
    update.votes = {};
  }
  await sb.from("game_state").update(update).eq("room_id", mpRoomId);
};

// Continue after elimination - check win conditions
async function mpContinueAfterElim() {
  if (!mpIsHost) return;
  var res = await sb.from("game_state").select("*").eq("room_id", mpRoomId).single();
  var gs = res.data;
  if (!gs) return;
  var roles = gs.roles || {};
  var eliminated = gs.eliminated || [];
  var aliveEntries = Object.entries(roles).filter(function(e) { return eliminated.indexOf(e[0]) < 0; });
  var ucAlive = aliveEntries.filter(function(e) { var r = typeof e[1]==="object"?e[1].role:e[1]; return r==="undercover"; }).length;
  var civAlive = aliveEntries.filter(function(e) { var r = typeof e[1]==="object"?e[1].role:e[1]; return r==="civil"; }).length;

  if (ucAlive === 0) {
    await sb.from("game_state").update({phase:"finished", winner:"civil"}).eq("room_id", mpRoomId);
  } else if (ucAlive >= civAlive) {
    await sb.from("game_state").update({phase:"finished", winner:"undercover"}).eq("room_id", mpRoomId);
  } else {
    // Continue to discuss
    await mpAdvancePhase("discuss");
  }
}

// Resolve vote with name tracking
var _origMpResolveVote = mpResolveVote;
mpResolveVote = async function() {
  if (!mpIsHost) return;
  var gs = (await sb.from("game_state").select("*").eq("room_id", mpRoomId).single()).data;
  if (!gs) return;
  var votes = gs.votes || {};
  var tally = {};
  Object.values(votes).forEach(function(v) { tally[v] = (tally[v]||0) + 1; });
  var maxV = Math.max(0, Math.max.apply(null, Object.values(tally).concat([0])));
  if (maxV === 0) return;
  var tied = Object.keys(tally).filter(function(k) { return tally[k] === maxV; });
  var elimId = tied[Math.floor(Math.random() * tied.length)];
  // Get name
  var pRes = await sb.from("room_players").select("username").eq("room_id", mpRoomId).eq("player_id", elimId).single();
  var elimName = pRes.data?.username || "Joueur";
  var newElim = (gs.eliminated || []).concat([elimId]);
  await sb.from("game_state").update({
    phase: "elimination",
    eliminated: newElim,
    eliminated_player: elimId,
    eliminated_name: elimName,
    votes: {}
  }).eq("room_id", mpRoomId);
};

// Revanche - new game same room
async function mpRevanche() {
  if (!mpIsHost) return;
  // Reset readiness
  await sb.from("room_players").update({is_ready: false}).eq("room_id", mpRoomId);
  // Delete old game state
  await sb.from("game_state").delete().eq("room_id", mpRoomId);
  // Reset room
  await sb.from("rooms").update({status: "waiting"}).eq("id", mpRoomId);
  showScreen("screen-mp-lobby");
  renderMpLobby();
}

// Override mpStartGame for richer role assignment
var _origMpStartGame = mpStartGame;
mpStartGame = async function() {
  if (!mpIsHost) return;
  await ImageLoader.load(); // Ensure images available
  // Pick pair based on mode
  var available = PAIRS.filter(function(p) { return (p.mode || "normal") === (GameState.currentMode || "normal"); });
  if (available.length === 0) available = PAIRS;
  var pair = available[Math.floor(Math.random() * available.length)];
  var res = await sb.from("room_players").select("*").eq("room_id", mpRoomId);
  var players = res.data || [];
  if (players.length < 3) { showToast("Il faut au moins 3 joueurs"); return; }
  // Shuffle and assign
  var indices = players.map(function(_,i){return i}).sort(function(){return Math.random()-0.5});
  var roles = {};
  players.forEach(function(p, i) {
    var roleIdx = indices.indexOf(i);
    var role = roleIdx === 0 ? "undercover" : "civil";
    roles[p.player_id] = {role: role, character: role === "undercover" ? pair.undercover : pair.civil};
  });
  await sb.from("game_state").upsert({
    room_id: mpRoomId, phase: "reveal",
    current_pair: {civil:pair.civil, undercover:pair.undercover, civilImg:pair.civilImg, undercoverImg:pair.undercoverImg, hint:pair.hint||""},
    roles: roles, votes: {}, eliminated: [], round: 1, total_rounds: 5,
    discuss_end_time: 0, eliminated_player: null, eliminated_name: null, winner: null
  });
  await sb.from("rooms").update({status: "playing"}).eq("id", mpRoomId);
  SoundFX.reveal();
};


// ===== WEBRTC VOICE CHAT =====
var voiceEnabled = false;
var localStream = null;
var peerConnections = {};
var voiceChannel = null;

async function toggleVoice() {
  if (voiceEnabled) { stopVoice(); return; }
  try {
    localStream = await navigator.mediaDevices.getUserMedia({audio: true, video: false});
    voiceEnabled = true;
    document.getElementById("voice-fab").classList.add("speaking");
    document.getElementById("voice-indicator").className = "voice-indicator connected";
    showToast("🎙️ Micro activé");
    // Setup signaling via Supabase
    setupVoiceSignaling();
  } catch(e) {
    showToast("Micro non disponible");
  }
}

function stopVoice() {
  voiceEnabled = false;
  if (localStream) { localStream.getTracks().forEach(function(t){t.stop()}); localStream = null; }
  Object.values(peerConnections).forEach(function(pc){pc.close()});
  peerConnections = {};
  document.getElementById("voice-fab").classList.remove("speaking");
  document.getElementById("voice-indicator").className = "voice-indicator disconnected";
  if (voiceChannel) { sb.removeChannel(voiceChannel); voiceChannel = null; }
}

function setupVoiceSignaling() {
  if (!sb || !mpRoomId) return;
  // Use Supabase broadcast for signaling (simpler than DB table)
  voiceChannel = sb.channel("voice-" + mpRoomId)
    .on("broadcast", {event: "offer"}, function(payload) { handleVoiceOffer(payload.payload); })
    .on("broadcast", {event: "answer"}, function(payload) { handleVoiceAnswer(payload.payload); })
    .on("broadcast", {event: "ice"}, function(payload) { handleVoiceIce(payload.payload); })
    .subscribe(function() {
      // Send offer to all peers
      broadcastVoiceOffer();
    });
}

async function broadcastVoiceOffer() {
  var res = await sb.from("room_players").select("player_id").eq("room_id", mpRoomId);
  var players = (res.data || []).filter(function(p){return p.player_id !== mpPlayerId});
  players.forEach(function(p) { createPeerConnection(p.player_id, true); });
}

function createPeerConnection(peerId, isInitiator) {
  if (peerConnections[peerId]) return peerConnections[peerId];
  var pc = new RTCPeerConnection({iceServers: [{urls: "stun:stun.l.google.com:19302"}]});
  peerConnections[peerId] = pc;

  if (localStream) {
    localStream.getTracks().forEach(function(track) { pc.addTrack(track, localStream); });
  }

  pc.ontrack = function(event) {
    var audio = new Audio();
    audio.srcObject = event.streams[0];
    audio.play().catch(function(){});
  };

  pc.onicecandidate = function(event) {
    if (event.candidate && voiceChannel) {
      voiceChannel.send({type:"broadcast", event:"ice", payload:{from:mpPlayerId, to:peerId, candidate:event.candidate}});
    }
  };

  if (isInitiator) {
    pc.createOffer().then(function(offer) {
      return pc.setLocalDescription(offer);
    }).then(function() {
      voiceChannel.send({type:"broadcast", event:"offer", payload:{from:mpPlayerId, to:peerId, sdp:pc.localDescription}});
    });
  }

  return pc;
}

function handleVoiceOffer(data) {
  if (data.to !== mpPlayerId) return;
  var pc = createPeerConnection(data.from, false);
  pc.setRemoteDescription(new RTCSessionDescription(data.sdp)).then(function() {
    return pc.createAnswer();
  }).then(function(answer) {
    return pc.setLocalDescription(answer);
  }).then(function() {
    voiceChannel.send({type:"broadcast", event:"answer", payload:{from:mpPlayerId, to:data.from, sdp:pc.localDescription}});
  });
}

function handleVoiceAnswer(data) {
  if (data.to !== mpPlayerId) return;
  var pc = peerConnections[data.from];
  if (pc) pc.setRemoteDescription(new RTCSessionDescription(data.sdp));
}

function handleVoiceIce(data) {
  if (data.to !== mpPlayerId) return;
  var pc = peerConnections[data.from];
  if (pc) pc.addIceCandidate(new RTCIceCandidate(data.candidate));
}

// Cleanup voice on leave
var _origMpLeaveRoom2 = mpLeaveRoom;
mpLeaveRoom = async function() {
  stopVoice();
  await _origMpLeaveRoom2();
};
"""

html = html.replace("\n</script>", JS + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"V13b patch applied! {len(html)//1024} KB")
