#!/usr/bin/env python3
"""Replace all MP gameplay with broadcast-only approach."""

with open("game_template.html", "r", encoding="utf-8") as f:
    html = f.read()

NEW_MP = r"""

// ═══ BROADCAST-ONLY MULTIPLAYER (no DB during gameplay) ═══
var _mpGS = null;

function mpBcast() {
  if (!mpIsHost || !mpChannel || !_mpGS) return;
  mpChannel.send({type:"broadcast",event:"gs",payload:_mpGS});
  _handleGS(_mpGS);
}

function _handleGS(s) {
  if (!s) return;
  _mpGS = s;
  showScreen("screen-mp-game");
  var c = document.getElementById("mp-game-content");
  if (!c) return;
  var r = (s.roles||{})[mpPlayerId];
  var rd = typeof r==="object"?r:{role:r||"civil"};
  var role = rd.role||"civil";
  var p = s.pair||{};
  var ch = role==="undercover"?p.undercover:role==="mrwhite"?"???":p.civil;
  var im = role==="undercover"?ImageLoader.resolve(p.undercoverImg):role==="mrwhite"?"":ImageLoader.resolve(p.civilImg);
  var rc = role==="undercover"?"var(--accent-undercover)":role==="mrwhite"?"var(--accent-mrwhite)":"var(--accent-civil)";
  var rl = role==="undercover"?"UNDERCOVER":role==="mrwhite"?"MR. WHITE":"CIVIL";

  if (s.phase==="reveal") {
    c.innerHTML="<h2>Ton rôle</h2><div style='display:inline-block;padding:24px;border-radius:20px;border:2px solid "+rc+";background:var(--bg-card)'>"+(im?"<img src='"+im+"' style='width:120px;height:120px;border-radius:16px;object-fit:cover;object-position:top;margin-bottom:10px'/>":"")+
    "<div style='font-size:1.5rem;font-weight:700;color:var(--text-bright)'>"+ch+"</div><div style='font-size:0.9rem;color:"+rc+";margin-top:6px'>"+rl+"</div></div>"+
    "<div style='margin-top:16px'><button class='btn btn-primary' onclick='mpSendReady()'>Mémorisé ✓</button></div>";
  }
  else if (s.phase==="discuss") {
    var rem=Math.max(0,Math.floor(((s.te||0)-Date.now())/1000));
    c.innerHTML="<h2>💬 Discussion</h2><div style='font-size:2rem;font-weight:900;color:var(--accent-gold)'>"+rem+"s</div>"+
    "<p style='color:var(--text-muted);font-size:0.85rem'>Donnez un indice !</p>"+
    (mpIsHost?"<button class='btn btn-primary' onclick='mpHA(\"vote\")' style='margin-top:14px'>Passer au vote</button>":"");
    clearInterval(window._mt);
    if(s.te>Date.now()){window._mt=setInterval(function(){var r2=Math.max(0,Math.floor(((s.te||0)-Date.now())/1000));var el=c.querySelector("div");if(el)el.textContent=r2+"s";if(r2<=0){clearInterval(window._mt);if(mpIsHost)mpHA("vote")}},1000)}
  }
  else if (s.phase==="vote") {
    clearInterval(window._mt);
    var al=_mpLocalPlayers.filter(function(x){return(s.el||[]).indexOf(x.player_id)<0});
    var mv=(s.v||{})[mpPlayerId];var tv=al.length;
    var vi=Object.keys(s.v||{}).length;
    var ta={};al.forEach(function(x){ta[x.player_id]=0});Object.values(s.v||{}).forEach(function(x){if(ta[x]!==undefined)ta[x]++});
    var mx=Math.max(1,Math.max.apply(null,Object.values(ta).concat([1])));
    var h="<h2>🗳️ Vote</h2><div style='font-size:0.8rem;color:var(--text-muted);margin-bottom:10px'>"+vi+"/"+tv+" votes</div>";
    if(!mv){h+="<div style='display:flex;flex-direction:column;gap:8px;width:100%;max-width:300px'>";al.forEach(function(x){if(x.player_id===mpPlayerId)return;h+="<button class='btn btn-ghost' data-v='"+x.player_id+"' onclick='mpSV(this.dataset.v)' style='justify-content:flex-start;gap:10px'><span style='font-size:1.2rem'>"+(x.avatar_emoji||"🕵️")+"</span> "+x.username+"</button>"});h+="</div>"}
    else{h+="<div style='color:var(--accent-green);margin-bottom:10px'>✓ Vote enregistré</div>"}
    h+="<div style='margin-top:10px;width:100%;max-width:350px'>";
    al.forEach(function(x){var cn=ta[x.player_id]||0;var pc=(cn/mx)*100;h+="<div style='display:flex;align-items:center;gap:8px;padding:4px 0'><span style='min-width:70px;font-size:0.8rem'>"+(x.avatar_emoji||"🕵️")+" "+(x.username||"").substring(0,8)+"</span><div style='flex:1;height:12px;background:rgba(255,255,255,0.06);border-radius:6px;overflow:hidden'><div style='height:100%;width:"+pc+"%;background:linear-gradient(90deg,var(--accent-undercover),#ff6b81);border-radius:6px;transition:width 0.4s'></div></div><span style='min-width:20px;font-size:0.75rem;color:var(--text-muted);text-align:right'>"+cn+"</span></div>"});
    h+="</div>";
    if(vi>=tv&&mpIsHost){h+="<button class='btn btn-primary' onclick='mpHRV()' style='margin-top:12px'>Résoudre</button>"}
    c.innerHTML=h;
  }
  else if (s.phase==="elim") {
    clearInterval(window._mt);
    var ei=s.le;var ep=_mpLocalPlayers.find(function(x){return x.player_id===ei});
    var er=(s.roles||{})[ei];var ers=typeof er==="object"?er.role:er;
    c.innerHTML="<h2>Éliminé !</h2><div style='background:var(--bg-card);border:2px solid var(--accent-undercover);border-radius:20px;padding:24px;text-align:center;max-width:320px;margin:0 auto'>"+
    "<div style='font-size:1.5rem;font-weight:700;color:var(--accent-undercover)'>"+(ep?.username||"Joueur")+"</div>"+
    "<div style='font-size:1rem;color:"+(ers==="undercover"?"var(--accent-undercover)":"var(--accent-civil)")+";margin-top:6px'>"+(ers==="undercover"?"UNDERCOVER":"CIVIL")+"</div></div>"+
    (p.hint?"<div class='hint-box' style='margin-top:12px'><div class='hint-label'>Le saviez-vous ?</div><div class='hint-text'>"+p.hint+"</div></div>":"")+
    (mpIsHost?"<button class='btn btn-primary' onclick='mpHC()' style='margin-top:14px'>Continuer</button>":"");
    SoundFX.eliminate();
  }
  else if (s.phase==="done") {
    clearInterval(window._mt);
    var w=s.w||"civil";
    c.innerHTML="<h2 style='color:"+(w==="civil"?"var(--accent-civil)":"var(--accent-undercover)")+"'>"+(w==="civil"?"Victoire des Civils !":"Undercover gagne !")+"</h2>"+
    "<div style='display:flex;gap:16px;justify-content:center;margin:16px 0'>"+
    "<div style='text-align:center'>"+(ImageLoader.resolve(p.civilImg)?"<img src='"+ImageLoader.resolve(p.civilImg)+"' style='width:80px;height:80px;border-radius:12px;object-fit:cover;object-position:top'/>":"")+
    "<div style='font-size:0.85rem;font-weight:600;color:var(--text-bright);margin-top:4px'>"+(p.civil||"")+"</div></div>"+
    "<div style='display:flex;align-items:center;color:var(--text-dim)'>VS</div>"+
    "<div style='text-align:center'>"+(ImageLoader.resolve(p.undercoverImg)?"<img src='"+ImageLoader.resolve(p.undercoverImg)+"' style='width:80px;height:80px;border-radius:12px;object-fit:cover;object-position:top'/>":"")+
    "<div style='font-size:0.85rem;font-weight:600;color:var(--text-bright);margin-top:4px'>"+(p.undercover||"")+"</div></div></div>"+
    (p.hint?"<div class='hint-box'><div class='hint-label'>Le saviez-vous ?</div><div class='hint-text'>"+p.hint+"</div></div>":"")+
    "<div style='display:flex;gap:10px;justify-content:center;margin-top:16px'>"+(mpIsHost?"<button class='btn btn-primary' onclick='mpHRe()'>Revanche</button>":"")+"<button class='btn btn-ghost' onclick='mpLeaveRoom()'>Quitter</button></div>";
    SoundFX.victory();spawnConfetti(30);
  }
}

function mpHA(ph){if(!mpIsHost||!_mpGS)return;_mpGS.phase=ph;if(ph==="discuss")_mpGS.te=Date.now()+60000;if(ph==="vote"){_mpGS.v={}}mpBcast()}
function mpHRV(){if(!mpIsHost||!_mpGS)return;var v=_mpGS.v||{};var t={};Object.entries(v).forEach(function(e){t[e[1]]=(t[e[1]]||0)+1});var m=Math.max(0,Math.max.apply(null,Object.values(t).concat([0])));if(m===0)return;var ti=Object.keys(t).filter(function(k){return t[k]===m});var ei=ti[Math.floor(Math.random()*ti.length)];if(!_mpGS.el)_mpGS.el=[];_mpGS.el.push(ei);_mpGS.le=ei;_mpGS.phase="elim";_mpGS.v={};mpBcast()}
function mpHC(){if(!mpIsHost||!_mpGS)return;var ro=_mpGS.roles||{};var el=_mpGS.el||[];var al=Object.entries(ro).filter(function(e){return el.indexOf(e[0])<0});var uc=al.filter(function(e){var r=typeof e[1]==="object"?e[1].role:e[1];return r==="undercover"}).length;var ci=al.filter(function(e){var r=typeof e[1]==="object"?e[1].role:e[1];return r==="civil"}).length;if(uc===0){_mpGS.phase="done";_mpGS.w="civil"}else if(uc>=ci){_mpGS.phase="done";_mpGS.w="undercover"}else{_mpGS.phase="discuss";_mpGS.te=Date.now()+60000;_mpGS.v={}}mpBcast()}
function mpHRe(){if(!mpIsHost)return;_mpGS=null;_mpLocalPlayers.forEach(function(p){p.is_ready=false});mpChannel.send({type:"broadcast",event:"player_list",payload:{players:_mpLocalPlayers}});showScreen("screen-mp-lobby");renderMpLobby()}
function mpSendReady(){if(mpChannel)mpChannel.send({type:"broadcast",event:"pr",payload:{id:mpPlayerId}});showToast("Prêt !")}
function mpSV(tid){if(mpChannel)mpChannel.send({type:"broadcast",event:"pv",payload:{id:mpPlayerId,t:tid}});if(_mpGS){if(!_mpGS.v)_mpGS.v={};_mpGS.v[mpPlayerId]=tid;_handleGS(_mpGS)}}

// Override old functions
handleMpGame = _handleGS;
mpStartGame = async function(){
  if(!mpIsHost)return;await ImageLoader.load();
  var av=PAIRS.filter(function(p){return(p.mode||"normal")===(GameState.currentMode||"normal")});if(!av.length)av=PAIRS;
  var pair=av[Math.floor(Math.random()*av.length)];var pl=_mpLocalPlayers.slice();
  if(pl.length<2){showToast("Min 2 joueurs");return}
  var ix=pl.map(function(_,i){return i}).sort(function(){return Math.random()-0.5});
  var ro={};pl.forEach(function(p,i){var ri=ix.indexOf(i);ro[p.player_id]={role:ri===0?"undercover":"civil",character:ri===0?pair.undercover:pair.civil}});
  _mpGS={phase:"reveal",pair:{civil:pair.civil,undercover:pair.undercover,civilImg:pair.civilImg,undercoverImg:pair.undercoverImg,hint:pair.hint||""},roles:ro,v:{},el:[],w:null,te:0,le:null};
  mpBcast();SoundFX.reveal();
};

// Override mpSubscribe for broadcast-only
mpSubscribe = function(){
  if(!sb||!mpRoomId)return;
  mpChannel=sb.channel("room-"+mpRoomId,{config:{broadcast:{self:true}}})
  .on("broadcast",{event:"player_list"},function(pl){if(pl.payload&&pl.payload.players){pl.payload.players.forEach(function(p){if(!_mpLocalPlayers.find(function(x){return x.player_id===p.player_id}))_mpLocalPlayers.push(p)});renderMpLobby()}})
  .on("broadcast",{event:"request_players"},function(){mpChannel.send({type:"broadcast",event:"player_list",payload:{players:_mpLocalPlayers}})})
  .on("broadcast",{event:"gs"},function(pl){if(pl.payload)_handleGS(pl.payload)})
  .on("broadcast",{event:"pv"},function(pl){if(mpIsHost&&_mpGS&&pl.payload){if(!_mpGS.v)_mpGS.v={};_mpGS.v[pl.payload.id]=pl.payload.t;mpBcast()}})
  .on("broadcast",{event:"pr"},function(){})
  .subscribe();
};
"""

html = html.replace("\n</script>", NEW_MP + "\n</script>")

with open("game_template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Broadcast-only MP implemented!")
