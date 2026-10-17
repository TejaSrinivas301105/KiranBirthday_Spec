import json, os

BASE = r'c:\Users\Teja\OneDrive\MS office\Working\Kiran Birthday_spe'

with open(os.path.join(BASE, '_rows.json'), 'r', encoding='utf-8') as f:
    rows_js = f.read()

# Read the current HTML up to (and including) "const ROWS = "
html_path = os.path.join(BASE, 'birthday.html')
with open(html_path, 'r', encoding='utf-8') as f:
    current = f.read()

# Find the cut point
marker = 'const ROWS = '
idx = current.find(marker)
assert idx != -1, "Marker not found"
base_html = current[:idx + len(marker)]

script_tail = r"""
const RAMP = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`. ';
const RL = RAMP.length; // 70

// ── COLOUR MAP ──────────────────────────────────────────────────────────────
function charToClass(ch) {
  const idx = RAMP.indexOf(ch);
  if (idx < 0) return 'd69';
  return 'd' + Math.min(69, Math.floor(idx / RL * 70));
}

// ── STARS CANVAS ────────────────────────────────────────────────────────────
const starsCanvas = document.getElementById('stars-canvas');
const sCtx = starsCanvas.getContext('2d');
let stars = [];
function resizeStars() {
  starsCanvas.width = innerWidth; starsCanvas.height = innerHeight;
  stars = Array.from({length: 180}, () => ({
    x: Math.random()*innerWidth, y: Math.random()*innerHeight,
    r: Math.random()*1.5+.3, a: Math.random(), da: (Math.random()*.015+.005)*(Math.random()<.5?1:-1)
  }));
}
window.addEventListener('resize', resizeStars); resizeStars();
function animStars() {
  sCtx.clearRect(0,0,starsCanvas.width,starsCanvas.height);
  stars.forEach(s => {
    s.a = Math.max(0, Math.min(1, s.a + s.da));
    if (s.a <= 0 || s.a >= 1) s.da *= -1;
    sCtx.beginPath(); sCtx.arc(s.x, s.y, s.r, 0, Math.PI*2);
    sCtx.fillStyle = `rgba(255,255,255,${s.a})`; sCtx.fill();
  });
  requestAnimationFrame(animStars);
}
animStars();

// ── SPLASH STARS ────────────────────────────────────────────────────────────
const splashStars = document.getElementById('splash-stars');
for (let i = 0; i < 60; i++) {
  const s = document.createElement('div'); s.className = 'splash-star';
  s.style.cssText = `left:${Math.random()*100}%;top:${Math.random()*100}%;
    animation-duration:${1.5+Math.random()*3}s;animation-delay:${Math.random()*3}s;
    width:${1+Math.random()*3}px;height:${1+Math.random()*3}px;`;
  splashStars.appendChild(s);
}

// ── BALLOONS ────────────────────────────────────────────────────────────────
const BALLOON_COLORS = ['#ff69b4','#a855f7','#38bdf8','#facc15','#34d399','#f97316'];
function spawnBalloon() {
  const b = document.createElement('div'); b.className = 'balloon';
  const sz = 40 + Math.random()*50;
  b.style.cssText = `left:${Math.random()*100}%;width:${sz}px;height:${sz*1.2}px;
    background:${BALLOON_COLORS[Math.floor(Math.random()*BALLOON_COLORS.length)]};
    animation-duration:${6+Math.random()*8}s;animation-delay:${Math.random()*4}s;`;
  document.getElementById('balloons').appendChild(b);
  setTimeout(() => b.remove(), 14000);
}
setInterval(spawnBalloon, 800);

// ── CONFETTI ────────────────────────────────────────────────────────────────
const confCanvas = document.getElementById('confetti-canvas');
const cCtx = confCanvas.getContext('2d');
confCanvas.width = innerWidth; confCanvas.height = innerHeight;
window.addEventListener('resize', () => { confCanvas.width=innerWidth; confCanvas.height=innerHeight; });
let confetti = [], confettiActive = false;
function launchConfetti() {
  confettiActive = true;
  for (let i = 0; i < 160; i++) confetti.push({
    x: Math.random()*innerWidth, y: -10-Math.random()*200,
    vx: (Math.random()-0.5)*4, vy: 2+Math.random()*4,
    color: BALLOON_COLORS[Math.floor(Math.random()*BALLOON_COLORS.length)],
    w: 6+Math.random()*8, h: 10+Math.random()*14,
    rot: Math.random()*360, drot: (Math.random()-0.5)*8, life: 1
  });
}
function animConfetti() {
  cCtx.clearRect(0,0,confCanvas.width,confCanvas.height);
  confetti = confetti.filter(c => c.life > 0);
  confetti.forEach(c => {
    c.x+=c.vx; c.y+=c.vy; c.rot+=c.drot; c.life-=0.006;
    cCtx.save(); cCtx.globalAlpha=c.life; cCtx.translate(c.x,c.y); cCtx.rotate(c.rot*Math.PI/180);
    cCtx.fillStyle=c.color; cCtx.fillRect(-c.w/2,-c.h/2,c.w,c.h); cCtx.restore();
  });
  requestAnimationFrame(animConfetti);
}
animConfetti();

// ── MUSIC NOTES ─────────────────────────────────────────────────────────────
const NOTES = ['♩','♪','♫','♬','🎵','🎶'];
function spawnNote() {
  const n = document.createElement('div'); n.className = 'note';
  n.textContent = NOTES[Math.floor(Math.random()*NOTES.length)];
  n.style.cssText = `left:${10+Math.random()*80}%;bottom:${60+Math.random()*20}%;
    color:hsl(${Math.random()*360},80%,70%);animation-duration:${2.5+Math.random()*2}s;`;
  document.body.appendChild(n);
  setTimeout(() => n.remove(), 4000);
}

// ── MUSIC ────────────────────────────────────────────────────────────────────
let audioCtx = null, musicPlaying = false, noteInterval = null;
const musicBtn = document.getElementById('music-btn');
function getAudioCtx() {
  if (!audioCtx) audioCtx = new (window.AudioContext||window.webkitAudioContext)();
  return audioCtx;
}
function playTone(freq, start, dur, vol=0.12) {
  const ctx = getAudioCtx();
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.connect(g); g.connect(ctx.destination);
  o.frequency.value = freq; o.type = 'sine';
  g.gain.setValueAtTime(0, ctx.currentTime+start);
  g.gain.linearRampToValueAtTime(vol, ctx.currentTime+start+0.02);
  g.gain.linearRampToValueAtTime(0, ctx.currentTime+start+dur);
  o.start(ctx.currentTime+start); o.stop(ctx.currentTime+start+dur+0.05);
}
function playBirthdayLoop() {
  if (!musicPlaying) return;
  // Happy Birthday melody (simplified)
  const melody = [
    [261,0,.3],[261,.35,.15],[293,.5,.5],[261,.1+.9,.5],[349,1.5,.5],[330,2.1,.9],
    [261,3.2,.3],[261,3.55,.15],[293,3.7,.5],[261,3.2+1.1,.5],[392,4.4,.5],[349,5,.9],
    [261,6.1,.3],[261,6.45,.15],[523,6.6,.5],[440,7.1,.5],[349,7.6,.4],[330,8.1,.4],[293,8.6,.9],
    [466,9.7,.3],[466,10.05,.15],[440,10.2,.5],[349,10.7,.5],[392,11.2,.5],[349,11.8,.9]
  ];
  const dur = 13;
  melody.forEach(([f,t,d]) => playTone(f,t,d));
  setTimeout(() => { if (musicPlaying) playBirthdayLoop(); }, dur*1000);
}
musicBtn.addEventListener('click', () => {
  musicPlaying = !musicPlaying;
  musicBtn.textContent = musicPlaying ? '🔊' : '🎵';
  musicBtn.classList.toggle('playing', musicPlaying);
  document.getElementById('eq-wrap').classList.toggle('show', musicPlaying);
  if (musicPlaying) {
    getAudioCtx().resume();
    playBirthdayLoop();
    noteInterval = setInterval(spawnNote, 1200);
  } else {
    clearInterval(noteInterval);
  }
});

// ── ASCII RENDER ─────────────────────────────────────────────────────────────
const artEl = document.getElementById('ascii-art');
const progressFill = document.getElementById('progress-fill');
const progressLabel = document.getElementById('progress-label');
const eqWrap = document.getElementById('eq-wrap');

function renderASCII() {
  const total = ROWS.length;
  let html = '';
  ROWS.forEach(row => {
    let line = '';
    for (let i = 0; i < row.length; i++) {
      const ch = row[i];
      const cls = charToClass(ch);
      const safe = ch === '<' ? '&lt;' : ch === '>' ? '&gt;' : ch === '&' ? '&amp;' : ch === ' ' ? ' ' : ch;
      line += `<span class="${cls}">${safe}</span>`;
    }
    html += line + '\n';
  });
  artEl.innerHTML = html;
}

function animateReveal() {
  const total = ROWS.length;
  let revealed = 0;
  eqWrap.classList.add('show');

  function revealChunk() {
    const chunk = Math.ceil(total / 60);
    const end = Math.min(revealed + chunk, total);
    let html = artEl.innerHTML;
    // Build incrementally
    if (revealed === 0) artEl.innerHTML = '';
    let addition = '';
    for (let r = revealed; r < end; r++) {
      const row = ROWS[r];
      let line = '';
      for (let i = 0; i < row.length; i++) {
        const ch = row[i];
        const cls = charToClass(ch);
        const safe = ch === '<' ? '&lt;' : ch === '>' ? '&gt;' : ch === '&' ? '&amp;' : ch === ' ' ? ' ' : ch;
        line += `<span class="${cls}">${safe}</span>`;
      }
      addition += line + '\n';
    }
    artEl.innerHTML += addition;
    revealed = end;
    const pct = Math.round(revealed / total * 100);
    progressFill.style.width = pct + '%';
    progressLabel.textContent = pct < 100 ? `RENDERING… ${pct}%` : 'PORTRAIT COMPLETE ✨';
    if (revealed < total) {
      requestAnimationFrame(revealChunk);
    } else {
      setTimeout(() => {
        document.getElementById('progress-wrap').style.opacity = '0';
        eqWrap.classList.remove('show');
        document.getElementById('bday-msg').classList.add('show');
        launchConfetti();
        setTimeout(launchConfetti, 2000);
      }, 600);
    }
  }
  revealChunk();
}

// ── START ────────────────────────────────────────────────────────────────────
function startShow() {
  document.getElementById('splash').style.transition = 'opacity .8s';
  document.getElementById('splash').style.opacity = '0';
  setTimeout(() => {
    document.getElementById('splash').style.display = 'none';
    const main = document.getElementById('main');
    main.classList.add('visible');
    setTimeout(animateReveal, 400);
  }, 800);
}
</script>
</body>
</html>
"""

complete_html = base_html + rows_js + ";\n" + script_tail

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(complete_html)

print(f"Done! birthday.html written ({len(complete_html):,} bytes)")
