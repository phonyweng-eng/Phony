import streamlit as st

st.set_page_config(page_title="Mario Game", layout="centered")

st.title("🍄 Mario Game (Real Version)")
st.caption("Use ← → to move, SPACE to jump")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
canvas {
    background: linear-gradient(#87ceeb, #ffffff);
    border: 3px solid #000;
}
</style>
</head>
<body>

<canvas id="game" width="800" height="300"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let player = {
    x: 50,
    y: 200,
    w: 30,
    h: 40,
    vy: 0,
    onGround: false
};

const gravity = 0.8;
const jumpPower = -12;
const speed = 4;

const platforms = [
    {x: 0, y: 240, w: 800, h: 60},
    {x: 300, y: 180, w: 120, h: 20},
    {x: 520, y: 140, w: 120, h: 20}
];

let keys = {};

document.addEventListener("keydown", e => keys[e.code] = true);
document.addEventListener("keyup", e => keys[e.code] = false);

function update() {
    // movement
    if (keys["ArrowRight"]) player.x += speed;
    if (keys["ArrowLeft"]) player.x -= speed;
    if (keys["Space"] && player.onGround) {
        player.vy = jumpPower;
        player.onGround = false;
    }

    // gravity
    player.vy += gravity;
    player.y += player.vy;

    player.onGround = false;

    // collision
    platforms.forEach(p => {
        if (
            player.x < p.x + p.w &&
            player.x + player.w > p.x &&
            player.y < p.y + p.h &&
            player.y + player.h > p.y
        ) {
            if (player.vy > 0) {
                player.y = p.y - player.h;
                player.vy = 0;
                player.onGround = true;
            }
        }
    });

    // bounds
    if (player.x < 0) player.x = 0;
    if (player.x > canvas.width - player.w)
        player.x = canvas.width - player.w;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // platforms
    ctx.fillStyle = "#228B22";
    platforms.forEach(p =>
        ctx.fillRect(p.x, p.y, p.w, p.h)
    );

    // player
    ctx.fillStyle = "red";
    ctx.fillRect(player.x, player.y, player.w, player.h);
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

st.components.v1.html(game_html, height=350)
