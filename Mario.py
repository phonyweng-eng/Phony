import streamlit as st

st.set_page_config(page_title="Mario Game", layout="centered")
st.title("🍄 Mario Game")
st.caption("← → move | SPACE jump")

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { margin:0; }
canvas {
  background: linear-gradient(#6ec6ff, #ffffff);
  border: 4px solid #000;
}
</style>
</head>
<body>

<canvas id="game" width="900" height="350"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// ---------------- PLAYER ----------------
let mario = {
  x: 100, y: 250, w: 30, h: 40,
  vy: 0, onGround: false
};

const gravity = 0.8;
const jump = -13;
const speed = 4;

// ---------------- WORLD ----------------
let cameraX = 0;
let score = 0;
let dead = false;

const platforms = [
  {x: 0, y: 290, w: 2000, h: 60},
  {x: 300, y: 220, w: 120, h: 20},
  {x: 550, y: 180, w: 120, h: 20},
  {x: 850, y: 220, w: 120, h: 20}
];

let coins = [
  {x: 320, y: 180, taken:false},
  {x: 580, y: 140, taken:false},
  {x: 880, y: 180, taken:false}
];

let enemy = { x: 700, y: 250, w: 30, h: 30, dir:1 };

// ---------------- INPUT ----------------
let keys = {};
document.addEventListener("keydown", e => keys[e.code] = true);
document.addEventListener("keyup", e => keys[e.code] = false);

// ---------------- GAME LOOP ----------------
function update() {
  if (dead) return;

  // move
  if (keys["ArrowRight"]) mario.x += speed;
  if (keys["ArrowLeft"]) mario.x -= speed;
  if (keys["Space"] && mario.onGround) {
    mario.vy = jump;
    mario.onGround = false;
  }

  // gravity
  mario.vy += gravity;
  mario.y += mario.vy;
  mario.onGround = false;

  // platforms
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

  // coins
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

  // enemy move
  enemy.x += enemy.dir * 2;
  if (enemy.x < 650 || enemy.x > 820) enemy.dir *= -1;

  // enemy collision
  if (
    mario.x < enemy.x + enemy.w &&
    mario.x + mario.w > enemy.x &&
    mario.y < enemy.y + enemy.h &&
    mario.y + mario.h > enemy.y
  ) {
    if (mario.vy > 0) {
      enemy.y = 1000; // kill enemy
      mario.vy = jump / 2;
    } else {
      dead = true;
    }
  }

  // camera
  cameraX = mario.x - 150;
  if (cameraX < 0) cameraX = 0;
}

function draw() {
  ctx.clearRect(0,0,canvas.width,canvas.height);

  ctx.save();
  ctx.translate(-cameraX, 0);

  // platforms
  ctx.fillStyle = "#2e8b57";
  platforms.forEach(p => ctx.fillRect(p.x, p.y, p.w, p.h));

  // coins
  ctx.fillStyle = "gold";
  coins.forEach(c => {
    if (!c.taken) {
      ctx.beginPath();
      ctx.arc(c.x+10, c.y+10, 10, 0, Math.PI*2);
      ctx.fill();
    }
  });

  // enemy
  ctx.fillStyle = "brown";
  ctx.fillRect(enemy.x, enemy.y, enemy.w, enemy.h);

  // mario
  ctx.fillStyle = "red";
  ctx.fillRect(mario.x, mario.y, mario.w, mario.h);

  ctx.restore();

  // UI
  ctx.fillStyle = "black";
  ctx.font = "18px Arial";
  ctx.fillText("Score: " + score, 20, 25);

  if (dead) {
    ctx.fillStyle = "red";
    ctx.font = "40px Arial";
    ctx.fillText("GAME OVER", 350, 170);
  }
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

st.components.v1.html(html, height=380)
