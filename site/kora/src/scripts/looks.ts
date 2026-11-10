import { LOOKS } from '../data/looks';
import { P, money } from '../data/products';
import { addToBag } from './ui';

const by = (id: string) => P.find((p) => p.id === id)!;
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
let raf = 0;

function init() {
  cancelAnimationFrame(raf);
  const stage = document.getElementById('stage');
  if (!stage || stage.dataset.ready) return;
  stage.dataset.ready = '1';
  const figs = Array.from(stage.querySelectorAll<HTMLElement>('.fig'));
  const idx = document.getElementById('idx')!, bar = document.getElementById('bar')!;
  let cur = 0, last = Date.now(), hold = 5600;

  function layout() {
    const W = stage!.clientWidth, H = stage!.clientHeight, narrow = W < 640; if (!W) return;
    const h = Math.round(H * (narrow ? 0.84 : 0.9)), s0 = narrow ? W * 0.4 : Math.min(W * 0.2, 300), s1 = narrow ? W * 0.26 : Math.min(W * 0.14, 200);
    figs.forEach((el, i) => {
      const n = LOOKS.length; let d = i - cur; if (d > 3) d -= n; if (d < -2) d += n;
      const a = Math.abs(d), sg = d < 0 ? -1 : 1;
      const x = d === 0 ? 0 : sg * (s0 + (a - 1) * s1);
      const sc = a === 0 ? 1 : a === 1 ? 0.78 : a === 2 ? 0.62 : 0.5, op = a === 0 ? 1 : a === 1 ? 0.5 : a === 2 ? 0.28 : 0.14, bl = a === 0 ? 0 : a === 1 ? 1.4 : a === 2 ? 2.4 : 3;
      el.style.height = h + 'px'; el.style.transform = `translate3d(calc(-50% + ${x.toFixed(1)}px),0,0) scale(${sc})`;
      el.style.opacity = String(op); el.style.filter = bl ? `blur(${bl}px)` : 'none'; el.style.zIndex = String(10 - a);
      el.classList.toggle('on', a === 0); el.setAttribute('aria-hidden', String(a !== 0));
    });
  }
  function pieceRow(l: typeof LOOKS[number], id: string, j: number) {
    const p = by(id);
    return `<div class="piece" data-id="${p.id}"><span class="n">${j + 1}</span><div class="th"><img src="${l.img}" alt="" style="object-position:50% ${j ? 85 : 18}%" width="56" height="72"></div>
      <div><small>KORA · ${j ? 'Bottom' : 'Top'}</small><strong><a href="/p/${p.id}/">${p.name}</a></strong><span class="pr">${money(p.price)}</span></div>
      <button class="add" type="button" data-add="${p.id}" data-size="M" aria-label="Add ${p.name}">+</button></div>`;
  }
  function setLook(i: number, user?: boolean) {
    cur = (i + LOOKS.length) % LOOKS.length; layout();
    const l = LOOKS[cur], total = by(l.top).price + by(l.bottom).price;
    document.getElementById('lk-no')!.textContent = `In this look · ${String(cur + 1).padStart(2, '0')} / ${String(LOOKS.length).padStart(2, '0')}`;
    document.getElementById('lk-name')!.textContent = l.name;
    document.getElementById('pieces')!.innerHTML = pieceRow(l, l.top, 0) + pieceRow(l, l.bottom, 1);
    document.getElementById('lk-total')!.textContent = money(total * 0.9);
    document.getElementById('lk-cta')!.textContent = money(total * 0.9) + ' →';
    Array.from(idx.children).forEach((b, k) => b.classList.toggle('on', k === cur));
    if (user) { last = Date.now(); hold = 12000; }
  }
  idx.addEventListener('click', (e) => { const b = (e.target as HTMLElement).closest<HTMLElement>('button'); if (b) setLook(+b.dataset.i!, true); });
  document.getElementById('prev')!.onclick = () => setLook(cur - 1, true);
  document.getElementById('next')!.onclick = () => setLook(cur + 1, true);

  let sx = 0, dragged = false, down = false;
  stage.addEventListener('pointerdown', (e) => { down = true; dragged = false; sx = e.clientX; stage!.classList.add('drag'); });
  addEventListener('pointermove', (e) => { if (down && Math.abs(e.clientX - sx) > 12) dragged = true; });
  addEventListener('pointerup', (e) => { if (!down) return; down = false; stage!.classList.remove('drag'); const dx = e.clientX - sx; if (Math.abs(dx) > 40) setLook(cur + (dx < 0 ? 1 : -1), true); setTimeout(() => (dragged = false), 0); });
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
    const el = Date.now() - last; bar.style.width = Math.min(100, (el / hold) * 100) + '%';
    if (!still && visible && el > hold && !document.documentElement.classList.contains('lock')) { last = Date.now(); hold = 5600; setLook(cur + 1); }
    raf = requestAnimationFrame(tick);
  }
  addEventListener('resize', layout);
  setLook(0); tick();
}
init();
document.addEventListener('astro:page-load', init);
