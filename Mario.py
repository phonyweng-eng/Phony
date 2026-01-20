import streamlit as st

st.set_page_config(page_title="Mario Game", layout="centered")
st.title("🍄 Mario Game — Visual Edition")
st.caption("← → move | SPACE jump")

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { margin:0; }
canvas {
  border: 4px solid black;
  background: linear-gradient(#6ec6ff, #ffffff);
}
</style>
</head>
<body>

<canvas id="game" width="900" height="380"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// ================= PLAYER =================
let mario = {
  x: 100, y: 260, w: 30, h: 40,
  vy: 0, onGround: false
};

const gravity = 0.8;
const jump = -14;
const speed = 4;

// ================= WORLD =================
let cameraX = 0;
let score = 0;
let dead = false;
let win = false;

// ================= PLATFORMS =================
const platforms = [
  {x: 0, y: 310, w: 3000, h: 70},
  {x: 300, y: 240, w: 120, h: 20},
  {x: 550, y: 200, w: 120, h: 20},
  {x: 800, y: 240, w: 120, h: 20},
  {x: 1100, y: 190, w: 140, h: 20},
  {x: 1450, y: 220, w: 120, h: 20}
];

// ================= COINS =================
let coins = [
  {x: 320, y: 200, taken:false},
  {x: 580, y: 160, taken:false},
  {x: 830, y: 200, taken:false},
  {x: 1130, y: 150, taken:false},
  {x: 1480, y: 180, taken:false}
];

// ================= ENEMIES =================
let enemies = [
  {x: 700, y: 270, w: 30, h: 30, dir:1},
  {x: 1250, y: 270, w: 30, h: 30, dir:-1}
];

// ================= FLAG =================
let flag = { x: 1800, y: 190, w: 10, h: 120 };

// ================= INPUT =================
let keys = {};
document.addEventListener("keydown", e => keys[e.code] = true);
document.addEventListener("keyup", e => keys[e.code] = false);

// ================= UPDATE =================
function update() {
  if (dead || win) return;

  if (keys["ArrowRight"]) mario.x += speed;
  if (keys["ArrowLeft"]) mario.x -= speed;
  if (keys["Space"] && mario.onGround) {
    mario.vy = jump;
    mario.onGround = false;
  }

  mario.vy += gravity;
  mario.y += mario.vy;
  mario.onGround = false;

  platforms.forEach(p => {
    if (
      mario.x < p.x + p.w &&
      mario.x + mario.w > p.x &&
      mario.y < p.y + p.h &&
      mario.y + mario.h > p.y &&
      mario.vy > 0
    ) {
      mario.y = p.y - mario.h;
      mario.vy = 0;
      mario.onGround = true;
    }
  });

  // Coins
  coins.forEach(c => {
    if (!c.taken &&
        mario.x < c.x + 20 &&
        mario.x + mario.w > c.x &&
        mario.y < c.y + 20 &&
        mario.y + mario.h > c.y) {
      c.taken = true;
      score++;
    }
  });

  // Enemies
  enemies.forEach(e => {
    e.x += e.dir * 2;
    if (e.x < 650 || e.x > 1550) e.dir *= -1;

    if (
      mario.x < e.x + e.w &&
      mario.x + mario.w > e.x &&
      mario.y < e.y + e.h &&
      mario.y + mario.h > e.y
    ) {
      if (mario.vy > 0) {
        e.y = 1000;
        mario.vy = jump / 2;
      } else {
        dead = true;
      }
    }
  });

  // Flag
  if (
    mario.x < flag.x + flag.w &&
    mario.x + mario.w > flag.x &&
    mario.y < flag.y + flag.h
  ) {
    win = true;
  }

  cameraX = mario.x - 200;
  if (cameraX < 0) cameraX = 0;
}

// ================= DRAW =================
function draw() {
  ctx.clearRect(0,0,canvas.width,canvas.height);

  // --- BACKGROUND PARALLAX ---
  ctx.fillStyle = "#b0e0ff";
  ctx.fillRect(0,0,canvas.width,canvas.height);

  ctx.fillStyle = "#9ad09a"; // hills
  for (let i=0;i<5;i++){
    ctx.beginPath();
    ctx.arc(300*i - cameraX*0.3, 340, 180, 0, Math.PI*2);
    ctx.fill();
  }

  ctx.fillStyle = "white"; // clouds
  for (let i=0;i<6;i++){
    ctx.beginPath();
    ctx.arc(250*i - cameraX*0.5, 80, 30, 0, Math.PI*2);
    ctx.fill();
  }

  ctx.save();
  ctx.translate(-cameraX,0);

  // Platforms
  ctx.fillStyle = "#2e8b57";
  platforms.forEach(p => ctx.fillRect(p.x,p.y,p.w,p.h));

  // Coins
  ctx.fillStyle = "gold";
  coins.forEach(c=>{
    if(!c.taken){
      ctx.beginPath();
      ctx.arc(c.x+10,c.y+10,10,0,Math.PI*2);
      ctx.fill();
    }
  });

  // Enemies
  ctx.fillStyle = "brown";
  enemies.forEach(e => ctx.fillRect(e.x,e.y,e.w,e.h));

  // Flag
  ctx.fillStyle = "black";
  ctx.fillRect(flag.x, flag.y, flag.w, flag.h);
  ctx.fillStyle = "red";
  ctx.fillRect(flag.x, flag.y, 40, 20);

  // Mario
  ctx.fillStyle = "red";
  ctx.fillRect(mario.x,mario.y,mario.w,mario.h);

  ctx.restore();

  // UI
  ctx.fillStyle = "black";
  ctx.font = "18px Arial";
  ctx.fillText("Score: " + score, 20, 25);

  if (dead) {
    ctx.fillStyle = "red";
    ctx.font = "40px Arial";
    ctx.fillText("GAME OVER", 350, 200);
  }

  if (win) {
    ctx.fillStyle = "green";
    ctx.font = "40px Arial";
    ctx.fillText("YOU WIN!", 370, 200);
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

st.components.v1.html(html, height=420)
