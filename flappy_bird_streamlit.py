import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Bird",
    page_icon="🐤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: linear-gradient(180deg,#75d9ff 0%,#b8f0ff 58%,#e7ffd2 100%);}
    .block-container {padding: .6rem .5rem 0 !important; max-width: 900px;}
    h1 {text-align:center; color:#174c78; font-weight:900; margin:0 0 .15rem 0;}
    .subtitle {text-align:center;color:#245b76;margin-bottom:.5rem;font-weight:600;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🐤 FLAPPY BIRD</h1><div class='subtitle'>Chạm màn hình hoặc nhấn SPACE để bay • Né ống nước và lập kỷ lục!</div>", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
*{box-sizing:border-box}
body{margin:0;background:transparent;font-family:Arial,sans-serif;overflow:hidden;touch-action:manipulation}
.wrap{width:100%;max-width:520px;margin:auto;position:relative}
canvas{display:block;width:100%;height:auto;border:4px solid #fff;border-radius:18px;box-shadow:0 8px 25px #23608055;background:#79d9ff;touch-action: manipulation}
.hud{position:absolute;top:12px;left:0;width:100%;text-align:center;color:white;font-size:34px;font-weight:900;text-shadow:2px 3px 0 #28633e;pointer-events:none}
.controls{display:flex;gap:9px;justify-content:center;margin:10px 0;flex-wrap:wrap}
button{border:0;border-radius:999px;padding:11px 18px;font-weight:800;font-size:15px;color:#fff;background:#168bdb;box-shadow:0 4px 0 #0863a4;cursor:pointer}
button:active{transform:translateY(3px);box-shadow:0 1px 0 #0863a4}
#sound{background:#20a56b;box-shadow:0 4px 0 #137448}
.tip{text-align:center;color:#245b76;font-size:13px;font-weight:700;margin-bottom:8px}
</style>
</head>
<body>
<div class="wrap">
 <canvas id="game" width="480" height="640"></canvas>
 <div class="hud" id="score">0</div>
</div>
<div class="controls">
 <button id="start">▶ CHƠI / CHƠI LẠI</button>
 <button id="sound">🔊 BẬT NHẠC</button>
</div>
<div class="tip">Chạm vào game / nhấn SPACE / ↑ để bay lên</div>
<script>
(() => {
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');
const W=480,H=640, groundY=575;
let bird, pipes, score, best=Number(localStorage.getItem('flappyBest')||0);
let running=false, started=false, over=false, frame=0, soundOn=false;
let audio=null, musicTimer=null, musicStep=0;
const scoreEl=document.getElementById('score');
function audioReady(){
 if(!audio) audio=new (window.AudioContext||window.webkitAudioContext)();
 if(audio.state==='suspended') audio.resume();
}
function tone(freq,dur,type='sine',vol=.035){
 if(!audio||!soundOn)return;
 const o=audio.createOscillator(),g=audio.createGain();
 o.type=type;o.frequency.value=freq;g.gain.setValueAtTime(vol,audio.currentTime);
 g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+dur);
 o.connect(g);g.connect(audio.destination);o.start();o.stop(audio.currentTime+dur);
}
function startMusic(){
 if(musicTimer)clearInterval(musicTimer);
 const melody=[523,659,784,659,587,698,880,698,523,659,784,1046,880,784,659,587];
 musicStep=0;
 musicTimer=setInterval(()=>{if(running&&soundOn){tone(melody[musicStep%melody.length],.19,'triangle',.022);if(musicStep%4===0)tone(131,.25,'sine',.025);musicStep++;}},220);
}
function flapSound(){tone(620,.09,'square',.035)}
function hitSound(){tone(130,.35,'sawtooth',.05)}
function reset(){
 bird={x:125,y:285,vy:0,r:17,rot:0};
 pipes=[];score=0;frame=0;over=false;started=true;running=true;
 scoreEl.textContent='0';
 for(let i=0;i<3;i++)pipes.push({x:540+i*220,gap:178,top:100+Math.random()*240,passed:false});
}
function flap(){
 if(!started||over){reset();}
 if(!running)return;
 bird.vy=-6.8;flapSound();
}
function input(e){if(e)e.preventDefault();if(!started||over){reset();return;}flap();}
canvas.addEventListener('pointerdown',input);
document.addEventListener('keydown',e=>{if(['Space','ArrowUp'].includes(e.code)){e.preventDefault();input(e);}});
document.getElementById('start').addEventListener('click',()=>{audioReady();reset();});
document.getElementById('sound').addEventListener('click',()=>{
 audioReady();soundOn=!soundOn;
 document.getElementById('sound').textContent=soundOn?'🔊 TẮT NHẠC':'🔊 BẬT NHẠC';
 if(soundOn)startMusic();else if(musicTimer)clearInterval(musicTimer);
});
function roundedRect(x,y,w,h,r,color){ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();}
function drawBackground(){
 let g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#69d5ff');g.addColorStop(1,'#d5f7ff');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 // clouds
 ctx.fillStyle='rgba(255,255,255,.82)';
 for(let i=0;i<4;i++){let x=((i*155-frame*.35)%(W+120)+W+120)%(W+120)-60,y=85+(i%2)*95;
 ctx.beginPath();ctx.arc(x,y,23,0,Math.PI*2);ctx.arc(x+25,y-10,30,0,Math.PI*2);ctx.arc(x+54,y,22,0,Math.PI*2);ctx.fill();}
 // distant hills
 ctx.fillStyle='#9bdc78';ctx.beginPath();ctx.moveTo(0,groundY);for(let x=0;x<=W;x+=40)ctx.lineTo(x,480+Math.sin((x+frame*.3)/65)*22);ctx.lineTo(W,groundY);ctx.fill();
 ctx.fillStyle='#79c957';ctx.fillRect(0,groundY,W,H-groundY);
 ctx.fillStyle='#4cae45';ctx.fillRect(0,groundY,W,13);
 for(let x=-(frame%32);x<W;x+=32){ctx.fillStyle='#d7f28a';ctx.fillRect(x,groundY+19,17,5);}
}
function drawPipe(p){
 const bottom=p.top+p.gap;
 // pipe bodies
 let grad=ctx.createLinearGradient(p.x,0,p.x+64,0);grad.addColorStop(0,'#168b35');grad.addColorStop(.25,'#66d64a');grad.addColorStop(.7,'#2ca83d');grad.addColorStop(1,'#126d2c');
 ctx.fillStyle=grad;
 ctx.fillRect(p.x,0,64,p.top);ctx.fillRect(p.x,bottom,64,groundY-bottom);
 ctx.fillStyle='#16762d';ctx.fillRect(p.x-5,p.top-25,74,25);ctx.fillRect(p.x-5,bottom,74,25);
 ctx.strokeStyle='#075d29';ctx.lineWidth=4;ctx.strokeRect(p.x,0,64,p.top);ctx.strokeRect(p.x,bottom,64,groundY-bottom);
 ctx.strokeRect(p.x-5,p.top-25,74,25);ctx.strokeRect(p.x-5,bottom,74,25);
 ctx.fillStyle='rgba(255,255,255,.22)';ctx.fillRect(p.x+10,0,8,p.top-25);ctx.fillRect(p.x+10,bottom+25,8,groundY-bottom-25);
}
function drawBird(){
 ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot);
 // tail
 ctx.fillStyle='#ed8b18';ctx.beginPath();ctx.moveTo(-15,1);ctx.lineTo(-30,-7);ctx.lineTo(-27,8);ctx.fill();
 // wing
 ctx.fillStyle='#eaa51d';ctx.beginPath();ctx.ellipse(-3,7+Math.sin(frame*.45)*3,13,8,-.3,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#9b5a13';ctx.lineWidth=2;ctx.stroke();
 // body
 ctx.fillStyle='#ffdc35';ctx.beginPath();ctx.ellipse(0,0,19,15,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#a66a16';ctx.lineWidth=2;ctx.stroke();
 // head feather
 ctx.fillStyle='#ef8a24';ctx.beginPath();ctx.moveTo(-7,-12);ctx.lineTo(-12,-23);ctx.lineTo(-1,-16);ctx.lineTo(3,-24);ctx.lineTo(5,-13);ctx.fill();
 // eye
 ctx.fillStyle='white';ctx.beginPath();ctx.arc(9,-6,6,0,Math.PI*2);ctx.fill();ctx.fillStyle='#20252a';ctx.beginPath();ctx.arc(11,-6,2.6,0,Math.PI*2);ctx.fill();
 // beak
 ctx.fillStyle='#f47a21';ctx.beginPath();ctx.moveTo(15,0);ctx.lineTo(29,4);ctx.lineTo(15,9);ctx.fill();ctx.strokeStyle='#a34c14';ctx.stroke();
 ctx.restore();
}
function collide(){
 const b=bird;
 if(b.y+b.r>groundY||b.y-b.r<0)return true;
 for(const p of pipes){
  if(b.x+b.r>p.x-5&&b.x-b.r<p.x+69&&(b.y-b.r<p.top||b.y+b.r>p.top+p.gap))return true;
 }
 return false;
}
function drawOverlay(title,sub){
 ctx.fillStyle='rgba(9,35,55,.48)';ctx.fillRect(0,0,W,H);
 roundedRect(48,215,384,190,22,'#fff5d8');
 ctx.textAlign='center';ctx.fillStyle='#174c78';ctx.font='900 34px Arial';ctx.fillText(title,W/2,270);
 ctx.font='bold 19px Arial';ctx.fillStyle='#3d6274';ctx.fillText(sub,W/2,315);
 ctx.font='bold 16px Arial';ctx.fillText('Kỷ lục: '+best,W/2,350);
 ctx.fillStyle='#168bdb';ctx.font='bold 17px Arial';ctx.fillText('Chạm màn hình để bắt đầu',W/2,382);
}
function loop(){
 requestAnimationFrame(loop);frame++;
 drawBackground();
 if(running){
  bird.vy+=.34;bird.y+=bird.vy;bird.rot=Math.min(.9,Math.max(-.5,bird.vy*.075));
  for(const p of pipes){p.x-=3.1;
   if(!p.passed&&p.x+64<bird.x){p.passed=true;score++;scoreEl.textContent=score;tone(900,.1,'sine',.04);}
  }
  if(pipes[0].x<-80){pipes.shift();pipes.push({x:pipes[pipes.length-1].x+220,gap:Math.max(145,178-score*.7),top:75+Math.random()*260,passed:false});}
  if(collide()){running=false;over=true;hitSound();if(score>best){best=score;localStorage.setItem('flappyBest',best);}}
 }
 pipes.forEach(drawPipe);drawBird();
 if(!started)drawOverlay('FLAPPY BIRD','Sẵn sàng thử thách chưa?');
 else if(over)drawOverlay('GAME OVER','Điểm của bạn: '+score);
 else if(!running)drawOverlay('TẠM DỪNG','Nhấn CHƠI để tiếp tục');
}
loop();
})();
</script>
</body>
</html>
"""

components.html(html, height=735, scrolling=False)
