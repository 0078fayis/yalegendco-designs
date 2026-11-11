// Small "feel" effects: 3D tilt on product photos (mouse, or the phone's gyroscope), hanger lean-in,
// count-up numbers, and the fly-to-bag clone. All transform/opacity only, skipped under reduced motion.
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;

// ---------- 3D tilt ----------
const MAX = 7; // degrees
const setTilt = (el: HTMLElement, rx: number, ry: number) => {
  el.style.setProperty('--rx', rx.toFixed(2) + 'deg'); el.style.setProperty('--ry', ry.toFixed(2) + 'deg');
  el.style.setProperty('--gx', (50 + ry * 4).toFixed(1) + '%'); el.style.setProperty('--gy', (50 - rx * 4).toFixed(1) + '%');
};
function pointerTilt(el: HTMLElement) {
  el.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse') return;
    const r = el.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
    el.classList.add('tilting'); setTilt(el, -py * MAX * 2, px * MAX * 2);
  });
  el.addEventListener('pointerleave', () => { el.classList.remove('tilting'); setTilt(el, 0, 0); });
}
// On phones there is no hover, so the cards lean with the device. Only cards on screen are touched.
const seen = new Set<HTMLElement>();
let gyroOn = false, base: number | null = null;
function gyro(e: DeviceOrientationEvent) {
  if (e.beta == null || e.gamma == null) return;
  if (base == null) base = e.beta; // holding angle when the page opened = flat
  const rx = Math.max(-MAX, Math.min(MAX, (base - e.beta) * 0.35));
  const ry = Math.max(-MAX, Math.min(MAX, e.gamma * 0.35));
  seen.forEach((el) => setTilt(el, rx, ry));
}
const io = new IntersectionObserver((en) => en.forEach((x) => { const el = x.target as HTMLElement; if (x.isIntersecting) seen.add(el); else { seen.delete(el); setTilt(el, 0, 0); } }), { rootMargin: '10% 0px' });

function wireTilt() {
  document.querySelectorAll<HTMLElement>('[data-tilt]:not([data-tilted])').forEach((el) => {
    el.dataset.tilted = '1';
    if (fine) pointerTilt(el); else io.observe(el);
  });
  if (!fine && !gyroOn && 'DeviceOrientationEvent' in window && typeof (DeviceOrientationEvent as any).requestPermission !== 'function') {
    gyroOn = true; addEventListener('deviceorientation', gyro, { passive: true });
  }
}

// ---------- hanger lean-in ----------
const lean = new IntersectionObserver((en) => en.forEach((x) => { if (x.isIntersecting) { x.target.classList.add('in'); lean.unobserve(x.target); } }), { rootMargin: '0px 0px -10% 0px' });
const wireLean = () => document.querySelectorAll<HTMLElement>('.hang:not(.in)').forEach((h) => lean.observe(h));

// ---------- count-up ----------
export function countUp(el: HTMLElement, ms = 1300) {
  if (el.dataset.counted) return; el.dataset.counted = '1';
  const raw = el.textContent || '0', target = parseInt(raw, 10) || 0, pad = raw.length;
  if (reduce) return;
  const t0 = performance.now();
  const tick = (t: number) => {
    const k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3);
    el.textContent = String(Math.round(target * e)).padStart(pad, '0');
    if (k < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

// ---------- fly to bag ----------
export function flyToBag(from: HTMLElement | null) {
  const btn = document.getElementById('bag-btn');
  const img = from?.closest('.pcard, .hang, .pdp, .look, .lk')?.querySelector<HTMLImageElement>('.pcard-pic img.a, .hang-pic img, #gal .g img, img')
    || (from && from.closest('.pdp') ? document.querySelector<HTMLImageElement>('#gal .g img') : null);
  if (reduce || !btn || !img) return Promise.resolve();
  const a = img.getBoundingClientRect(), b = btn.getBoundingClientRect();
  if (!a.width) return Promise.resolve();
  const ghost = document.createElement('div');
  ghost.className = 'fly';
  ghost.style.cssText = `left:${a.left}px;top:${a.top}px;width:${a.width}px;height:${a.height}px;background-image:url("${img.currentSrc || img.src}")`;
  document.body.appendChild(ghost);
  const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
  const anim = ghost.animate([
    { transform: 'translate(0,0) scale(1) rotate(0deg)', opacity: 1, borderRadius: '0' },
    { transform: `translate(${dx * 0.5}px,${dy * 0.6 - 60}px) scale(.45) rotate(-4deg)`, opacity: 1, borderRadius: '8px', offset: 0.55 },
    { transform: `translate(${dx}px,${dy}px) scale(.04) rotate(2deg)`, opacity: 0.2, borderRadius: '50%' },
  ], { duration: 780, easing: 'cubic-bezier(.4,0,.2,1)', fill: 'forwards' });
  return new Promise<void>((res) => { anim.onfinish = () => { ghost.remove(); res(); }; setTimeout(() => { ghost.remove(); res(); }, 900); });
}

function init() { if (reduce) return; wireTilt(); wireLean(); }
init(); document.addEventListener('astro:page-load', init);
