import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
let firstLoad = true;
let rotate: number | undefined;
let cur = 0;

function init() {
  const loader = document.getElementById('loader');
  const frame = document.getElementById('frame');
  const heroH = document.getElementById('hero-h');
  clearInterval(rotate);
  if (!frame || !heroH) { loader?.remove(); firstLoad = false; return; }

  const lines = heroH.querySelectorAll('.r-line > span');
  const rest = document.querySelectorAll('.r-hero');

  if (reduce) { loader?.remove(); return; }

  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
  if (firstLoad && loader) {
    // Opening sequence only on a cold load; page transitions skip the counter
    document.documentElement.style.overflow = 'hidden';
    const n = { v: 0 }; const nEl = document.getElementById('loader-n')!;
    tl.to(n, { v: 100, duration: 1.4, ease: 'power2.inOut', onUpdate: () => { nEl.textContent = String(Math.round(n.v)).padStart(2, '0'); } })
      .to('#loader-n span', { yPercent: -110, duration: 0.7, ease: 'power3.in' }, '+=0.1')
      .to('.loader-mark', { yPercent: -110, duration: 0.5, ease: 'power3.in' }, '<')
      .to(loader, { yPercent: -100, duration: 1.1, ease: 'power4.inOut', onComplete() { document.documentElement.style.overflow = ''; loader.remove(); } }, '-=0.2');
  } else { loader?.remove(); }
  tl.fromTo(frame, { scale: 1.06, filter: 'brightness(1.08)' }, { scale: 1, filter: 'brightness(1)', duration: 2, ease: 'power3.out' }, firstLoad ? '-=0.8' : 0)
    .to(lines, { y: 0, duration: 1.5, ease: 'power4.out', stagger: 0.14 }, '-=1.6')
    .to(rest, { opacity: 1, y: 0, duration: 1.1, stagger: 0.1 }, '-=1.0');
  firstLoad = false;

  const shots = Array.from(frame.querySelectorAll<HTMLElement>('.shot')).filter((s) => getComputedStyle(s).display !== 'none');
  const dots = document.getElementById('shot-dots');
  if (dots) dots.innerHTML = shots.map((_, k) => `<i class="${k === 0 ? 'on' : ''}"></i>`).join('');
  cur = 0;
  const show = (n: number) => { cur = (n + shots.length) % shots.length; shots.forEach((s, k) => s.classList.toggle('on', k === cur)); dots?.querySelectorAll('i').forEach((d, k) => d.classList.toggle('on', k === cur)); };
  const arm = () => { clearInterval(rotate); rotate = window.setInterval(() => show(cur + 1), 5000); };
  arm();
  const prev = document.getElementById('shot-prev'), next = document.getElementById('shot-next');
  const noFocus = (e: Event) => e.preventDefault(); // focusing inside the sticky hero makes phones scroll-jump
  if (prev) { prev.onclick = () => { show(cur - 1); arm(); }; prev.onmousedown = noFocus; }
  if (next) { next.onclick = () => { show(cur + 1); arm(); }; next.onmousedown = noFocus; }
  // Depth: the photo drifts a little against the mouse (or the phone's tilt) while the headline goes the other way
  const pin = frame.parentElement as HTMLElement;
  const depth = (x: number, y: number) => { pin.style.setProperty('--px', x.toFixed(3)); pin.style.setProperty('--py', y.toFixed(3)); };
  frame.onpointermove = (e) => { if (e.pointerType !== 'mouse') return; depth((e.clientX / innerWidth - 0.5) * -2, (e.clientY / innerHeight - 0.5) * -2); };
  frame.onpointerleave = () => depth(0, 0);
  if (!matchMedia('(hover:hover)').matches && typeof (DeviceOrientationEvent as any)?.requestPermission !== 'function') {
    let b0: number | null = null;
    window.ondeviceorientation = (e) => { if (e.gamma == null || e.beta == null) return; if (b0 == null) b0 = e.beta; depth(Math.max(-1, Math.min(1, -e.gamma / 25)), Math.max(-1, Math.min(1, (e.beta - b0) / 25))); };
  }
  let x0 = 0, y0 = 0;
  frame.onpointerdown = (e) => { x0 = e.clientX; y0 = e.clientY; };
  frame.onpointerup = (e) => { const dx = e.clientX - x0, dy = e.clientY - y0; if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) { show(dx < 0 ? cur + 1 : cur - 1); arm(); } };

  const mq = matchMedia('(max-width: 760px)').matches;
  const inset = mq ? 'inset(10vh 16px 14vh 16px)' : 'inset(8vh 8vw 10vh 8vw)';
  gsap.timeline({ scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom bottom', scrub: 0.6,
      onUpdate(self) { frame.classList.toggle('inset', self.progress > 0.35); } } })
    .fromTo(frame, { clipPath: 'inset(0px 0px 0px 0px)' }, { clipPath: inset, ease: 'none' }, 0)
    .to(frame.querySelectorAll('.shot img'), { scale: 1.0, yPercent: 7, ease: 'none' }, 0)
    .to('.hero-copy', { yPercent: 30, opacity: 0, ease: 'none' }, 0)
    .to('.scroll-hint', { opacity: 0, ease: 'none' }, 0);
}

// motion.ts kills all ScrollTriggers at page-load, then fires this; hero rebuilds after it
document.addEventListener('kora:motion-ready', init);
if (reduce) document.addEventListener('astro:page-load', init);
