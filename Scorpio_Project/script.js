const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let mouse = { x: canvas.width / 2, y: canvas.height / 2 };
let particles = []; // مصفوفة لتخزين الشرارات

// تتبع اللمس والماوس
const updatePos = (e) => {
    const x = e.clientX || (e.touches ? e.touches[0].clientX : mouse.x);
    const y = e.clientY || (e.touches ? e.touches[0].clientY : mouse.y);
    
    // إطلاق جزيئات عند الحركة
    for(let i=0; i<2; i++) {
        particles.push(new Particle(x, y));
    }
    
    mouse.x = x;
    mouse.y = y;
};

window.addEventListener('mousemove', updatePos);
window.addEventListener('touchmove', (e) => { updatePos(e); e.preventDefault(); }, {passive: false});

// فئة الجزيئات (الشرارات)
class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.size = Math.random() * 3 + 1;
        this.speedX = (Math.random() - 0.5) * 5;
        this.speedY = (Math.random() - 0.5) * 5;
        this.color = `hsl(${Math.random() * 60 + 180}, 100%, 50%)`;
        this.opacity = 1;
    }
    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.opacity -= 0.02;
    }
    draw() {
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }
}

// فئة مفاصل العقرب (كما هي مع تحسين التوهج)
class Segment {
    constructor(length, thickness, color) {
        this.x = 0; this.y = 0;
        this.angle = 0;
        this.length = length;
        this.thickness = thickness;
        this.color = color;
    }
    follow(tx, ty) {
        const dx = tx - this.x;
        const dy = ty - this.y;
        this.angle = Math.atan2(dy, dx);
        this.x = tx - Math.cos(this.angle) * this.length;
        this.y = ty - Math.sin(this.angle) * this.length;
    }
    draw(nx, ny) {
        ctx.shadowBlur = 20;
        ctx.shadowColor = this.color;
        ctx.strokeStyle = this.color;
        ctx.lineWidth = this.thickness;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(nx, ny);
        ctx.stroke();
        ctx.shadowBlur = 0;
    }
}

const segments = [];
const numSegments = 160;
for (let i = 0; i < numSegments; i++) {
    const thickness = Math.max(1, 10 - (i * 0.05));
    const color = `hsl(${190 + i * 0.8}, 100%, 50%)`;
    segments.push(new Segment(6, thickness, color));
}

function animate() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // تحديث ورسم الجزيئات
    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
        if (particles[i].opacity <= 0) {
            particles.splice(i, 1);
            i--;
        }
    }

    let tx = mouse.x;
    let ty = mouse.y;
    for (let i = 0; i < segments.length; i++) {
        segments[i].follow(tx, ty);
        const nx = segments[i].x + Math.cos(segments[i].angle) * segments[i].length;
        const ny = segments[i].y + Math.sin(segments[i].angle) * segments[i].length;
        segments[i].draw(nx, ny);
        tx = segments[i].x;
        ty = segments[i].y;
    }
    requestAnimationFrame(animate);
}

animate();

