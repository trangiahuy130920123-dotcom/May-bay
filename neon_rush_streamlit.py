import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NEON RUSH - Đua xe", page_icon="🏎️", layout="wide")

st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden}
.stApp {background:linear-gradient(180deg,#080d1b,#111b31);color:#fff}
.block-container {padding:1rem .5rem .2rem;max-width:900px}
h1 {text-align:center;color:#62e8ff;font-weight:950;letter-spacing:2px;margin:0}
.sub {text-align:center;color:#b8c9df;margin:0 0 10px}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏎️ NEON RUSH</h1><p class='sub'>Đua xe tốc độ cao • Né xe • Chinh phục kỷ lục</p>", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
body{margin:0;background:transparent;font-family:Arial,sans-serif;touch-action:pan-y}
.shell{max-width:560px;margin:auto}
canvas{width:100%;height:auto;display:block;border:3px solid #526d91;border-radius:15px;background:#15213a;box-shadow:0 8px 28px #0008;touch-action:none}
.hud{display:flex;justify-content:space-between;gap:6px;margin:7px 2px;color:#eaf7ff;font-weight:900;font-size:13px}
.pill{background:#1d2e4d;border:1px solid #3c638b;border-radius:9px;padding:7px 9px}
.controls{display:flex;justify-content:center;align-items:center;gap:10px;margin:10px auto 5px;flex-wrap:wrap}
button{border:0;border-radius:12px;padding:12px 15px;background:#147dc1;color:white;font-size:16px;font-weight:900;box-shadow:0 4px 0 #075184;touch-action:manipulation}
button:active{transform:translateY(3px);box-shadow:0 1px 0 #075184}
.pad{display:flex;gap:10px}
.pad button{width:65px;height:54px;font-size:24px;padding:0;background:#263d62}
#start{background:#00a987;box-shadow:0 4px 0 #08745e}
#sound{background:#7a4ac7;box-shadow:0 4px 0 #4b2c84}
.tip{text-align:center;color:#afc4dc;font-size:12px;margin:8px 0}
</style></head><body><div class="shell">
<div class="hud">
 <span class="pill">🏁 ĐIỂM: <b id="score">0</b></span>
 <span class="pill">⚡ TỐC ĐỘ: <b id="speed">1</b></span>
 <span class="pill">🏆 KỶ LỤC: <b id="best">0</b></span>
</div>
<canvas id="game" width="480" height="680"></canvas>
<div class="controls">
 <div class="pad"><button id="left" aria-label="Sang trái">◀</button><button id="right" aria-label="Sang phải">▶</button></div>
 <button id="start">▶ BẮT ĐẦU</button>
 <button id="sound">🔇 BẬT NHẠC</button>
</div>
<div class="tip">Máy tính: phím ← → hoặc A / D • Điện thoại: nút ◀ ▶ hoặc vuốt trên đường đua</div>
</div>
<script>
(()=>{
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
const W=480,H=680, roadL=65,roadR=415,laneW=(roadR-roadL)/3;
const scoreEl=document.getElementById('score'),speedEl=document.getElementById('speed'),bestEl=document.getElementById('best');
let best=Number(localStorage.getItem('neonRushBest')||0);
bestEl.textContent=best;
let lane=1,playerY=548,traffic=[],score=0,frame=0,roadOffset=0,running=false,started=false,gameOver=false;
let audio=null,musicOn=false,musicTimer=null,musicIndex=0;
const colors=['#ff4d6d','#ffd166','#a78bfa','#45d6c5','#f4f7ff'];
function audioInit(){if(!audio)audio=new (window.AudioContext||window.webkitAudioContext)();if(audio.state==='suspended')audio.resume();}
function beep(freq,duration=.12,type='triangle',volume=.035){
 if(!audio||!musicOn)return;
 const osc=audio.createOscillator(),gain=audio.createGain();
 osc.type=type;osc.frequency.value=freq;gain.gain.setValueAtTime(volume,audio.currentTime);
 gain.gain.exponentialRampToValueAtTime(.001,audio.currentTime+duration);
 osc.connect(gain);gain.connect(audio.destination);osc.start();osc.stop(audio.currentTime+duration);
}
function musicStart(){
 if(musicTimer)clearInterval(musicTimer);
 const notes=[523,659,784,659,587,698,880,698,523,659,784,988,880,784,659,587];
 musicIndex=0;
 musicTimer=setInterval(()=>{
  if(musicOn&&running){beep(notes[musicIndex%notes.length],.18,'triangle',.025);if(musicIndex%4===0)beep(131,.22,'sine',.018);musicIndex++;}
 },210);
}
function reset(){
 lane=1;traffic=[];score=0;frame=0;roadOffset=0;running=true;started=true;gameOver=false;
 scoreEl.textContent='0';speedEl.textContent='1';
}
function move(dir){if(!running)return;lane=Math.max(0,Math.min(2,lane+dir));}
function bindHold(id,dir){
 const el=document.getElementById(id);
 el.addEventListener('pointerdown',e=>{e.preventDefault();move(dir);});
 el.addEventListener('click',e=>{e.preventDefault();move(dir);});
}
bindHold('left',-1);bindHold('right',1);
document.getElementById('start').addEventListener('click',()=>{reset();});
document.getElementById('sound').addEventListener('click',()=>{
 audioInit();musicOn=!musicOn;
 document.getElementById('sound').textContent=musicOn?'🔊 TẮT NHẠC':'🔇 BẬT NHẠC';
 if(musicOn)musicStart();else if(musicTimer)clearInterval(musicTimer);
});
document.addEventListener('keydown',e=>{
 if(['ArrowLeft','ArrowRight','KeyA','KeyD','Space'].includes(e.code))e.preventDefault();
 if(e.code==='ArrowLeft'||e.code==='KeyA')move(-1);
 if(e.code==='ArrowRight'||e.code==='KeyD')move(1);
 if(e.code==='Space'&&(!running))reset();
});
let touchX=null;
canvas.addEventListener('pointerdown',e=>{touchX=e.clientX;});
canvas.addEventListener('pointerup',e=>{
 if(touchX===null)return;
 const dx=e.clientX-touchX;
 if(Math.abs(dx)>18)move(dx>0?1:-1);
 touchX=null;
});
function rounded(x,y,w,h,r,color){
 ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();
}
function drawCar(x,y,color,isPlayer=false){
 ctx.save();ctx.translate(x,y);
 // shadow and wheels
 rounded(-22,-34,44,72,12,'rgba(0,0,0,.28)');
 rounded(-25,-27,8,19,3,'#111820');rounded(17,-27,8,19,3,'#111820');
 rounded(-25,12,8,19,3,'#111820');rounded(17,12,8,19,3,'#111820');
 // body
 rounded(-19,-36,38,74,11,color);
 rounded(-14,-22,28,23,7,isPlayer?'#9cecff':'#b9d8e8');
 rounded(-13,8,26,18,5,'#26394d');
 ctx.fillStyle=isPlayer?'#fff2a6':'#ffefb0';
 ctx.fillRect(-14,-32,7,5);ctx.fillRect(7,-32,7,5);
 ctx.fillStyle='#ff394f';ctx.fillRect(-14,31,7,4);ctx.fillRect(7,31,7,4);
 if(isPlayer){ctx.fillStyle='#e9fbff';ctx.fillRect(-3,-35,6,8);}
 ctx.restore();
}
function drawRoad(){
 ctx.fillStyle='#101c2c';ctx.fillRect(0,0,W,H);
 ctx.fillStyle='#1b2638';ctx.fillRect(roadL,0,roadR-roadL,H);
 ctx.fillStyle='#d6e5f0';ctx.fillRect(roadL-5,0,5,H);ctx.fillRect(roadR,0,5,H);
 ctx.fillStyle='#34475b';
 for(let i=1;i<3;i++){
  let x=roadL+i*laneW;
  for(let y=-70+(roadOffset%100);y<H;y+=100)ctx.fillRect(x-2,y,4,52);
 }
 // roadside neon markers
 for(let y=-50+(roadOffset%90);y<H;y+=90){
  rounded(25,y,17,37,5,'#f4b942');rounded(438,y,17,37,5,'#f4b942');
 }
 // subtle roadside grass
 ctx.fillStyle='#172d2c';ctx.fillRect(0,0,roadL-5,H);ctx.fillRect(roadR+5,0,W-roadR-5,H);
}
function draw(){
 drawRoad();
 traffic.forEach(t=>drawCar(roadL+laneW*(t.lane+.5),t.y,t.color,false));
 drawCar(roadL+laneW*(lane+.5),playerY,'#16b8ee',true);
}
function overlay(title,line1,line2){
 ctx.fillStyle='rgba(3,9,20,.68)';ctx.fillRect(0,0,W,H);
 rounded(42,220,396,225,22,'#f1f7ff');
 ctx.textAlign='center';ctx.fillStyle='#102a43';ctx.font='900 34px Arial';ctx.fillText(title,W/2,275);
 ctx.font='bold 19px Arial';ctx.fillStyle='#31516b';ctx.fillText(line1,W/2,325);
 ctx.font='bold 16px Arial';ctx.fillText(line2,W/2,360);
 ctx.fillStyle='#078c78';ctx.font='900 18px Arial';ctx.fillText('Nhấn BẮT ĐẦU để chơi',W/2,410);
}
function update(){
 if(!running)return;
 frame++;
 let speed=4+Math.min(5,score*.035);
 roadOffset+=speed;
 if(frame%Math.max(28,68-Math.floor(score/5))===0){
  let l=Math.floor(Math.random()*3);
  traffic.push({lane:l,y:-65,color:colors[Math.floor(Math.random()*colors.length)]});
 }
 for(let i=traffic.length-1;i>=0;i--){
  let t=traffic[i];t.y+=speed;
  if(t.y>H+60){traffic.splice(i,1);score++;scoreEl.textContent=score;speedEl.textContent=(1+Math.floor(score/8));}
  else if(t.lane===lane&&Math.abs(t.y-playerY)<58){
   running=false;gameOver=true;
   if(score>best){best=score;bestEl.textContent=best;localStorage.setItem('neonRushBest',best);}
   beep(100,.4,'sawtooth',.06);
  }
 }
}
function loop(){
 requestAnimationFrame(loop);
 if(running)update();
 draw();
 if(!started)overlay('NEON RUSH','Sẵn sàng xuất phát?','Né những chiếc xe phía trước!');
 else if(gameOver)overlay('GAME OVER','Điểm của bạn: '+score,'Kỷ lục: '+best);
 else if(!running)overlay('TẠM DỪNG','Nhấn BẮT ĐẦU để chơi tiếp','');
}
loop();
})();
</script></body></html>
"""
components.html(html, height=805, scrolling=False)
