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
  let cur = 0, last = Date.now(), hold = 5600;

  // 3D turntable: figures stand on a ring, the ring turns to bring the chosen look to the front.
  const n = LOOKS.length; let ang = 0, target = 0, lastLand = -1;
  const floor = stage.querySelector<HTMLElement>('.floor');
  const replay = (el: Element | null, cls: string) => { if (!el) return; el.classList.remove(cls); void (el as HTMLElement).offsetWidth; el.classList.add(cls); };
  function layout() {
    const W = stage!.clientWidth, H = stage!.clientHeight, narrow = W < 640; if (!W) return;
    const h = Math.round(H * (narrow ? 0.8 : 0.86)), R = narrow ? W * 0.5 : Math.min(W * 0.36, 470);
    figs.forEach((el, i) => {
      let d = i - ang; d = ((d % n) + n) % n; if (d > n / 2) d -= n; // -n/2..n/2, 0 = front
      const th = (d / n) * Math.PI * 2, depth = Math.cos(th); // depth 1 front, -1 back
      const x = R * Math.sin(th) * (1 + 0.3 * depth), z = R * (depth - 1) * 1.1, k = (depth + 1) / 2; // wider at the front so back figures peek between
      el.style.height = h + 'px'; el.style.transform = `translate3d(calc(-50% + ${x.toFixed(1)}px),0,${z.toFixed(1)}px)`;
      el.style.opacity = (0.18 + 0.82 * k * k).toFixed(3); el.style.filter = depth < 0.9 ? `blur(${((1 - k) * 2.2).toFixed(2)}px)` : 'none'; el.style.zIndex = String(Math.round(k * 20));
      const front = Math.abs(d) < 0.5; el.classList.toggle('on', front); el.setAttribute('aria-hidden', String(!front));
      if (front && Math.abs(d) < 0.08 && lastLand !== i && !still) { // the model has arrived at the front: land, sweep, pop the pins
        lastLand = i; replay(el, 'land'); replay(floor, 'pulse'); setTimeout(() => el.classList.remove('land'), 1300);
      }
    });
  }
  const nearest = (from: number, to: number) => { let d = ((to - from) % n + n) % n; if (d > n / 2) d -= n; return from + d; }; // shortest way round
  function pieceRow(l: typeof LOOKS[number], id: string, j: number) {
    const p = by(id);
    return `<div class="piece" data-id="${p.id}"><span class="n">${j + 1}</span><div class="th"><img src="${l.img}" alt="" style="object-position:50% ${j ? 85 : 18}%" width="56" height="72"></div>
      <div><small>KORA · ${j ? 'Bottom' : 'Top'}</small><strong><a href="/p/${p.id}/">${p.name}</a></strong><span class="pr">${money(p.price)}</span></div>
      <button class="add" type="button" data-add="${p.id}" data-size="M" aria-label="Add ${p.name}">+</button></div>`;
  }
  function setLook(i: number, user?: boolean) {
    cur = (i + LOOKS.length) % LOOKS.length; target = nearest(target, cur);
    const l = LOOKS[cur], total = by(l.top).price + by(l.bottom).price;
    document.getElementById('lk-no')!.textContent = `In this look · ${String(cur + 1).padStart(2, '0')} / ${String(LOOKS.length).padStart(2, '0')}`;
    const nm = document.getElementById('lk-name')!; nm.textContent = l.name; if (!still) replay(nm, 'swap');
    document.getElementById('pieces')!.innerHTML = pieceRow(l, l.top, 0) + pieceRow(l, l.bottom, 1);
    document.getElementById('lk-total')!.textContent = money(total * 0.9);
    document.getElementById('lk-cta')!.textContent = money(total * 0.9) + ' →';
    Array.from(idx.children).forEach((b, k) => b.classList.toggle('on', k === cur));
    if (user) { last = Date.now(); hold = 12000; }
  }
  idx.addEventListener('click', (e) => { const b = (e.target as HTMLElement).closest<HTMLElement>('button'); if (b) setLook(+b.dataset.i!, true); });
  document.getElementById('prev')!.onclick = () => setLook(cur - 1, true);
  document.getElementById('next')!.onclick = () => setLook(cur + 1, true);

  let sx = 0, dragged = false, down = false, t0 = 0, vx = 0, lastX = 0, lastT = 0;
  stage.addEventListener('pointerdown', (e) => { down = true; dragged = false; sx = lastX = e.clientX; lastT = performance.now(); t0 = target; vx = 0; stage!.classList.add('drag'); });
  addEventListener('pointermove', (e) => {
    if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 12) dragged = true;
    const per = Math.max(140, stage!.clientWidth * 0.28); // px of drag per look
    target = t0 - dx / per; const now = performance.now(); if (now > lastT) vx = (e.clientX - lastX) / (now - lastT); lastX = e.clientX; lastT = now;
  });
  addEventListener('pointerup', () => {
    if (!down) return; down = false; stage!.classList.remove('drag');
    const per = Math.max(140, stage!.clientWidth * 0.28);
    const fling = -vx * 140 / per; // carry the flick on a little, then settle on a look
    const settle = Math.round(target + fling); const idx2 = ((settle % n) + n) % n;
    if (idx2 !== cur || Math.abs(target - settle) > 0.01) { target = settle; setLook(idx2, true); target = settle; }
    setTimeout(() => (dragged = false), 0);
  });
  stage.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') setLook(cur + 1, true); if (e.key === 'ArrowLeft') setLook(cur - 1, true); });
  stage.addEventListener('click', (e) => {
    const t = e.target as HTMLElement;
    const pin = t.closest<HTMLElement>('.pin');
    if (pin) { e.stopPropagation(); const el = document.querySelector(`#panel .piece[data-id="${pin.dataset.id}"]`); el?.classList.add('hl'); el?.scrollIntoView({ block: 'nearest', behavior: still ? 'auto' : 'smooth' }); setTimeout(() => el?.classList.remove('hl'), 1400); pin.classList.add('hot'); setTimeout(() => pin.classList.remove('hot'), 1200); last = Date.now(); hold = 12000; return; }
    if (dragged) return;
    const f = t.closest<HTMLElement>('.fig'); if (!f) return;
    const i = +f.dataset.i!; if (i === cur) location.href = `/p/${LOOKS[cur].top}/`; else setLook(i, true);
  });
  document.getElementById('addlook')!.addEventListener('click', () => { const l = LOOKS[cur]; addToBag(l.top, 'M'); addToBag(l.bottom, 'M'); });

  const io = new IntersectionObserver((en) => { visible = en[0].isIntersecting; }, { threshold: 0.3 });
  let visible = false; io.observe(stage);
  function tick() {
    if (!stage!.isConnected) return; // page changed; a fresh init will start its own loop
    const el = Date.now() - last;
    if (Math.abs(target - ang) > 0.0005) { ang += (target - ang) * (down ? 0.35 : 0.075); layout(); } else if (ang !== target) { ang = target; layout(); } bar.style.width = Math.min(100, (el / hold) * 100) + '%';
    if (!still && visible && el > hold && !document.documentElement.classList.contains('lock')) { last = Date.now(); hold = 5600; setLook(cur + 1); }
    raf = requestAnimationFrame(tick);
  }
  addEventListener('resize', layout);
  setLook(0); layout(); tick();
}
init();
document.addEventListener('astro:page-load', init);
