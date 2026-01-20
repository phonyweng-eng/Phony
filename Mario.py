import streamlit as st

st.set_page_config(page_title="Mario Extended Game", layout="centered")
st.title("🍄 Extended Mario Game")
st.caption("← → move | SPACE jump")

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { margin:0; overflow:hidden; }
canvas {
  border: 4px solid black;
  display:block;
  background: linear-gradient(#6ec6ff, #ffffff);
}
</style>
</head>
<body>

<canvas id="game" width="900" height="450"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// ================= PLAYER =================
let mario = {
  x: 100, y: 350, w: 30, h: 40,
  vy: 0, onGround: false, lives: 3
};

// ================= GAME =================
let cameraX = 0;
let score = 0;
let dead = false;
let win = false;

// ================= PLATFORMS =================
const platforms = [
  {x:0,y:400,w:3000,h:50},
  {x:300,y:330,w:120,h:20},
  {x:550,y:290,w:120,h:20},
  {x:800,y:330,w:120,h:20},
  {x:1100,y:270,w:140,h:20},
  {x:1450,y:300,w:120,h:20},
  {x:1750,y:240,w:140,h:20},
  {x:2100,y:300,w:120,h:20}
];

// ================= COINS =================
let coins = [
  {x:320,y:300,taken:false},
  {x:580,y:260,taken:false},
  {x:830,y:300,taken:false},
  {x:1130,y:230,taken:false},
  {x:1480,y:280,taken:false},
  {x:1770,y:210,taken:false},
  {x:2130,y:260,taken:false}
];

// ================= ENEMIES =================
let enemies = [
  {x:700,y:370,w:30,h:30,dir:1},
  {x:1250,y:370,w:30,h:30,dir:-1},
  {x:1800,y:370,w:30,h:30,dir:1}
];

// ================= FLAG =================
let flag = {x:2300,y:200,w:10,h:200};

// ================= INPUT =================
let keys = {};
document.addEventListener("keydown", e => keys[e.code]=true);
document.addEventListener("keyup", e => keys[e.code]=false);

// ================= PHYSICS =================
const gravity = 0.8;
const jump = -14;
const speed = 4;

// ================= UPDATE =================
function update(){
  if(dead || win) return;

  // movement
  if(keys["ArrowRight"]) mario.x += speed;
  if(keys["ArrowLeft"]) mario.x -= speed;
  if(keys["Space"] && mario.onGround){
    mario.vy = jump;
    mario.onGround = false;
  }

  mario.vy += gravity;
  mario.y += mario.vy;
  mario.onGround = false;

  // collision with platforms
  platforms.forEach(p=>{
    if(
      mario.x < p.x+p.w &&
      mario.x+mario.w > p.x &&
      mario.y < p.y+p.h &&
      mario.y+mario.h > p.y &&
      mario.vy > 0
    ){
      mario.y = p.y - mario.h;
      mario.vy = 0;
      mario.onGround = true;
    }
  });

  // collect coins
  coins.forEach(c=>{
    if(!c.taken &&
       mario.x < c.x+20 &&
       mario.x+mario.w > c.x &&
       mario.y < c.y+20 &&
       mario.y+mario.h > c.y){
         c.taken = true;
         score++;
       }
  });

  // enemy movement & collision
  enemies.forEach(e=>{
    e.x += e.dir*2;
    if(e.x<650 || e.x>2150) e.dir*=-1;

    if(
      mario.x < e.x+e.w &&
      mario.x+mario.w > e.x &&
      mario.y < e.y+e.h &&
      mario.y+mario.h > e.y
    ){
      if(mario.vy > 0){
        e.y = 1000; // kill enemy
        mario.vy = jump/2;
      }else{
        mario.lives--;
        mario.x = 100;
        mario.y = 350;
        if(mario.lives <=0) dead = true;
      }
    }
  });

  // check win
  if(mario.x > flag.x) win = true;

  cameraX = mario.x - 200;
  if(cameraX <0) cameraX=0;
}

// ================= DRAW =================
function draw(){
  ctx.clearRect(0,0,canvas.width,canvas.height);

  // --- BACKGROUND PARALLAX ---
  // sky
  ctx.fillStyle="#6ec6ff";
  ctx.fillRect(0,0,canvas.width,canvas.height);

  // clouds
  ctx.fillStyle="white";
  for(let i=0;i<6;i++){
    ctx.beginPath();
    ctx.arc(250*i - cameraX*0.5, 80, 30,0,Math.PI*2);
    ctx.fill();
  }

  // hills
  ctx.fillStyle="#9ad09a";
  for(let i=0;i<6;i++){
    ctx.beginPath();
    ctx.arc(300*i - cameraX*0.3, 450, 180,0,Math.PI*2);
    ctx.fill();
  }

  ctx.save();
  ctx.translate(-cameraX,0);

  // platforms
  ctx.fillStyle="#2e8b57";
  platforms.forEach(p=>ctx.fillRect(p.x,p.y,p.w,p.h));

  // coins
  coins.forEach(c=>{
    if(!c.taken){
      ctx.fillStyle="gold";
      ctx.beginPath();
      ctx.arc(c.x+10,c.y+10,10,0,Math.PI*2);
      ctx.fill();
    }
  });

  // enemies
  ctx.fillStyle="brown";
  enemies.forEach(e=>ctx.fillRect(e.x,e.y,e.w,e.h));

  // flag
  ctx.fillStyle="black";
  ctx.fillRect(flag.x, flag.y, flag.w, flag.h);
  ctx.fillStyle="red";
  ctx.fillRect(flag.x, flag.y, 40, 20);

  // mario
  ctx.fillStyle="red";
  ctx.fillRect(mario.x,mario.y,mario.w,mario.h);

  ctx.restore();

  // UI
  ctx.fillStyle="black";
  ctx.font="20px Arial";
  ctx.fillText("Score: "+score,20,30);
  ctx.fillText("Lives: "+mario.lives,20,60);

  if(dead){
    ctx.fillStyle="red";
    ctx.font="50px Arial";
    ctx.fillText("GAME OVER",300,200);
  }
  if(win){
    ctx.fillStyle="green";
    ctx.font="50px Arial";
    ctx.fillText("YOU WIN!",320,200);
  }
}

// ================= LOOP =================
function loop(){
  update();
  draw();
  requestAnimationFrame(loop);
}
loop();
</script>
</body>
</html>
"""

st.components.v1.html(html, height=480)
