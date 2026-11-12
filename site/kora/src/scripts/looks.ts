import { LOOKS } from '../data/looks';
import { P, money } from '../data/products';
import { addToBag } from './ui';

const by = (id: string) => P.find((p) => p.id === id)!;
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
let raf = 0;

function init() {
  const stage = document.getElementById('stage');
  if (!stage || stage.dataset.ready) return; // page-load fires after the first run; do not kill the running loop
  cancelAnimationFrame(raf);
  stage.dataset.ready = '1';
  const figs = Array.from(stage.querySelectorAll<HTMLElement>('.fig'));
  const idx = document.getElementById('idx')!, bar = document.getElementById('bar')!;
  let cur = 0, last = Date.now(), hold = 5600, focus = false;

  // Line-up: the six models stand in a row on one floor. The row slides so the chosen look is in the
  // middle and sharp; the others stand back, a touch smaller and softer. Tap the middle one to step in.
  const n = LOOKS.length; let ang = 0, target = 0, lastLand = -1;
  const floor = stage.querySelector<HTMLElement>('.floor');
  const replay = (el: Element | null, cls: string) => { if (!el) return; el.classList.remove(cls); void (el as HTMLElement).offsetWidth; el.classList.add(cls); };
  const clamp = (v: number) => Math.max(0, Math.min(n - 1, v));
  function layout() {
    const W = stage!.clientWidth, H = stage!.clientHeight, narrow = W < 640; if (!W) return;
    const h = Math.round(H * (narrow ? 0.78 : 0.84)), gap = narrow ? W * 0.34 : Math.min(W / (n + 0.3), 240);
    // the whole row sits centred; it only slides when it cannot fit (phones), and never past its ends
    const c = (n - 1) / 2, maxShift = Math.max(0, c - (W / 2 - gap * 0.6) / gap), shift = Math.max(-maxShift, Math.min(maxShift, ang - c));
    figs.forEach((el, i) => {
      const d = i - ang, a = Math.abs(d), front = a < 0.5;
      let x = (i - c - shift) * gap, s = Math.max(0.78, 1 - a * 0.07), y = 0, op = Math.max(0.3, 1 - a * 0.14), blur = a > 0.5 ? Math.min(2.4, (a - 0.3) * 0.9) : 0;
      if (focus) { if (i === cur) { s = narrow ? 1.06 : 1.12; y = 10; x = narrow ? 0 : x * 0.15; } else { x = x * 1.6; op = 0; blur = 4; } }
      el.style.height = h + 'px';
      el.style.transform = `translate3d(calc(-50% + ${x.toFixed(1)}px),${y}px,0) scale(${s.toFixed(3)})`;
      el.style.opacity = op.toFixed(3); el.style.filter = blur ? `blur(${blur.toFixed(2)}px)` : 'none'; el.style.zIndex = String(20 - Math.round(a * 4));
      el.classList.toggle('on', front); el.setAttribute('aria-hidden', String(!front));
      if (front && a < 0.08 && lastLand !== i && !still) { // the model has arrived in the middle: settle, sweep, pulse the floor
        lastLand = i; replay(el, 'land'); replay(floor, 'pulse'); setTimeout(() => el.classList.remove('land'), 1300);
      }
    });
  }
  function pieceRow(l: typeof LOOKS[number], id: string, j: number) {
    const p = by(id);
    return `<div class="piece" data-id="${p.id}"><span class="n">${j + 1}</span><div class="th"><img src="${l.img}" alt="" style="object-position:50% ${j ? 85 : 18}%" width="56" height="72"></div>
      <div><small>KORA · ${j ? 'Bottom' : 'Top'}</small><strong><a href="/p/${p.id}/">${p.name}</a></strong><span class="pr">${money(p.price)}</span></div>
      <button class="add" type="button" data-add="${p.id}" data-size="M" aria-label="Add ${p.name}">+</button></div>`;
  }
  function setLook(i: number, user?: boolean) {
    cur = clamp(i); target = cur;
    const l = LOOKS[cur], total = by(l.top).price + by(l.bottom).price;
    document.getElementById('lk-no')!.textContent = `In this look · ${String(cur + 1).padStart(2, '0')} / ${String(LOOKS.length).padStart(2, '0')}`;
    document.getElementById('lk-tagno')!.textContent = `Look ${String(cur + 1).padStart(2, '0')}`;
    document.getElementById('lk-tagname')!.textContent = l.name;
    const nm = document.getElementById('lk-name')!; nm.textContent = l.name; if (!still) replay(nm, 'swap');
    document.getElementById('pieces')!.innerHTML = pieceRow(l, l.top, 0) + pieceRow(l, l.bottom, 1);
    document.getElementById('lk-total')!.textContent = money(total * 0.9);
    document.getElementById('lk-cta')!.textContent = money(total * 0.9) + ' →';
    Array.from(idx.children).forEach((b, k) => b.classList.toggle('on', k === cur));
    if (user) { last = Date.now(); hold = 12000; }
  }
  function setFocus(on: boolean) {
    focus = on; stage!.classList.toggle('focus', on); last = Date.now(); hold = on ? 1e12 : 12000; layout();
    if (on && innerWidth < 980) document.getElementById('panel')?.scrollIntoView({ block: 'nearest', behavior: still ? 'auto' : 'smooth' });
  }
  const step = (i: number) => { if (focus) setFocus(false); setLook(i, true); };
  idx.addEventListener('click', (e) => { const b = (e.target as HTMLElement).closest<HTMLElement>('button'); if (b) step(+b.dataset.i!); });
  document.getElementById('prev')!.onclick = () => step(cur - 1 < 0 ? n - 1 : cur - 1);
  document.getElementById('next')!.onclick = () => step((cur + 1) % n);
  document.getElementById('lk-close')!.onclick = () => setFocus(false);
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && focus) setFocus(false); });

  let sx = 0, dragged = false, down = false, t0 = 0, vx = 0, lastX = 0, lastT = 0;
  stage.addEventListener('pointerdown', (e) => { if (focus) return; down = true; dragged = false; sx = lastX = e.clientX; lastT = performance.now(); t0 = target; vx = 0; stage!.classList.add('drag'); });
  addEventListener('pointermove', (e) => {
    if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 12) dragged = true;
    const per = Math.max(140, stage!.clientWidth * 0.28); // px of drag per look
    target = Math.max(-0.4, Math.min(n - 0.6, t0 - dx / per)); const now = performance.now(); if (now > lastT) vx = (e.clientX - lastX) / (now - lastT); lastX = e.clientX; lastT = now;
  });
  addEventListener('pointerup', () => {
    if (!down) return; down = false; stage!.classList.remove('drag');
    const per = Math.max(140, stage!.clientWidth * 0.28);
    const fling = -vx * 140 / per; // carry the flick on a little, then settle on a look
    const settle = clamp(Math.round(target + fling));
    setLook(settle, true);
    setTimeout(() => (dragged = false), 0);
  });
  stage.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') step((cur + 1) % n); if (e.key === 'ArrowLeft') step(cur ? cur - 1 : n - 1); });
  stage.addEventListener('click', (e) => {
    const t = e.target as HTMLElement;
    const pin = t.closest<HTMLElement>('.pin');
    if (pin) { e.stopPropagation(); const el = document.querySelector(`#panel .piece[data-id="${pin.dataset.id}"]`); el?.classList.add('hl'); el?.scrollIntoView({ block: 'nearest', behavior: still ? 'auto' : 'smooth' }); setTimeout(() => el?.classList.remove('hl'), 1400); pin.classList.add('hot'); setTimeout(() => pin.classList.remove('hot'), 1200); return; }
    if (dragged) return;
    const f = t.closest<HTMLElement>('.fig'); if (!f) { if (focus) setFocus(false); return; }
    const i = +f.dataset.i!; if (i === cur) setFocus(!focus); else step(i);
  });
  document.getElementById('addlook')!.addEventListener('click', () => { const l = LOOKS[cur]; addToBag(l.top, 'M'); addToBag(l.bottom, 'M'); });

  const io = new IntersectionObserver((en) => { visible = en[0].isIntersecting; }, { threshold: 0.3 });
  let visible = false; io.observe(stage);
  function tick() {
    if (!stage!.isConnected) return; // page changed; a fresh init will start its own loop
    const el = Date.now() - last;
    if (Math.abs(target - ang) > 0.0005) { ang += (target - ang) * (down ? 0.35 : 0.075); layout(); } else if (ang !== target) { ang = target; layout(); } bar.style.width = Math.min(100, (el / hold) * 100) + '%';
    if (!still && visible && el > hold && !document.documentElement.classList.contains('lock')) { last = Date.now(); hold = 5600; setLook((cur + 1) % n); }
    raf = requestAnimationFrame(tick);
  }
  addEventListener('resize', layout);
  setLook(0); layout(); tick();
}
init();
document.addEventListener('astro:page-load', init);
